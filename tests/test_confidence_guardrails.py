from src.confidence_guardrails import (
    build_decision_confidence,
    build_job_confidence_guardrails,
)


def test_build_job_confidence_guardrails_is_high_for_clean_explicit_jd() -> None:
    result = build_job_confidence_guardrails(
        {
            "level": "high",
            "known_requirement_count": 5,
            "open_set_requirement_count": 0,
            "embedding_enabled": False,
        },
        taxonomy_coverage={"coverage_ratio": 1.0},
        open_set_filter_summary={"candidate_count": 0},
        explicit_technical_recovery_summary={
            "recovery_triggered": False,
            "usable_explicit_technical_count": 4,
            "explicit_technical_contamination_count": 1,
        },
        requirement_provenance_summary=[
            {"requirement_source_kind": "explicit_requirement"}
            for _ in range(5)
        ],
        payload_diagnostics={"flags": []},
        job_quality={"quality_label": "eligible", "recommendation_eligible": True},
        job_role_profile={
            "primary_role_family": "BACKEND_ENGINEERING",
            "confidence": 0.82,
        },
    )

    assert result["level"] == "high"
    assert result["review_required"] is False
    assert result["reason_codes"] == []


def test_build_job_confidence_guardrails_flags_sparse_recovery_and_embedding_gap() -> None:
    result = build_job_confidence_guardrails(
        {
            "level": "low",
            "known_requirement_count": 0,
            "open_set_requirement_count": 4,
            "embedding_enabled": False,
        },
        taxonomy_coverage={"coverage_ratio": 0.0},
        open_set_filter_summary={"candidate_count": 4},
        explicit_technical_recovery_summary={
            "recovery_triggered": True,
            "usable_explicit_technical_count": 0,
            "explicit_technical_contamination_count": 2,
        },
        requirement_provenance_summary=[
            {"requirement_source_kind": "promoted_responsibility"}
            for _ in range(4)
        ],
        payload_diagnostics={"flags": []},
        job_quality={"quality_label": "eligible", "recommendation_eligible": True},
        job_role_profile={
            "primary_role_family": "IT_SUPPORT_INFRA",
            "confidence": 0.78,
        },
    )

    assert result["level"] == "low"
    assert result["review_required"] is True
    assert result["reason_codes"] == [
        "sparse_recovery_active",
        "explicit_technical_core_sparse",
        "explicit_technical_contamination_detected",
        "promoted_source_dominant",
        "unknown_requirement_count_high",
        "open_set_heavy_embedding_disabled",
    ]


def test_build_decision_confidence_is_high_for_confirmed_core_fit() -> None:
    result = build_decision_confidence(
        {
            "scores": {"evidence": 1.0},
            "hard_skill_gate": {"applied": False},
            "core_requirement_fit_summary": {
                "overall": {"semantic_only_ratio": 0.0},
                "core": {
                    "total": 4,
                    "confirmed_coverage": 1.0,
                    "semantic_only_ratio": 0.0,
                },
            },
            "matched_skills": [
                {"score": 1.0, "match_type": "exact_match", "evidence_level": 3}
                for _ in range(4)
            ],
            "role_alignment_impact": {"applied": False},
            "source_alignment_impact": {"applied": False},
        }
    )

    assert result["level"] == "high"
    assert result["review_required"] is False
    assert result["reason_codes"] == []


def test_build_decision_confidence_is_low_when_confirmation_is_weak() -> None:
    result = build_decision_confidence(
        {
            "scores": {"evidence": 0.4},
            "hard_skill_gate": {"applied": True},
            "core_requirement_fit_summary": {
                "overall": {"semantic_only_ratio": 0.75},
                "core": {
                    "total": 4,
                    "confirmed_coverage": 0.25,
                    "semantic_only_ratio": 0.75,
                },
            },
            "matched_skills": [
                {"score": 0.65, "match_type": "semantic_only_match", "evidence_level": 1}
                for _ in range(3)
            ],
            "role_alignment_impact": {"applied": True},
            "source_alignment_impact": {"applied": True},
        }
    )

    assert result["level"] == "low"
    assert result["review_required"] is True
    assert result["reason_codes"] == [
        "weak_hard_skill_confirmation",
        "confirmed_core_ratio_low",
        "semantic_only_ratio_high",
        "evidence_mostly_keyword_level",
        "direct_evidence_sparse",
        "role_alignment_adjustment_applied",
        "source_alignment_adjustment_applied",
    ]
