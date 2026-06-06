import pytest

from src.document_loader import load_text_file
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.skill_normalizer import normalize_skill, normalize_skills
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_normalize_skill_maps_alias_to_canonical_skill() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    assert normalize_skill("SpringBoot", taxonomy) == "Spring Boot"
    assert normalize_skill("Postgres", taxonomy) == "PostgreSQL"
    assert normalize_skill("JS", taxonomy) == "JavaScript"
    assert normalize_skill("Basic Docker", taxonomy) == "Docker"


def test_normalize_skill_is_case_insensitive_and_trims_whitespace() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    assert normalize_skill("  springboot  ", taxonomy) == "Spring Boot"
    assert normalize_skill(" reactjs ", taxonomy) == "React"


def test_normalize_skill_keeps_unknown_skill_text() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    assert normalize_skill("Legacy ERP", taxonomy) == "Legacy ERP"


def test_normalize_skill_rejects_non_string_input() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    with pytest.raises(TypeError, match="Skill must be a string"):
        normalize_skill(123, taxonomy)  # type: ignore[arg-type]


def test_normalize_skills_removes_duplicates_after_normalization() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    normalized = normalize_skills(
        ["JS", "ReactJS", "Postgres", "React.js", "", "  ", "Legacy ERP"],
        taxonomy,
    )

    assert normalized == ["JavaScript", "React", "PostgreSQL", "Legacy ERP"]


def test_normalize_resume_parser_output() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))

    normalized = normalize_skills(profile["raw_skills"], taxonomy)

    assert normalized == ["Java", "Spring Boot", "REST API", "MySQL", "Docker"]


def test_normalize_jd_parser_output() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    criteria = parse_jd(load_text_file("data/jobs/jd_backend_java.txt"))

    normalized_must_have = normalize_skills(criteria["must_have_skills"], taxonomy)
    normalized_nice_to_have = normalize_skills(
        criteria["nice_to_have_skills"],
        taxonomy,
    )

    assert normalized_must_have == ["Java", "Spring Boot", "REST API", "SQL", "Docker"]
    assert normalized_nice_to_have == ["AWS", "Kafka", "Kubernetes"]
