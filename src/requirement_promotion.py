"""Controlled promotion of technical responsibility signals into scoring input."""

from __future__ import annotations

from typing import Any

from src.open_set_requirement_filter import filter_open_set_requirement_candidates
from src.requirement_types import (
    CERTIFICATION_REQUIREMENT,
    MUST_HAVE_PRIORITY,
    NICE_TO_HAVE_PRIORITY,
    TECH_SKILL,
    TOOL_PLATFORM,
)
from src.responsibility_signal_extractor import SPECIFICITY_HIGH, SUPPORTED_SIGNAL_TYPES
from src.skill_extractor import merge_skill_lists


EXPLICIT_REQUIREMENT_SOURCE = "explicit_requirement"
PROMOTED_RESPONSIBILITY_SOURCE = "promoted_responsibility"

DEFAULT_PROMOTION_REASON = "sparse_explicit_technical_requirements"
MAX_PROMOTED_REQUIREMENTS = 4
MIN_USABLE_EXPLICIT_TECHNICAL_LINES = 2


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
    recovery_summary = build_explicit_technical_recovery_summary(job_criteria)
    if not recovery_summary.get("recovery_triggered", False):
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


def build_explicit_technical_recovery_summary(
    job_criteria: dict[str, Any],
) -> dict[str, Any]:
    """Summarize whether explicit technical requirements are strong enough to block recovery."""
    requirement_groups = dict(job_criteria.get("requirement_groups", {}))
    typed_lookup = {
        str(item.get("text", "")).strip(): str(item.get("type", "")).strip()
        for item in job_criteria.get("typed_requirements", [])
        if str(item.get("text", "")).strip()
    }
    explicit_required_lines = merge_skill_lists(
        requirement_groups.get("must_have_technical", []),
        requirement_groups.get("certifications", []),
    )
    usable_lines: list[str] = []
    contaminated_lines: list[str] = []

    for line in explicit_required_lines:
        requirement_type = typed_lookup.get(line, "")
        if _is_usable_explicit_technical_line(line, requirement_type):
            usable_lines.append(line)
        else:
            contaminated_lines.append(line)

    usable_count = len(usable_lines)
    responsibility_signals = list(job_criteria.get("responsibility_signals", []))
    supported_high_specificity_signal_count = sum(
        1
        for signal in responsibility_signals
        if str(signal.get("signal_type", "")) in SUPPORTED_SIGNAL_TYPES
        and str(signal.get("specificity", "")) == SPECIFICITY_HIGH
        and bool(signal.get("technical_terms"))
    )
    technical_responsibility_candidates = list(
        job_criteria.get("technical_responsibility_candidates", [])
    )

    recovery_triggered = (
        usable_count < MIN_USABLE_EXPLICIT_TECHNICAL_LINES
        and supported_high_specificity_signal_count > 0
        and len(technical_responsibility_candidates) > 0
    )

    if usable_count >= MIN_USABLE_EXPLICIT_TECHNICAL_LINES:
        reason = "usable_explicit_technical_requirements_present"
    elif not technical_responsibility_candidates:
        reason = "no_recoverable_responsibility_signals"
    elif not supported_high_specificity_signal_count:
        reason = "responsibility_signals_not_specific_enough"
    elif usable_count == 1:
        reason = "explicit_technical_too_thin_for_sparse_jd"
    elif contaminated_lines:
        reason = "explicit_technical_contamination_detected"
    else:
        reason = DEFAULT_PROMOTION_REASON

    return {
        "raw_explicit_technical_count": len(explicit_required_lines),
        "usable_explicit_technical_count": usable_count,
        "explicit_technical_contamination_count": len(contaminated_lines),
        "usable_explicit_technical_lines": usable_lines,
        "contaminated_explicit_technical_lines": contaminated_lines,
        "supported_high_specificity_signal_count": supported_high_specificity_signal_count,
        "technical_responsibility_candidate_count": len(
            technical_responsibility_candidates
        ),
        "recovery_triggered": recovery_triggered,
        "recovery_reason": reason,
    }


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


def _is_usable_explicit_technical_line(text: str, requirement_type: str) -> bool:
    """Return True when an explicit technical line is specific enough to block sparse-JD recovery."""
    if requirement_type == CERTIFICATION_REQUIREMENT:
        return True
    if requirement_type == TOOL_PLATFORM:
        return True
    if requirement_type != TECH_SKILL:
        return False

    candidates = filter_open_set_requirement_candidates([{"text": text}])
    if not candidates:
        return False

    candidate = candidates[0]
    return candidate.get("keep_for_matching") is True
