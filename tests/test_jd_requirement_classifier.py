from src.jd_parser import parse_jd
from src.jd_requirement_classifier import (
    build_scoring_requirement_lines,
    classify_jd_requirements,
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
    assert groups["domain_context"] == [
        "Co kinh nghiem lam viec trong linh vuc tai chinh ngan hang."
    ]
    assert groups["ignored"] == []


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
