"""Screening pipeline that accepts web/API JSON payloads."""

from __future__ import annotations

import re
from typing import Any

from src.api_models import CandidatePayload, JobPayload, ScreeningRequest
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.review_card_generator import generate_review_card
from src.scorer import rank_candidates, score_candidate
from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    _build_job_skill_list,
    _enrich_resume_skills,
)
from src.semantic_matcher import match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


def build_jd_text_from_payload(job: dict[str, Any] | JobPayload) -> str:
    """Build parser-friendly JD text from a web job payload."""
    job_payload = _to_plain_dict(job)
    raw_text = str(job_payload.get("raw_text", "")).strip()
    if raw_text:
        return raw_text

    job_title = str(job_payload.get("job_title", "")).strip()
    description = str(job_payload.get("description", "")).strip()
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
    cv_text = str(candidate_payload.get("cv_text", "")).strip()

    if not cv_text:
        cv_text = _build_structured_cv_text(candidate_payload)

    if not cv_text:
        candidate_name = str(candidate_payload.get("candidate_name", "")).strip()
        raise ValueError(
            f"Candidate payload must include cv_text or structured CV data: {candidate_name}"
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
    job_criteria = parse_jd(job_text)
    required_skills = _build_job_skill_list(
        job_criteria.get("must_have_skills", []),
        job_text,
        taxonomy,
        use_full_text_fallback=True,
        include_unknown_skills=embedding_matcher is not None,
    )
    nice_to_have_skills = _build_job_skill_list(
        job_criteria.get("nice_to_have_skills", []),
        "",
        taxonomy,
        use_full_text_fallback=False,
        include_unknown_skills=embedding_matcher is not None,
    )

    candidate_results = [
        _process_candidate_payload(
            candidate_payload,
            job_criteria,
            taxonomy,
            required_skills,
            nice_to_have_skills,
            embedding_matcher,
        )
        for candidate_payload in candidate_payloads
    ]
    ranked_candidates = rank_candidates(candidate_results)

    for candidate in ranked_candidates:
        candidate["review_card"] = generate_review_card(candidate, job_criteria)

    return {
        "job": _build_job_output(job_payload, job_criteria, required_skills, nice_to_have_skills),
        "candidates": ranked_candidates,
    }


def _process_candidate_payload(
    candidate_payload: dict[str, Any],
    job_criteria: dict[str, Any],
    taxonomy: dict[str, dict[str, Any]],
    required_skills: list[str],
    nice_to_have_skills: list[str],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Process one candidate payload into a scored candidate result."""
    document = build_cv_document_from_payload(candidate_payload)
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
    nice_to_have_matches = match_skills(
        nice_to_have_skills,
        candidate_skills,
        taxonomy,
        embedding_matcher=embedding_matcher,
    )
    scored_candidate = score_candidate(
        job_criteria,
        resume_profile,
        enriched_matches,
        nice_to_have_matches,
    )

    if not scored_candidate.get("candidate_name") and document.get("candidate_name"):
        scored_candidate["candidate_name"] = document["candidate_name"]

    return {
        **scored_candidate,
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
) -> dict[str, Any]:
    """Build a stable API job response object."""
    return {
        "job_id": job_payload.get("job_id"),
        "title": job_criteria.get("job_title", ""),
        "must_have_skills": required_skills,
        "nice_to_have_skills": nice_to_have_skills,
        "minimum_experience_years": job_criteria.get("minimum_experience_years", 0),
        "seniority": job_criteria.get("seniority", "Not specified"),
        "domain": job_criteria.get("domain", []),
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

    candidate_name = str(candidate_payload.get("candidate_name", "candidate")).strip()
    return f"{_slugify(candidate_name or 'candidate')}.txt"


def _string_list(value: Any) -> list[str]:
    """Convert common payload values into a clean list of strings."""
    if value is None:
        return []
    if isinstance(value, str):
        return [line.strip("- ").strip() for line in value.splitlines() if line.strip()]
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    return [str(value).strip()] if str(value).strip() else []


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
