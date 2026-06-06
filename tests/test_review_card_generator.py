from src.document_loader import load_text_file
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.review_card_generator import (
    build_evidence_highlights,
    format_review_card_markdown,
    generate_review_card,
)
from src.scorer import score_candidate
from src.semantic_matcher import match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_build_evidence_highlights_filters_weak_or_missing_evidence() -> None:
    matches = [
        {
            "required_skill": "Java",
            "candidate_skill": "Java",
            "match_type": "exact_match",
            "evidence_level": 3,
            "evidence_text": "Built Java services.",
            "evidence_source": "work_experience",
        },
        {
            "required_skill": "Docker",
            "candidate_skill": "Docker",
            "match_type": "exact_match",
            "evidence_level": 1,
            "evidence_text": "Docker",
            "evidence_source": "skills",
        },
        {
            "required_skill": "Kafka",
            "candidate_skill": None,
            "match_type": "no_match",
            "evidence_level": 0,
            "evidence_text": "",
            "evidence_source": "none",
        },
        {
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "evidence_level": 2,
            "evidence_text": "Backend service stack: Java, Spring Boot, MySQL.",
            "evidence_source": "projects",
        },
    ]

    highlights = build_evidence_highlights(matches)

    assert highlights == [
        {
            "skill": "Java",
            "required_skill": "Java",
            "candidate_skill": "Java",
            "match_type": "exact_match",
            "evidence_level": 3,
            "evidence_text": "Built Java services.",
            "evidence_source": "work_experience",
        },
        {
            "skill": "SQL via MySQL",
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "evidence_level": 2,
            "evidence_text": "Backend service stack: Java, Spring Boot, MySQL.",
            "evidence_source": "projects",
        },
    ]


def test_generate_review_card_returns_structured_explanation() -> None:
    candidate_result = _sample_candidate_result()
    job_criteria = {"job_title": "Backend Java Developer"}

    card = generate_review_card(candidate_result, job_criteria)

    assert card["candidate_name"] == "Nguyen Van A"
    assert card["job_title"] == "Backend Java Developer"
    assert card["summary"] == (
        "Nguyen Van A is a Strong Review candidate for Backend Java Developer "
        "with a final score of 87/100."
    )
    assert card["score_breakdown"] == candidate_result["scores"]
    assert card["strengths"] == [
        "Strong must-have skill coverage.",
        "Strong evidence in work or project descriptions.",
        "Good domain alignment with the role.",
        "Seniority appears aligned with the role.",
        "Clear evidence for Java and SQL via MySQL.",
    ]
    assert card["concerns"] == [
        "Missing must-have skills: Kafka.",
        "Optional nice-to-have gaps: AWS.",
    ]
    assert card["suggested_interview_questions"] == [
        (
            "Can you explain how you used Java in this work example: "
            "Built REST APIs using Java and Spring Boot?"
        ),
        (
            "Can you explain how you used SQL via MySQL in this work example: "
            "Designed MySQL database schemas?"
        ),
        "How would you handle Kafka in this role?",
        "Do you have production experience with AWS?",
    ]


def test_format_review_card_markdown_returns_readable_sections() -> None:
    card = generate_review_card(
        _sample_candidate_result(),
        {"job_title": "Backend Java Developer"},
    )

    markdown = format_review_card_markdown(card)

    assert markdown.startswith("# Nguyen Van A")
    assert "Role: Backend Java Developer" in markdown
    assert "Score: 87/100" in markdown
    assert "Recommendation: Strong Review" in markdown
    assert "## Score Breakdown" in markdown
    assert "- Skill semantic: 0.95" in markdown
    assert "## Evidence Highlights" in markdown
    assert (
        "- SQL via MySQL (level 3, work_experience): "
        "Designed MySQL database schemas."
    ) in markdown
    assert "## Suggested Interview Questions" in markdown
    assert (
        "1. Can you explain how you used Java in this work example: "
        "Built REST APIs using Java and Spring Boot?"
    ) in markdown


def test_demo_pipeline_generates_explainable_review_card() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))
    criteria = parse_jd(load_text_file("data/jobs/jd_backend_java.txt"))

    candidate_skills = normalize_skills(profile["raw_skills"], taxonomy)
    required_skills = normalize_skills(criteria["must_have_skills"], taxonomy)
    nice_to_have_skills = normalize_skills(criteria["nice_to_have_skills"], taxonomy)
    matches = detect_all_evidence(
        match_skills(required_skills, candidate_skills, taxonomy),
        profile,
    )
    nice_to_have_matches = match_skills(
        nice_to_have_skills,
        candidate_skills,
        taxonomy,
    )
    scored_candidate = score_candidate(
        criteria,
        profile,
        matches,
        nice_to_have_matches,
    )

    card = generate_review_card(scored_candidate, criteria)

    assert card["candidate_name"] == "Nguyen Van A"
    assert card["job_title"] == "Backend Java Developer"
    assert card["final_score"] == 87
    assert card["recommendation"] == "Strong Review"
    assert len(card["evidence_highlights"]) == 5
    assert card["concerns"] == ["Optional nice-to-have gaps: AWS and Kafka."]
    assert card["strengths"][-1] == (
        "Clear evidence for Java, Spring Boot, REST API, SQL via MySQL, and Docker."
    )
    assert card["suggested_interview_questions"] == [
        (
            "Can you explain how you used Java in this work example: "
            "Built REST APIs using Java and Spring Boot?"
        ),
        (
            "Can you explain how you used SQL via MySQL in this work example: "
            "Designed MySQL database schemas for product and order modules?"
        ),
        (
            "Can you explain how you used Docker in this work example: "
            "Used Docker Compose for local development and testing?"
        ),
        "Do you have production experience with AWS?",
        "Do you have production experience with Kafka?",
    ]


def _sample_candidate_result() -> dict:
    return {
        "candidate_name": "Nguyen Van A",
        "final_score": 87,
        "recommendation": "Strong Review",
        "scores": {
            "skill_semantic": 0.95,
            "evidence": 1.0,
            "experience": 0.5,
            "seniority": 1.0,
            "domain": 1.0,
            "nice_to_have": 0.3333,
        },
        "matched_skills": [
            {
                "required_skill": "Java",
                "candidate_skill": "Java",
                "match_type": "exact_match",
                "score": 1.0,
                "evidence_level": 3,
                "evidence_text": "Built REST APIs using Java and Spring Boot.",
                "evidence_source": "work_experience",
            },
            {
                "required_skill": "SQL",
                "candidate_skill": "MySQL",
                "match_type": "related_match",
                "score": 0.75,
                "evidence_level": 3,
                "evidence_text": "Designed MySQL database schemas.",
                "evidence_source": "work_experience",
            },
        ],
        "missing_skills": ["Kafka"],
        "nice_to_have_matches": [
            {
                "required_skill": "AWS",
                "candidate_skill": None,
                "match_type": "no_match",
                "score": 0.0,
            }
        ],
        "seniority": "Junior",
        "experience_years": 0.58,
        "domain": ["Backend", "Web Application"],
    }
