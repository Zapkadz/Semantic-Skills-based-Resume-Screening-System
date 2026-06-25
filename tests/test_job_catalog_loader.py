from src.job_catalog_loader import build_job_catalog


def test_build_job_catalog_returns_normalized_job_cards() -> None:
    catalog = build_job_catalog(
        [
            {
                "job_id": 10,
                "job_title": "Backend Java Developer",
                "requirements": [
                    "Java",
                    "Spring Boot",
                    "REST API",
                    "SQL",
                    "Basic Docker",
                    "1+ year backend experience",
                ],
                "nice_to_have": ["AWS"],
            }
        ]
    )

    assert len(catalog) == 1
    job_card = catalog[0]
    assert job_card["job_id"] == 10
    assert job_card["job_title"] == "Backend Java Developer"
    assert job_card["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    assert job_card["nice_to_have_skills"] == ["AWS"]
    assert job_card["minimum_experience_years"] == 1
    assert job_card["domain"] == ["Backend", "Web Application"]
    assert job_card["open_set_requirements"] == []
    assert job_card["open_set_filter_summary"] == {
        "candidate_count": 0,
        "kept_count": 0,
        "discarded_count": 0,
        "kept_for_matching_count": 0,
        "kept_for_suggestion_count": 0,
        "discarded_reason_counts": {},
    }
    assert job_card["taxonomy_coverage"]["coverage_ratio"] == 1.0
    assert job_card["payload_diagnostics"]["flags"] == [
        "jd_missing_responsibilities_input"
    ]
    assert job_card["typed_requirements"][0]["type"] == "TECH_SKILL"
    assert job_card["job_quality"]["recommendation_eligible"] is True
    assert job_card["job_quality"]["quality_label"] in {
        "eligible",
        "eligible_with_warning",
    }
