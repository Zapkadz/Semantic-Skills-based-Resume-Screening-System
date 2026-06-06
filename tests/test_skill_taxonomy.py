import json
from pathlib import Path

import pytest

from src.skill_taxonomy import build_alias_map, load_taxonomy, make_lookup_key


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_load_taxonomy_reads_skills_json() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    assert "Java" in taxonomy
    assert taxonomy["Spring Boot"]["category"] == "Backend Framework"
    assert "SpringBoot" in taxonomy["Spring Boot"]["aliases"]


def test_build_alias_map_maps_canonical_names_and_aliases() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)

    alias_map = build_alias_map(taxonomy)

    assert alias_map[make_lookup_key("Spring Boot")] == "Spring Boot"
    assert alias_map[make_lookup_key("SpringBoot")] == "Spring Boot"
    assert alias_map[make_lookup_key("Postgres")] == "PostgreSQL"
    assert alias_map[make_lookup_key("JS")] == "JavaScript"
    assert alias_map[make_lookup_key("k8s")] == "Kubernetes"


def test_load_taxonomy_raises_when_file_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Taxonomy file not found"):
        load_taxonomy(tmp_path / "missing.json")


def test_load_taxonomy_raises_for_unsupported_extension(tmp_path: Path) -> None:
    taxonomy_file = tmp_path / "skills.txt"
    taxonomy_file.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported taxonomy file extension"):
        load_taxonomy(taxonomy_file)


def test_load_taxonomy_raises_for_invalid_json(tmp_path: Path) -> None:
    taxonomy_file = tmp_path / "skills.json"
    taxonomy_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid taxonomy JSON"):
        load_taxonomy(taxonomy_file)


def test_load_taxonomy_raises_when_required_field_missing(tmp_path: Path) -> None:
    taxonomy_file = tmp_path / "skills.json"
    taxonomy_file.write_text(
        json.dumps(
            {
                "Java": {
                    "aliases": [],
                    "category": "Programming Language",
                    "related": [],
                }
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing fields"):
        load_taxonomy(taxonomy_file)


def test_build_alias_map_rejects_ambiguous_aliases() -> None:
    taxonomy = {
        "JavaScript": {
            "aliases": ["JS"],
            "category": "Programming Language",
            "related": [],
            "transferable": [],
        },
        "Job Scheduler": {
            "aliases": ["JS"],
            "category": "Tool",
            "related": [],
            "transferable": [],
        },
    }

    with pytest.raises(ValueError, match="ambiguous"):
        build_alias_map(taxonomy)
