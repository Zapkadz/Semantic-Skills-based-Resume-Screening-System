from src.document_loader import load_text_file
from src.evidence_detector import detect_all_evidence
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.scorer import (
    calculate_evidence_score,
    calculate_experience_score,
    calculate_final_score,
    calculate_hard_skill_gate_metrics,
    calculate_nice_to_have_score,
    calculate_skill_semantic_score,
    detect_candidate_domains,
    detect_candidate_seniority,
    estimate_experience_years,
    get_recommendation_label,
    rank_candidates,
    score_candidate,
)
from src.semantic_matcher import match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_calculate_skill_semantic_score_averages_match_scores() -> None:
    matches = [
        {"score": 1.0},
        {"score": 0.75},
        {"score": 0.0},
    ]

    assert calculate_skill_semantic_score(matches) == 0.5833


def test_calculate_evidence_score_maps_levels_to_strengths() -> None:
    matches = [
        {"evidence_level": 3},
        {"evidence_level": 2},
        {"evidence_level": 1},
        {"evidence_level": 0},
    ]

    assert calculate_evidence_score(matches) == 0.525


def test_calculate_experience_score_uses_requirement_bands() -> None:
    assert calculate_experience_score(3, 3) == 1.0
    assert calculate_experience_score(2.25, 3) == 0.75
    assert calculate_experience_score(1.5, 3) == 0.5
    assert calculate_experience_score(1.0, 3) == 0.25
    assert calculate_experience_score(0, 0) == 1.0


def test_calculate_nice_to_have_score_counts_non_missing_matches() -> None:
    nice_to_have_matches = [
        {"match_type": "no_match"},
        {"match_type": "related_match"},
        {"match_type": "exact_match"},
    ]

    assert calculate_nice_to_have_score(nice_to_have_matches) == 0.6667
    assert calculate_nice_to_have_score([]) == 0.5
    assert calculate_nice_to_have_score(None) == 0.5


def test_calculate_final_score_applies_phase_weights() -> None:
    scores = {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.5,
        "seniority": 1.0,
        "domain": 1.0,
        "nice_to_have": 0.3333,
    }

    assert calculate_final_score(scores) == 87


def test_get_recommendation_label_uses_thresholds() -> None:
    assert get_recommendation_label(85) == "Strong Review"
    assert get_recommendation_label(70) == "Review"
    assert get_recommendation_label(55) == "Maybe Review"
    assert get_recommendation_label(40) == "Low Priority"
    assert get_recommendation_label(39) == "Not Enough Evidence"


def test_estimate_experience_years_from_demo_resume_duration() -> None:
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))

    assert round(estimate_experience_years(profile), 2) == 0.58


def test_estimate_experience_years_handles_vietnamese_present_duration() -> None:
    profile = {
        "work_experience": [
            {"duration": "07/2018 - 12/2020"},
            {"duration": "01/2021 – Hiện tại"},
        ]
    }

    assert estimate_experience_years(profile) >= 5


def test_estimate_experience_years_uses_summary_years_as_fallback() -> None:
    profile = {
        "headline": "IT Security & Governance Officer",
        "summary": "IT Security professional with over 5 years of experience.",
        "work_experience": [{"duration": ""}],
    }

    assert estimate_experience_years(profile) == 5


def test_detect_candidate_seniority_and_domains_from_demo_resume() -> None:
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))

    assert detect_candidate_seniority(profile) == "Junior"
    assert detect_candidate_domains(profile) == ["Backend", "Web Application"]


def test_detect_candidate_domains_detects_security_grc_without_service_false_positive() -> None:
    profile = {
        "headline": "Senior IT Security & Governance Officer",
        "summary": (
            "Experienced in banking and financial services with vulnerability "
            "management, access governance, compliance, personal data protection, "
            "and IT risk management."
        ),
        "raw_skills": [
            "Qualys",
            "Vulnerability Management",
            "Access Management",
            "IT Governance",
            "Compliance Management",
        ],
        "work_experience": [],
        "projects": [],
    }

    assert detect_candidate_domains(profile) == ["IT Security/GRC"]


def test_score_candidate_returns_explainable_demo_result() -> None:
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

    result = score_candidate(criteria, profile, matches, nice_to_have_matches)

    assert result["candidate_name"] == "Nguyen Van A"
    assert result["final_score"] == 87
    assert result["recommendation"] == "Strong Review"
    assert result["base_score"] == 87
    assert result["hard_skill_gate"]["passed"] is True
    assert result["hard_skill_gate"]["applied"] is False
    assert result["scores"] == {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.5,
        "seniority": 1.0,
        "domain": 1.0,
        "nice_to_have": 0.3333,
    }
    assert result["missing_skills"] == []
    assert result["experience_years"] == 0.58
    assert result["seniority"] == "Junior"
    assert result["domain"] == ["Backend", "Web Application"]


def test_score_candidate_returns_missing_skills_and_low_recommendation() -> None:
    criteria = {
        "minimum_experience_years": 2,
        "seniority": "Middle",
        "domain": ["Backend"],
    }
    profile = {
        "candidate_name": "Le Van C",
        "headline": "Frontend Developer",
        "summary": "",
        "raw_skills": ["React"],
        "work_experience": [],
        "projects": [],
    }
    matches = [
        {
            "required_skill": "Java",
            "candidate_skill": None,
            "match_type": "no_match",
            "score": 0.0,
            "evidence_level": 0,
        }
    ]

    result = score_candidate(criteria, profile, matches, [])

    assert result["final_score"] == 18
    assert result["recommendation"] == "Not Enough Evidence"
    assert result["missing_skills"] == ["Java"]
    assert result["hard_skill_gate"]["applied"] is False


def test_hard_skill_gate_metrics_separate_confirmed_weak_and_missing() -> None:
    matches = [
        {
            "required_skill": "Python",
            "candidate_skill": "Python",
            "match_type": "exact_match",
            "score": 1.0,
            "evidence_level": 1,
        },
        {
            "required_skill": "Face Alignment",
            "candidate_skill": "Face Matching",
            "match_type": "semantic_match",
            "score": 0.85,
            "evidence_level": 3,
        },
        {
            "required_skill": "ONNX",
            "candidate_skill": None,
            "match_type": "no_semantic_evidence",
            "score": 0.0,
            "evidence_level": 0,
        },
    ]

    assert calculate_hard_skill_gate_metrics(matches) == {
        "total_must_have": 3,
        "positive_match_count": 2,
        "confirmed_match_count": 1,
        "weak_match_count": 1,
        "missing_count": 1,
        "positive_coverage": 0.6667,
        "confirmed_coverage": 0.3333,
        "weak_match_ratio": 0.5,
    }


def test_score_candidate_caps_review_when_hard_skill_evidence_is_incomplete() -> None:
    criteria = {
        "minimum_experience_years": 3,
        "seniority": "Middle",
        "domain": ["Computer Vision"],
    }
    profile = {
        "candidate_name": "Senior CV Candidate",
        "headline": "Senior Computer Vision Engineer",
        "summary": (
            "Senior Computer Vision Engineer with over 6 years of experience "
            "in biometric authentication and mobile AI deployment."
        ),
        "raw_skills": ["Python"],
        "work_experience": [],
        "projects": [],
    }
    matches = [
        {
            "required_skill": "Python",
            "candidate_skill": "Python",
            "match_type": "exact_match",
            "score": 1.0,
            "evidence_level": 1,
        },
        {
            "required_skill": "Mobile AI",
            "candidate_skill": "Mobile AI",
            "match_type": "exact_match",
            "score": 1.0,
            "evidence_level": 1,
        },
        {
            "required_skill": "ONNX",
            "candidate_skill": "Mobile AI",
            "match_type": "related_match",
            "score": 0.75,
            "evidence_level": 1,
        },
        {
            "required_skill": "Model Optimization",
            "candidate_skill": None,
            "match_type": "no_semantic_evidence",
            "score": 0.0,
            "evidence_level": 0,
        },
    ]

    result = score_candidate(criteria, profile, matches, [])

    assert result["base_score"] == 70
    assert result["final_score"] == 69
    assert result["recommendation"] == "Maybe Review"
    assert result["hard_skill_gate"]["applied"] is True
    assert result["hard_skill_gate"]["score_cap"] == 69
    assert result["hard_skill_gate"]["metrics"]["confirmed_coverage"] == 0.0
    assert [
        reason["code"] for reason in result["hard_skill_gate"]["reasons"]
    ] == ["weak_evidence", "low_confirmed_coverage"]


def test_rank_candidates_sorts_by_score_evidence_then_name() -> None:
    results = [
        {
            "candidate_name": "Tran B",
            "final_score": 75,
            "scores": {"evidence": 0.8},
        },
        {
            "candidate_name": "Nguyen A",
            "final_score": 91,
            "scores": {"evidence": 0.7},
        },
        {
            "candidate_name": "Le C",
            "final_score": 75,
            "scores": {"evidence": 0.9},
        },
        {
            "candidate_name": "Do D",
            "final_score": 75,
            "scores": {"evidence": 0.9},
        },
    ]

    ranked_results = rank_candidates(results)

    assert [
        (result["rank"], result["candidate_name"])
        for result in ranked_results
    ] == [
        (1, "Nguyen A"),
        (2, "Do D"),
        (3, "Le C"),
        (4, "Tran B"),
    ]
