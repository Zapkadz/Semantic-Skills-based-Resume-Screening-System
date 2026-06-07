"""End-to-end screening pipeline for CLI and future UI use."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.document_loader import load_text_file, load_text_files_from_directory
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.review_card_generator import (
    format_review_card_markdown,
    generate_review_card,
)
from src.scorer import rank_candidates, score_candidate
from src.semantic_matcher import match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


DEFAULT_TAXONOMY_PATH = "data/taxonomy/skills.json"


def run_screening_pipeline(
    jd_path: str | Path,
    cv_dir: str | Path,
    taxonomy_path: str | Path = DEFAULT_TAXONOMY_PATH,
) -> dict[str, Any]:
    """Run the full text-based screening pipeline for one JD and many CVs."""
    taxonomy = load_taxonomy(taxonomy_path)
    job_criteria = parse_jd(load_text_file(jd_path))
    cv_documents = load_text_files_from_directory(cv_dir)

    required_skills = normalize_skills(
        job_criteria.get("must_have_skills", []),
        taxonomy,
    )
    nice_to_have_skills = normalize_skills(
        job_criteria.get("nice_to_have_skills", []),
        taxonomy,
    )

    candidate_results = [
        _process_candidate_document(
            document,
            job_criteria,
            taxonomy,
            required_skills,
            nice_to_have_skills,
        )
        for document in cv_documents
    ]
    ranked_candidates = rank_candidates(candidate_results)

    for candidate in ranked_candidates:
        candidate["review_card"] = generate_review_card(candidate, job_criteria)

    return {
        "job": _build_job_output(job_criteria, required_skills, nice_to_have_skills),
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
) -> dict[str, Any]:
    """Process one loaded CV document into a scored candidate result."""
    resume_profile = parse_resume(document["text"])
    candidate_skills = normalize_skills(resume_profile.get("raw_skills", []), taxonomy)
    must_have_matches = match_skills(required_skills, candidate_skills, taxonomy)
    enriched_matches = detect_all_evidence(must_have_matches, resume_profile)
    nice_to_have_matches = match_skills(
        nice_to_have_skills,
        candidate_skills,
        taxonomy,
    )
    scored_candidate = score_candidate(
        job_criteria,
        resume_profile,
        enriched_matches,
        nice_to_have_matches,
    )

    return {
        **scored_candidate,
        "source_file": document.get("filename", ""),
        "source_path": document.get("path", ""),
    }


def _build_job_output(
    job_criteria: dict[str, Any],
    required_skills: list[str],
    nice_to_have_skills: list[str],
) -> dict[str, Any]:
    """Build a stable job summary for pipeline output."""
    return {
        "title": job_criteria.get("job_title", ""),
        "must_have_skills": required_skills,
        "nice_to_have_skills": nice_to_have_skills,
        "minimum_experience_years": job_criteria.get("minimum_experience_years", 0),
        "seniority": job_criteria.get("seniority", "Not specified"),
        "domain": job_criteria.get("domain", []),
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
