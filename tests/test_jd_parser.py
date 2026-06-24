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
    assert criteria["sections"]["requirements"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Basic Docker",
        "1+ year backend experience",
    ]
    assert criteria["sections"]["nice_to_have"] == ["AWS", "Kafka", "Kubernetes"]


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

    assert criteria["job_title"] == "Frontend Developer"
    assert criteria["must_have_skills"] == []
    assert criteria["nice_to_have_skills"] == []
    assert criteria["responsibilities"] == []
    assert criteria["minimum_experience_years"] == 0
    assert criteria["seniority"] == "Not specified"
    assert criteria["domain"] == []
    assert criteria["sections"]["title"] == "Frontend Developer"
    assert criteria["sections"]["description"] == []
    assert criteria["description_lines"] == []


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


def test_parse_jd_supports_bare_english_headings_and_stops_at_benefits() -> None:
    criteria = parse_jd(
        "AI Computer Vision Engineer\n"
        "\n"
        "Job Description\n"
        "Build computer vision models for eKYC.\n"
        "\n"
        "Requirements\n"
        "- Strong Python programming skills.\n"
        "- At least 3 years of experience.\n"
        "- Face Detection\n"
        "\n"
        "Benefits\n"
        "- Laptop support"
    )

    assert criteria["must_have_skills"] == [
        "Strong Python programming skills.",
        "Face Detection",
    ]
    assert criteria["responsibilities"] == [
        "Build computer vision models for eKYC."
    ]
    assert criteria["description_lines"] == [
        "Build computer vision models for eKYC."
    ]
    assert criteria["minimum_experience_years"] == 3
    assert criteria["seniority"] == "Middle"
    assert criteria["domain"] == [
        "AI/Machine Learning",
        "Computer Vision",
        "eKYC/Biometrics",
    ]


def test_parse_jd_supports_vietnamese_headings_and_experience() -> None:
    criteria = parse_jd(
        "Backend Developer\n"
        "\n"
        "Yeu cau\n"
        "- Java\n"
        "- Toi thieu 2 nam kinh nghiem\n"
        "\n"
        "Mo ta cong viec\n"
        "- Xay dung REST API."
    )

    assert criteria["must_have_skills"] == ["Java"]
    assert criteria["responsibilities"] == ["Xay dung REST API."]
    assert criteria["minimum_experience_years"] == 2
    assert criteria["seniority"] == "Middle"
    assert criteria["sections"]["requirements"] == [
        "Java",
        "Toi thieu 2 nam kinh nghiem",
    ]
    assert criteria["sections"]["description"] == ["Xay dung REST API."]


def test_parse_jd_infers_title_from_first_responsibility_heading() -> None:
    criteria = parse_jd(
        "Mo ta Cong Viec\n"
        "1. IT Security Operations\n"
        "- Monitor security logs.\n"
        "\n"
        "Yeu Cau Cong Viec\n"
        "- At least 3 yeear of experience in IT Security Operations, Governance, Compliance.\n"
        "- Knowledge of vulnerability management tools."
    )

    assert criteria["job_title"] == "IT Security Operations"
    assert criteria["minimum_experience_years"] == 3
    assert criteria["seniority"] == "Middle"
    assert criteria["domain"] == ["IT Security/GRC"]


def test_parse_jd_domain_matching_does_not_match_edge_inside_knowledge() -> None:
    criteria = parse_jd(
        "Data Engineer\n\n"
        "Requirements:\n"
        "- Knowledge of vulnerability management tools."
    )

    assert "Mobile AI" not in criteria["domain"]
