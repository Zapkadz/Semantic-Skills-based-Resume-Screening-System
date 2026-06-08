from src.document_loader import load_text_file
from src.resume_parser import parse_resume


def test_parse_resume_extracts_demo_candidate_profile() -> None:
    text = load_text_file("data/cvs/cv_strong.txt")

    profile = parse_resume(text)

    assert profile["candidate_name"] == "Nguyen Van A"
    assert profile["headline"] == "Backend Developer"
    assert (
        profile["summary"]
        == "Backend developer with experience building Java Spring Boot services and REST APIs."
    )
    assert profile["raw_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "MySQL",
        "Docker",
    ]
    assert profile["education"] == ["Bachelor of Software Engineering"]
    assert profile["certifications"] == []


def test_parse_resume_extracts_work_experience_from_demo_cv() -> None:
    text = load_text_file("data/cvs/cv_strong.txt")

    profile = parse_resume(text)

    assert profile["work_experience"] == [
        {
            "title": "Backend Developer Intern",
            "company": "ABC Tech",
            "duration": "06/2024 - 12/2024",
            "description": [
                "Built REST APIs using Java and Spring Boot.",
                "Designed MySQL database schemas for product and order modules.",
                "Used Docker Compose for local development and testing.",
            ],
        }
    ]


def test_parse_resume_extracts_projects_from_demo_cv() -> None:
    text = load_text_file("data/cvs/cv_strong.txt")

    profile = parse_resume(text)

    assert profile["projects"] == [
        {
            "name": "E-commerce API",
            "description": [
                "Developed authentication and order management modules.",
                "Implemented JWT login for backend services.",
                "Created RESTful APIs with Spring Boot and MySQL.",
            ],
            "technologies": [],
        }
    ]


def test_parse_resume_handles_minimal_resume_without_sections() -> None:
    profile = parse_resume("Tran Thi B\nFrontend Developer")

    assert profile == {
        "candidate_name": "Tran Thi B",
        "headline": "Frontend Developer",
        "summary": "",
        "raw_skills": [],
        "work_experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
    }


def test_parse_resume_supports_inline_summary_heading() -> None:
    profile = parse_resume(
        "Le Van C\nTester\n\nSummary: Manual tester with API testing exposure."
    )

    assert profile["summary"] == "Manual tester with API testing exposure."


def test_parse_resume_supports_vietnamese_sections_and_project_labels() -> None:
    profile = parse_resume(
        "Lê Văn A\n"
        "AI Engineer\n"
        "\n"
        "KỸ NĂNG\n"
        "Python\n"
        "PyTorch, TensorFlow\n"
        "\n"
        "KINH NGHIỆM LÀM VIỆC\n"
        "01/2021 - Nay\n"
        "AI Engineer\n"
        "ABC AI Lab\n"
        "Mô tả:\n"
        "- Xây dựng hệ thống Liveness Detection.\n"
        "\n"
        "DỰ ÁN\n"
        "Tên dự án: eKYC Face System\n"
        "Mô tả:\n"
        "Xây dựng hệ thống nhận diện khuôn mặt.\n"
        "Công nghệ:\n"
        "OpenCV\n"
        "ONNX"
    )

    assert profile["candidate_name"] == "Lê Văn A"
    assert profile["raw_skills"] == ["Python", "PyTorch", "TensorFlow"]
    assert profile["work_experience"] == [
        {
            "title": "AI Engineer",
            "company": "ABC AI Lab",
            "duration": "01/2021 - Nay",
            "description": ["Xây dựng hệ thống Liveness Detection."],
        }
    ]
    assert profile["projects"] == [
        {
            "name": "eKYC Face System",
            "description": ["Xây dựng hệ thống nhận diện khuôn mặt."],
            "technologies": ["OpenCV", "ONNX"],
        }
    ]


def test_parse_resume_repairs_common_mojibake_before_section_parsing() -> None:
    mojibake_name = "Nguyễn Văn A".encode("utf-8").decode("cp1252")
    mojibake_skills = "KỸ NĂNG".encode("utf-8").decode("cp1252")

    profile = parse_resume(f"{mojibake_name}\nAI Engineer\n\n{mojibake_skills}\nPython")

    assert profile["candidate_name"] == "Nguyễn Văn A"
    assert profile["raw_skills"] == ["Python"]
