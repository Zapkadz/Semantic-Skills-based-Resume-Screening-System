"""Runtime diagnostics builders for API-facing screening and recommendation flows."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from src.payload_diagnostics import (
    summarize_candidate_payload_diagnostics,
    summarize_job_payload_diagnostics,
)


def build_trace_id(endpoint: str) -> str:
    """Create a stable-looking trace ID for one pipeline execution."""
    endpoint_slug = endpoint.strip().replace("/", "-") or "trace"
    return f"{endpoint_slug}-{uuid4().hex[:12]}"


def build_screening_diagnostics(
    trace_id: str,
    job_payload_diagnostics: dict[str, Any],
    candidate_payload_diagnostics: list[dict[str, Any]],
    candidate_payloads: list[dict[str, Any]],
    job_quality: dict[str, Any],
    job_output: dict[str, Any],
    ranked_candidates: list[dict[str, Any]],
    embedding_enabled: bool,
) -> dict[str, Any]:
    """Build top-level diagnostics for the employer-side screening endpoint."""
    return {
        "endpoint": "screening",
        "trace_id": trace_id,
        "payload": {
            "job": job_payload_diagnostics,
            "candidates": summarize_candidate_payload_diagnostics(
                candidate_payload_diagnostics,
                candidates=candidate_payloads,
            ),
        },
        "runtime": {
            "embedding_enabled": embedding_enabled,
            "candidate_count": len(candidate_payloads),
            "ranked_candidate_count": len(ranked_candidates),
            "job_quality": _runtime_job_quality(job_quality),
            "screening_confidence": job_output.get("screening_confidence", {}),
            "taxonomy_coverage": job_output.get("taxonomy_coverage", {}),
            "open_set_requirement_count": len(job_output.get("open_set_requirements", [])),
        },
    }


def build_recommendation_diagnostics(
    trace_id: str,
    candidate_payload_diagnostics: dict[str, Any],
    job_catalog: list[dict[str, Any]],
    retrieval_stats: dict[str, Any],
    job_quality_stats: dict[str, Any],
    top_jobs: list[dict[str, Any]],
    excluded_jobs: list[dict[str, Any]],
    embedding_enabled: bool,
) -> dict[str, Any]:
    """Build top-level diagnostics for the candidate-side recommendation endpoint."""
    job_payload_diags = [job.get("payload_diagnostics", {}) for job in job_catalog]
    job_payloads = [job.get("job_payload", {}) for job in job_catalog]
    job_summary = summarize_job_payload_diagnostics(job_payload_diags, jobs=job_payloads)
    job_summary["eligible_jobs"] = job_quality_stats.get("eligible_jobs", 0)
    job_summary["excluded_jobs"] = job_quality_stats.get("excluded_jobs", 0)
    job_summary["excluded_job_ids"] = [job.get("job_id") for job in excluded_jobs]

    return {
        "endpoint": "recommend-jobs",
        "trace_id": trace_id,
        "payload": {
            "candidate": candidate_payload_diagnostics,
            "jobs": job_summary,
        },
        "runtime": {
            "embedding_enabled": embedding_enabled,
            **retrieval_stats,
            **job_quality_stats,
            "top_job_ids": [job.get("job_id") for job in top_jobs],
            "excluded_job_ids": [job.get("job_id") for job in excluded_jobs],
        },
    }


def _runtime_job_quality(job_quality: dict[str, Any]) -> dict[str, Any]:
    """Keep only the most useful job-quality fields in screening diagnostics."""
    return {
        "quality_score": job_quality.get("quality_score", 0),
        "quality_label": job_quality.get("quality_label", ""),
        "recommendation_eligible": job_quality.get("recommendation_eligible", False),
        "flags": list(job_quality.get("flags", [])),
        "reasons": list(job_quality.get("reasons", [])),
        "metrics": dict(job_quality.get("metrics", {})),
    }
