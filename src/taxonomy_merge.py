"""Custom taxonomy overlay merge helpers."""

from __future__ import annotations

import json
from copy import deepcopy
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.skill_taxonomy import build_alias_map, load_taxonomy, make_lookup_key


OVERLAY_VERSION = 1
DEFAULT_CUSTOM_CATEGORY = "Pending Classification"


def load_custom_taxonomy_overlay(path: str | Path) -> dict[str, Any]:
    """Load and validate an Admin-approved custom taxonomy overlay JSON file."""
    overlay_path = Path(path)
    _validate_json_file_path(overlay_path, "Custom taxonomy overlay")

    try:
        overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        raise ValueError(f"Invalid custom taxonomy overlay JSON: {overlay_path}") from exc

    return _normalize_overlay(overlay)


def merge_taxonomies(
    base_taxonomy: dict[str, dict[str, Any]],
    custom_overlay: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Merge base taxonomy with Admin-approved custom skills and aliases."""
    build_alias_map(base_taxonomy)
    overlay = _normalize_overlay(custom_overlay)
    merged_taxonomy = deepcopy(base_taxonomy)

    for custom_skill in overlay["custom_skills"]:
        skill_name = custom_skill["skill_name"]
        if skill_name in merged_taxonomy:
            raise ValueError(
                f"Custom skill '{skill_name}' already exists in taxonomy. "
                "Use alias_updates for existing skills."
            )

        merged_taxonomy[skill_name] = {
            "aliases": _dedupe_strings(custom_skill["aliases"]),
            "category": custom_skill["category"],
            "related": _dedupe_strings(custom_skill["related"]),
            "transferable": _dedupe_strings(custom_skill["transferable"]),
        }

    for alias_update in overlay["alias_updates"]:
        target_skill_name = alias_update["target_skill_name"]
        if target_skill_name not in merged_taxonomy:
            raise ValueError(
                f"Alias update target skill not found: {target_skill_name}"
            )

        current_aliases = list(merged_taxonomy[target_skill_name]["aliases"])
        merged_taxonomy[target_skill_name]["aliases"] = _dedupe_strings(
            [*current_aliases, *alias_update["aliases"]]
        )

    build_alias_map(merged_taxonomy)
    return merged_taxonomy


def save_merged_taxonomy(
    taxonomy: dict[str, dict[str, Any]],
    output_path: str | Path,
) -> str:
    """Save a merged taxonomy JSON file atomically and return the saved path."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    build_alias_map(taxonomy)

    temp_path = output.with_name(f"{output.stem}.tmp{output.suffix}")
    temp_path.write_text(
        json.dumps(taxonomy, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    load_taxonomy(temp_path)
    temp_path.replace(output)
    return str(output)


def build_taxonomy_merge_report(
    base_taxonomy: dict[str, dict[str, Any]],
    custom_overlay: dict[str, Any],
    merged_taxonomy: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Build a small audit-friendly report for a taxonomy merge operation."""
    overlay = _normalize_overlay(custom_overlay)
    updated_skills = [
        alias_update["target_skill_name"] for alias_update in overlay["alias_updates"]
    ]

    return {
        "base_skill_count": len(base_taxonomy),
        "custom_skills_added": len(overlay["custom_skills"]),
        "alias_updates_applied": len(overlay["alias_updates"]),
        "merged_skill_count": len(merged_taxonomy),
        "added_skills": [
            custom_skill["skill_name"] for custom_skill in overlay["custom_skills"]
        ],
        "updated_skills": _dedupe_strings(updated_skills),
    }


def _normalize_overlay(overlay: Any) -> dict[str, Any]:
    """Validate and normalize the custom taxonomy overlay contract."""
    if not isinstance(overlay, dict):
        raise ValueError("Custom taxonomy overlay must be a JSON object.")

    version = overlay.get("version", OVERLAY_VERSION)
    if not isinstance(version, int):
        raise ValueError("Custom taxonomy overlay version must be an integer.")

    custom_skills = overlay.get("custom_skills", [])
    alias_updates = overlay.get("alias_updates", [])
    if not isinstance(custom_skills, list):
        raise ValueError("custom_skills must be a list.")
    if not isinstance(alias_updates, list):
        raise ValueError("alias_updates must be a list.")

    return {
        "version": version,
        "custom_skills": [
            _normalize_custom_skill(custom_skill, index)
            for index, custom_skill in enumerate(custom_skills)
        ],
        "alias_updates": [
            _normalize_alias_update(alias_update, index)
            for index, alias_update in enumerate(alias_updates)
        ],
    }


def _normalize_custom_skill(value: Any, index: int) -> dict[str, Any]:
    """Normalize one approved custom skill entry."""
    if not isinstance(value, dict):
        raise ValueError(f"custom_skills[{index}] must be an object.")

    skill_name = _required_string(value.get("skill_name"), f"custom_skills[{index}].skill_name")
    category = _optional_string(
        value.get("category"),
        DEFAULT_CUSTOM_CATEGORY,
        f"custom_skills[{index}].category",
    )

    return {
        "skill_name": skill_name,
        "category": category,
        "aliases": _string_list(value.get("aliases", []), f"custom_skills[{index}].aliases"),
        "related": _string_list(value.get("related", []), f"custom_skills[{index}].related"),
        "transferable": _string_list(
            value.get("transferable", []),
            f"custom_skills[{index}].transferable",
        ),
    }


def _normalize_alias_update(value: Any, index: int) -> dict[str, Any]:
    """Normalize one approved alias update entry."""
    if not isinstance(value, dict):
        raise ValueError(f"alias_updates[{index}] must be an object.")

    target_skill_name = _required_string(
        value.get("target_skill_name"),
        f"alias_updates[{index}].target_skill_name",
    )
    aliases = _string_list(value.get("aliases", []), f"alias_updates[{index}].aliases")
    if not aliases:
        raise ValueError(f"alias_updates[{index}].aliases must include at least one alias.")

    return {
        "target_skill_name": target_skill_name,
        "aliases": aliases,
    }


def _validate_json_file_path(path: Path, label: str) -> None:
    """Validate a JSON input path before reading."""
    if not path.exists():
        raise FileNotFoundError(f"{label} file not found: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Expected {label} JSON file, got directory: {path}")
    if path.suffix.lower() != ".json":
        raise ValueError(f"{label} file must use .json extension: {path}")


def _required_string(value: Any, field_name: str) -> str:
    """Return a stripped required string or raise a useful validation error."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")

    return value.strip()


def _optional_string(value: Any, default: str, field_name: str) -> str:
    """Return a stripped optional string with a default."""
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string.")

    return value.strip() or default


def _string_list(value: Any, field_name: str) -> list[str]:
    """Normalize a JSON value into a clean list of strings."""
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list.")

    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str):
            raise ValueError(f"{field_name}[{index}] must be a string.")
        stripped_item = item.strip()
        if stripped_item:
            items.append(stripped_item)

    return items


def _dedupe_strings(values: list[str]) -> list[str]:
    """Deduplicate strings with the same taxonomy lookup semantics."""
    seen: set[str] = set()
    deduped: list[str] = []

    for value in values:
        lookup_key = make_lookup_key(value)
        if not lookup_key or lookup_key in seen:
            continue

        seen.add(lookup_key)
        deduped.append(value)

    return deduped
