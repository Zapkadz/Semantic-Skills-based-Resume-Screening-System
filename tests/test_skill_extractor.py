from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_extract_taxonomy_skills_from_vietnamese_text() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    skills = extract_taxonomy_skills_from_text(
        (
            "Xây dựng hệ thống nhận diện khuôn mặt và chống giả mạo "
            "trong quy trình eKYC bằng PyTorch."
        ),
        taxonomy,
    )

    assert "Face Recognition" in skills
    assert "Anti-Spoofing" in skills
    assert "eKYC" in skills
    assert "PyTorch" in skills


def test_extract_taxonomy_skills_repairs_mojibake_text() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    text = "nhận diện khuôn mặt".encode("utf-8").decode("cp1252")

    skills = extract_taxonomy_skills_from_text(text, taxonomy)

    assert skills == ["Face Recognition"]


def test_extract_taxonomy_skills_avoids_lowercase_acronym_false_positive() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    skills = extract_taxonomy_skills_from_text(
        "This CV was updated far from the production environment.",
        taxonomy,
    )

    assert "FAR" not in skills
    assert "Computer Vision" not in skills


def test_merge_skill_lists_deduplicates_accent_insensitive_aliases() -> None:
    merged = merge_skill_lists(
        ["Nhận diện khuôn mặt", "Python"],
        ["nhan dien khuon mat", "PyTorch"],
    )

    assert merged == ["Nhận diện khuôn mặt", "Python", "PyTorch"]
