"""Build retrieval-friendly index documents from normalized job cards."""

from __future__ import annotations

from typing import Any

from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text


def build_job_index_documents(job_catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert normalized job cards into retrieval index documents."""
    return [build_job_index_document(job_card) for job_card in job_catalog]


def build_job_index_document(job_card: dict[str, Any]) -> dict[str, Any]:
    """Build one retrieval document from one normalized job card."""
    job_title = str(job_card.get("job_title", "")).strip()
    must_have_skills = list(job_card.get("must_have_skills", []))
    nice_to_have_skills = list(job_card.get("nice_to_have_skills", []))
    open_set_requirements = list(job_card.get("open_set_requirements", []))
    domains = list(job_card.get("domain", []))
    requirement_groups = job_card.get("requirement_groups", {})
    domain_context = list(requirement_groups.get("domain_context", []))

    sparse_segments = [
        job_title,
        *must_have_skills,
        *nice_to_have_skills,
        *open_set_requirements,
        *domains,
        *domain_context,
    ]
    sparse_text = " ".join(segment.strip() for segment in sparse_segments if str(segment).strip())
    dense_text = _build_dense_text(job_card)

    return {
        "job_id": job_card.get("job_id"),
        "job_title": job_title,
        "sparse_text": sparse_text,
        "dense_text": dense_text,
        "must_have_skill_keys": {
            make_lookup_key(skill) for skill in must_have_skills if isinstance(skill, str)
        },
        "nice_to_have_skill_keys": {
            make_lookup_key(skill)
            for skill in nice_to_have_skills
            if isinstance(skill, str)
        },
        "domain_keys": {
            make_lookup_key(domain) for domain in domains if isinstance(domain, str)
        },
        "title_terms": _term_set(job_title),
        "sparse_terms": _term_set(sparse_text),
        "job_card": job_card,
    }


def _build_dense_text(job_card: dict[str, Any]) -> str:
    """Build one readable dense retrieval string for one job."""
    job_title = str(job_card.get("job_title", "")).strip() or "Untitled Job"
    must_have_skills = list(job_card.get("must_have_skills", []))
    nice_to_have_skills = list(job_card.get("nice_to_have_skills", []))
    open_set_requirements = list(job_card.get("open_set_requirements", []))
    domains = list(job_card.get("domain", []))
    minimum_experience_years = job_card.get("minimum_experience_years", 0)
    seniority = str(job_card.get("seniority", "Not specified")).strip()

    parts = [job_title]
    if must_have_skills:
        parts.append(f"Must-have skills: {', '.join(must_have_skills)}.")
    if nice_to_have_skills:
        parts.append(f"Nice-to-have skills: {', '.join(nice_to_have_skills)}.")
    if open_set_requirements:
        parts.append(f"Additional requirements: {', '.join(open_set_requirements)}.")
    if domains:
        parts.append(f"Domain: {', '.join(domains)}.")
    if minimum_experience_years:
        parts.append(f"Minimum experience: {minimum_experience_years} years.")
    if seniority and seniority != "Not specified":
        parts.append(f"Seniority: {seniority}.")

    return " ".join(parts)


def _term_set(value: str) -> set[str]:
    """Build a normalized sparse term set from text."""
    normalized = normalize_search_text(value)
    return set(normalized.split()) if normalized else set()
