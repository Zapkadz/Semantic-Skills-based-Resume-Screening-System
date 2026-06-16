from src.job_catalog_loader import build_job_catalog
from src.job_indexer import build_job_index_documents
from src.job_retriever import build_candidate_query_profile, retrieve_candidate_jobs


def test_retrieve_candidate_jobs_prefers_backend_role_for_backend_candidate() -> None:
    candidate_profile = build_candidate_query_profile(
        {
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
                "- Docker"
            ),
        }
    )
    job_catalog = build_job_catalog(
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
                ],
            },
            {
                "job_id": 20,
                "job_title": "Frontend React Developer",
                "requirements": [
                    "JavaScript",
                    "React",
                    "CSS",
                ],
            },
            {
                "job_id": 30,
                "job_title": "IT Security Analyst",
                "requirements": [
                    "Qualys",
                    "Vulnerability Management",
                    "Linux Administration",
                ],
            },
        ]
    )
    indexed_jobs = build_job_index_documents(job_catalog)

    retrieved_jobs = retrieve_candidate_jobs(candidate_profile, indexed_jobs, top_n=2)

    assert len(retrieved_jobs) == 2
    assert retrieved_jobs[0]["job_id"] == 10
    assert retrieved_jobs[0]["retrieval_score"] > retrieved_jobs[1]["retrieval_score"]
    assert "must-have" in " ".join(retrieved_jobs[0]["retrieval_reasons"]).casefold()
    assert retrieved_jobs[0]["retrieval_components"]["must_have_overlap"] > 0
