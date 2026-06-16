from src.job_indexer import build_job_index_documents


def test_build_job_index_documents_creates_searchable_fields() -> None:
    indexed_jobs = build_job_index_documents(
        [
            {
                "job_id": 10,
                "job_title": "Backend Java Developer",
                "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
                "nice_to_have_skills": ["AWS"],
                "open_set_requirements": [],
                "minimum_experience_years": 1,
                "seniority": "Junior",
                "domain": ["Backend", "Web Application"],
                "requirement_groups": {"domain_context": []},
            }
        ]
    )

    assert len(indexed_jobs) == 1
    indexed_job = indexed_jobs[0]
    assert indexed_job["job_id"] == 10
    assert "Backend Java Developer" in indexed_job["sparse_text"]
    assert "Spring Boot" in indexed_job["dense_text"]
    assert "AWS" in indexed_job["dense_text"]
    assert "backend" in indexed_job["title_terms"]
    assert "java" in indexed_job["sparse_terms"]
    assert "spring boot" in indexed_job["must_have_skill_keys"]
    assert "aws" in indexed_job["nice_to_have_skill_keys"]
    assert indexed_job["job_card"]["job_title"] == "Backend Java Developer"
