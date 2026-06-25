from src.requirement_extractor import (
    build_screening_confidence,
    extract_unknown_requirement_debug,
    extract_unknown_requirement_texts,
)


def test_extract_unknown_requirement_texts_decomposes_long_security_requirements() -> None:
    job_criteria = {
        "must_have_skills": [
            "Qualifications & Experience",
            "Professional requirements: Proficiency in Linux, Nutanix administration, Commvault, and Qualys; ability to perform patch upgrades for both Windows and Linux.",
            "At least 3 yeear of experience in IT Security Operations, Governance, Compliance, Personal Data Protection, preferably in banking/finance.",
            "Knowledge of vulnerability management tools (e.g., Qualys) and access control principles.",
            "Understanding of Personal Data Protection regulations.",
            "Skills",
            "Strong analytical, detail-oriented, and process-driven mindset.",
            "Relevant certifications: Security+, CEH, ISO 27001, or Privacy certifications (CIPP/E, CIPM) are an advantage.",
        ]
    }

    requirements = extract_unknown_requirement_texts(job_criteria, "", {})

    assert requirements == [
        "Linux",
        "Nutanix administration",
        "Commvault",
        "Qualys",
        "patch upgrades for Windows",
        "vulnerability management",
        "access control",
        "CIPP/E",
        "CIPM",
        "CEH",
        "ISO 27001",
        "Security+",
    ]


def test_extract_unknown_requirement_debug_returns_kept_and_discarded_candidates() -> None:
    job_criteria = {
        "must_have_skills": [
            "Linux",
            "Governance",
            "Qualys",
            "Personal Data Protection",
            "vulnerability management",
        ]
    }

    debug_payload = extract_unknown_requirement_debug(job_criteria, "", {})

    assert debug_payload["open_set_requirements"] == [
        "Linux",
        "Qualys",
        "vulnerability management",
    ]
    assert [
        (candidate["text"], candidate["status"], candidate["reason"])
        for candidate in debug_payload["open_set_candidates"]
    ] == [
        ("Linux", "kept", "explicit_tool_signal"),
        ("Governance", "discarded", "generic_context_only"),
        ("Qualys", "kept", "explicit_tool_signal"),
        ("Personal Data Protection", "discarded", "generic_context_only"),
        ("vulnerability management", "kept", "technical_capability_phrase"),
    ]
    assert debug_payload["open_set_filter_summary"] == {
        "candidate_count": 5,
        "kept_count": 3,
        "discarded_count": 2,
        "kept_for_matching_count": 3,
        "kept_for_suggestion_count": 3,
        "discarded_reason_counts": {
            "generic_context_only": 2,
        },
    }


def test_extract_unknown_requirement_texts_skips_taxonomy_known_phrases() -> None:
    taxonomy = {
        "Python": {
            "aliases": ["Python programming"],
            "category": "Programming Language",
            "related": [],
            "transferable": [],
        },
        "REST API": {
            "aliases": ["REST APIs"],
            "category": "Backend",
            "related": [],
            "transferable": [],
        },
    }
    job_criteria = {
        "must_have_skills": [
            "Strong Python programming skills.",
            "REST API",
        ]
    }

    assert extract_unknown_requirement_texts(job_criteria, "", taxonomy) == []


def test_extract_unknown_requirement_texts_skips_plain_experience_field() -> None:
    job_criteria = {
        "must_have_skills": [
            "Linux",
            "3 năm",
            "3 years",
        ]
    }

    assert extract_unknown_requirement_texts(job_criteria, "", {}) == ["Linux"]


def test_extract_unknown_requirement_texts_uses_typed_requirements_to_skip_language_and_soft() -> None:
    job_criteria = {
        "must_have_skills": [
            "Qualys",
            "Written English for cross-team coordination.",
            "Strong communication and teamwork.",
        ],
        "typed_requirements": [
            {
                "text": "Qualys",
                "type": "TOOL_PLATFORM",
                "priority": "must_have",
                "ignored": "false",
            },
            {
                "text": "Written English for cross-team coordination.",
                "type": "LANGUAGE_REQUIREMENT",
                "priority": "must_have",
                "ignored": "false",
            },
            {
                "text": "Strong communication and teamwork.",
                "type": "SOFT_SKILL",
                "priority": "must_have",
                "ignored": "false",
            },
        ],
    }

    assert extract_unknown_requirement_texts(job_criteria, "", {}) == ["Qualys"]


def test_extract_unknown_requirement_texts_strips_vietnamese_technical_leadins() -> None:
    job_criteria = {
        "must_have_skills": [
            "Thành thạo cơ sở dữ liệu Oracle",
            "Có kiến thức về Monolithic, Micro-service, OOP",
            "Có hiểu biết cơ bản về DevOps, CI/CD.",
        ]
    }

    assert extract_unknown_requirement_texts(job_criteria, "", {}) == [
        "Oracle",
        "OOP",
        "Monolithic",
        "Micro-service",
        "CI/CD",
        "DevOps",
    ]


def test_build_screening_confidence_warns_when_open_set_embedding_is_disabled() -> None:
    confidence = build_screening_confidence(
        known_requirements=[],
        open_set_requirements=["Qualys"],
        embedding_matcher=None,
    )

    assert confidence == {
        "level": "low",
        "known_requirement_count": 0,
        "open_set_requirement_count": 1,
        "embedding_enabled": False,
        "warnings": [
            "Open-set requirements detected but embedding matcher is disabled."
        ],
    }


def test_build_screening_confidence_is_medium_for_embedding_open_set_only() -> None:
    confidence = build_screening_confidence(
        known_requirements=[],
        open_set_requirements=["Qualys"],
        embedding_matcher=object(),
    )

    assert confidence == {
        "level": "medium",
        "known_requirement_count": 0,
        "open_set_requirement_count": 1,
        "embedding_enabled": True,
        "warnings": [],
    }
