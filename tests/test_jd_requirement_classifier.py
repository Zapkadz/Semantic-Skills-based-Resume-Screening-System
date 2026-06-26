from src.jd_parser import parse_jd
from src.jd_requirement_classifier import (
    build_scoring_requirement_lines,
    build_typed_requirements,
    classify_jd_requirements,
    enrich_job_criteria_with_requirement_metadata,
)
from src.requirement_types import (
    DOMAIN_CONTEXT,
    EDUCATION_REQUIREMENT,
    EXPERIENCE_REQUIREMENT,
    LANGUAGE_REQUIREMENT,
    RESPONSIBILITY_CONTEXT,
    SOFT_SKILL,
    TECH_SKILL,
    TOOL_PLATFORM,
)


def test_classify_jd_requirements_splits_required_preferred_and_soft_groups() -> None:
    jd_text = (
        "Fullstack Developer (Java / Spring Boot / Angular)\n"
        "\n"
        "Mo ta cong viec\n"
        "- Thuc hien lap trinh phat trien API.\n"
        "\n"
        "Yeu cau cong viec\n"
        "Dieu kien bat buoc:\n"
        "- Tot nghiep Dai hoc nganh CNTT, Toan tin hoac tuong duong.\n"
        "- Thanh thao Java, Spring Boot, Angular, Javascript.\n"
        "- Thanh thao co so du lieu Oracle.\n"
        "- Co kien thuc ve Monolithic, Micro-service, OOP.\n"
        "- Co hieu biet co ban ve DevOps, CI/CD.\n"
        "- Toi thieu 02 nam kinh nghiem phat trien ung dung.\n"
        "- Kha nang lam viec theo nhom, giao tiep, trinh bay.\n"
        "- Nhiet tinh, dam me hoc hoi, chiu duoc ap luc.\n"
        "- Written English for cross-team coordination.\n"
        "\n"
        "Dieu kien uu tien:\n"
        "- Thanh thao Java, Spring Boot, Angular, Strust, Jsp, Ajax, Jquery, HTML, CSS.\n"
        "- Thanh thao ngon ngu lap trinh .NET, C#, ASP .NET, Web-form.\n"
        "- Co hieu biet co ban ve Cloud.\n"
        "- Co kinh nghiem su dung Git, GitLab, Docker container.\n"
        "- Co kinh nghiem lam viec trong linh vuc tai chinh ngan hang.\n"
    )
    criteria = parse_jd(jd_text)

    groups = classify_jd_requirements(criteria, jd_text, taxonomy={})
    must_have, nice_to_have = build_scoring_requirement_lines(groups)

    assert criteria["nice_to_have_skills"] == [
        "Thanh thao Java, Spring Boot, Angular, Strust, Jsp, Ajax, Jquery, HTML, CSS.",
        "Thanh thao ngon ngu lap trinh .NET, C#, ASP .NET, Web-form.",
        "Co hieu biet co ban ve Cloud.",
        "Co kinh nghiem su dung Git, GitLab, Docker container.",
        "Co kinh nghiem lam viec trong linh vuc tai chinh ngan hang.",
    ]
    assert must_have == [
        "Thanh thao Java, Spring Boot, Angular, Javascript.",
        "Thanh thao co so du lieu Oracle.",
        "Co kien thuc ve Monolithic, Micro-service, OOP.",
        "Co hieu biet co ban ve DevOps, CI/CD.",
    ]
    assert nice_to_have == [
        "Thanh thao Java, Spring Boot, Angular, Strust, Jsp, Ajax, Jquery, HTML, CSS.",
        "Thanh thao ngon ngu lap trinh .NET, C#, ASP .NET, Web-form.",
        "Co hieu biet co ban ve Cloud.",
        "Co kinh nghiem su dung Git, GitLab, Docker container.",
    ]
    assert groups["education"] == [
        "Tot nghiep Dai hoc nganh CNTT, Toan tin hoac tuong duong."
    ]
    assert groups["experience"] == [
        "Toi thieu 02 nam kinh nghiem phat trien ung dung."
    ]
    assert groups["soft_skills"] == [
        "Kha nang lam viec theo nhom, giao tiep, trinh bay.",
        "Nhiet tinh, dam me hoc hoi, chiu duoc ap luc.",
    ]
    assert groups["language"] == ["Written English for cross-team coordination."]
    assert groups["domain_context"] == [
        "Co kinh nghiem lam viec trong linh vuc tai chinh ngan hang."
    ]
    assert groups["ignored"] == []

    typed_requirements = build_typed_requirements(criteria, jd_text, taxonomy={})
    typed_by_text = {
        requirement["text"]: requirement["type"] for requirement in typed_requirements
    }
    assert typed_by_text["Tot nghiep Dai hoc nganh CNTT, Toan tin hoac tuong duong."] == (
        EDUCATION_REQUIREMENT
    )
    assert typed_by_text["Toi thieu 02 nam kinh nghiem phat trien ung dung."] == (
        EXPERIENCE_REQUIREMENT
    )
    assert typed_by_text["Kha nang lam viec theo nhom, giao tiep, trinh bay."] == (
        SOFT_SKILL
    )
    assert typed_by_text["Written English for cross-team coordination."] == (
        LANGUAGE_REQUIREMENT
    )
    assert typed_by_text["Co kinh nghiem lam viec trong linh vuc tai chinh ngan hang."] == (
        DOMAIN_CONTEXT
    )
    assert typed_by_text["Thanh thao co so du lieu Oracle."] == TOOL_PLATFORM
    assert typed_by_text["Thanh thao Java, Spring Boot, Angular, Javascript."] in {
        TECH_SKILL,
        TOOL_PLATFORM,
    }


def test_classify_jd_requirements_keeps_required_certifications_scored() -> None:
    criteria = {
        "must_have_skills": [
            "Security+ certification",
            "Relevant certifications: CEH or ISO 27001 are an advantage.",
        ],
        "nice_to_have_skills": [],
        "responsibilities": [],
    }

    groups = classify_jd_requirements(criteria, "", taxonomy={})
    must_have, nice_to_have = build_scoring_requirement_lines(groups)

    assert groups["certifications"] == ["Security+ certification"]
    assert must_have == ["Security+ certification"]
    assert nice_to_have == [
        "Relevant certifications: CEH or ISO 27001 are an advantage."
    ]


def test_build_typed_requirements_marks_description_and_responsibilities_as_context() -> None:
    jd_text = (
        "Senior AI Computer Vision Engineer\n"
        "\n"
        "Job Description\n"
        "- Design and deploy computer vision models.\n"
        "\n"
        "Responsibilities\n"
        "- Collaborate with backend teams.\n"
        "\n"
        "Requirements\n"
        "- Python\n"
    )
    criteria = parse_jd(jd_text)

    typed_requirements = build_typed_requirements(criteria, jd_text, taxonomy={})
    typed_by_text = {
        requirement["text"]: requirement["type"] for requirement in typed_requirements
    }

    assert typed_by_text["Design and deploy computer vision models."] == RESPONSIBILITY_CONTEXT
    assert typed_by_text["Collaborate with backend teams."] == RESPONSIBILITY_CONTEXT


def test_enrich_job_criteria_adds_responsibility_signal_metadata() -> None:
    jd_text = (
        "IT Support Engineer\n"
        "\n"
        "Responsibilities\n"
        "- Manage Active Directory and troubleshoot DNS/DHCP issues.\n"
        "- Collaborate with internal teams.\n"
    )
    criteria = parse_jd(jd_text)

    enriched = enrich_job_criteria_with_requirement_metadata(criteria, jd_text, taxonomy={})

    assert enriched["technical_responsibility_candidates"] == [
        "Active Directory",
        "DNS",
        "DHCP",
    ]
    assert [item["text"] for item in enriched["promoted_requirements"]] == [
        "Active Directory",
        "DNS",
        "DHCP",
    ]
    assert [signal["signal_type"] for signal in enriched["responsibility_signals"]] == [
        "TECHNICAL_TASK",
        "OPERATIONAL_TASK",
    ]


def test_classify_jd_requirements_keeps_english_soft_skills_out_of_technical_bucket() -> None:
    jd_text = (
        "IT Staff / IT Support / IT Helpdesk\n"
        "\n"
        "Requirements\n"
        "- Good at writing & speaking English to work with oversea team.\n"
        "- Enthusiastic and eager to learn.\n"
        "\n"
        "Responsibilities\n"
        "- Manage Active Directory and troubleshoot DNS/DHCP issues.\n"
    )
    criteria = parse_jd(jd_text)

    enriched = enrich_job_criteria_with_requirement_metadata(criteria, jd_text, taxonomy={})
    groups = enriched["requirement_groups"]

    assert groups["must_have_technical"] == []
    assert groups["soft_skills"] == ["Enthusiastic and eager to learn."]
    assert groups["language"] == [
        "Good at writing & speaking English to work with oversea team."
    ]
    assert enriched["explicit_technical_recovery_summary"] == {
        "raw_explicit_technical_count": 0,
        "usable_explicit_technical_count": 0,
        "explicit_technical_contamination_count": 0,
        "usable_explicit_technical_lines": [],
        "contaminated_explicit_technical_lines": [],
        "supported_high_specificity_signal_count": 1,
        "technical_responsibility_candidate_count": 3,
        "recovery_triggered": True,
        "recovery_reason": "sparse_explicit_technical_requirements",
    }
