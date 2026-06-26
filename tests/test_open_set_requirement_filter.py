from src.open_set_requirement_filter import (
    build_open_set_filter_summary,
    filter_open_set_requirement_candidates,
)


def test_filter_open_set_requirement_candidates_keeps_technical_phrases() -> None:
    candidates = filter_open_set_requirement_candidates(
        [
            {"text": "identity verification"},
            {"text": "Qualys"},
            {"text": "face recognition"},
        ]
    )

    assert [
        (candidate["canonical_text"], candidate["status"], candidate["reason"])
        for candidate in candidates
    ] == [
        ("identity verification", "kept", "technical_capability_phrase"),
        ("Qualys", "kept", "explicit_tool_signal"),
        ("face recognition", "kept", "technical_capability_phrase"),
    ]


def test_filter_open_set_requirement_candidates_discards_generic_context_phrases() -> None:
    candidates = filter_open_set_requirement_candidates(
        [
            {"text": "Governance"},
            {"text": "Compliance"},
            {"text": "IT Security Operations"},
            {"text": "Personal Data Protection"},
        ]
    )

    assert [
        (candidate["canonical_text"], candidate["status"], candidate["reason"])
        for candidate in candidates
    ] == [
        ("Governance", "discarded", "generic_context_only"),
        ("Compliance", "discarded", "generic_context_only"),
        ("IT Security Operations", "discarded", "generic_context_only"),
        ("Personal Data Protection", "discarded", "generic_context_only"),
    ]
    assert build_open_set_filter_summary(candidates) == {
        "candidate_count": 4,
        "kept_count": 0,
        "discarded_count": 4,
        "kept_for_matching_count": 0,
        "kept_for_suggestion_count": 0,
        "discarded_reason_counts": {
            "generic_context_only": 4,
        },
    }


def test_filter_open_set_requirement_candidates_discards_known_requirement_duplicates() -> None:
    candidates = filter_open_set_requirement_candidates(
        [{"text": "Qualys"}],
        known_requirement_labels=["Qualys"],
    )

    assert candidates == [
        {
            "text": "Qualys",
            "canonical_text": "Qualys",
            "normalized_text": "qualys",
            "status": "discarded",
            "reason": "known_requirement_duplicate",
            "technical_confidence": 0.0,
            "keep_for_matching": False,
            "keep_for_suggestion": False,
        }
    ]


def test_filter_open_set_requirement_candidates_discards_generic_it_systems_phrase() -> None:
    candidates = filter_open_set_requirement_candidates(
        [{"text": "Knowledge of IT systems"}]
    )

    assert candidates == [
        {
            "text": "Knowledge of IT systems",
            "canonical_text": "Knowledge of IT systems",
            "normalized_text": "knowledge of it systems",
            "status": "discarded",
            "reason": "low_technical_specificity",
            "technical_confidence": 0.0,
            "keep_for_matching": False,
            "keep_for_suggestion": False,
        }
    ]
