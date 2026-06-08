"""Skill taxonomy loading and lookup helpers."""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.text_normalization import normalize_lookup_text


REQUIRED_SKILL_FIELDS = {"aliases", "category", "related", "transferable"}


def load_taxonomy(path: str | Path) -> dict[str, dict[str, Any]]:
    """Load and validate a skill taxonomy JSON file."""
    taxonomy_path = Path(path)
    _validate_taxonomy_path(taxonomy_path)

    try:
        taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        raise ValueError(f"Invalid taxonomy JSON: {taxonomy_path}") from exc

    _validate_taxonomy(taxonomy)
    return taxonomy


def build_alias_map(taxonomy: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Build a case-insensitive lookup map from aliases to canonical skills."""
    _validate_taxonomy(taxonomy)

    alias_map: dict[str, str] = {}
    for canonical_skill, metadata in taxonomy.items():
        _add_alias(alias_map, canonical_skill, canonical_skill)
        for alias in metadata["aliases"]:
            _add_alias(alias_map, alias, canonical_skill)

    return alias_map


def make_lookup_key(value: str) -> str:
    """Normalize text for case-insensitive skill lookup."""
    return normalize_lookup_text(value)


def _validate_taxonomy_path(taxonomy_path: Path) -> None:
    """Validate a taxonomy file path before reading JSON."""
    if not taxonomy_path.exists():
        raise FileNotFoundError(f"Taxonomy file not found: {taxonomy_path}")

    if not taxonomy_path.is_file():
        raise IsADirectoryError(
            f"Expected a taxonomy JSON file, got directory: {taxonomy_path}"
        )

    if taxonomy_path.suffix.lower() != ".json":
        raise ValueError(
            f"Unsupported taxonomy file extension '{taxonomy_path.suffix}'. "
            "Expected .json"
        )


def _validate_taxonomy(taxonomy: Any) -> None:
    """Validate the minimal taxonomy structure needed by the MVP."""
    if not isinstance(taxonomy, dict):
        raise ValueError("Taxonomy must be a JSON object.")

    for skill_name, metadata in taxonomy.items():
        if not isinstance(skill_name, str) or not skill_name.strip():
            raise ValueError("Each taxonomy skill name must be a non-empty string.")

        if not isinstance(metadata, dict):
            raise ValueError(f"Skill metadata must be an object: {skill_name}")

        missing_fields = REQUIRED_SKILL_FIELDS - metadata.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Skill '{skill_name}' is missing fields: {missing}")

        if not isinstance(metadata["aliases"], list):
            raise ValueError(f"Skill '{skill_name}' aliases must be a list.")
        if not isinstance(metadata["category"], str):
            raise ValueError(f"Skill '{skill_name}' category must be a string.")
        if not isinstance(metadata["related"], list):
            raise ValueError(f"Skill '{skill_name}' related must be a list.")
        if not isinstance(metadata["transferable"], list):
            raise ValueError(f"Skill '{skill_name}' transferable must be a list.")


def _add_alias(alias_map: dict[str, str], alias: str, canonical_skill: str) -> None:
    """Add an alias lookup and reject ambiguous aliases."""
    if not isinstance(alias, str) or not alias.strip():
        raise ValueError(f"Alias for '{canonical_skill}' must be a non-empty string.")

    lookup_key = make_lookup_key(alias)
    existing_skill = alias_map.get(lookup_key)
    if existing_skill and existing_skill != canonical_skill:
        raise ValueError(
            f"Alias '{alias}' is ambiguous: '{existing_skill}' vs '{canonical_skill}'"
        )

    alias_map[lookup_key] = canonical_skill
