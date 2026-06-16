import pytest

from src.candidate_job_reranker import (
    build_fit_summary,
    get_candidate_fit_label,
    rank_candidate_job_matches,
)


@pytest.mark.parametrize(
    ("fit_score", "expected_label"),
    [
        (86, "Strong Fit"),
        (72, "Good Fit"),
        (58, "Potential Fit"),
        (45, "Stretch"),
        (25, "Low Fit"),
    ],
)
def test_get_candidate_fit_label_maps_score_bands(
    fit_score: int,
    expected_label: str,
) -> None:
    assert get_candidate_fit_label(fit_score) == expected_label


def test_build_fit_summary_mentions_hard_skill_gate_when_applied() -> None:
    summary = build_fit_summary(
        "Potential Fit",
        ["Strong must-have skill coverage."],
        ["Add explicit evidence for SQL if you have used it in work."],
        {"applied": True},
    )

    assert summary == (
        "This role is currently a Potential Fit because must-have technical "
        "evidence is incomplete. To improve your fit, add explicit evidence "
        "for SQL if you have used it in work."
    )


def test_rank_candidate_job_matches_uses_fit_then_evidence_then_gate_then_retrieval() -> None:
    ranked_jobs = rank_candidate_job_matches(
        [
            {
                "job_id": 10,
                "job_title": "Role B",
                "fit_score": 72,
                "scores": {"evidence": 0.6},
                "hard_skill_gate": {"passed": False},
                "retrieval_score": 0.95,
            },
            {
                "job_id": 20,
                "job_title": "Role A",
                "fit_score": 72,
                "scores": {"evidence": 0.8},
                "hard_skill_gate": {"passed": True},
                "retrieval_score": 0.20,
            },
            {
                "job_id": 30,
                "job_title": "Role C",
                "fit_score": 58,
                "scores": {"evidence": 1.0},
                "hard_skill_gate": {"passed": True},
                "retrieval_score": 1.0,
            },
        ]
    )

    assert [job["job_id"] for job in ranked_jobs] == [20, 10, 30]
    assert [job["rank"] for job in ranked_jobs] == [1, 2, 3]
