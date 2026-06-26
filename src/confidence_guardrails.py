"""Shared confidence and diagnostics guardrails for screening outputs."""

from __future__ import annotations

from typing import Any

from src.requirement_provenance import (
    EXPLICIT_REQUIREMENT_SOURCE,
    PROMOTED_RESPONSIBILITY_SOURCE,
)


LOW_CONFIDENCE = "low"
MEDIUM_CONFIDENCE = "medium"
HIGH_CONFIDENCE = "high"

JOB_GUARDRAIL_MESSAGES = {
    "job_payload_warning_present": (
        "The incoming job payload already shows warning signals, so downstream AI "
        "results should be reviewed carefully."
    ),
    "jd_quality_warning_present": (
        "The JD quality gate reported warnings, so the extracted requirement set may "
        "still be incomplete or noisy."
    ),
    "sparse_recovery_active": (
        "Sparse-JD recovery was activated because explicit technical requirements were "
        "too weak to score directly."
    ),
    "explicit_technical_core_sparse": (
        "The explicit technical core is sparse, so the system depends more on promoted "
        "technical signals."
    ),
    "explicit_technical_contamination_detected": (
        "Some explicit technical requirement lines look contaminated by generic or "
        "non-technical text."
    ),
    "promoted_source_dominant": (
        "Promoted technical responsibility signals currently dominate the scorable "
        "technical core for this JD."
    ),
    "unknown_requirement_count_high": (
        "A large share of the scorable requirements sit outside the current taxonomy."
    ),
    "open_set_heavy_embedding_disabled": (
        "Open-set requirements were detected, but the embedding matcher is disabled."
    ),
    "role_family_low_confidence": (
        "The JD role-family inference is still too generic or low-confidence."
    ),
}

DECISION_CONFIDENCE_MESSAGES = {
    "weak_hard_skill_confirmation": (
        "The hard-skill gate was triggered because confirmed must-have evidence is "
        "still too weak for a stronger recommendation."
    ),
    "confirmed_core_ratio_low": (
        "Too few core technical requirements are confirmed with strong evidence."
    ),
    "semantic_only_ratio_high": (
        "A large share of the positive technical overlap is still semantic-only."
    ),
    "evidence_mostly_keyword_level": (
        "Most positive evidence is still weak or keyword-level rather than directly "
        "demonstrated in work/project context."
    ),
    "direct_evidence_sparse": (
        "Direct, high-quality work/project evidence is still sparse."
    ),
    "role_alignment_adjustment_applied": (
        "Role-aware calibration adjusted the score because the candidate's strongest "
        "role family does not align cleanly enough with the JD."
    ),
    "source_alignment_adjustment_applied": (
        "Source-aware calibration adjusted the score because the requirement mix needs "
        "more careful interpretation."
    ),
}


def build_job_confidence_guardrails(
    screening_confidence: dict[str, Any] | None,
    *,
    taxonomy_coverage: dict[str, Any] | None = None,
    open_set_filter_summary: dict[str, Any] | None = None,
    explicit_technical_recovery_summary: dict[str, Any] | None = None,
    requirement_provenance_summary: list[dict[str, Any]] | None = None,
    payload_diagnostics: dict[str, Any] | None = None,
    job_quality: dict[str, Any] | None = None,
    job_role_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one job-level confidence and warning summary."""
    screening_confidence = screening_confidence or {}
    taxonomy_coverage = taxonomy_coverage or {}
    open_set_filter_summary = open_set_filter_summary or {}
    explicit_technical_recovery_summary = explicit_technical_recovery_summary or {}
    payload_diagnostics = payload_diagnostics or {}
    job_quality = job_quality or {}
    job_role_profile = job_role_profile or {}

    explicit_count, promoted_count = _count_requirement_sources(
        requirement_provenance_summary or []
    )
    known_count = int(screening_confidence.get("known_requirement_count", 0) or 0)
    open_set_count = int(
        screening_confidence.get("open_set_requirement_count", 0) or 0
    )
    embedding_enabled = bool(screening_confidence.get("embedding_enabled", False))
    screening_level = str(
        screening_confidence.get("level", HIGH_CONFIDENCE) or HIGH_CONFIDENCE
    ).strip().casefold()
    role_family_confidence = float(job_role_profile.get("confidence", 0.0) or 0.0)
    primary_role_family = str(
        job_role_profile.get("primary_role_family", "") or ""
    ).strip()
    payload_flags = list(payload_diagnostics.get("flags", []))
    job_quality_flags = list(job_quality.get("flags", []))
    quality_label = str(job_quality.get("quality_label", "")).strip()
    recovery_triggered = bool(
        explicit_technical_recovery_summary.get("recovery_triggered", False)
    )
    usable_explicit_count = int(
        explicit_technical_recovery_summary.get("usable_explicit_technical_count", 0)
        or 0
    )
    contamination_count = int(
        explicit_technical_recovery_summary.get(
            "explicit_technical_contamination_count",
            0,
        )
        or 0
    )

    reason_codes: list[str] = []
    if payload_flags:
        _add_reason_code(reason_codes, "job_payload_warning_present")
    if quality_label and quality_label not in {"ok", "eligible"}:
        _add_reason_code(reason_codes, "jd_quality_warning_present")
    if job_quality_flags and quality_label in {"eligible_with_warning", "warning"}:
        _add_reason_code(reason_codes, "jd_quality_warning_present")
    if recovery_triggered:
        _add_reason_code(reason_codes, "sparse_recovery_active")
    if recovery_triggered and usable_explicit_count == 0:
        _add_reason_code(reason_codes, "explicit_technical_core_sparse")
    if contamination_count > 0 and (recovery_triggered or usable_explicit_count <= 1):
        _add_reason_code(reason_codes, "explicit_technical_contamination_detected")
    if promoted_count > explicit_count and promoted_count > 0:
        _add_reason_code(reason_codes, "promoted_source_dominant")
    if open_set_count >= max(2, known_count):
        _add_reason_code(reason_codes, "unknown_requirement_count_high")
    if open_set_count > 0 and not embedding_enabled:
        _add_reason_code(reason_codes, "open_set_heavy_embedding_disabled")
    if primary_role_family == "GENERIC_TECH" or role_family_confidence < 0.60:
        _add_reason_code(reason_codes, "role_family_low_confidence")

    level = _classify_job_guardrail_level(
        screening_level=screening_level,
        reason_codes=reason_codes,
        recommendation_eligible=bool(
            job_quality.get("recommendation_eligible", True)
        ),
    )

    return {
        "level": level,
        "review_required": level != HIGH_CONFIDENCE,
        "reason_codes": reason_codes,
        "messages": [
            JOB_GUARDRAIL_MESSAGES[code]
            for code in reason_codes
            if code in JOB_GUARDRAIL_MESSAGES
        ],
        "metrics": {
            "known_requirement_count": known_count,
            "open_set_requirement_count": open_set_count,
            "explicit_requirement_count": explicit_count,
            "promoted_requirement_count": promoted_count,
            "taxonomy_coverage_ratio": float(
                taxonomy_coverage.get("coverage_ratio", 0.0) or 0.0
            ),
            "open_set_candidate_count": int(
                open_set_filter_summary.get("candidate_count", 0) or 0
            ),
            "sparse_recovery_active": recovery_triggered,
            "usable_explicit_technical_count": usable_explicit_count,
            "explicit_technical_contamination_count": contamination_count,
            "role_family_confidence": role_family_confidence,
            "payload_warning_count": len(payload_flags),
            "job_quality_flag_count": len(job_quality_flags),
        },
    }


def build_decision_confidence(
    candidate_result: dict[str, Any],
    *,
    job_confidence_guardrails: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one candidate/job decision-confidence summary."""
    scores = dict(candidate_result.get("scores", {}))
    hard_skill_gate = _as_dict(candidate_result.get("hard_skill_gate"))
    role_alignment_impact = _as_dict(candidate_result.get("role_alignment_impact"))
    source_alignment_impact = _as_dict(candidate_result.get("source_alignment_impact"))
    fit_summary = _as_dict(candidate_result.get("core_requirement_fit_summary"))
    overall_bucket = _as_dict(fit_summary.get("overall"))
    core_bucket = _as_dict(fit_summary.get("core"))
    job_confidence_guardrails = job_confidence_guardrails or {}

    core_total = int(core_bucket.get("total", 0) or 0)
    confirmed_core_ratio = float(core_bucket.get("confirmed_coverage", 0.0) or 0.0)
    core_semantic_only_ratio = float(
        core_bucket.get("semantic_only_ratio", 0.0) or 0.0
    )
    overall_semantic_only_ratio = float(
        overall_bucket.get("semantic_only_ratio", 0.0) or 0.0
    )
    evidence_score = float(scores.get("evidence", 0.0) or 0.0)
    direct_evidence_count = _count_direct_confirmed_matches(
        list(candidate_result.get("matched_skills", []))
    )

    reason_codes: list[str] = []
    if hard_skill_gate.get("applied") is True:
        _add_reason_code(reason_codes, "weak_hard_skill_confirmation")
    if core_total >= 2 and confirmed_core_ratio < 0.5:
        _add_reason_code(reason_codes, "confirmed_core_ratio_low")
    if core_total >= 1 and core_semantic_only_ratio >= 0.5:
        _add_reason_code(reason_codes, "semantic_only_ratio_high")
    if evidence_score < 0.5:
        _add_reason_code(reason_codes, "evidence_mostly_keyword_level")
    if direct_evidence_count <= 1 and evidence_score < 0.7:
        _add_reason_code(reason_codes, "direct_evidence_sparse")
    if role_alignment_impact.get("applied") is True:
        _add_reason_code(reason_codes, "role_alignment_adjustment_applied")
    if source_alignment_impact.get("applied") is True:
        _add_reason_code(reason_codes, "source_alignment_adjustment_applied")

    level = _classify_decision_confidence_level(
        reason_codes=reason_codes,
        hard_skill_gate_applied=bool(hard_skill_gate.get("applied", False)),
        confirmed_core_ratio=confirmed_core_ratio,
        evidence_score=evidence_score,
        core_semantic_only_ratio=core_semantic_only_ratio,
        job_review_required=bool(job_confidence_guardrails.get("review_required", False)),
    )

    return {
        "level": level,
        "review_required": level != HIGH_CONFIDENCE,
        "reason_codes": reason_codes,
        "messages": [
            DECISION_CONFIDENCE_MESSAGES[code]
            for code in reason_codes
            if code in DECISION_CONFIDENCE_MESSAGES
        ],
        "confirmed_core_ratio": round(confirmed_core_ratio, 4),
        "semantic_only_ratio": round(overall_semantic_only_ratio, 4),
        "core_semantic_only_ratio": round(core_semantic_only_ratio, 4),
        "evidence_score": round(evidence_score, 4),
        "core_requirement_total": core_total,
        "direct_confirmed_evidence_count": direct_evidence_count,
    }


def summarize_confidence_levels(
    items: list[dict[str, Any]],
    *,
    field_name: str,
) -> dict[str, int]:
    """Count low/medium/high confidence summaries across one item list."""
    counts = {
        HIGH_CONFIDENCE: 0,
        MEDIUM_CONFIDENCE: 0,
        LOW_CONFIDENCE: 0,
    }

    for item in items:
        confidence = _as_dict(item.get(field_name))
        level = str(confidence.get("level", "") or "").strip().casefold()
        if level in counts:
            counts[level] += 1

    return counts


def summarize_reason_codes(
    items: list[dict[str, Any]],
    *,
    field_name: str,
) -> dict[str, int]:
    """Count stable reason codes across one confidence-summary field."""
    counts: dict[str, int] = {}
    for item in items:
        confidence = _as_dict(item.get(field_name))
        for code in confidence.get("reason_codes", []):
            normalized_code = str(code).strip()
            if not normalized_code:
                continue
            counts[normalized_code] = counts.get(normalized_code, 0) + 1

    return counts


def _classify_job_guardrail_level(
    *,
    screening_level: str,
    reason_codes: list[str],
    recommendation_eligible: bool,
) -> str:
    """Map job-level signals to one stable confidence level."""
    high_risk_codes = {
        "open_set_heavy_embedding_disabled",
    }

    if not recommendation_eligible:
        return LOW_CONFIDENCE
    if screening_level == LOW_CONFIDENCE:
        return LOW_CONFIDENCE
    if any(code in high_risk_codes for code in reason_codes):
        return LOW_CONFIDENCE
    if reason_codes or screening_level == MEDIUM_CONFIDENCE:
        return MEDIUM_CONFIDENCE

    return HIGH_CONFIDENCE


def _classify_decision_confidence_level(
    *,
    reason_codes: list[str],
    hard_skill_gate_applied: bool,
    confirmed_core_ratio: float,
    evidence_score: float,
    core_semantic_only_ratio: float,
    job_review_required: bool,
) -> str:
    """Map candidate/job-level decision signals to one confidence level."""
    risk_score = 0

    if hard_skill_gate_applied:
        risk_score += 2
    if confirmed_core_ratio < 0.5:
        risk_score += 1
    if evidence_score < 0.5:
        risk_score += 1
    if core_semantic_only_ratio >= 0.5:
        risk_score += 1
    if "role_alignment_adjustment_applied" in reason_codes:
        risk_score += 1
    if "source_alignment_adjustment_applied" in reason_codes:
        risk_score += 1
    if risk_score >= 3:
        return LOW_CONFIDENCE
    if risk_score >= 1:
        return MEDIUM_CONFIDENCE

    return HIGH_CONFIDENCE


def _count_requirement_sources(
    requirement_provenance_summary: list[dict[str, Any]],
) -> tuple[int, int]:
    """Count explicit vs promoted requirement entries."""
    explicit_count = 0
    promoted_count = 0

    for item in requirement_provenance_summary:
        source_kind = str(item.get("requirement_source_kind", "")).strip().casefold()
        if source_kind == PROMOTED_RESPONSIBILITY_SOURCE:
            promoted_count += 1
        else:
            explicit_count += 1

    return explicit_count, promoted_count


def _count_direct_confirmed_matches(matches: list[dict[str, Any]]) -> int:
    """Count positive must-have matches with direct, confirmed evidence."""
    return sum(
        1
        for match in matches
        if float(match.get("score", 0.0) or 0.0) > 0.0
        and str(match.get("match_type", "")).strip()
        not in {"no_match", "no_semantic_evidence"}
        and int(match.get("evidence_level", 0) or 0) >= 2
    )


def _add_reason_code(reason_codes: list[str], code: str) -> None:
    """Append one stable reason code only once."""
    if code not in reason_codes:
        reason_codes.append(code)


def _as_dict(value: Any) -> dict[str, Any]:
    """Return a safe dictionary view for optional nested metadata."""
    return value if isinstance(value, dict) else {}
