import pytest

from src.job_recommendation_pipeline import run_job_recommendation_payload


def test_run_job_recommendation_payload_returns_ranked_top_jobs() -> None:
    result = run_job_recommendation_payload(_demo_recommendation_payload())

    assert result["candidate"] == {
        "candidate_id": 456,
        "candidate_name": "Nguyen Van A",
        "source_file": "candidate-456.txt",
        "cv_file_path": "",
    }
    assert result["retrieval_stats"] == {
        "jobs_received": 3,
        "jobs_indexed": 3,
        "jobs_retrieved": 2,
        "jobs_reranked": 2,
        "top_k": 2,
        "retrieval_top_n": 2,
        "retrieval_applied": True,
    }

    assert len(result["top_jobs"]) == 2

    top_job = result["top_jobs"][0]
    assert top_job["rank"] == 1
    assert top_job["job_id"] == 10
    assert top_job["job_title"] == "Backend Java Developer"
    assert top_job["retrieval_rank"] == 1
    assert top_job["retrieval_score"] > 0
    assert top_job["retrieval_reasons"]
    assert top_job["fit_score"] >= 80
    assert top_job["matched_must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    assert top_job["missing_must_have_skills"] == []
    assert top_job["optional_strengths"] == []
    assert top_job["why_fit"]
    assert "AWS" in " ".join(top_job["what_to_improve"])
    assert top_job["review_card"]["job_title"] == "Backend Java Developer"

    second_job = result["top_jobs"][1]
    assert second_job["rank"] == 2
    assert second_job["job_id"] != top_job["job_id"]
    assert second_job["fit_score"] <= top_job["fit_score"]


def test_run_job_recommendation_payload_accepts_resume_and_title_aliases() -> None:
    payload = {
        "candidate": {
            "candidate_id": "cand-01",
            "candidate_name": "Digital ID Candidate",
            "resume_text": (
                "Digital ID Candidate\n"
                "Identity Engineer\n"
                "\n"
                "Skills:\n"
                "- digital identity verification"
            ),
        },
        "jobs": [
            {
                "job_id": "job-01",
                "title": "Identity Platform Specialist",
                "job_description_text": (
                    "Requirements:\n"
                    "- identity verification"
                ),
            }
        ],
    }

    result = run_job_recommendation_payload(payload)

    assert result["candidate"]["candidate_id"] == "cand-01"
    assert result["top_jobs"][0]["job_id"] == "job-01"
    assert result["top_jobs"][0]["job_title"] == "Identity Platform Specialist"


def test_run_job_recommendation_payload_rejects_empty_job_list() -> None:
    payload = {
        "candidate": {
            "candidate_name": "No Jobs Candidate",
            "cv_text": "No Jobs Candidate\nBackend Developer",
        },
        "jobs": [],
    }

    with pytest.raises(ValueError, match="at least one job"):
        run_job_recommendation_payload(payload)


def _demo_recommendation_payload() -> dict:
    return {
        "candidate": {
            "candidate_id": 456,
            "candidate_name": "Nguyen Van A",
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
        },
        "jobs": [
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
            },
            {
                "job_id": 20,
                "job_title": "Frontend React Developer",
                "requirements": [
                    "JavaScript",
                    "React",
                    "CSS",
                    "2+ years frontend experience",
                ],
            },
            {
                "job_id": 30,
                "job_title": "IT Security Analyst",
                "requirements": [
                    "Qualys",
                    "Vulnerability Management",
                    "Linux Administration",
                    "ISO 27001",
                ],
            },
        ],
        "options": {
            "top_k": 2,
            "retrieval_top_n": 2,
        },
    }
