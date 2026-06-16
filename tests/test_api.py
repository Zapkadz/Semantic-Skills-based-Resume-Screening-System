from fastapi.testclient import TestClient

from api import app
from src.document_loader import load_text_file


client = TestClient(app)


def test_health_endpoint_returns_service_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    result = response.json()
    assert result["status"] == "ok"
    assert result["service"] == "semantic-skills-resume-screening"
    assert result["phase"] == "Phase 17 - Taxonomy-independent Open-set Screening Core"
    assert "embedding_enabled" in result
    assert "embedding_model" in result
    assert "embedding_loaded" in result
    assert "embedding_local_only" in result
    assert "embedding_threshold" in result


def test_screening_endpoint_returns_ranked_candidates() -> None:
    response = client.post("/screening", json=_demo_api_payload())

    assert response.status_code == 200
    result = response.json()

    assert result["job"]["job_id"] == 10
    assert result["job"]["title"] == "Backend Java Developer"
    assert len(result["candidates"]) == 1

    candidate = result["candidates"][0]
    assert candidate["rank"] == 1
    assert candidate["application_id"] == 123
    assert candidate["candidate_id"] == 456
    assert candidate["candidate_name"] == "Nguyen Van A"
    assert candidate["final_score"] == 87
    assert candidate["recommendation"] == "Strong Review"
    assert candidate["review_card"]["summary"] == (
        "Nguyen Van A is a Strong Review candidate for Backend Java Developer "
        "with a final score of 87/100."
    )


def test_screening_endpoint_returns_422_for_invalid_schema() -> None:
    response = client.post("/screening", json={})

    assert response.status_code == 422


def test_screening_endpoint_returns_400_for_missing_candidate_cv_text() -> None:
    response = client.post(
        "/screening",
        json={
            "job": {
                "job_id": 10,
                "job_title": "Backend Java Developer",
                "requirements": ["Java"],
            },
            "candidates": [
                {
                    "application_id": 123,
                    "candidate_id": 456,
                    "candidate_name": "No CV",
                }
            ],
        },
    )

    assert response.status_code == 400
    assert "Candidate payload must include" in response.json()["detail"]


def _demo_api_payload() -> dict:
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
                "cv_text": load_text_file("data/cvs/cv_strong.txt"),
            }
        ],
    }
