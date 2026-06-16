"""Candidate-side job recommendation pipeline for one CV and many JDs."""

from __future__ import annotations

from typing import Any

from src.api_models import JobRecommendationRequest
from src.embedding_matcher import SemanticEmbeddingMatcher
from src.job_catalog_loader import build_job_catalog
from src.job_indexer import build_job_index_documents
from src.job_retriever import build_candidate_query_profile, retrieve_candidate_jobs
from src.payload_pipeline import build_cv_document_from_payload, run_screening_payload
from src.screening_pipeline import DEFAULT_TAXONOMY_PATH


DEFAULT_TOP_K = 10
DEFAULT_RETRIEVAL_TOP_N = 50
MAX_WHY_FIT_ITEMS = 4
MAX_IMPROVEMENT_ITEMS = 5


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

    candidate_document = build_cv_document_from_payload(candidate_payload)
    candidate_profile = build_candidate_query_profile(
        candidate_payload,
        taxonomy_path=taxonomy_path,
        candidate_document=candidate_document,
    )
    job_catalog = build_job_catalog(job_payloads, taxonomy_path=taxonomy_path)
    indexed_jobs = build_job_index_documents(job_catalog)
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
    job_recommendations = [
        _build_job_recommendation(
            candidate_payload,
            retrieved_job["job_card"]["job_payload"],
            taxonomy_path,
            embedding_matcher,
            retrieval_metadata=retrieved_job,
        )
        for retrieved_job in retrieved_jobs
    ]
    ranked_jobs = _rank_job_recommendations(job_recommendations)
    top_jobs = [
        {
            "rank": index,
            **job_result,
        }
        for index, job_result in enumerate(ranked_jobs[:top_k], start=1)
    ]

    candidate_summary = _build_candidate_summary(
        candidate_payload,
        candidate_document,
        top_jobs,
    )

    return {
        "candidate": candidate_summary,
        "top_jobs": top_jobs,
        "retrieval_stats": {
            "jobs_received": len(job_payloads),
            "jobs_indexed": len(indexed_jobs),
            "jobs_retrieved": len(retrieved_jobs),
            "jobs_reranked": len(job_recommendations),
            "top_k": min(top_k, len(job_payloads)),
            "retrieval_top_n": retrieval_top_n,
            "retrieval_applied": len(retrieved_jobs) < len(job_payloads),
        },
    }


def _build_job_recommendation(
    candidate_payload: dict[str, Any],
    job_payload: dict[str, Any],
    taxonomy_path: str,
    embedding_matcher: SemanticEmbeddingMatcher | None,
    retrieval_metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one candidate-vs-one-job screening and convert it to a job result."""
    screening_result = run_screening_payload(
        {
            "job": job_payload,
            "candidates": [candidate_payload],
            "taxonomy_path": taxonomy_path,
        },
        embedding_matcher=embedding_matcher,
    )
    job_output = screening_result["job"]
    candidate_result = screening_result["candidates"][0]
    review_card = candidate_result.get("review_card", {})
    retrieval_metadata = retrieval_metadata or {}

    return {
        "job_id": job_output.get("job_id", job_payload.get("job_id")),
        "job_title": job_output.get("title", ""),
        "retrieval_rank": retrieval_metadata.get("retrieval_rank"),
        "retrieval_score": retrieval_metadata.get("retrieval_score"),
        "retrieval_reasons": retrieval_metadata.get("retrieval_reasons", []),
        "retrieval_components": retrieval_metadata.get("retrieval_components", {}),
        "fit_score": candidate_result.get("final_score", 0),
        "base_score": candidate_result.get("base_score", 0),
        "recommendation": candidate_result.get("recommendation", ""),
        "scores": candidate_result.get("scores", {}),
        "hard_skill_gate": candidate_result.get("hard_skill_gate", {}),
        "matched_must_have_skills": _matched_required_skill_labels(
            candidate_result.get("matched_skills", [])
        ),
        "missing_must_have_skills": list(candidate_result.get("missing_skills", [])),
        "optional_strengths": _matched_optional_skill_labels(
            candidate_result.get("nice_to_have_matches", [])
        ),
        "why_fit": _build_why_fit(review_card, candidate_result),
        "what_to_improve": _build_what_to_improve(review_card, candidate_result),
        "requirement_group_summary": candidate_result.get(
            "requirement_group_summary",
            {},
        ),
        "taxonomy_coverage": job_output.get("taxonomy_coverage", {}),
        "screening_confidence": job_output.get("screening_confidence", {}),
        "open_set_requirements": job_output.get("open_set_requirements", []),
        "requirement_groups": job_output.get("requirement_groups", {}),
        "review_card": review_card,
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


def _rank_job_recommendations(
    job_recommendations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Sort jobs by fit score and a few deterministic tie-breakers."""
    return sorted(
        job_recommendations,
        key=lambda job: (
            -int(job.get("fit_score", 0)),
            -float(job.get("scores", {}).get("evidence", 0.0)),
            -float(job.get("retrieval_score") or 0.0),
            -int(job.get("base_score", 0)),
            str(job.get("job_title", "")).casefold(),
        ),
    )


def _matched_required_skill_labels(matches: list[dict[str, Any]]) -> list[str]:
    """Return unique must-have requirement labels with positive matches."""
    labels: list[str] = []
    seen: set[str] = set()
    for match in matches:
        if match.get("match_type") in {"no_match", "no_semantic_evidence"}:
            continue

        label = str(match.get("required_skill", "")).strip()
        if not label or label in seen:
            continue

        seen.add(label)
        labels.append(label)

    return labels


def _matched_optional_skill_labels(matches: list[dict[str, Any]]) -> list[str]:
    """Return unique nice-to-have requirement labels with positive matches."""
    labels: list[str] = []
    seen: set[str] = set()
    for match in matches:
        if match.get("match_type") == "no_match":
            continue

        label = str(match.get("required_skill", "")).strip()
        if not label or label in seen:
            continue

        seen.add(label)
        labels.append(label)

    return labels


def _build_why_fit(
    review_card: dict[str, Any],
    candidate_result: dict[str, Any],
) -> list[str]:
    """Build concise candidate-facing reasons why a job is a fit."""
    strengths = [
        str(item).strip()
        for item in review_card.get("strengths", [])
        if str(item).strip()
    ]
    if strengths:
        return strengths[:MAX_WHY_FIT_ITEMS]

    score_breakdown = candidate_result.get("scores", {})
    reasons: list[str] = []
    if float(score_breakdown.get("skill_semantic", 0.0)) >= 0.70:
        reasons.append("Your must-have skill coverage looks strong for this role.")
    if float(score_breakdown.get("experience", 0.0)) >= 0.75:
        reasons.append("Your experience level appears close to the role requirement.")
    if float(score_breakdown.get("domain", 0.0)) >= 0.85:
        reasons.append("Your domain background appears aligned with this role.")

    return reasons[:MAX_WHY_FIT_ITEMS] or [
        "This role shows some measurable overlap with your current CV."
    ]


def _build_what_to_improve(
    review_card: dict[str, Any],
    candidate_result: dict[str, Any],
) -> list[str]:
    """Build short candidate-facing actions to improve fit for one job."""
    improvements: list[str] = []
    missing_skills = list(candidate_result.get("missing_skills", []))
    nice_to_have_matches = list(candidate_result.get("nice_to_have_matches", []))
    score_breakdown = candidate_result.get("scores", {})
    hard_skill_gate = candidate_result.get("hard_skill_gate", {})

    for skill in missing_skills[:3]:
        improvements.append(
            f"Add explicit evidence for {skill} if you have used it in work, projects, or certifications."
        )

    optional_gaps = [
        str(match.get("required_skill", "")).strip()
        for match in nice_to_have_matches
        if match.get("match_type") == "no_match"
        and str(match.get("required_skill", "")).strip()
    ]
    for skill in optional_gaps[:2]:
        improvements.append(
            f"Optional strength to add for this role: {skill}."
        )

    if float(score_breakdown.get("evidence", 0.0)) < 0.50:
        improvements.append(
            "Make your CV more concrete by describing outcomes, technologies, and project responsibilities."
        )

    if hard_skill_gate.get("applied") is True:
        improvements.append(
            "Strengthen must-have hard-skill evidence so this role is not capped by the hard-skill gate."
        )

    if not improvements:
        concerns = [
            str(item).strip()
            for item in review_card.get("concerns", [])
            if str(item).strip()
        ]
        improvements.extend(concerns[:MAX_IMPROVEMENT_ITEMS])

    return improvements[:MAX_IMPROVEMENT_ITEMS] or [
        "Your CV already looks broadly aligned with this role; refine evidence details to improve confidence."
    ]


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
