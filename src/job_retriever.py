"""Retrieve top-N candidate-side jobs before expensive reranking."""

from __future__ import annotations

from typing import Any

from src.api_models import CandidatePayload
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.payload_pipeline import build_cv_document_from_payload
from src.resume_parser import parse_resume
from src.scorer import calculate_experience_score, detect_candidate_domains, estimate_experience_years
from src.screening_pipeline import DEFAULT_TAXONOMY_PATH
from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy, make_lookup_key
from src.text_normalization import normalize_search_text


SPARSE_SCORE_WEIGHTS = {
    "must_have_overlap": 0.45,
    "title_overlap": 0.20,
    "domain_overlap": 0.20,
    "nice_to_have_overlap": 0.10,
    "experience_compatibility": 0.05,
}

HYBRID_SPARSE_WEIGHT = 0.70
HYBRID_DENSE_WEIGHT = 0.30


def build_candidate_query_profile(
    candidate: dict[str, Any] | CandidatePayload,
    taxonomy_path: str = DEFAULT_TAXONOMY_PATH,
    candidate_document: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a retrieval-focused candidate query profile from one payload."""
    candidate_payload = _to_plain_dict(candidate)
    taxonomy = load_taxonomy(taxonomy_path)

    if candidate_document is None:
        candidate_document = build_cv_document_from_payload(candidate_payload)

    resume_profile = parse_resume(candidate_document["text"])
    parsed_skills = list(resume_profile.get("raw_skills", []))
    extracted_skills = extract_taxonomy_skills_from_text(
        candidate_document["text"],
        taxonomy,
    )
    normalized_skills = normalize_skills(
        merge_skill_lists(parsed_skills, extracted_skills),
        taxonomy,
    )
    resume_profile["raw_skills"] = normalized_skills

    headline = str(resume_profile.get("headline", "")).strip()
    summary_text = str(resume_profile.get("summary", "")).strip()
    domains = detect_candidate_domains(resume_profile)
    experience_years = round(estimate_experience_years(resume_profile), 2)
    dense_query_text = _build_dense_query_text(
        headline,
        summary_text,
        normalized_skills,
        domains,
        experience_years,
    )
    sparse_query_text = " ".join(
        segment
        for segment in (
            resume_profile.get("candidate_name", ""),
            headline,
            summary_text,
            " ".join(normalized_skills),
            " ".join(domains),
        )
        if str(segment).strip()
    )

    return {
        "candidate_name": resume_profile.get("candidate_name", ""),
        "headline": headline,
        "summary_text": summary_text,
        "skills": normalized_skills,
        "domains": domains,
        "experience_years": experience_years,
        "dense_query_text": dense_query_text,
        "sparse_query_text": sparse_query_text,
        "skill_keys": {
            make_lookup_key(skill) for skill in normalized_skills if isinstance(skill, str)
        },
        "domain_keys": {
            make_lookup_key(domain) for domain in domains if isinstance(domain, str)
        },
        "headline_terms": _term_set(headline),
        "sparse_terms": _term_set(sparse_query_text),
        "resume_profile": resume_profile,
        "candidate_document": candidate_document,
    }


def retrieve_candidate_jobs(
    candidate_profile: dict[str, Any],
    indexed_jobs: list[dict[str, Any]],
    top_n: int = 50,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> list[dict[str, Any]]:
    """Retrieve top candidate-side jobs using sparse-first hybrid scoring."""
    if not indexed_jobs:
        return []

    dense_scores = _build_dense_score_map(
        candidate_profile,
        indexed_jobs,
        embedding_matcher,
    )

    retrieved_jobs = [
        _score_retrieval_document(candidate_profile, document, dense_scores.get(index))
        for index, document in enumerate(indexed_jobs)
    ]
    retrieved_jobs.sort(
        key=lambda job: (
            -float(job.get("retrieval_score", 0.0)),
            -float(job.get("retrieval_components", {}).get("must_have_overlap", 0.0)),
            -float(job.get("retrieval_components", {}).get("dense_score") or 0.0),
            str(job.get("job_title", "")).casefold(),
        )
    )

    return [
        {
            "retrieval_rank": index,
            **job,
        }
        for index, job in enumerate(retrieved_jobs[:top_n], start=1)
    ]


def _score_retrieval_document(
    candidate_profile: dict[str, Any],
    indexed_job: dict[str, Any],
    dense_score: float | None,
) -> dict[str, Any]:
    """Score one indexed job for retrieval and attach debug reasons."""
    job_card = indexed_job["job_card"]
    must_have_overlap = _overlap_ratio(
        candidate_profile.get("skill_keys", set()),
        indexed_job.get("must_have_skill_keys", set()),
    )
    nice_to_have_overlap = _overlap_ratio(
        candidate_profile.get("skill_keys", set()),
        indexed_job.get("nice_to_have_skill_keys", set()),
    )
    domain_overlap = _overlap_ratio(
        candidate_profile.get("domain_keys", set()),
        indexed_job.get("domain_keys", set()),
    )
    title_overlap = _overlap_ratio(
        candidate_profile.get("headline_terms", set()),
        indexed_job.get("title_terms", set()),
    )
    experience_compatibility = calculate_experience_score(
        float(candidate_profile.get("experience_years", 0.0)),
        int(job_card.get("minimum_experience_years", 0) or 0),
    )
    sparse_score = round(
        (
            must_have_overlap * SPARSE_SCORE_WEIGHTS["must_have_overlap"]
            + title_overlap * SPARSE_SCORE_WEIGHTS["title_overlap"]
            + domain_overlap * SPARSE_SCORE_WEIGHTS["domain_overlap"]
            + nice_to_have_overlap * SPARSE_SCORE_WEIGHTS["nice_to_have_overlap"]
            + experience_compatibility * SPARSE_SCORE_WEIGHTS["experience_compatibility"]
        ),
        4,
    )
    retrieval_score = _combine_sparse_and_dense_scores(sparse_score, dense_score)

    return {
        "job_id": indexed_job.get("job_id"),
        "job_title": indexed_job.get("job_title", ""),
        "retrieval_score": retrieval_score,
        "retrieval_reasons": _build_retrieval_reasons(
            must_have_overlap,
            title_overlap,
            domain_overlap,
            nice_to_have_overlap,
            experience_compatibility,
            dense_score,
        ),
        "retrieval_components": {
            "must_have_overlap": must_have_overlap,
            "title_overlap": title_overlap,
            "domain_overlap": domain_overlap,
            "nice_to_have_overlap": nice_to_have_overlap,
            "experience_compatibility": experience_compatibility,
            "sparse_score": sparse_score,
            "dense_score": dense_score,
        },
        "job_card": job_card,
    }


def _build_dense_score_map(
    candidate_profile: dict[str, Any],
    indexed_jobs: list[dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None,
) -> dict[int, float]:
    """Build a dense retrieval score per indexed job when embedding is available."""
    if embedding_matcher is None:
        return {}

    dense_query_text = str(candidate_profile.get("dense_query_text", "")).strip()
    if not dense_query_text:
        return {}

    dense_texts = [str(job.get("dense_text", "")).strip() for job in indexed_jobs]
    similarities = embedding_matcher.similarity_matrix([dense_query_text], dense_texts)
    if not similarities:
        return {}

    return {
        index: round(max(0.0, float(score)), 4)
        for index, score in enumerate(similarities[0])
    }


def _build_dense_query_text(
    headline: str,
    summary_text: str,
    skills: list[str],
    domains: list[str],
    experience_years: float,
) -> str:
    """Build a readable dense retrieval query string for one candidate."""
    parts = []
    if headline:
        parts.append(headline)
    if summary_text:
        parts.append(summary_text)
    if skills:
        parts.append(f"Skills: {', '.join(skills)}.")
    if domains:
        parts.append(f"Domains: {', '.join(domains)}.")
    if experience_years > 0:
        parts.append(f"Experience: {experience_years} years.")

    return " ".join(parts)


def _combine_sparse_and_dense_scores(
    sparse_score: float,
    dense_score: float | None,
) -> float:
    """Combine sparse and dense retrieval scores into one sortable value."""
    if dense_score is None:
        return sparse_score

    return round(
        sparse_score * HYBRID_SPARSE_WEIGHT + dense_score * HYBRID_DENSE_WEIGHT,
        4,
    )


def _build_retrieval_reasons(
    must_have_overlap: float,
    title_overlap: float,
    domain_overlap: float,
    nice_to_have_overlap: float,
    experience_compatibility: float,
    dense_score: float | None,
) -> list[str]:
    """Build short human-readable reasons for one retrieval result."""
    reasons: list[str] = []

    if must_have_overlap >= 0.6:
        reasons.append("Strong must-have skill overlap.")
    elif must_have_overlap > 0:
        reasons.append("Some must-have skill overlap.")

    if title_overlap >= 0.2:
        reasons.append("Job title overlaps with the current candidate profile.")

    if domain_overlap > 0:
        reasons.append("Domain overlap detected.")

    if nice_to_have_overlap > 0:
        reasons.append("Optional skill overlap detected.")

    if experience_compatibility >= 0.75:
        reasons.append("Experience level appears compatible.")

    if dense_score is not None and dense_score >= 0.75:
        reasons.append("Semantic profile similarity is strong.")

    return reasons or ["Broad profile overlap detected."]


def _overlap_ratio(left: set[str], right: set[str]) -> float:
    """Calculate overlap over the job-side set size for retrieval scoring."""
    if not right:
        return 0.0

    overlap_count = len(left & right)
    return round(overlap_count / len(right), 4)


def _term_set(value: str) -> set[str]:
    """Build a normalized sparse term set from text."""
    normalized = normalize_search_text(value)
    return set(normalized.split()) if normalized else set()


def _to_plain_dict(value: Any) -> dict[str, Any]:
    """Convert Pydantic models and dict-like values to plain dictionaries."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()

    raise TypeError("Expected a dictionary or Pydantic model payload.")
