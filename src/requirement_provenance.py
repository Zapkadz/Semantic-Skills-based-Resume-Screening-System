"""Requirement provenance helpers for source-aware scoring."""

from __future__ import annotations

from typing import Any

from src.requirement_promotion import (
    EXPLICIT_REQUIREMENT_SOURCE,
    PROMOTED_RESPONSIBILITY_SOURCE,
)
from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import make_lookup_key


DEFAULT_REQUIREMENT_PRIORITY = "must_have"
KNOWN_TAXONOMY_STATUS = "known"
UNKNOWN_TAXONOMY_STATUS = "unknown"


def build_requirement_provenance_summary(
    required_skills: list[str],
    open_set_requirements: list[str],
    scoring_requirement_entries: list[dict[str, Any]],
    open_set_candidates: list[dict[str, Any]],
    taxonomy: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build stable provenance metadata for known and open-set requirements."""
    known_lookup: dict[str, dict[str, Any]] = {}
    for entry in scoring_requirement_entries:
        entry_text = str(entry.get("text", "")).strip()
        if not entry_text:
            continue

        extracted_skills = _extract_entry_known_skills(entry_text, taxonomy)
        if not extracted_skills:
            continue

        for skill in extracted_skills:
            lookup_key = make_lookup_key(skill)
            if not lookup_key or lookup_key in known_lookup:
                continue

            known_lookup[lookup_key] = _summary_item(
                skill,
                source_kind=_normalize_source_kind(entry.get("source_kind")),
                source_text=str(entry.get("source_text", "")).strip() or entry_text,
                priority=str(entry.get("priority", "")).strip()
                or DEFAULT_REQUIREMENT_PRIORITY,
                taxonomy_status=KNOWN_TAXONOMY_STATUS,
            )

    open_set_lookup: dict[str, dict[str, Any]] = {}
    for candidate in open_set_candidates:
        if candidate.get("keep_for_matching") is not True:
            continue

        canonical_text = str(candidate.get("canonical_text", "")).strip()
        lookup_key = make_lookup_key(canonical_text)
        if not lookup_key or lookup_key in open_set_lookup:
            continue

        source_text = str(candidate.get("text", "")).strip() or canonical_text
        open_set_lookup[lookup_key] = _summary_item(
            canonical_text,
            source_kind=_normalize_source_kind(
                candidate.get("source_kind") or candidate.get("source")
            ),
            source_text=source_text,
            priority=str(candidate.get("priority", "")).strip()
            or DEFAULT_REQUIREMENT_PRIORITY,
            taxonomy_status=UNKNOWN_TAXONOMY_STATUS,
        )

    summary: list[dict[str, Any]] = []
    for skill in required_skills:
        lookup_key = make_lookup_key(skill)
        summary.append(
            known_lookup.get(
                lookup_key,
                _summary_item(
                    skill,
                    source_kind=EXPLICIT_REQUIREMENT_SOURCE,
                    source_text=skill,
                    priority=DEFAULT_REQUIREMENT_PRIORITY,
                    taxonomy_status=KNOWN_TAXONOMY_STATUS,
                ),
            )
        )

    for requirement in open_set_requirements:
        lookup_key = make_lookup_key(requirement)
        summary.append(
            open_set_lookup.get(
                lookup_key,
                _summary_item(
                    requirement,
                    source_kind=EXPLICIT_REQUIREMENT_SOURCE,
                    source_text=requirement,
                    priority=DEFAULT_REQUIREMENT_PRIORITY,
                    taxonomy_status=UNKNOWN_TAXONOMY_STATUS,
                ),
            )
        )

    return summary


def build_requirement_provenance_lookup(
    requirement_provenance_summary: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a lookup from normalized requirement text to provenance metadata."""
    return {
        make_lookup_key(str(item.get("text", ""))): item
        for item in requirement_provenance_summary
        if make_lookup_key(str(item.get("text", "")))
    }


def _extract_entry_known_skills(
    entry_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Extract canonical known skills from one scoring requirement entry."""
    normalized_items = normalize_skills([entry_text], taxonomy)
    normalized_known_skills = [
        item for item in normalized_items if item in taxonomy
    ]
    extracted_skills = extract_taxonomy_skills_from_text(entry_text, taxonomy)
    return merge_skill_lists(normalized_known_skills, extracted_skills)


def _normalize_source_kind(value: Any) -> str:
    """Normalize arbitrary source labels into stable source kinds."""
    normalized_value = str(value or "").strip().casefold()
    if normalized_value == PROMOTED_RESPONSIBILITY_SOURCE:
        return PROMOTED_RESPONSIBILITY_SOURCE

    return EXPLICIT_REQUIREMENT_SOURCE


def _summary_item(
    text: str,
    *,
    source_kind: str,
    source_text: str,
    priority: str,
    taxonomy_status: str,
) -> dict[str, Any]:
    """Build one stable provenance summary item."""
    return {
        "text": text,
        "requirement_source_kind": source_kind,
        "requirement_source_text": source_text,
        "requirement_priority": priority,
        "taxonomy_status": taxonomy_status,
    }
