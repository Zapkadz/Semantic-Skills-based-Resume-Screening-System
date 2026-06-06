import pytest

from src.document_loader import load_text_file
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.semantic_matcher import get_missing_skills, match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_match_skills_returns_exact_match() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["Java"], ["Java", "Docker"], taxonomy)

    assert matches == [
        {
            "required_skill": "Java",
            "candidate_skill": "Java",
            "match_type": "exact_match",
            "score": 1.0,
        }
    ]


def test_match_skills_treats_alias_as_canonical_exact_match() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["SpringBoot"], ["Spring Framework"], taxonomy)

    assert matches == [
        {
            "required_skill": "Spring Boot",
            "candidate_skill": "Spring Boot",
            "match_type": "exact_match",
            "score": 1.0,
        }
    ]


def test_match_skills_returns_related_match() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["SQL"], ["MySQL"], taxonomy)

    assert matches == [
        {
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "score": 0.75,
        }
    ]


def test_match_skills_returns_transferable_match() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["Spring Boot"], ["ASP.NET Core"], taxonomy)

    assert matches == [
        {
            "required_skill": "Spring Boot",
            "candidate_skill": "ASP.NET Core",
            "match_type": "transferable_match",
            "score": 0.55,
        }
    ]


def test_match_skills_returns_no_match() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["Kafka"], ["React"], taxonomy)

    assert matches == [
        {
            "required_skill": "Kafka",
            "candidate_skill": None,
            "match_type": "no_match",
            "score": 0.0,
        }
    ]


def test_match_skills_prioritizes_exact_over_related() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["REST API"], ["Spring Boot", "REST API"], taxonomy)

    assert matches[0]["candidate_skill"] == "REST API"
    assert matches[0]["match_type"] == "exact_match"
    assert matches[0]["score"] == 1.0


def test_get_missing_skills_returns_no_match_required_skills() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    matches = match_skills(["Java", "Kafka"], ["Java", "React"], taxonomy)

    assert get_missing_skills(matches) == ["Kafka"]


def test_match_skills_removes_duplicate_inputs_after_canonicalization() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    matches = match_skills(["JS", "JavaScript"], ["ECMAScript"], taxonomy)

    assert matches == [
        {
            "required_skill": "JavaScript",
            "candidate_skill": "JavaScript",
            "match_type": "exact_match",
            "score": 1.0,
        }
    ]


def test_match_skills_rejects_non_string_input() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    with pytest.raises(TypeError, match="Skill must be a string"):
        match_skills(["Java"], [123], taxonomy)  # type: ignore[list-item]


def test_demo_resume_matches_demo_jd_must_have_skills() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))
    criteria = parse_jd(load_text_file("data/jobs/jd_backend_java.txt"))

    candidate_skills = normalize_skills(profile["raw_skills"], taxonomy)
    required_skills = normalize_skills(criteria["must_have_skills"], taxonomy)
    matches = match_skills(required_skills, candidate_skills, taxonomy)

    assert matches == [
        {
            "required_skill": "Java",
            "candidate_skill": "Java",
            "match_type": "exact_match",
            "score": 1.0,
        },
        {
            "required_skill": "Spring Boot",
            "candidate_skill": "Spring Boot",
            "match_type": "exact_match",
            "score": 1.0,
        },
        {
            "required_skill": "REST API",
            "candidate_skill": "REST API",
            "match_type": "exact_match",
            "score": 1.0,
        },
        {
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "score": 0.75,
        },
        {
            "required_skill": "Docker",
            "candidate_skill": "Docker",
            "match_type": "exact_match",
            "score": 1.0,
        },
    ]
    assert get_missing_skills(matches) == []
