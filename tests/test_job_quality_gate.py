from src.job_quality_gate import evaluate_job_quality


def test_evaluate_job_quality_marks_placeholder_test_post_ineligible() -> None:
    result = evaluate_job_quality(
        {
            "job_title": "Test",
            "description": "test",
        },
        {
            "job_title": "Test",
        },
        "Test\n\ntest",
        {
            "must_have_technical": [],
            "nice_to_have_technical": [],
            "soft_skills": [],
            "education": [],
            "experience": [],
            "certifications": [],
            "domain_context": [],
            "responsibilities": [],
            "ignored": [],
        },
        must_have_skills=[],
        nice_to_have_skills=[],
        open_set_requirements=[],
    )

    assert result["recommendation_eligible"] is False
    assert result["quality_label"] == "insufficient_jd_data"
    assert "placeholder_title" in result["flags"]
    assert "missing_requirements" in result["flags"]
    assert result["quality_score"] < 50


def test_evaluate_job_quality_accepts_real_backend_jd() -> None:
    result = evaluate_job_quality(
        {
            "job_title": "Backend Java Developer",
            "description": (
                "<p>Build backend services and REST APIs for business systems.</p>"
            ),
            "requirements": [
                "Java",
                "Spring Boot",
                "REST API",
                "SQL",
            ],
            "responsibilities": [
                "Develop backend services.",
                "Build RESTful APIs.",
            ],
        },
        {
            "job_title": "Backend Java Developer",
        },
        "Backend Java Developer\n\nRequirements:\n- Java\n- Spring Boot\n- REST API\n- SQL",
        {
            "must_have_technical": [
                "Java",
                "Spring Boot",
                "REST API",
                "SQL",
            ],
            "nice_to_have_technical": [],
            "soft_skills": [],
            "education": [],
            "experience": [],
            "certifications": [],
            "domain_context": [],
            "responsibilities": [
                "Develop backend services.",
                "Build RESTful APIs.",
            ],
            "ignored": [],
        },
        must_have_skills=["Java", "Spring Boot", "REST API", "SQL"],
        nice_to_have_skills=[],
        open_set_requirements=[],
    )

    assert result["recommendation_eligible"] is True
    assert result["quality_label"] == "eligible"
    assert result["flags"] == []
    assert result["quality_score"] >= 80


def test_evaluate_job_quality_rejects_short_description_without_requirements_section() -> None:
    result = evaluate_job_quality(
        {
            "job_title": "Customer Support Staff",
            "description": "mo ta test",
        },
        {
            "job_title": "Customer Support Staff",
        },
        "Customer Support Staff\n\nmo ta test",
        {
            "must_have_technical": ["mo ta test"],
            "nice_to_have_technical": [],
            "soft_skills": [],
            "education": [],
            "experience": [],
            "certifications": [],
            "domain_context": [],
            "responsibilities": [],
            "ignored": [],
        },
        must_have_skills=[],
        nice_to_have_skills=[],
        open_set_requirements=["mo ta test"],
    )

    assert result["recommendation_eligible"] is False
    assert result["quality_label"] == "insufficient_jd_data"
    assert "missing_explicit_requirements" in result["flags"]


def test_evaluate_job_quality_rejects_bare_experience_and_placeholder_description() -> None:
    result = evaluate_job_quality(
        {
            "job_title": "Test",
            "requirements": ["1 năm"],
            "responsibilities": ["mô tả test"],
            "description": "mô tả test",
        },
        {
            "job_title": "Test",
        },
        "Test\n\nYêu cầu ứng viên\n- 1 năm\n\nMô tả công việc\n- mô tả test",
        {
            "must_have_technical": [],
            "nice_to_have_technical": [],
            "soft_skills": [],
            "education": [],
            "experience": ["1 năm"],
            "certifications": [],
            "domain_context": [],
            "responsibilities": ["mô tả test"],
            "ignored": [],
        },
        must_have_skills=[],
        nice_to_have_skills=[],
        open_set_requirements=[],
    )

    assert result["recommendation_eligible"] is False
    assert result["quality_label"] == "insufficient_jd_data"
    assert "missing_explicit_requirements" in result["flags"]
    assert result["metrics"]["structured_requirement_count"] == 0
