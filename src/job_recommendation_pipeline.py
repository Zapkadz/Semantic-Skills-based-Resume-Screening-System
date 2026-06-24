"""Candidate-side job recommendation pipeline for one CV and many JDs."""

from __future__ import annotations

from typing import Any

from src.api_models import JobRecommendationRequest
from src.candidate_job_reranker import rerank_candidate_jobs
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.job_catalog_loader import build_job_catalog
from src.job_indexer import build_job_index_documents
from src.payload_diagnostics import diagnose_candidate_payload
from src.job_retriever import build_candidate_query_profile, retrieve_candidate_jobs
from src.payload_pipeline import build_cv_document_from_payload
from src.runtime_diagnostics import build_recommendation_diagnostics, build_trace_id
from src.screening_pipeline import DEFAULT_TAXONOMY_PATH


DEFAULT_TOP_K = 10
DEFAULT_RETRIEVAL_TOP_N = 50


def run_job_recommendation_payload(
    payload: dict[str, Any] | JobRecommendationRequest,
    taxonomy_path: str = DEFAULT_TAXONOMY_PATH,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Recommend top matching jobs for one candidate payload."""
    payload_data = _to_plain_dict(payload)
    if payload_data.get("taxonomy_path"):
        taxonomy_path = str(payload_data["taxonomy_path"])

    candidate_payload = _to_plain_dict(payload_data.get("candidate", {}))
    job_payloads = [_to_plain_dict(job) for job in payload_data.get("jobs", [])]
    options = _to_plain_dict(payload_data.get("options", {}))
    top_k = _coerce_positive_int(
        options.get("top_k", DEFAULT_TOP_K),
        option_name="top_k",
    )

    if not job_payloads:
        raise ValueError("Recommendation payload must include at least one job.")

    trace_id = build_trace_id("recommend-jobs")
    candidate_document = build_cv_document_from_payload(candidate_payload)
    candidate_payload_diagnostics = diagnose_candidate_payload(
        candidate_payload,
        candidate_document,
    )
    candidate_profile = build_candidate_query_profile(
        candidate_payload,
        taxonomy_path=taxonomy_path,
        candidate_document=candidate_document,
    )
    job_catalog = build_job_catalog(job_payloads, taxonomy_path=taxonomy_path)
    eligible_job_catalog = [
        job
        for job in job_catalog
        if job.get("job_quality", {}).get("recommendation_eligible") is True
    ]
    excluded_jobs = [
        _build_excluded_job_summary(job)
        for job in job_catalog
        if job.get("job_quality", {}).get("recommendation_eligible") is not True
    ]
    indexed_jobs = build_job_index_documents(eligible_job_catalog)
    retrieval_top_n = min(
        len(indexed_jobs),
        _coerce_positive_int(
            options.get(
                "retrieval_top_n",
                _default_retrieval_top_n(top_k, len(indexed_jobs)),
            ),
            option_name="retrieval_top_n",
        ),
    )
    retrieved_jobs = retrieve_candidate_jobs(
        candidate_profile,
        indexed_jobs,
        top_n=retrieval_top_n,
        embedding_matcher=embedding_matcher,
    )
    reranked_jobs = rerank_candidate_jobs(
        candidate_payload,
        retrieved_jobs,
        taxonomy_path,
        embedding_matcher=embedding_matcher,
    )
    top_jobs = reranked_jobs[:top_k]

    candidate_summary = _build_candidate_summary(
        candidate_payload,
        candidate_document,
        top_jobs,
    )
    retrieval_stats = {
        "jobs_received": len(job_payloads),
        "jobs_indexed": len(indexed_jobs),
        "jobs_retrieved": len(retrieved_jobs),
        "jobs_reranked": len(reranked_jobs),
        "top_k": min(top_k, len(eligible_job_catalog)),
        "retrieval_top_n": retrieval_top_n,
        "retrieval_applied": bool(indexed_jobs)
        and len(retrieved_jobs) < len(indexed_jobs),
    }
    job_quality_stats = {
        "jobs_received": len(job_payloads),
        "eligible_jobs": len(eligible_job_catalog),
        "excluded_jobs": len(excluded_jobs),
    }
    warnings = _build_recommendation_warnings(eligible_job_catalog, excluded_jobs)

    return {
        "trace_id": trace_id,
        "candidate": candidate_summary,
        "top_jobs": top_jobs,
        "excluded_jobs": excluded_jobs,
        "retrieval_stats": retrieval_stats,
        "job_quality_stats": job_quality_stats,
        "warnings": warnings,
        "diagnostics": build_recommendation_diagnostics(
            trace_id=trace_id,
            candidate_payload_diagnostics=candidate_payload_diagnostics,
            job_catalog=job_catalog,
            retrieval_stats=retrieval_stats,
            job_quality_stats=job_quality_stats,
            top_jobs=top_jobs,
            excluded_jobs=excluded_jobs,
            embedding_enabled=embedding_matcher is not None,
        ),
    }


def _build_candidate_summary(
    candidate_payload: dict[str, Any],
    candidate_document: dict[str, Any],
    top_jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a stable candidate summary for the recommendation response."""
    candidate_name = str(candidate_payload.get("candidate_name", "")).strip()
    if not candidate_name and top_jobs:
        candidate_name = str(
            top_jobs[0].get("review_card", {}).get("candidate_name", "")
        ).strip()

    return {
        "candidate_id": candidate_payload.get("candidate_id"),
        "candidate_name": candidate_name,
        "source_file": candidate_document.get("filename", ""),
        "cv_file_path": candidate_document.get("cv_file_path", ""),
    }


def _build_excluded_job_summary(job_card: dict[str, Any]) -> dict[str, Any]:
    """Build a compact summary for jobs excluded by the JD quality gate."""
    return {
        "job_id": job_card.get("job_id"),
        "job_title": job_card.get("job_title", ""),
        "job_quality": job_card.get("job_quality", {}),
        "payload_diagnostics": job_card.get("payload_diagnostics", {}),
        "taxonomy_coverage": job_card.get("taxonomy_coverage", {}),
        "typed_requirements": job_card.get("typed_requirements", []),
        "open_set_requirements": job_card.get("open_set_requirements", []),
        "requirement_groups": job_card.get("requirement_groups", {}),
    }


def _build_recommendation_warnings(
    eligible_job_catalog: list[dict[str, Any]],
    excluded_jobs: list[dict[str, Any]],
) -> list[str]:
    """Build top-level candidate-side warnings for recommendation consumers."""
    warnings: list[str] = []
    if excluded_jobs:
        warnings.append(
            f"{len(excluded_jobs)} jobs were excluded because the JD content was not strong enough for reliable AI recommendation."
        )
    if not eligible_job_catalog:
        warnings.append(
            "No active jobs contain enough JD content for AI recommendation right now."
        )

    return warnings



def _coerce_positive_int(value: Any, option_name: str) -> int:
    """Convert an option value from dict payloads into a positive integer."""
    try:
        parsed_value = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"Recommendation option {option_name} must be a positive integer."
        ) from exc

    if parsed_value <= 0:
        raise ValueError(
            f"Recommendation option {option_name} must be a positive integer."
        )

    return parsed_value


def _default_retrieval_top_n(top_k: int, jobs_count: int) -> int:
    """Pick a safe top-N retrieval size before expensive reranking."""
    if jobs_count <= 0:
        return DEFAULT_RETRIEVAL_TOP_N

    return min(jobs_count, max(top_k * 3, 10))


def _to_plain_dict(value: Any) -> dict[str, Any]:
    """Convert Pydantic models and dict-like values to plain dictionaries."""
    if isinstance(value, dict):
        return value
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if value is None:
        return {}

    raise TypeError("Expected a dictionary or Pydantic model payload.")
