from src.payload_diagnostics import (
    diagnose_candidate_payload,
    diagnose_job_payload,
    summarize_candidate_payload_diagnostics,
    summarize_job_payload_diagnostics,
)


def test_diagnose_job_payload_flags_placeholder_and_missing_sections() -> None:
    result = diagnose_job_payload(
        {
            "job_title": "Test",
            "description": "<p>test</p>",
            "requirements": [],
            "responsibilities": [],
        },
        "Test\n\ntest",
    )

    assert result["quality_label"] == "warning"
    assert "job_title_placeholder" in result["flags"]
    assert "jd_text_too_short" in result["flags"]
    assert "jd_missing_requirements_input" in result["flags"]
    assert "jd_missing_responsibilities_input" in result["flags"]
    assert result["metrics"]["html_tag_count"] >= 2


def test_diagnose_candidate_payload_detects_short_sparse_cv() -> None:
    result = diagnose_candidate_payload(
        {
            "candidate_name": "Noi That",
            "cv_text": "Noi That\nJava",
        },
        {
            "text": "Noi That\nJava",
        },
    )

    assert result["source"]["source_mode"] == "cv_text"
    assert "cv_text_too_short" in result["flags"]
    assert "candidate_profile_sparse" in result["flags"]
    assert result["metrics"]["cv_word_count"] == 3


def test_summarize_candidate_payload_diagnostics_counts_flagged_candidates() -> None:
    diagnostics = [
        {
            "flags": ["cv_text_too_short"],
            "quality_label": "warning",
            "source": {"source_mode": "cv_text"},
            "metrics": {"cv_word_count": 8},
        },
        {
            "flags": [],
            "quality_label": "ok",
            "source": {"source_mode": "structured_cv"},
            "metrics": {"cv_word_count": 80},
        },
    ]
    result = summarize_candidate_payload_diagnostics(
        diagnostics,
        candidates=[
            {"application_id": 1, "candidate_id": 10, "candidate_name": "A"},
            {"application_id": 2, "candidate_id": 20, "candidate_name": "B"},
        ],
    )

    assert result["received_count"] == 2
    assert result["flagged_count"] == 1
    assert result["flag_counts"]["cv_text_too_short"] == 1
    assert result["flagged_candidates"][0]["candidate_id"] == 10


def test_summarize_job_payload_diagnostics_counts_flagged_jobs() -> None:
    diagnostics = [
        {
            "flags": ["job_title_placeholder", "jd_text_too_short"],
            "quality_label": "warning",
            "metrics": {
                "jd_word_count": 2,
                "requirements_count": 0,
                "responsibilities_count": 0,
            },
        },
        {
            "flags": [],
            "quality_label": "ok",
            "metrics": {
                "jd_word_count": 60,
                "requirements_count": 4,
                "responsibilities_count": 2,
            },
        },
    ]
    result = summarize_job_payload_diagnostics(
        diagnostics,
        jobs=[
            {"job_id": 4, "job_title": "Test"},
            {"job_id": 10, "job_title": "Backend Java Developer"},
        ],
    )

    assert result["received_count"] == 2
    assert result["flagged_count"] == 1
    assert result["flag_counts"]["job_title_placeholder"] == 1
    assert result["flagged_jobs"][0]["job_id"] == 4
