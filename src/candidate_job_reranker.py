"""Candidate-side reranking and fit labeling on top of the core scorer."""

from __future__ import annotations

from typing import Any

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.payload_pipeline import run_screening_payload
from src.skill_gap_explainer import explain_skill_gaps


FIT_LABEL_THRESHOLDS = [
    (85, "Strong Fit"),
    (70, "Good Fit"),
    (55, "Potential Fit"),
    (40, "Stretch"),
    (0, "Low Fit"),
]

MAX_WHY_FIT_ITEMS = 4


def rerank_candidate_jobs(
    candidate_payload: dict[str, Any],
    retrieved_jobs: list[dict[str, Any]],
    taxonomy_path: str,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> list[dict[str, Any]]:
    """Score retrieved jobs with the core scorer and map them to fit labels."""
    reranked_jobs = [
        score_retrieved_job_match(
            candidate_payload,
            retrieved_job,
            taxonomy_path,
            embedding_matcher=embedding_matcher,
        )
        for retrieved_job in retrieved_jobs
    ]

    return rank_candidate_job_matches(reranked_jobs)


def score_retrieved_job_match(
    candidate_payload: dict[str, Any],
    retrieved_job: dict[str, Any],
    taxonomy_path: str,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Score one retrieved job and convert it into candidate-facing fit output."""
    job_card = dict(retrieved_job.get("job_card", {}))
    job_payload = dict(job_card.get("job_payload", {}))
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
    gap_explanation = explain_skill_gaps(candidate_result, job_output)

    fit_score = int(candidate_result.get("final_score", 0))
    fit_label = get_candidate_fit_label(fit_score)
    why_fit = build_candidate_why_fit(review_card, candidate_result)
    what_to_improve = list(gap_explanation.get("next_best_actions", []))
    fit_summary = build_fit_summary(
        fit_label,
        why_fit,
        what_to_improve,
        candidate_result.get("hard_skill_gate", {}),
    )

    return {
        "job_id": job_output.get("job_id", job_payload.get("job_id")),
        "job_title": job_output.get("title", ""),
        "retrieval_rank": retrieved_job.get("retrieval_rank"),
        "retrieval_score": retrieved_job.get("retrieval_score"),
        "retrieval_reasons": retrieved_job.get("retrieval_reasons", []),
        "retrieval_components": retrieved_job.get("retrieval_components", {}),
        "fit_score": fit_score,
        "fit_label": fit_label,
        "fit_summary": fit_summary,
        "base_score": candidate_result.get("base_score", 0),
        "recommendation": candidate_result.get("recommendation", ""),
        "scores": candidate_result.get("scores", {}),
        "hard_skill_gate": candidate_result.get("hard_skill_gate", {}),
        "candidate_role_profile": candidate_result.get("candidate_role_profile", {}),
        "role_family_alignment": candidate_result.get("role_family_alignment", {}),
        "matched_must_have_skills": _matched_required_skill_labels(
            candidate_result.get("matched_skills", [])
        ),
        "missing_must_have_skills": list(candidate_result.get("missing_skills", [])),
        "optional_strengths": _matched_optional_skill_labels(
            candidate_result.get("nice_to_have_matches", [])
        ),
        "why_fit": why_fit,
        "what_to_improve": what_to_improve,
        "skill_gap_summary": gap_explanation.get("skill_gap_summary", {}),
        "skill_gaps": gap_explanation.get("skill_gaps", {}),
        "cv_improvement_suggestions": gap_explanation.get(
            "cv_improvement_suggestions",
            [],
        ),
        "next_best_actions": gap_explanation.get("next_best_actions", []),
        "requirement_group_summary": candidate_result.get(
            "requirement_group_summary",
            {},
        ),
        "taxonomy_coverage": job_output.get("taxonomy_coverage", {}),
        "screening_confidence": job_output.get("screening_confidence", {}),
        "job_role_profile": job_output.get("job_role_profile", {}),
        "open_set_requirements": job_output.get("open_set_requirements", []),
        "open_set_candidates": job_output.get("open_set_candidates", []),
        "discarded_open_set_candidates": job_output.get(
            "discarded_open_set_candidates",
            [],
        ),
        "open_set_filter_summary": job_output.get("open_set_filter_summary", {}),
        "requirement_intent_summary": job_output.get("requirement_intent_summary", []),
        "typed_requirements": job_output.get("typed_requirements", []),
        "requirement_groups": job_output.get("requirement_groups", {}),
        "job_quality": job_card.get("job_quality", {}),
        "review_card": review_card,
    }


def rank_candidate_job_matches(job_matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort candidate-side jobs by fit-first ordering rules."""
    ranked_results = sorted(
        job_matches,
        key=lambda job: (
            -int(job.get("fit_score", 0)),
            -float(job.get("scores", {}).get("evidence", 0.0)),
            -_gate_pass_value(job.get("hard_skill_gate", {})),
            -float(job.get("retrieval_score") or 0.0),
            str(job.get("job_title", "")).casefold(),
        ),
    )

    return [
        {
            "rank": index,
            **job,
        }
        for index, job in enumerate(ranked_results, start=1)
    ]


def get_candidate_fit_label(fit_score: int | float) -> str:
    """Map a final fit score to a candidate-facing fit label."""
    for threshold, label in FIT_LABEL_THRESHOLDS:
        if fit_score >= threshold:
            return label

    return "Low Fit"


def build_fit_summary(
    fit_label: str,
    why_fit: list[str],
    what_to_improve: list[str],
    hard_skill_gate: dict[str, Any] | None = None,
) -> str:
    """Build one concise candidate-facing fit summary sentence."""
    hard_skill_gate = hard_skill_gate or {}
    first_reason = _strip_sentence_end(why_fit[0]) if why_fit else ""
    first_improvement = (
        _strip_sentence_end(what_to_improve[0]) if what_to_improve else ""
    )

    if hard_skill_gate.get("applied") is True:
        summary = (
            f"This role is currently a {fit_label} because must-have technical "
            "evidence is incomplete."
        )
        if first_improvement:
            summary += f" To improve your fit, {_to_clause(first_improvement)}."
        return summary

    if fit_label == "Low Fit":
        summary = (
            "This role is currently a Low Fit because several core requirements "
            "are still missing or weakly evidenced."
        )
        if first_improvement:
            summary += f" To improve your fit, {_to_clause(first_improvement)}."
        return summary

    if fit_label == "Stretch":
        summary = (
            "This role is currently a Stretch because your profile only partially "
            "matches the must-have requirements."
        )
        if first_improvement:
            summary += f" To improve your fit, {_to_clause(first_improvement)}."
        return summary

    summary = f"This role is a {fit_label}"
    if first_reason:
        summary += f" because {_to_clause(first_reason)}."
    else:
        summary += "."

    if fit_label in {"Potential Fit", "Stretch", "Low Fit"} and first_improvement:
        summary += f" To improve your fit, {_to_clause(first_improvement)}."

    return summary


def build_candidate_why_fit(
    review_card: dict[str, Any],
    candidate_result: dict[str, Any],
) -> list[str]:
    """Build concise candidate-facing reasons why a job fits."""
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


def _gate_pass_value(hard_skill_gate: dict[str, Any]) -> int:
    """Return 1 when the hard-skill gate passed, else 0, for stable tie-breaks."""
    return 1 if hard_skill_gate.get("passed") is True else 0


def _strip_sentence_end(value: str) -> str:
    """Remove trailing punctuation before inserting into summaries."""
    return value.strip().rstrip(".!?")


def _to_clause(value: str) -> str:
    """Make a sentence fragment fit after 'because' or 'to improve'."""
    if not value:
        return ""
    if value[:2].isupper():
        return value

    return value[:1].casefold() + value[1:]
