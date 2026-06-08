"""Taxonomy-based skill extraction from raw JD/CV text."""

from __future__ import annotations

import re
from typing import Any

from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text, repair_mojibake


def extract_taxonomy_skills_from_text(
    text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Extract canonical taxonomy skills found in raw text."""
    if not isinstance(text, str) or not text.strip():
        return []

    repaired_text = repair_mojibake(text)
    normalized_text = normalize_search_text(repaired_text)
    found_skills: list[tuple[int, int, str]] = []

    for taxonomy_index, (canonical_skill, metadata) in enumerate(taxonomy.items()):
        aliases = _skill_aliases(canonical_skill, metadata)
        best_start = _find_best_alias_start(repaired_text, normalized_text, aliases)
        if best_start is not None:
            found_skills.append((best_start, taxonomy_index, canonical_skill))

    found_skills.sort(key=lambda item: (item[0], item[1]))
    return merge_skill_lists([skill for _, _, skill in found_skills])


def merge_skill_lists(*skill_lists: list[str]) -> list[str]:
    """Merge skill lists while preserving first-seen canonical order."""
    merged: list[str] = []
    seen_keys: set[str] = set()

    for skill_list in skill_lists:
        for skill in skill_list:
            if not isinstance(skill, str):
                continue

            clean_skill = skill.strip()
            if not clean_skill:
                continue

            lookup_key = make_lookup_key(clean_skill)
            if lookup_key in seen_keys:
                continue

            seen_keys.add(lookup_key)
            merged.append(clean_skill)

    return merged


def _skill_aliases(canonical_skill: str, metadata: dict[str, Any]) -> list[str]:
    """Return searchable aliases for one taxonomy skill."""
    aliases = [canonical_skill]
    aliases.extend(
        alias
        for alias in metadata.get("aliases", [])
        if isinstance(alias, str) and alias.strip()
    )

    return merge_skill_lists(aliases)


def _find_best_alias_start(
    original_text: str,
    normalized_text: str,
    aliases: list[str],
) -> int | None:
    """Find the earliest occurrence among aliases."""
    starts = [
        start
        for alias in aliases
        if (start := _find_alias_start(original_text, normalized_text, alias)) is not None
    ]
    if not starts:
        return None

    return min(starts)


def _find_alias_start(
    original_text: str,
    normalized_text: str,
    alias: str,
) -> int | None:
    """Find one alias in original or normalized text."""
    if _is_short_acronym(alias):
        match = re.search(
            rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])",
            original_text,
        )
        return match.start() if match else None

    normalized_alias = normalize_search_text(alias)
    if not normalized_alias:
        return None

    pattern = rf"(?<!\w){re.escape(normalized_alias)}(?!\w)"
    match = re.search(pattern, normalized_text)
    return match.start() if match else None


def _is_short_acronym(value: str) -> bool:
    """Return True for short uppercase technical metrics like FAR or AUC."""
    return value.isupper() and 2 <= len(value) <= 4 and value.isalpha()
