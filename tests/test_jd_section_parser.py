from src.jd_section_parser import parse_jd_sections


def test_parse_jd_sections_splits_title_description_requirements_and_benefits() -> None:
    sections = parse_jd_sections(
        "Backend Developer\n"
        "\n"
        "Job Description\n"
        "- Build REST APIs.\n"
        "\n"
        "Requirements\n"
        "- Java\n"
        "- Spring Boot\n"
        "\n"
        "Nice to have\n"
        "- AWS\n"
        "\n"
        "Benefits\n"
        "- Laptop support"
    )

    assert sections == {
        "title": "Backend Developer",
        "intro": [],
        "description": ["Build REST APIs."],
        "requirements": ["Java", "Spring Boot"],
        "qualifications": [],
        "responsibilities": [],
        "nice_to_have": ["AWS"],
        "benefits": ["Laptop support"],
    }


def test_parse_jd_sections_supports_vietnamese_and_qualification_headings() -> None:
    sections = parse_jd_sections(
        "IT Security Officer\n"
        "\n"
        "Mo ta cong viec\n"
        "- Quan ly he thong bao mat.\n"
        "\n"
        "Qualifications & Experience\n"
        "- Linux\n"
        "- 3+ years of experience\n"
        "\n"
        "Yeu cau ung vien\n"
        "- Qualys\n"
        "\n"
        "Dieu kien uu tien\n"
        "- CEH"
    )

    assert sections["title"] == "IT Security Officer"
    assert sections["description"] == ["Quan ly he thong bao mat."]
    assert sections["qualifications"] == ["Linux", "3+ years of experience"]
    assert sections["requirements"] == ["Qualys"]
    assert sections["nice_to_have"] == ["CEH"]
