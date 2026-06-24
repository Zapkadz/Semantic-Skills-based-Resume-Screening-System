import json
from pathlib import Path

from src.screening_pipeline import (
    format_ranking_summary,
    run_screening_pipeline,
    save_pipeline_result_json,
    save_review_cards,
)


def test_run_screening_pipeline_returns_ranked_demo_result(tmp_path: Path) -> None:
    result = run_screening_pipeline(
        jd_path="data/jobs/jd_backend_java.txt",
        cv_dir=_demo_cv_dir(tmp_path),
    )

    job = result["job"]
    assert job["title"] == "Backend Java Developer"
    assert job["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    assert job["nice_to_have_skills"] == ["AWS", "Kafka", "Kubernetes"]
    assert job["open_set_requirements"] == []
    assert job["minimum_experience_years"] == 1
    assert job["seniority"] == "Junior"
    assert job["domain"] == ["Backend", "Web Application"]
    assert job["taxonomy_coverage"] == {
        "known_count": 5,
        "unknown_count": 0,
        "coverage_ratio": 1.0,
        "known_requirements": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
        "unknown_requirements": [],
    }
    assert job["screening_confidence"] == {
        "level": "high",
        "known_requirement_count": 5,
        "open_set_requirement_count": 0,
        "embedding_enabled": False,
        "warnings": [],
    }
    assert job["requirement_groups"] == {
        "must_have_technical": [
            "Java",
            "Spring Boot",
            "REST API",
            "SQL",
            "Basic Docker",
        ],
        "nice_to_have_technical": ["AWS", "Kafka", "Kubernetes"],
        "soft_skills": [],
        "education": [],
        "experience": ["1+ year backend experience"],
        "certifications": [],
        "language": [],
        "domain_context": [],
        "responsibilities": [
            "Develop backend services.",
            "Build RESTful APIs.",
            "Work with relational databases.",
            "Collaborate with frontend developers.",
        ],
        "ignored": [],
    }
    assert [item["type"] for item in job["typed_requirements"]] == [
        "TECH_SKILL",
        "TOOL_PLATFORM",
        "TECH_SKILL",
        "TOOL_PLATFORM",
        "TOOL_PLATFORM",
        "EXPERIENCE_REQUIREMENT",
        "TOOL_PLATFORM",
        "TOOL_PLATFORM",
        "TOOL_PLATFORM",
        "RESPONSIBILITY_CONTEXT",
        "RESPONSIBILITY_CONTEXT",
        "RESPONSIBILITY_CONTEXT",
        "RESPONSIBILITY_CONTEXT",
    ]
    assert len(result["candidates"]) == 1

    candidate = result["candidates"][0]
    assert candidate["rank"] == 1
    assert candidate["candidate_name"] == "Nguyen Van A"
    assert candidate["source_file"] == "cv_strong.txt"
    assert candidate["final_score"] == 87
    assert candidate["recommendation"] == "Strong Review"
    assert candidate["review_card"]["summary"] == (
        "Nguyen Van A is a Strong Review candidate for Backend Java Developer "
        "with a final score of 87/100."
    )


def test_format_ranking_summary_returns_cli_friendly_text(tmp_path: Path) -> None:
    result = run_screening_pipeline(
        jd_path="data/jobs/jd_backend_java.txt",
        cv_dir=_demo_cv_dir(tmp_path),
    )

    summary = format_ranking_summary(result)

    assert summary == (
        "Semantic Skills-based Resume Screening System\n"
        "Phase 10 - CLI Pipeline and Output\n"
        "\n"
        "Job: Backend Java Developer\n"
        "Candidates analyzed: 1\n"
        "\n"
        "Ranking:\n"
        "1. Nguyen Van A - 87/100 - Strong Review"
    )


def test_save_pipeline_result_json_writes_pretty_json(tmp_path: Path) -> None:
    result = run_screening_pipeline(
        jd_path="data/jobs/jd_backend_java.txt",
        cv_dir=_demo_cv_dir(tmp_path),
    )
    output_path = tmp_path / "ranking_results.json"

    saved_path = save_pipeline_result_json(result, output_path)

    assert saved_path == str(output_path)
    saved_result = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved_result["job"]["title"] == "Backend Java Developer"
    assert saved_result["candidates"][0]["candidate_name"] == "Nguyen Van A"


def test_save_review_cards_writes_markdown_files(tmp_path: Path) -> None:
    result = run_screening_pipeline(
        jd_path="data/jobs/jd_backend_java.txt",
        cv_dir=_demo_cv_dir(tmp_path),
    )
    output_dir = tmp_path / "reports"

    saved_paths = save_review_cards(result, output_dir)

    assert saved_paths == [str(output_dir / "rank-01-nguyen-van-a.md")]
    markdown = Path(saved_paths[0]).read_text(encoding="utf-8")
    assert markdown.startswith("# Nguyen Van A")
    assert "Score: 87/100" in markdown
    assert "## Suggested Interview Questions" in markdown


def test_run_screening_pipeline_handles_empty_cv_directory(tmp_path: Path) -> None:
    result = run_screening_pipeline(
        jd_path="data/jobs/jd_backend_java.txt",
        cv_dir=tmp_path,
    )

    assert result["job"]["title"] == "Backend Java Developer"
    assert result["candidates"] == []
    assert "No candidates found." in format_ranking_summary(result)


def _demo_cv_dir(tmp_path: Path) -> Path:
    cv_dir = tmp_path / "cvs"
    cv_dir.mkdir()
    cv_text = Path("data/cvs/cv_strong.txt").read_text(encoding="utf-8")
    (cv_dir / "cv_strong.txt").write_text(cv_text, encoding="utf-8")
    return cv_dir
