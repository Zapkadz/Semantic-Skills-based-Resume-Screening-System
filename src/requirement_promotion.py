"""Controlled promotion of technical responsibility signals into scoring input."""

from __future__ import annotations

from typing import Any

from src.requirement_types import MUST_HAVE_PRIORITY, NICE_TO_HAVE_PRIORITY
from src.responsibility_signal_extractor import SPECIFICITY_HIGH, SUPPORTED_SIGNAL_TYPES
from src.skill_extractor import merge_skill_lists


EXPLICIT_REQUIREMENT_SOURCE = "explicit_requirement"
PROMOTED_RESPONSIBILITY_SOURCE = "promoted_responsibility"

DEFAULT_PROMOTION_REASON = "sparse_explicit_technical_requirements"
MAX_PROMOTED_REQUIREMENTS = 4


def build_scoring_requirement_entries(
    job_criteria: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build scored requirement entries with explicit-vs-promoted provenance."""
    requirement_groups = dict(job_criteria.get("requirement_groups", {}))

    entries = [
        *[
            _entry(
                line,
                priority=MUST_HAVE_PRIORITY,
                source_kind=EXPLICIT_REQUIREMENT_SOURCE,
            )
            for line in requirement_groups.get("must_have_technical", [])
        ],
        *[
            _entry(
                line,
                priority=MUST_HAVE_PRIORITY,
                source_kind=EXPLICIT_REQUIREMENT_SOURCE,
            )
            for line in requirement_groups.get("certifications", [])
        ],
        *[
            _entry(
                line,
                priority=NICE_TO_HAVE_PRIORITY,
                source_kind=EXPLICIT_REQUIREMENT_SOURCE,
            )
            for line in requirement_groups.get("nice_to_have_technical", [])
        ],
    ]

    promoted_requirements = build_promoted_requirements(job_criteria)
    entries.extend(promoted_requirements)

    return _dedupe_entries(entries)


def build_scoring_requirement_lines_from_entries(
    scoring_requirement_entries: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    """Flatten scoring entries into must-have and nice-to-have lines."""
    must_have = merge_skill_lists(
        [
            str(entry.get("text", "")).strip()
            for entry in scoring_requirement_entries
            if str(entry.get("priority", "")) == MUST_HAVE_PRIORITY
            and str(entry.get("text", "")).strip()
        ]
    )
    nice_to_have = merge_skill_lists(
        [
            str(entry.get("text", "")).strip()
            for entry in scoring_requirement_entries
            if str(entry.get("priority", "")) == NICE_TO_HAVE_PRIORITY
            and str(entry.get("text", "")).strip()
        ]
    )
    return must_have, nice_to_have


def build_promoted_requirements(job_criteria: dict[str, Any]) -> list[dict[str, Any]]:
    """Promote high-specificity responsibility signals when explicit technical input is empty."""
    requirement_groups = dict(job_criteria.get("requirement_groups", {}))
    explicit_required_lines = merge_skill_lists(
        requirement_groups.get("must_have_technical", []),
        requirement_groups.get("certifications", []),
    )
    if explicit_required_lines:
        return []

    responsibility_signals = list(job_criteria.get("responsibility_signals", []))
    if not responsibility_signals:
        return []

    promoted_entries: list[dict[str, Any]] = []
    seen_terms: set[str] = set()

    for signal in responsibility_signals:
        if str(signal.get("signal_type", "")) not in SUPPORTED_SIGNAL_TYPES:
            continue
        if str(signal.get("specificity", "")) != SPECIFICITY_HIGH:
            continue

        source_text = str(signal.get("text", "")).strip()
        signal_type = str(signal.get("signal_type", "")).strip()
        specificity = str(signal.get("specificity", "")).strip()
        for term in signal.get("technical_terms", []):
            clean_term = str(term).strip()
            if not clean_term:
                continue
            lookup_key = clean_term.casefold()
            if lookup_key in seen_terms:
                continue

            promoted_entries.append(
                {
                    "text": clean_term,
                    "priority": MUST_HAVE_PRIORITY,
                    "source_kind": PROMOTED_RESPONSIBILITY_SOURCE,
                    "source_text": source_text,
                    "signal_type": signal_type,
                    "promotion_specificity": specificity,
                    "promotion_reason": DEFAULT_PROMOTION_REASON,
                }
            )
            seen_terms.add(lookup_key)

            if len(promoted_entries) >= MAX_PROMOTED_REQUIREMENTS:
                return promoted_entries

    return promoted_entries


def _entry(
    text: str,
    *,
    priority: str,
    source_kind: str,
) -> dict[str, Any]:
    """Build one explicit scoring requirement entry."""
    clean_text = str(text).strip()
    return {
        "text": clean_text,
        "priority": priority,
        "source_kind": source_kind,
        "source_text": clean_text,
    }


def _dedupe_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate entries by normalized text and priority while preserving first source."""
    deduped: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()

    for entry in entries:
        text = str(entry.get("text", "")).strip()
        priority = str(entry.get("priority", "")).strip()
        if not text or not priority:
            continue

        key = (text.casefold(), priority)
        if key in seen_keys:
            continue

        seen_keys.add(key)
        deduped.append(entry)

    return deduped
