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
    assert result["phase"] == (
        "Phase 27 - Typed Requirement Schema and Section-aware JD Parsing"
    )
    assert "embedding_enabled" in result
    assert "embedding_model" in result
    assert "embedding_loaded" in result
    assert "embedding_local_only" in result
    assert "embedding_threshold" in result


def test_screening_endpoint_returns_ranked_candidates() -> None:
    response = client.post("/screening", json=_demo_api_payload())

    assert response.status_code == 200
    result = response.json()

    assert result["trace_id"].startswith("screening-")
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
    assert candidate["base_score"] == 87
    assert candidate["hard_skill_gate"]["passed"] is True
    assert candidate["review_card"]["summary"] == (
        "Nguyen Van A is a Strong Review candidate for Backend Java Developer "
        "with a final score of 87/100."
    )
    assert result["diagnostics"]["trace_id"] == result["trace_id"]
    assert result["diagnostics"]["payload"]["candidates"]["received_count"] == 1


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


def test_recommend_jobs_endpoint_returns_ranked_top_jobs() -> None:
    response = client.post("/recommend-jobs", json=_demo_recommendation_payload())

    assert response.status_code == 200
    result = response.json()

    assert result["trace_id"].startswith("recommend-jobs-")
    assert result["candidate"]["candidate_id"] == 456
    assert result["candidate"]["candidate_name"] == "Nguyen Van A"
    assert result["retrieval_stats"]["jobs_received"] == 3
    assert result["retrieval_stats"]["jobs_indexed"] == 3
    assert result["retrieval_stats"]["jobs_retrieved"] == 2
    assert result["retrieval_stats"]["jobs_reranked"] == 2
    assert result["retrieval_stats"]["top_k"] == 2
    assert result["retrieval_stats"]["retrieval_top_n"] == 2
    assert result["job_quality_stats"] == {
        "jobs_received": 3,
        "eligible_jobs": 3,
        "excluded_jobs": 0,
    }
    assert result["excluded_jobs"] == []
    assert result["warnings"] == []
    assert result["diagnostics"]["trace_id"] == result["trace_id"]
    assert result["diagnostics"]["payload"]["jobs"]["received_count"] == 3
    assert len(result["top_jobs"]) == 2

    top_job = result["top_jobs"][0]
    assert top_job["rank"] == 1
    assert top_job["job_id"] == 10
    assert top_job["job_title"] == "Backend Java Developer"
    assert top_job["retrieval_rank"] == 1
    assert top_job["retrieval_score"] > 0
    assert top_job["retrieval_reasons"]
    assert top_job["fit_score"] >= 80
    assert top_job["fit_label"] == "Strong Fit"
    assert "Strong Fit" in top_job["fit_summary"]
    assert top_job["matched_must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    assert top_job["skill_gap_summary"] == {
        "missing_must_have_count": 0,
        "weak_evidence_count": 0,
        "optional_growth_count": 1,
        "presentation_gap_count": 0,
    }
    assert top_job["skill_gaps"]["optional_growth"] == [
        {
            "skill": "AWS",
            "gap_type": "optional_growth",
        }
    ]
    assert top_job["cv_improvement_suggestions"]
    assert top_job["next_best_actions"]
    assert top_job["job_quality"]["recommendation_eligible"] is True
    assert top_job["job_quality"]["quality_label"] in {
        "eligible",
        "eligible_with_warning",
    }
    assert top_job["review_card"]["job_title"] == "Backend Java Developer"


def test_recommend_jobs_endpoint_returns_422_for_invalid_schema() -> None:
    response = client.post("/recommend-jobs", json={})

    assert response.status_code == 422


def test_recommend_jobs_endpoint_returns_400_for_empty_job_list() -> None:
    response = client.post(
        "/recommend-jobs",
        json={
            "candidate": {
                "candidate_name": "No Jobs Candidate",
                "cv_text": "No Jobs Candidate\nBackend Developer",
            },
            "jobs": [],
        },
    )

    assert response.status_code == 400
    assert "at least one job" in response.json()["detail"]


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


def _demo_recommendation_payload() -> dict:
    return {
        "candidate": {
            "candidate_id": 456,
            "candidate_name": "Nguyen Van A",
            "cv_text": load_text_file("data/cvs/cv_strong.txt"),
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
