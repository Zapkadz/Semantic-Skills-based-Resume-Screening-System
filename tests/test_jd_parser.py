from src.document_loader import load_text_file
from src.jd_parser import parse_jd


def test_parse_jd_extracts_demo_job_criteria() -> None:
    text = load_text_file("data/jobs/jd_backend_java.txt")

    criteria = parse_jd(text)

    assert criteria["job_title"] == "Backend Java Developer"
    assert criteria["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Basic Docker",
    ]
    assert criteria["nice_to_have_skills"] == ["AWS", "Kafka", "Kubernetes"]
    assert criteria["minimum_experience_years"] == 1
    assert criteria["seniority"] == "Junior"
    assert criteria["domain"] == ["Backend", "Web Application"]


def test_parse_jd_extracts_demo_responsibilities() -> None:
    text = load_text_file("data/jobs/jd_backend_java.txt")

    criteria = parse_jd(text)

    assert criteria["responsibilities"] == [
        "Develop backend services.",
        "Build RESTful APIs.",
        "Work with relational databases.",
        "Collaborate with frontend developers.",
    ]


def test_parse_jd_handles_missing_sections() -> None:
    criteria = parse_jd("Frontend Developer")

    assert criteria == {
        "job_title": "Frontend Developer",
        "must_have_skills": [],
        "nice_to_have_skills": [],
        "responsibilities": [],
        "minimum_experience_years": 0,
        "seniority": "Not specified",
        "domain": [],
    }


def test_parse_jd_detects_seniority_from_title_before_years() -> None:
    criteria = parse_jd(
        "Senior Backend Developer\n\nRequirements:\n- Java\n- 2+ years experience"
    )

    assert criteria["seniority"] == "Senior"
    assert criteria["minimum_experience_years"] == 2
    assert criteria["must_have_skills"] == ["Java"]


def test_parse_jd_supports_inline_requirements_heading() -> None:
    criteria = parse_jd("QA Tester\n\nRequirements: API testing")

    assert criteria["must_have_skills"] == ["API testing"]
    assert criteria["domain"] == ["Backend", "Web Application", "Testing"]
