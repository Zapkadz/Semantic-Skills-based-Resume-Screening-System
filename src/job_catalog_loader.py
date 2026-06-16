"""Build a normalized job catalog for candidate-side retrieval."""

from __future__ import annotations

from typing import Any

from src.api_models import JobPayload
from src.jd_parser import parse_jd
from src.jd_requirement_classifier import (
    build_scoring_requirement_lines,
    classify_jd_requirements,
)
from src.job_quality_gate import evaluate_job_quality
from src.open_set_matcher import build_taxonomy_coverage
from src.payload_pipeline import build_jd_text_from_payload
from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    _build_job_skill_list,
    _build_open_set_requirements,
)
from src.skill_taxonomy import load_taxonomy


def build_job_catalog(
    jobs: list[dict[str, Any] | JobPayload],
    taxonomy_path: str = DEFAULT_TAXONOMY_PATH,
) -> list[dict[str, Any]]:
    """Build normalized job cards from raw API/web job payloads."""
    taxonomy = load_taxonomy(taxonomy_path)
    job_catalog: list[dict[str, Any]] = []

    for job in jobs:
        job_payload = _to_plain_dict(job)
        jd_text = build_jd_text_from_payload(job_payload)
        job_criteria = parse_jd(jd_text)
        requirement_groups = classify_jd_requirements(job_criteria, jd_text, taxonomy)
        job_criteria = {
            **job_criteria,
            "requirement_groups": requirement_groups,
        }
        required_requirement_lines, nice_to_have_requirement_lines = (
            build_scoring_requirement_lines(requirement_groups)
        )
        must_have_skills = _build_job_skill_list(
            required_requirement_lines,
            "\n".join(required_requirement_lines),
            taxonomy,
            use_full_text_fallback=True,
            include_unknown_skills=False,
        )
        open_set_requirements = _build_open_set_requirements(
            {**job_criteria, "must_have_skills": required_requirement_lines},
            "\n".join(required_requirement_lines),
            must_have_skills,
            taxonomy,
        )
        nice_to_have_skills = _build_job_skill_list(
            nice_to_have_requirement_lines,
            "\n".join(nice_to_have_requirement_lines),
            taxonomy,
            use_full_text_fallback=False,
            include_unknown_skills=False,
        )
        job_quality = evaluate_job_quality(
            job_payload,
            job_criteria,
            jd_text,
            requirement_groups,
            must_have_skills,
            nice_to_have_skills,
            open_set_requirements,
        )

        job_catalog.append(
            {
                "job_id": job_payload.get("job_id"),
                "job_title": job_criteria.get("job_title", "")
                or job_payload.get("job_title")
                or job_payload.get("title", ""),
                "raw_text": jd_text,
                "job_payload": job_payload,
                "job_criteria": job_criteria,
                "must_have_skills": must_have_skills,
                "nice_to_have_skills": nice_to_have_skills,
                "open_set_requirements": open_set_requirements,
                "minimum_experience_years": job_criteria.get(
                    "minimum_experience_years",
                    0,
                ),
                "seniority": job_criteria.get("seniority", "Not specified"),
                "domain": job_criteria.get("domain", []),
                "taxonomy_coverage": build_taxonomy_coverage(
                    must_have_skills,
                    open_set_requirements,
                ),
                "requirement_groups": requirement_groups,
                "job_quality": job_quality,
            }
        )

    return job_catalog


def _to_plain_dict(value: Any) -> dict[str, Any]:
    """Convert Pydantic models and dict-like values to plain dictionaries."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()

    raise TypeError("Expected a dictionary or Pydantic model payload.")
