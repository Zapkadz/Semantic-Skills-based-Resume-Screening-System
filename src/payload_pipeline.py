"""Screening pipeline that accepts web/API JSON payloads."""

from __future__ import annotations

import re
from typing import Any

from src.api_models import CandidatePayload, JobPayload, ScreeningRequest
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.job_quality_gate import evaluate_job_quality
from src.open_set_matcher import (
    build_taxonomy_coverage,
    find_semantic_requirement_evidence,
)
from src.payload_diagnostics import (
    diagnose_candidate_payload,
    diagnose_job_payload,
)
from src.requirement_provenance import build_requirement_provenance_summary
from src.requirement_promotion import build_scoring_requirement_lines_from_entries
from src.requirement_extractor import build_screening_confidence
from src.role_family import infer_job_role_profile
from src.resume_parser import parse_resume
from src.review_card_generator import generate_review_card
from src.runtime_diagnostics import build_screening_diagnostics, build_trace_id
from src.scorer import rank_candidates, score_candidate
from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    _build_open_set_requirement_data,
    _build_job_skill_list,
    _build_requirement_group_summary,
    _enrich_resume_skills,
    _with_requirement_groups,
)
from src.semantic_matcher import match_skills
from src.skill_extractor import merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy
from src.technical_intent import (
    annotate_matches_with_requirement_intents,
    build_requirement_intent_summary,
)
from src.text_normalization import html_to_plain_text, strip_list_marker


def build_jd_text_from_payload(job: dict[str, Any] | JobPayload) -> str:
    """Build parser-friendly JD text from a web job payload."""
    job_payload = _to_plain_dict(job)
    raw_text = _clean_payload_text(
        job_payload.get("raw_text") or job_payload.get("job_description_text", "")
    )
    if raw_text:
        job_title = _clean_payload_text(
            job_payload.get("job_title") or job_payload.get("title", "")
        )
        if job_title and not raw_text.casefold().startswith(job_title.casefold()):
            return f"{job_title}\n\n{raw_text}"
        return raw_text

    job_title = _clean_payload_text(
        job_payload.get("job_title") or job_payload.get("title", "")
    )
    description = _clean_payload_text(
        job_payload.get("description") or job_payload.get("job_description_text", "")
    )
    requirements = _string_list(
        job_payload.get("requirements") or job_payload.get("must_have_skills")
    )
    nice_to_have = _string_list(
        job_payload.get("nice_to_have") or job_payload.get("nice_to_have_skills")
    )
    responsibilities = _string_list(job_payload.get("responsibilities"))

    minimum_years = job_payload.get("minimum_experience_years")
    if minimum_years and not _has_experience_requirement(requirements):
        requirements.append(f"{minimum_years}+ year experience")

    if not job_title and not description:
        raise ValueError("Job payload must include job_title, raw_text, or description.")

    lines = [job_title or "Untitled Job", ""]
    if requirements:
        lines.extend(["Requirements:", *_format_bullets(requirements), ""])
    elif description:
        lines.extend(["Requirements:", f"- {description}", ""])

    if nice_to_have:
        lines.extend(["Nice to have:", *_format_bullets(nice_to_have), ""])

    if responsibilities:
        lines.extend(["Responsibilities:", *_format_bullets(responsibilities), ""])

    return "\n".join(lines).strip()


def build_cv_document_from_payload(
    candidate: dict[str, Any] | CandidatePayload,
) -> dict[str, Any]:
    """Build a loader-like document dict from a candidate payload."""
    candidate_payload = _to_plain_dict(candidate)
    cv_text = _clean_payload_text(
        candidate_payload.get("cv_text") or candidate_payload.get("resume_text", "")
    )

    if not cv_text:
        cv_text = _build_structured_cv_text(candidate_payload)

    if not cv_text:
        candidate_name = str(candidate_payload.get("candidate_name", "")).strip()
        raise ValueError(
            "Candidate payload must include cv_text/resume_text or structured CV data: "
            f"{candidate_name}"
        )

    filename = _build_candidate_source_filename(candidate_payload)
    return {
        "filename": filename,
        "path": "",
        "text": cv_text,
        "application_id": candidate_payload.get("application_id"),
        "candidate_id": candidate_payload.get("candidate_id"),
        "email": candidate_payload.get("email", ""),
        "phone": candidate_payload.get("phone", ""),
        "applied_at": candidate_payload.get("applied_at", ""),
        "cv_file_path": candidate_payload.get("cv_file_path", ""),
        "candidate_name": candidate_payload.get("candidate_name", ""),
    }


def run_screening_payload(
    payload: dict[str, Any] | ScreeningRequest,
    taxonomy_path: str = DEFAULT_TAXONOMY_PATH,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Run the screening pipeline from a web/API JSON payload."""
    payload_data = _to_plain_dict(payload)
    if "taxonomy_path" in payload_data and payload_data["taxonomy_path"]:
        taxonomy_path = str(payload_data["taxonomy_path"])

    job_payload = payload_data.get("job", {})
    candidate_payloads = list(payload_data.get("candidates", []))
    taxonomy = load_taxonomy(taxonomy_path)

    job_text = build_jd_text_from_payload(job_payload)
    trace_id = build_trace_id("screening")
    job_payload_diagnostics = diagnose_job_payload(job_payload, job_text)
    job_criteria = parse_jd(job_text)
    job_criteria = _with_requirement_groups(job_criteria, job_text, taxonomy)
    required_requirement_lines, nice_to_have_requirement_lines = (
        build_scoring_requirement_lines_from_entries(
            job_criteria.get("scoring_requirement_entries", [])
        )
    )
    required_skills = _build_job_skill_list(
        required_requirement_lines,
        "\n".join(required_requirement_lines),
        taxonomy,
        use_full_text_fallback=True,
        include_unknown_skills=False,
    )
    open_set_data = _build_open_set_requirement_data(
        {**job_criteria, "must_have_skills": required_requirement_lines},
        "\n".join(required_requirement_lines),
        required_skills,
        taxonomy,
    )
    unknown_requirements = open_set_data["open_set_requirements"]
    taxonomy_coverage = build_taxonomy_coverage(
        required_skills,
        unknown_requirements,
    )
    job_role_profile = infer_job_role_profile(
        job_title=job_criteria.get("job_title", "") or job_payload.get("job_title", ""),
        required_skills=required_skills,
        open_set_requirements=unknown_requirements,
        responsibilities=job_criteria.get("requirement_groups", {}).get(
            "responsibilities",
            [],
        ),
        typed_requirements=job_criteria.get("typed_requirements", []),
    )
    nice_to_have_skills = _build_job_skill_list(
        nice_to_have_requirement_lines,
        "\n".join(nice_to_have_requirement_lines),
        taxonomy,
        use_full_text_fallback=False,
        include_unknown_skills=embedding_matcher is not None,
    )
    if embedding_matcher is not None:
        nice_to_have_open_set_data = _build_open_set_requirement_data(
            {**job_criteria, "must_have_skills": nice_to_have_requirement_lines},
            "\n".join(nice_to_have_requirement_lines),
            nice_to_have_skills,
            taxonomy,
        )
        nice_to_have_skills = merge_skill_lists(
            nice_to_have_skills,
            nice_to_have_open_set_data["open_set_requirements"],
        )
    requirement_provenance_summary = build_requirement_provenance_summary(
        required_skills,
        unknown_requirements,
        list(job_criteria.get("scoring_requirement_entries", [])),
        list(open_set_data.get("open_set_candidates", [])),
        taxonomy,
    )
    requirement_intent_summary = build_requirement_intent_summary(
        job_role_profile,
        required_skills,
        unknown_requirements,
        typed_requirements=job_criteria.get("typed_requirements", []),
        requirement_provenance_summary=requirement_provenance_summary,
    )
    job_criteria = {
        **job_criteria,
        "job_role_profile": job_role_profile,
        "requirement_intent_summary": requirement_intent_summary,
        "requirement_provenance_summary": requirement_provenance_summary,
    }

    candidate_documents = [
        build_cv_document_from_payload(candidate_payload)
        for candidate_payload in candidate_payloads
    ]
    candidate_payload_diagnostics = [
        diagnose_candidate_payload(candidate_payload, candidate_document)
        for candidate_payload, candidate_document in zip(
            candidate_payloads,
            candidate_documents,
        )
    ]
    job_quality = evaluate_job_quality(
        job_payload,
        job_criteria,
        job_text,
        job_criteria["requirement_groups"],
        required_skills,
        nice_to_have_skills,
        unknown_requirements,
    )
    candidate_results = [
        _process_candidate_payload(
            candidate_payload,
            candidate_document,
            job_criteria,
            taxonomy,
            required_skills,
            nice_to_have_skills,
            unknown_requirements,
            requirement_intent_summary,
            embedding_matcher,
        )
        for candidate_payload, candidate_document in zip(
            candidate_payloads,
            candidate_documents,
        )
    ]
    ranked_candidates = rank_candidates(candidate_results)

    for candidate in ranked_candidates:
        candidate["review_card"] = generate_review_card(candidate, job_criteria)

    job_output = _build_job_output(
        job_payload,
        job_criteria,
        required_skills,
        nice_to_have_skills,
        taxonomy_coverage,
        open_set_data,
        job_role_profile,
        requirement_intent_summary,
        embedding_matcher,
    )

    return {
        "trace_id": trace_id,
        "job": job_output,
        "candidates": ranked_candidates,
        "diagnostics": build_screening_diagnostics(
            trace_id=trace_id,
            job_payload_diagnostics=job_payload_diagnostics,
            candidate_payload_diagnostics=candidate_payload_diagnostics,
            candidate_payloads=candidate_payloads,
            job_quality=job_quality,
            job_output=job_output,
            ranked_candidates=ranked_candidates,
            embedding_enabled=embedding_matcher is not None,
        ),
    }


def _process_candidate_payload(
    candidate_payload: dict[str, Any],
    document: dict[str, Any],
    job_criteria: dict[str, Any],
    taxonomy: dict[str, dict[str, Any]],
    required_skills: list[str],
    nice_to_have_skills: list[str],
    unknown_requirements: list[str],
    requirement_intent_summary: list[dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Process one candidate payload into a scored candidate result."""
    resume_profile = parse_resume(document["text"])
    _enrich_resume_skills(resume_profile, document["text"], taxonomy)

    candidate_skills = normalize_skills(resume_profile.get("raw_skills", []), taxonomy)
    must_have_matches = match_skills(
        required_skills,
        candidate_skills,
        taxonomy,
        embedding_matcher=embedding_matcher,
    )
    enriched_matches = detect_all_evidence(must_have_matches, resume_profile, taxonomy)
    open_set_matches = find_semantic_requirement_evidence(
        unknown_requirements,
        resume_profile,
        embedding_matcher,
    )
    scored_matches = annotate_matches_with_requirement_intents(
        [*enriched_matches, *open_set_matches],
        requirement_intent_summary,
    )
    annotated_open_set_matches = [
        match
        for match in scored_matches
        if str(match.get("taxonomy_status", "")).strip() == "unknown"
    ]
    nice_to_have_matches = match_skills(
        nice_to_have_skills,
        candidate_skills,
        taxonomy,
        embedding_matcher=embedding_matcher,
    )
    scored_candidate = score_candidate(
        job_criteria,
        resume_profile,
        scored_matches,
        nice_to_have_matches,
    )

    if not scored_candidate.get("candidate_name") and document.get("candidate_name"):
        scored_candidate["candidate_name"] = document["candidate_name"]

    return {
        **scored_candidate,
        "open_set_requirement_matches": annotated_open_set_matches,
        "requirement_group_summary": _build_requirement_group_summary(
            scored_matches,
            nice_to_have_matches,
        ),
        "application_id": document.get("application_id"),
        "candidate_id": document.get("candidate_id"),
        "email": document.get("email", ""),
        "phone": document.get("phone", ""),
        "applied_at": document.get("applied_at", ""),
        "cv_file_path": document.get("cv_file_path", ""),
        "source_file": document.get("filename", ""),
        "source_path": document.get("path", ""),
    }


def _build_job_output(
    job_payload: dict[str, Any],
    job_criteria: dict[str, Any],
    required_skills: list[str],
    nice_to_have_skills: list[str],
    taxonomy_coverage: dict[str, Any] | None = None,
    open_set_data: dict[str, Any] | None = None,
    job_role_profile: dict[str, Any] | None = None,
    requirement_intent_summary: list[dict[str, Any]] | None = None,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Build a stable API job response object."""
    open_set_data = open_set_data or {}
    open_set_requirements = list(open_set_data.get("open_set_requirements", []))
    return {
        "job_id": job_payload.get("job_id"),
        "title": job_criteria.get("job_title", "") or job_payload.get("job_title", ""),
        "must_have_skills": required_skills,
        "nice_to_have_skills": nice_to_have_skills,
        "open_set_requirements": open_set_requirements,
        "open_set_candidates": list(open_set_data.get("open_set_candidates", [])),
        "discarded_open_set_candidates": list(
            open_set_data.get("discarded_open_set_candidates", [])
        ),
        "open_set_filter_summary": dict(
            open_set_data.get("open_set_filter_summary", {})
        ),
        "minimum_experience_years": job_criteria.get("minimum_experience_years", 0),
        "seniority": job_criteria.get("seniority", "Not specified"),
        "domain": job_criteria.get("domain", []),
        "job_role_profile": dict(job_role_profile or {}),
        "requirement_intent_summary": list(requirement_intent_summary or []),
        "taxonomy_coverage": taxonomy_coverage or build_taxonomy_coverage(
            required_skills,
            open_set_requirements,
        ),
        "screening_confidence": build_screening_confidence(
            required_skills,
            open_set_requirements,
            embedding_matcher,
        ),
        "explicit_technical_recovery_summary": job_criteria.get(
            "explicit_technical_recovery_summary",
            {},
        ),
        "promoted_requirements": job_criteria.get("promoted_requirements", []),
        "scoring_requirement_entries": job_criteria.get(
            "scoring_requirement_entries",
            [],
        ),
        "responsibility_signals": job_criteria.get("responsibility_signals", []),
        "technical_responsibility_candidates": job_criteria.get(
            "technical_responsibility_candidates",
            [],
        ),
        "requirement_groups": job_criteria.get("requirement_groups", {}),
        "typed_requirements": job_criteria.get("typed_requirements", []),
        "requirement_provenance_summary": job_criteria.get(
            "requirement_provenance_summary",
            [],
        ),
    }


def _build_structured_cv_text(candidate_payload: dict[str, Any]) -> str:
    """Build parser-friendly CV text when no raw cv_text is supplied."""
    candidate_name = str(candidate_payload.get("candidate_name", "")).strip()
    headline = str(candidate_payload.get("headline", "")).strip()
    summary = str(candidate_payload.get("summary", "")).strip()
    skills = _string_list(candidate_payload.get("skills"))
    work_experience = list(candidate_payload.get("work_experience") or [])
    projects = list(candidate_payload.get("projects") or [])
    education = _string_list(candidate_payload.get("education"))
    certifications = _string_list(candidate_payload.get("certifications"))

    if not any(
        [
            headline,
            summary,
            skills,
            work_experience,
            projects,
            education,
            certifications,
        ]
    ):
        return ""

    lines = [candidate_name or "Unknown Candidate"]
    if headline:
        lines.append(headline)

    if summary:
        lines.extend(["", "Summary:", summary])

    if skills:
        lines.extend(["", "Skills:", *_format_bullets(skills)])

    if work_experience:
        lines.extend(["", "Work Experience:"])
        for entry in work_experience:
            lines.extend(_format_work_experience_entry(entry))

    if projects:
        lines.extend(["", "Projects:"])
        for project in projects:
            lines.extend(_format_project_entry(project))

    if education:
        lines.extend(["", "Education:", *education])

    if certifications:
        lines.extend(["", "Certifications:", *certifications])

    return "\n".join(lines).strip()


def _format_work_experience_entry(entry: dict[str, Any]) -> list[str]:
    """Format one structured work experience entry for the resume parser."""
    title = str(entry.get("title", "")).strip()
    company = str(entry.get("company", "")).strip()
    duration = str(entry.get("duration", "")).strip()
    descriptions = _string_list(entry.get("description") or entry.get("descriptions"))

    heading = " - ".join(part for part in (title, company) if part)
    lines = [heading or "Work Experience"]
    if duration:
        lines.append(duration)
    lines.extend(_format_bullets(descriptions))
    return lines


def _format_project_entry(project: dict[str, Any]) -> list[str]:
    """Format one structured project entry for the resume parser."""
    name = str(project.get("name", "") or project.get("title", "")).strip()
    descriptions = _string_list(project.get("description") or project.get("descriptions"))
    technologies = _string_list(project.get("technologies"))

    lines = [name or "Project"]
    lines.extend(_format_bullets(descriptions))
    if technologies:
        lines.append(f"Technologies: {', '.join(technologies)}")
    return lines


def _build_candidate_source_filename(candidate_payload: dict[str, Any]) -> str:
    """Build a source filename that PHP can map back to application/candidate IDs."""
    application_id = candidate_payload.get("application_id")
    candidate_id = candidate_payload.get("candidate_id")

    if application_id is not None and candidate_id is not None:
        return f"application-{application_id}__candidate-{candidate_id}.txt"
    if application_id is not None:
        return f"application-{application_id}.txt"
    if candidate_id is not None:
        return f"candidate-{candidate_id}.txt"

    candidate_name = _clean_payload_text(candidate_payload.get("candidate_name", "candidate"))
    return f"{_slugify(candidate_name or 'candidate')}.txt"


def _string_list(value: Any) -> list[str]:
    """Convert common payload values into a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return _split_payload_text(value)
    if isinstance(value, list):
        lines: list[str] = []
        for item in value:
            lines.extend(_split_payload_text(item))
        return lines

    return _split_payload_text(value)


def _split_payload_text(value: Any) -> list[str]:
    """Split plain or HTML payload text into parser-friendly lines."""
    text = _clean_payload_text(value)
    return [strip_list_marker(line) for line in text.splitlines() if strip_list_marker(line)]


def _clean_payload_text(value: Any) -> str:
    """Normalize user/editor payload text without changing its meaning."""
    return html_to_plain_text(str(value or "")).strip()


def _format_bullets(items: list[str]) -> list[str]:
    """Format strings as bullet lines."""
    return [f"- {item}" for item in items if item]


def _has_experience_requirement(requirements: list[str]) -> bool:
    """Return True when requirements already mention years of experience."""
    return any(
        re.search(r"\d+\+?\s*(year|years|yr|yrs)", requirement, re.IGNORECASE)
        for requirement in requirements
    )


def _slugify(value: str) -> str:
    """Create a filesystem-ish slug for source file names."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold())
    return slug.strip("-") or "candidate"


def _to_plain_dict(value: Any) -> dict[str, Any]:
    """Convert Pydantic models and dict-like values to plain dictionaries."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()

    raise TypeError("Expected a dictionary or Pydantic model payload.")
