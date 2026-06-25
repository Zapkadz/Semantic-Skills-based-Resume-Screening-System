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


def test_generate_review_card_flags_semantic_only_unknown_requirements() -> None:
    candidate_result = _sample_candidate_result()
    candidate_result["matched_skills"].append(
        {
            "required_skill": "carbon footprint analysis",
            "candidate_skill": None,
            "match_type": "semantic_only_match",
            "taxonomy_status": "unknown",
            "score": 0.65,
            "similarity": 0.8421,
            "evidence_level": 3,
            "evidence_text": "Built carbon emission reports for ESG audits.",
            "evidence_source": "projects",
        }
    )

    card = generate_review_card(candidate_result, {"job_title": "ESG Analyst"})

    assert (
        "Some requirements were evaluated with semantic-only evidence outside "
        "the taxonomy: carbon footprint analysis."
    ) in card["concerns"]
    assert any(
        highlight["match_type"] == "semantic_only_match"
        for highlight in card["evidence_highlights"]
    )


def test_generate_review_card_flags_experience_met_but_hard_skill_evidence_incomplete() -> None:
    candidate_result = _sample_candidate_result()
    candidate_result["scores"] = {
        "skill_semantic": 0.68,
        "evidence": 0.45,
        "experience": 1.0,
        "seniority": 0.85,
        "domain": 1.0,
        "nice_to_have": 0.5,
    }
    candidate_result["missing_skills"] = [
        "ONNX",
        "model optimization under resource constraints",
    ]

    card = generate_review_card(candidate_result, {"job_title": "Computer Vision Engineer"})

    assert card["concerns"][0] == (
        "The candidate appears to meet the experience requirement, "
        "but hard-skill evidence is incomplete; review missing and "
        "weakly evidenced must-have skills before shortlisting."
    )
    assert card["concerns"][1] == (
        "Missing must-have skills: ONNX and model optimization under resource constraints."
    )


def test_generate_review_card_explains_hard_skill_gate_score_cap() -> None:
    candidate_result = _sample_candidate_result()
    candidate_result["base_score"] = 72
    candidate_result["final_score"] = 69
    candidate_result["recommendation"] = "Maybe Review"
    candidate_result["hard_skill_gate"] = {
        "passed": False,
        "applied": True,
        "score_cap": 69,
        "base_score": 72,
        "final_score": 69,
        "reasons": [
            {
                "code": "weak_evidence",
                "message": "Evidence strength is below the Review threshold.",
            }
        ],
        "metrics": {
            "confirmed_coverage": 0.3125,
        },
    }

    card = generate_review_card(candidate_result, {"job_title": "Computer Vision Engineer"})

    assert card["summary"] == (
        "Nguyen Van A is a Maybe Review candidate for Computer Vision Engineer "
        "with a final score of 69/100. The hard-skill gate capped the base "
        "score from 72/100 because must-have skill evidence is incomplete."
    )
    assert card["concerns"][0] == (
        "Hard-skill gate applied: the base score was capped from 72/100 "
        "to 69/100. Evidence strength is below the Review threshold."
    )
    assert card["hard_skill_gate"]["applied"] is True


def test_generate_review_card_explains_role_aware_calibration() -> None:
    candidate_result = _sample_candidate_result()
    candidate_result["raw_base_score"] = 76
    candidate_result["role_calibrated_score"] = 70
    candidate_result["base_score"] = 70
    candidate_result["final_score"] = 70
    candidate_result["recommendation"] = "Review"
    candidate_result["role_score_adjustment"] = -6
    candidate_result["role_family_alignment"] = {
        "status": "partial_alignment",
        "note": "The candidate shows adjacent role-family overlap, but not as the primary profile.",
    }
    candidate_result["role_alignment_impact"] = {
        "applied": True,
        "adjustment": -6,
        "reason": (
            "The profile overlaps with an adjacent role family, but most core "
            "requirements are still semantic-only or weakly confirmed."
        ),
    }
    candidate_result["core_requirement_fit_summary"] = {
        "core": {
            "total": 3,
            "confirmed_coverage": 0.3333,
        }
    }

    card = generate_review_card(candidate_result, {"job_title": "AI Computer Vision Engineer"})

    assert card["summary"] == (
        "Nguyen Van A is a Review candidate for AI Computer Vision Engineer "
        "with a final score of 70/100. Role-aware calibration adjusted the "
        "weighted score from 76/100 to 70/100 because the profile overlaps "
        "with an adjacent role family, but most core requirements are still "
        "semantic-only or weakly confirmed."
    )
    assert "Core technical requirements are still missing or weakly evidenced." in card["concerns"]
    assert (
        "Role-aware calibration reduced the score: The profile overlaps with an adjacent role family, but most core requirements are still semantic-only or weakly confirmed."
        in card["concerns"]
    )


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
