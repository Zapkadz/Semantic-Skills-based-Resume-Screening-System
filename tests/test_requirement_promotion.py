from src.jd_parser import parse_jd
from src.jd_requirement_classifier import enrich_job_criteria_with_requirement_metadata
from src.requirement_promotion import (
    EXPLICIT_REQUIREMENT_SOURCE,
    PROMOTED_RESPONSIBILITY_SOURCE,
    build_explicit_technical_recovery_summary,
    build_promoted_requirements,
    build_scoring_requirement_entries,
    build_scoring_requirement_lines_from_entries,
)


def test_requirement_promotion_promotes_sparse_technical_responsibilities() -> None:
    jd_text = (
        "IT Staff / IT Support / IT Helpdesk\n"
        "\n"
        "Requirements\n"
        "- At least 3 years experience working in IT.\n"
        "- Good at writing and speaking English.\n"
        "\n"
        "Responsibilities\n"
        "- Manage Active Directory and troubleshoot DNS/DHCP issues.\n"
        "- Support firewall, router, switch, VPN, and Google Workspace incidents.\n"
    )
    job_criteria = enrich_job_criteria_with_requirement_metadata(
        parse_jd(jd_text),
        jd_text,
        taxonomy={},
    )

    promoted = build_promoted_requirements(job_criteria)
    must_have_lines, nice_to_have_lines = build_scoring_requirement_lines_from_entries(
        build_scoring_requirement_entries(job_criteria)
    )

    assert [item["text"] for item in promoted] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
    ]
    assert all(
        item["source_kind"] == PROMOTED_RESPONSIBILITY_SOURCE for item in promoted
    )
    assert must_have_lines == ["Active Directory", "DNS", "DHCP", "Firewall"]
    assert nice_to_have_lines == []


def test_requirement_promotion_does_not_fire_when_explicit_technical_requirements_exist() -> None:
    jd_text = (
        "Backend Developer\n"
        "\n"
        "Requirements\n"
        "- Java\n"
        "- Spring Boot\n"
        "\n"
        "Responsibilities\n"
        "- Build REST APIs and maintain SQL services.\n"
    )
    job_criteria = enrich_job_criteria_with_requirement_metadata(
        parse_jd(jd_text),
        jd_text,
        taxonomy={},
    )

    promoted = build_promoted_requirements(job_criteria)
    scoring_entries = build_scoring_requirement_entries(job_criteria)

    assert promoted == []
    assert [item["text"] for item in scoring_entries] == ["Java", "Spring Boot"]
    assert all(
        item["source_kind"] == EXPLICIT_REQUIREMENT_SOURCE
        for item in scoring_entries
    )


def test_requirement_promotion_recovers_when_explicit_technical_is_only_generic_noise() -> None:
    jd_text = (
        "IT Staff / IT Support / IT Helpdesk\n"
        "\n"
        "Requirements\n"
        "- Knowledge of IT systems.\n"
        "- Good at writing and speaking English.\n"
        "- Enthusiastic and eager to learn.\n"
        "\n"
        "Responsibilities\n"
        "- Manage Active Directory and troubleshoot DNS/DHCP issues.\n"
        "- Support firewall, router, switch, VPN, and Google Workspace incidents.\n"
    )
    job_criteria = enrich_job_criteria_with_requirement_metadata(
        parse_jd(jd_text),
        jd_text,
        taxonomy={},
    )

    summary = build_explicit_technical_recovery_summary(job_criteria)
    promoted = build_promoted_requirements(job_criteria)

    assert summary == {
        "raw_explicit_technical_count": 1,
        "usable_explicit_technical_count": 0,
        "explicit_technical_contamination_count": 1,
        "usable_explicit_technical_lines": [],
        "contaminated_explicit_technical_lines": ["Knowledge of IT systems."],
        "supported_high_specificity_signal_count": 2,
        "technical_responsibility_candidate_count": 8,
        "recovery_triggered": True,
        "recovery_reason": "explicit_technical_contamination_detected",
    }
    assert [item["text"] for item in promoted] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
    ]
