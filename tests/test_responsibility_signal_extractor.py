from src.jd_parser import parse_jd
from src.jd_requirement_classifier import enrich_job_criteria_with_requirement_metadata
from src.responsibility_signal_extractor import (
    TECHNICAL_TASK,
)


def test_responsibility_signal_extractor_builds_technical_candidate_pool() -> None:
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

    assert job_criteria["requirement_groups"]["must_have_technical"] == []
    assert job_criteria["technical_responsibility_candidates"] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
        "Google Workspace",
        "Router",
        "Switch",
        "VPN",
    ]
    assert all(
        signal["signal_type"] == TECHNICAL_TASK
        for signal in job_criteria["responsibility_signals"]
    )
    assert all(
        signal["specificity"] == "high"
        for signal in job_criteria["responsibility_signals"]
    )


def test_responsibility_signal_extractor_ignores_generic_operational_lines() -> None:
    jd_text = (
        "Operations Coordinator\n"
        "\n"
        "Responsibilities\n"
        "- Collaborate with internal teams and report weekly progress.\n"
        "- Coordinate stakeholder communication and prepare documentation.\n"
    )

    job_criteria = enrich_job_criteria_with_requirement_metadata(
        parse_jd(jd_text),
        jd_text,
        taxonomy={},
    )

    assert job_criteria["technical_responsibility_candidates"] == []
    assert [signal["signal_type"] for signal in job_criteria["responsibility_signals"]] == [
        "OPERATIONAL_TASK",
        "OPERATIONAL_TASK",
    ]


def test_responsibility_signal_extractor_keeps_technical_terms_inside_domain_lines() -> None:
    jd_text = (
        "Banking Infrastructure Engineer\n"
        "\n"
        "Responsibilities\n"
        "- Support banking VPN operations and monitor firewall events.\n"
    )

    job_criteria = enrich_job_criteria_with_requirement_metadata(
        parse_jd(jd_text),
        jd_text,
        taxonomy={},
    )

    assert job_criteria["technical_responsibility_candidates"] == ["Firewall", "VPN"]
    assert job_criteria["responsibility_signals"][0]["signal_type"] == TECHNICAL_TASK
    assert (
        job_criteria["responsibility_signals"][0]["source_requirement_type"]
        == "DOMAIN_CONTEXT"
    )
