"""Build a normalized job catalog for candidate-side retrieval."""

from __future__ import annotations

from typing import Any

from src.api_models import JobPayload
from src.jd_parser import parse_jd
from src.jd_requirement_classifier import (
    enrich_job_criteria_with_requirement_metadata,
)
from src.job_quality_gate import evaluate_job_quality
from src.open_set_matcher import build_taxonomy_coverage
from src.payload_diagnostics import diagnose_job_payload
from src.payload_pipeline import build_jd_text_from_payload
from src.requirement_promotion import build_scoring_requirement_lines_from_entries
from src.role_family import infer_job_role_profile
from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    _build_job_skill_list,
    _build_open_set_requirement_data,
)
from src.skill_taxonomy import load_taxonomy
from src.technical_intent import build_requirement_intent_summary


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
        payload_diagnostics = diagnose_job_payload(job_payload, jd_text)
        job_criteria = parse_jd(jd_text)
        job_criteria = enrich_job_criteria_with_requirement_metadata(
            job_criteria,
            jd_text,
            taxonomy,
        )
        typed_requirements = job_criteria["typed_requirements"]
        requirement_groups = job_criteria["requirement_groups"]
        required_requirement_lines, nice_to_have_requirement_lines = (
            build_scoring_requirement_lines_from_entries(
                job_criteria.get("scoring_requirement_entries", [])
            )
        )
        must_have_skills = _build_job_skill_list(
            required_requirement_lines,
            "\n".join(required_requirement_lines),
            taxonomy,
            use_full_text_fallback=True,
            include_unknown_skills=False,
        )
        open_set_data = _build_open_set_requirement_data(
            {**job_criteria, "must_have_skills": required_requirement_lines},
            "\n".join(required_requirement_lines),
            must_have_skills,
            taxonomy,
        )
        open_set_requirements = open_set_data["open_set_requirements"]
        job_role_profile = infer_job_role_profile(
            job_title=job_criteria.get("job_title", "")
            or job_payload.get("job_title")
            or job_payload.get("title", ""),
            required_skills=must_have_skills,
            open_set_requirements=open_set_requirements,
            responsibilities=requirement_groups.get("responsibilities", []),
            typed_requirements=typed_requirements,
        )
        requirement_intent_summary = build_requirement_intent_summary(
            job_role_profile,
            must_have_skills,
            open_set_requirements,
            typed_requirements=typed_requirements,
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
                "payload_diagnostics": payload_diagnostics,
                "job_criteria": job_criteria,
                "must_have_skills": must_have_skills,
                "nice_to_have_skills": nice_to_have_skills,
                "open_set_requirements": open_set_requirements,
                "open_set_candidates": open_set_data["open_set_candidates"],
                "discarded_open_set_candidates": open_set_data[
                    "discarded_open_set_candidates"
                ],
                "open_set_filter_summary": open_set_data["open_set_filter_summary"],
                "minimum_experience_years": job_criteria.get(
                    "minimum_experience_years",
                    0,
                ),
                "seniority": job_criteria.get("seniority", "Not specified"),
                "domain": job_criteria.get("domain", []),
                "job_role_profile": job_role_profile,
                "requirement_intent_summary": requirement_intent_summary,
                "taxonomy_coverage": build_taxonomy_coverage(
                    must_have_skills,
                    open_set_requirements,
                ),
                "responsibility_signals": job_criteria.get("responsibility_signals", []),
                "technical_responsibility_candidates": job_criteria.get(
                    "technical_responsibility_candidates",
                    [],
                ),
                "promoted_requirements": job_criteria.get("promoted_requirements", []),
                "scoring_requirement_entries": job_criteria.get(
                    "scoring_requirement_entries",
                    [],
                ),
                "typed_requirements": typed_requirements,
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
