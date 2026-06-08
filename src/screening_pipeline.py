"""End-to-end screening pipeline for CLI and future UI use."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.document_loader import load_text_file, load_text_files_from_directory
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.open_set_matcher import (
    build_taxonomy_coverage,
    find_semantic_requirement_evidence,
    split_known_and_unknown_requirements,
)
from src.resume_parser import parse_resume
from src.review_card_generator import (
    format_review_card_markdown,
    generate_review_card,
)
from src.scorer import rank_candidates, score_candidate
from src.semantic_matcher import match_skills
from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


DEFAULT_TAXONOMY_PATH = "data/taxonomy/skills.json"


def run_screening_pipeline(
    jd_path: str | Path,
    cv_dir: str | Path,
    taxonomy_path: str | Path = DEFAULT_TAXONOMY_PATH,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Run the full text-based screening pipeline for one JD and many CVs."""
    taxonomy = load_taxonomy(taxonomy_path)
    jd_text = load_text_file(jd_path)
    job_criteria = parse_jd(jd_text)
    cv_documents = load_text_files_from_directory(cv_dir)

    required_skills = _build_job_skill_list(
        job_criteria.get("must_have_skills", []),
        jd_text,
        taxonomy,
        use_full_text_fallback=True,
        include_unknown_skills=False,
    )
    open_set_requirements = split_known_and_unknown_requirements(
        job_criteria.get("must_have_skills", []),
        required_skills,
        taxonomy,
    )
    unknown_requirements = open_set_requirements["unknown_requirements"]
    taxonomy_coverage = build_taxonomy_coverage(
        required_skills,
        unknown_requirements,
    )
    nice_to_have_skills = _build_job_skill_list(
        job_criteria.get("nice_to_have_skills", []),
        "",
        taxonomy,
        use_full_text_fallback=False,
        include_unknown_skills=embedding_matcher is not None,
    )

    candidate_results = [
        _process_candidate_document(
            document,
            job_criteria,
            taxonomy,
            required_skills,
            nice_to_have_skills,
            unknown_requirements,
            embedding_matcher,
        )
        for document in cv_documents
    ]
    ranked_candidates = rank_candidates(candidate_results)

    for candidate in ranked_candidates:
        candidate["review_card"] = generate_review_card(candidate, job_criteria)

    return {
        "job": _build_job_output(
            job_criteria,
            required_skills,
            nice_to_have_skills,
            taxonomy_coverage,
        ),
        "candidates": ranked_candidates,
    }


def save_pipeline_result_json(
    result: dict[str, Any],
    output_path: str | Path,
) -> str:
    """Save a pipeline result as pretty JSON and return the saved path."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return str(path)


def save_review_cards(
    result: dict[str, Any],
    output_dir: str | Path,
) -> list[str]:
    """Save candidate review cards as Markdown files and return saved paths."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    saved_paths: list[str] = []
    for candidate in result.get("candidates", []):
        review_card = candidate.get("review_card", {})
        filename = _build_review_card_filename(candidate)
        output_path = directory / filename
        output_path.write_text(
            format_review_card_markdown(review_card),
            encoding="utf-8",
        )
        saved_paths.append(str(output_path))

    return saved_paths


def format_ranking_summary(result: dict[str, Any]) -> str:
    """Format a short terminal ranking summary."""
    job = result.get("job", {})
    candidates = result.get("candidates", [])
    lines = [
        "Semantic Skills-based Resume Screening System",
        "Phase 10 - CLI Pipeline and Output",
        "",
        f"Job: {job.get('title', '')}",
        f"Candidates analyzed: {len(candidates)}",
        "",
        "Ranking:",
    ]

    if not candidates:
        lines.append("- No candidates found.")
        return "\n".join(lines)

    for candidate in candidates:
        lines.append(
            (
                f"{candidate.get('rank')}. {candidate.get('candidate_name')} - "
                f"{candidate.get('final_score')}/100 - "
                f"{candidate.get('recommendation')}"
            )
        )

    return "\n".join(lines)


def _process_candidate_document(
    document: dict[str, Any],
    job_criteria: dict[str, Any],
    taxonomy: dict[str, dict[str, Any]],
    required_skills: list[str],
    nice_to_have_skills: list[str],
    unknown_requirements: list[str],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Process one loaded CV document into a scored candidate result."""
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
    scored_matches = [*enriched_matches, *open_set_matches]
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

    return {
        **scored_candidate,
        "open_set_requirement_matches": open_set_matches,
        "source_file": document.get("filename", ""),
        "source_path": document.get("path", ""),
    }


def _build_job_skill_list(
    raw_items: list[str],
    fallback_text: str,
    taxonomy: dict[str, dict[str, Any]],
    use_full_text_fallback: bool,
    include_unknown_skills: bool = False,
) -> list[str]:
    """Build a precise job skill list from parsed items plus taxonomy extraction."""
    normalized_skills = normalize_skills(raw_items, taxonomy)
    known_skills = [skill for skill in normalized_skills if skill in taxonomy]
    unknown_skill_labels = [
        skill
        for skill in normalized_skills
        if skill not in taxonomy and _looks_like_skill_label(skill)
    ]
    extracted_skills = extract_taxonomy_skills_from_text("\n".join(raw_items), taxonomy)

    if not extracted_skills and use_full_text_fallback:
        extracted_skills = extract_taxonomy_skills_from_text(fallback_text, taxonomy)

    if extracted_skills or known_skills:
        if include_unknown_skills:
            return merge_skill_lists(extracted_skills, known_skills, unknown_skill_labels)

        return merge_skill_lists(extracted_skills, known_skills)

    if include_unknown_skills:
        return merge_skill_lists(unknown_skill_labels)

    return []


def _enrich_resume_skills(
    resume_profile: dict[str, Any],
    raw_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> None:
    """Add taxonomy skills found in raw resume text to parsed resume skills."""
    parsed_skills = list(resume_profile.get("raw_skills", []))
    extracted_skills = extract_taxonomy_skills_from_text(raw_text, taxonomy)
    resume_profile["raw_skills"] = merge_skill_lists(parsed_skills, extracted_skills)


def _looks_like_skill_label(value: str) -> bool:
    """Avoid treating long requirement sentences as unknown skill labels."""
    words = value.split()
    if len(words) > 5 or len(value) > 60:
        return False
    if value.rstrip().endswith(":"):
        return False
    if value.rstrip().endswith((".", "!", "?")):
        return False

    return True


def _build_job_output(
    job_criteria: dict[str, Any],
    required_skills: list[str],
    nice_to_have_skills: list[str],
    taxonomy_coverage: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a stable job summary for pipeline output."""
    return {
        "title": job_criteria.get("job_title", ""),
        "must_have_skills": required_skills,
        "nice_to_have_skills": nice_to_have_skills,
        "minimum_experience_years": job_criteria.get("minimum_experience_years", 0),
        "seniority": job_criteria.get("seniority", "Not specified"),
        "domain": job_criteria.get("domain", []),
        "taxonomy_coverage": taxonomy_coverage or build_taxonomy_coverage(
            required_skills,
            [],
        ),
    }


def _build_review_card_filename(candidate: dict[str, Any]) -> str:
    """Build a stable Markdown filename for one candidate review card."""
    rank = int(candidate.get("rank", 0))
    candidate_name = str(candidate.get("candidate_name", "candidate")).strip()
    slug = _slugify(candidate_name or "candidate")
    return f"rank-{rank:02d}-{slug}.md"


def _slugify(value: str) -> str:
    """Create a filesystem-friendly ASCII-ish slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold())
    return slug.strip("-") or "candidate"
