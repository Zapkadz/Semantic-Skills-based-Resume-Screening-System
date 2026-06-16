from src.skill_gap_explainer import explain_skill_gaps


def test_explain_skill_gaps_builds_structured_gaps_and_actions() -> None:
    result = explain_skill_gaps(
        {
            "matched_skills": [
                {
                    "required_skill": "Docker",
                    "match_type": "exact_match",
                    "score": 1.0,
                    "evidence_level": 1,
                },
                {
                    "required_skill": "Java",
                    "match_type": "exact_match",
                    "score": 1.0,
                    "evidence_level": 3,
                },
            ],
            "missing_skills": ["AWS"],
            "nice_to_have_matches": [
                {
                    "required_skill": "Kafka",
                    "match_type": "no_match",
                }
            ],
            "scores": {
                "evidence": 0.4,
                "domain": 1.0,
            },
            "hard_skill_gate": {
                "applied": True,
            },
        },
        {
            "requirement_groups": {
                "domain_context": ["banking and fintech"],
            }
        },
    )

    assert result["skill_gap_summary"] == {
        "missing_must_have_count": 1,
        "weak_evidence_count": 1,
        "optional_growth_count": 1,
        "presentation_gap_count": 3,
    }
    assert result["skill_gaps"]["missing_must_have"] == [
        {
            "skill": "AWS",
            "gap_type": "missing_must_have",
        }
    ]
    assert result["skill_gaps"]["weak_evidence"] == [
        {
            "skill": "Docker",
            "gap_type": "weak_evidence",
            "current_evidence_level": 1,
            "match_type": "exact_match",
        }
    ]
    assert result["skill_gaps"]["optional_growth"] == [
        {
            "skill": "Kafka",
            "gap_type": "optional_growth",
        }
    ]
    assert any(
        suggestion.startswith("If you have real experience with AWS")
        for suggestion in result["cv_improvement_suggestions"]
    )
    assert any(
        "Move Docker from a keyword-only mention" in suggestion
        for suggestion in result["cv_improvement_suggestions"]
    )
    assert len(result["next_best_actions"]) <= 4
