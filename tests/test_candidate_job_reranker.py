import pytest

from src import candidate_job_reranker
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


def test_score_retrieved_job_match_includes_skill_gap_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_run_screening_payload(
        request: dict,
        embedding_matcher=None,
    ) -> dict:
        return {
            "job": {
                "job_id": 10,
                "title": "Backend Java Developer",
            },
            "candidates": [
                {
                    "final_score": 72,
                    "raw_base_score": 74,
                    "role_calibrated_score": 72,
                    "base_score": 72,
                    "role_score_adjustment": -2,
                    "recommendation": "Review",
                    "scores": {
                        "evidence": 0.75,
                    },
                    "hard_skill_gate": {
                        "passed": True,
                        "applied": False,
                    },
                    "matched_skills": [
                        {
                            "required_skill": "Java",
                            "match_type": "exact_match",
                        }
                    ],
                    "missing_skills": ["AWS"],
                    "nice_to_have_matches": [],
                    "core_requirement_fit_summary": {
                        "core": {
                            "total": 2,
                            "confirmed_coverage": 0.5,
                        }
                    },
                    "role_alignment_impact": {
                        "applied": True,
                        "reason": "The profile is adjacent to the JD role family, but core requirements still need stronger direct evidence.",
                    },
                    "requirement_group_summary": {},
                    "review_card": {
                        "strengths": ["Strong Java background."],
                    },
                }
            ],
        }

    def fake_explain_skill_gaps(candidate_result: dict, job_output: dict) -> dict:
        return {
            "skill_gap_summary": {
                "missing_must_have_count": 1,
                "weak_evidence_count": 0,
                "optional_growth_count": 0,
                "presentation_gap_count": 0,
            },
            "skill_gaps": {
                "missing_must_have": [
                    {
                        "skill": "AWS",
                        "gap_type": "missing_must_have",
                    }
                ],
                "weak_evidence": [],
                "optional_growth": [],
                "presentation_gaps": [],
            },
            "cv_improvement_suggestions": [
                "If you have real experience with AWS, add it explicitly in your Skills section and mention one concrete usage example in work or projects."
            ],
            "next_best_actions": [
                "If you have real experience with AWS, add it explicitly in your Skills section and mention one concrete usage example in work or projects."
            ],
        }

    monkeypatch.setattr(
        candidate_job_reranker,
        "run_screening_payload",
        fake_run_screening_payload,
    )
    monkeypatch.setattr(
        candidate_job_reranker,
        "explain_skill_gaps",
        fake_explain_skill_gaps,
    )

    result = candidate_job_reranker.score_retrieved_job_match(
        candidate_payload={
            "candidate_name": "Nguyen Van A",
            "cv_text": "Java developer",
        },
        retrieved_job={
            "retrieval_rank": 1,
            "retrieval_score": 0.91,
            "retrieval_reasons": ["Strong skill overlap."],
            "job_card": {
                "job_payload": {
                    "job_id": 10,
                    "job_title": "Backend Java Developer",
                    "requirements": ["Java", "AWS"],
                }
            },
        },
        taxonomy_path="data/taxonomy/skills.json",
    )

    assert result["fit_label"] == "Good Fit"
    assert result["raw_base_score"] == 74
    assert result["role_calibrated_score"] == 72
    assert result["role_score_adjustment"] == -2
    assert result["skill_gap_summary"]["missing_must_have_count"] == 1
    assert result["skill_gaps"]["missing_must_have"] == [
        {
            "skill": "AWS",
            "gap_type": "missing_must_have",
        }
    ]
    assert result["what_to_improve"] == [
        "If you have real experience with AWS, add it explicitly in your Skills section and mention one concrete usage example in work or projects."
    ]
    assert result["cv_improvement_suggestions"] == result["next_best_actions"]
