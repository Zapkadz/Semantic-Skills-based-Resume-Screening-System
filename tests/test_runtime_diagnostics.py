from src.runtime_diagnostics import (
    build_recommendation_diagnostics,
    build_screening_diagnostics,
    build_trace_id,
)


def test_build_trace_id_uses_endpoint_prefix() -> None:
    trace_id = build_trace_id("screening")

    assert trace_id.startswith("screening-")
    assert len(trace_id) > len("screening-")


def test_build_screening_diagnostics_returns_payload_and_runtime_summary() -> None:
    result = build_screening_diagnostics(
        trace_id="screening-abc123",
        job_payload_diagnostics={
            "flags": ["jd_text_too_short"],
            "warnings": ["Job text looks too short for reliable AI analysis."],
            "quality_label": "warning",
            "source": {},
            "metrics": {"jd_word_count": 8},
        },
        candidate_payload_diagnostics=[
            {
                "flags": ["cv_text_too_short"],
                "warnings": [],
                "quality_label": "warning",
                "source": {"source_mode": "cv_text"},
                "metrics": {"cv_word_count": 10},
            }
        ],
        candidate_payloads=[
            {
                "application_id": 1,
                "candidate_id": 2,
                "candidate_name": "A",
            }
        ],
        job_quality={
            "quality_score": 20,
            "quality_label": "insufficient_jd_data",
            "recommendation_eligible": False,
            "flags": ["missing_requirements"],
            "reasons": ["No meaningful must-have requirements were detected."],
            "metrics": {"structured_requirement_count": 0},
        },
        job_output={
            "screening_confidence": {"level": "low"},
            "taxonomy_coverage": {"coverage_ratio": 0.0},
            "open_set_requirements": [],
            "open_set_filter_summary": {"candidate_count": 0},
            "job_role_profile": {"primary_role_family": "GENERIC_TECH"},
        },
        ranked_candidates=[{"candidate_id": 2}],
        embedding_enabled=False,
    )

    assert result["trace_id"] == "screening-abc123"
    assert result["payload"]["candidates"]["flagged_count"] == 1
    assert result["runtime"]["job_quality"]["quality_label"] == "insufficient_jd_data"
    assert result["runtime"]["candidate_count"] == 1
    assert result["runtime"]["open_set_filter_summary"] == {"candidate_count": 0}
    assert result["runtime"]["job_role_profile"]["primary_role_family"] == "GENERIC_TECH"


def test_build_recommendation_diagnostics_returns_flagged_jobs_summary() -> None:
    result = build_recommendation_diagnostics(
        trace_id="recommend-jobs-xyz789",
        candidate_payload_diagnostics={
            "flags": [],
            "warnings": [],
            "quality_label": "ok",
            "source": {"source_mode": "cv_text"},
            "metrics": {"cv_word_count": 120},
        },
        job_catalog=[
            {
                "job_id": 4,
                "job_title": "Test",
                "job_payload": {"job_id": 4, "job_title": "Test"},
                "payload_diagnostics": {
                    "flags": ["job_title_placeholder"],
                    "warnings": [],
                    "quality_label": "warning",
                    "metrics": {"jd_word_count": 2, "requirements_count": 0, "responsibilities_count": 0},
                },
            },
            {
                "job_id": 10,
                "job_title": "Backend Java Developer",
                "job_payload": {"job_id": 10, "job_title": "Backend Java Developer"},
                "payload_diagnostics": {
                    "flags": [],
                    "warnings": [],
                    "quality_label": "ok",
                    "metrics": {"jd_word_count": 60, "requirements_count": 4, "responsibilities_count": 2},
                },
            },
        ],
        retrieval_stats={
            "jobs_received": 2,
            "jobs_indexed": 1,
            "jobs_retrieved": 1,
            "jobs_reranked": 1,
            "top_k": 1,
            "retrieval_top_n": 1,
            "retrieval_applied": True,
        },
        job_quality_stats={
            "jobs_received": 2,
            "eligible_jobs": 1,
            "excluded_jobs": 1,
        },
        top_jobs=[{"job_id": 10, "role_score_adjustment": -4}],
        excluded_jobs=[{"job_id": 4}],
        embedding_enabled=False,
    )

    assert result["trace_id"] == "recommend-jobs-xyz789"
    assert result["payload"]["jobs"]["flagged_count"] == 1
    assert result["payload"]["jobs"]["excluded_job_ids"] == [4]
    assert result["runtime"]["top_job_ids"] == [10]
    assert result["runtime"]["top_job_role_score_adjustments"] == {10: -4}
    assert result["runtime"]["top_job_open_set_requirement_counts"] == {10: 0}
