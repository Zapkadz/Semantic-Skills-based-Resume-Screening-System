import pytest

from src.payload_pipeline import (
    build_cv_document_from_payload,
    build_jd_text_from_payload,
    run_screening_payload,
)
from src.embedding_matcher import SemanticEmbeddingMatcher


class FakeMultilingualEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "identity verification": [1.0, 0.0],
            "digital identity verification": [0.96, 0.04],
            "eKYC": [0.90, 0.10],
        }
        return [vectors[text] for text in texts]


def test_build_jd_text_from_payload_uses_structured_sections() -> None:
    job = {
        "job_title": "Backend Java Developer",
        "requirements": ["Java", "Spring Boot"],
        "nice_to_have": ["AWS"],
        "responsibilities": ["Build REST APIs."],
        "minimum_experience_years": 1,
    }

    text = build_jd_text_from_payload(job)

    assert text == (
        "Backend Java Developer\n"
        "\n"
        "Requirements:\n"
        "- Java\n"
        "- Spring Boot\n"
        "- 1+ year experience\n"
        "\n"
        "Nice to have:\n"
        "- AWS\n"
        "\n"
        "Responsibilities:\n"
        "- Build REST APIs."
    )


def test_build_jd_text_from_payload_prefers_raw_text() -> None:
    raw_text = "QA Tester\n\nRequirements:\n- API testing"

    assert build_jd_text_from_payload({"raw_text": raw_text}) == raw_text


def test_build_cv_document_from_payload_uses_cv_text_and_ids() -> None:
    candidate = {
        "application_id": 123,
        "candidate_id": 456,
        "candidate_name": "Nguyen Van A",
        "email": "candidate@example.com",
        "cv_text": "Nguyen Van A\nBackend Developer\n\nSkills:\n- Java",
    }

    document = build_cv_document_from_payload(candidate)

    assert document == {
        "filename": "application-123__candidate-456.txt",
        "path": "",
        "text": "Nguyen Van A\nBackend Developer\n\nSkills:\n- Java",
        "application_id": 123,
        "candidate_id": 456,
        "email": "candidate@example.com",
        "phone": "",
        "applied_at": "",
        "cv_file_path": "",
        "candidate_name": "Nguyen Van A",
    }


def test_build_cv_document_from_payload_can_build_structured_cv_text() -> None:
    candidate = {
        "application_id": 123,
        "candidate_id": 456,
        "candidate_name": "Nguyen Van A",
        "headline": "Backend Developer",
        "summary": "Backend developer with Java experience.",
        "skills": ["Java", "Spring Boot"],
        "work_experience": [
            {
                "title": "Backend Developer Intern",
                "company": "ABC Tech",
                "duration": "06/2024 - 12/2024",
                "description": ["Built REST APIs using Java."],
            }
        ],
        "projects": [
            {
                "name": "E-commerce API",
                "description": ["Created RESTful APIs."],
                "technologies": ["Java", "Spring Boot"],
            }
        ],
        "education": ["Bachelor of Software Engineering"],
    }

    document = build_cv_document_from_payload(candidate)

    assert document["filename"] == "application-123__candidate-456.txt"
    assert document["text"] == (
        "Nguyen Van A\n"
        "Backend Developer\n"
        "\n"
        "Summary:\n"
        "Backend developer with Java experience.\n"
        "\n"
        "Skills:\n"
        "- Java\n"
        "- Spring Boot\n"
        "\n"
        "Work Experience:\n"
        "Backend Developer Intern - ABC Tech\n"
        "06/2024 - 12/2024\n"
        "- Built REST APIs using Java.\n"
        "\n"
        "Projects:\n"
        "E-commerce API\n"
        "- Created RESTful APIs.\n"
        "Technologies: Java, Spring Boot\n"
        "\n"
        "Education:\n"
        "Bachelor of Software Engineering"
    )


def test_run_screening_payload_returns_ranked_candidates_with_web_ids() -> None:
    result = run_screening_payload(_demo_screening_payload())

    assert result["job"]["job_id"] == 10
    assert result["job"]["title"] == "Backend Java Developer"
    assert result["job"]["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]

    candidate = result["candidates"][0]
    assert candidate["rank"] == 1
    assert candidate["application_id"] == 123
    assert candidate["candidate_id"] == 456
    assert candidate["candidate_name"] == "Nguyen Van A"
    assert candidate["source_file"] == "application-123__candidate-456.txt"
    assert candidate["final_score"] == 87
    assert candidate["recommendation"] == "Strong Review"
    assert candidate["review_card"]["job_title"] == "Backend Java Developer"
    assert candidate["review_card"]["concerns"] == [
        "Optional nice-to-have gaps: AWS and Kafka."
    ]


def test_run_screening_payload_rejects_missing_job_text() -> None:
    payload = {"job": {}, "candidates": []}

    with pytest.raises(ValueError, match="Job payload must include"):
        run_screening_payload(payload)


def test_run_screening_payload_rejects_candidate_without_cv_data() -> None:
    payload = {
        "job": {"job_title": "Backend Java Developer", "requirements": ["Java"]},
        "candidates": [{"application_id": 123, "candidate_name": "No CV"}],
    }

    with pytest.raises(ValueError, match="Candidate payload must include"):
        run_screening_payload(payload)


def test_run_screening_payload_matches_english_jd_with_vietnamese_cv() -> None:
    payload = {
        "job": {
            "job_id": 20,
            "raw_text": (
                "Computer Vision Engineer\n"
                "\n"
                "Requirements\n"
                "- Experience with face recognition and anti-spoofing.\n"
                "- Python"
            ),
        },
        "candidates": [
            {
                "application_id": 555,
                "candidate_name": "Le Van AI",
                "cv_text": (
                    "Le Van AI\n"
                    "AI Engineer\n"
                    "\n"
                    "Kỹ năng\n"
                    "Python\n"
                    "\n"
                    "Dự án\n"
                    "Tên dự án: eKYC Face System\n"
                    "Mô tả:\n"
                    "- Xây dựng hệ thống nhận diện khuôn mặt và chống giả mạo."
                ),
            }
        ],
    }

    result = run_screening_payload(payload)

    assert result["job"]["must_have_skills"] == [
        "Face Recognition",
        "Anti-Spoofing",
        "Python",
    ]
    candidate = result["candidates"][0]
    assert candidate["candidate_name"] == "Le Van AI"
    assert candidate["final_score"] >= 70
    assert candidate["missing_skills"] == []
    assert [
        (match["required_skill"], match["evidence_level"])
        for match in candidate["matched_skills"]
    ] == [
        ("Face Recognition", 3),
        ("Anti-Spoofing", 3),
        ("Python", 1),
    ]


def test_run_screening_payload_can_use_injected_multilingual_embedding_matcher() -> None:
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeMultilingualEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_id": 30,
            "job_title": "Identity Platform Specialist",
            "requirements": ["identity verification"],
        },
        "candidates": [
            {
                "application_id": 777,
                "candidate_name": "Digital ID Candidate",
                "cv_text": (
                    "Digital ID Candidate\n"
                    "Identity Engineer\n"
                    "\n"
                    "Skills:\n"
                    "- digital identity verification"
                ),
            }
        ],
    }

    result = run_screening_payload(payload, embedding_matcher=embedding_matcher)

    match = result["candidates"][0]["matched_skills"][0]
    assert match["required_skill"] == "identity verification"
    assert match["candidate_skill"] == "digital identity verification"
    assert match["match_type"] == "semantic_match"
    assert match["similarity"] == 0.9991


def _demo_screening_payload() -> dict:
    return {
        "job": {
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
            "nice_to_have": ["AWS", "Kafka", "Kubernetes"],
            "responsibilities": [
                "Develop backend services.",
                "Build RESTful APIs.",
                "Work with relational databases.",
            ],
        },
        "candidates": [
            {
                "application_id": 123,
                "candidate_id": 456,
                "candidate_name": "Nguyen Van A",
                "email": "candidate@example.com",
                "cv_text": (
                    "Nguyen Van A\n"
                    "Backend Developer\n"
                    "\n"
                    "Summary:\n"
                    "Backend developer with experience building Java Spring Boot services and REST APIs.\n"
                    "\n"
                    "Skills:\n"
                    "- Java\n"
                    "- Spring Boot\n"
                    "- REST API\n"
                    "- MySQL\n"
                    "- Docker\n"
                    "\n"
                    "Work Experience:\n"
                    "Backend Developer Intern - ABC Tech\n"
                    "06/2024 - 12/2024\n"
                    "- Built REST APIs using Java and Spring Boot.\n"
                    "- Designed MySQL database schemas for product and order modules.\n"
                    "- Used Docker Compose for local development and testing.\n"
                    "\n"
                    "Projects:\n"
                    "E-commerce API\n"
                    "- Developed authentication and order management modules.\n"
                    "- Implemented JWT login for backend services.\n"
                    "- Created RESTful APIs with Spring Boot and MySQL.\n"
                    "\n"
                    "Education:\n"
                    "Bachelor of Software Engineering"
                ),
            }
        ],
    }
