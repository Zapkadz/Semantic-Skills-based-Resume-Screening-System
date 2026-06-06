"""Skill normalization helpers based on the project taxonomy."""

from __future__ import annotations

from typing import Any

from src.skill_taxonomy import build_alias_map, make_lookup_key


def normalize_skill(skill: str, taxonomy: dict[str, dict[str, Any]]) -> str:
    """Normalize a raw skill name to its canonical taxonomy name when possible."""
    alias_map = build_alias_map(taxonomy)
    return _normalize_skill_with_alias_map(skill, alias_map)


def normalize_skills(
    skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Normalize skills and remove duplicates while preserving first-seen order."""
    alias_map = build_alias_map(taxonomy)
    normalized_skills: list[str] = []
    seen_keys: set[str] = set()

    for skill in skills:
        normalized_skill = _normalize_skill_with_alias_map(skill, alias_map)
        if not normalized_skill:
            continue

        lookup_key = make_lookup_key(normalized_skill)
        if lookup_key in seen_keys:
            continue

        seen_keys.add(lookup_key)
        normalized_skills.append(normalized_skill)

    return normalized_skills


def _normalize_skill_with_alias_map(skill: str, alias_map: dict[str, str]) -> str:
    """Normalize a single skill using a prebuilt alias map."""
    if not isinstance(skill, str):
        raise TypeError("Skill must be a string.")

    clean_skill = skill.strip()
    if not clean_skill:
        return ""

    return alias_map.get(make_lookup_key(clean_skill), clean_skill)
