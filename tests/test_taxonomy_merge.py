import json
from pathlib import Path

import pytest

from src.skill_taxonomy import load_taxonomy
from src.taxonomy_merge import (
    DEFAULT_CUSTOM_CATEGORY,
    build_taxonomy_merge_report,
    load_custom_taxonomy_overlay,
    merge_taxonomies,
    save_merged_taxonomy,
)
from taxonomy_merge import main as taxonomy_merge_main


def test_merge_taxonomies_adds_custom_skill_without_mutating_base() -> None:
    base_taxonomy = _base_taxonomy()
    overlay = {
        "version": 1,
        "custom_skills": [
            {
                "skill_name": "Carbon Footprint Analysis",
                "aliases": [
                    "carbon footprint analysis",
                    "CO2 emission reporting",
                    "carbon footprint analysis",
                ],
            }
        ],
    }

    merged_taxonomy = merge_taxonomies(base_taxonomy, overlay)

    assert "Carbon Footprint Analysis" not in base_taxonomy
    assert merged_taxonomy["Carbon Footprint Analysis"] == {
        "aliases": ["carbon footprint analysis", "CO2 emission reporting"],
        "category": DEFAULT_CUSTOM_CATEGORY,
        "related": [],
        "transferable": [],
    }


def test_merge_taxonomies_applies_alias_updates_to_existing_skill() -> None:
    overlay = {
        "version": 1,
        "alias_updates": [
            {
                "target_skill_name": "Face Recognition",
                "aliases": [
                    "nhan dien khuon mat",
                    "face verification",
                    "Face Verification",
                ],
            }
        ],
    }

    merged_taxonomy = merge_taxonomies(_base_taxonomy(), overlay)

    assert merged_taxonomy["Face Recognition"]["aliases"] == [
        "face recognition",
        "facial recognition",
        "nhan dien khuon mat",
        "face verification",
    ]


def test_merge_taxonomies_applies_alias_update_to_custom_skill() -> None:
    overlay = {
        "version": 1,
        "custom_skills": [
            {
                "skill_name": "Carbon Footprint Analysis",
                "category": "Sustainability / ESG",
                "aliases": ["carbon footprint analysis"],
            }
        ],
        "alias_updates": [
            {
                "target_skill_name": "Carbon Footprint Analysis",
                "aliases": ["carbon accounting"],
            }
        ],
    }

    merged_taxonomy = merge_taxonomies(_base_taxonomy(), overlay)

    assert merged_taxonomy["Carbon Footprint Analysis"]["aliases"] == [
        "carbon footprint analysis",
        "carbon accounting",
    ]


def test_merge_taxonomies_rejects_custom_skill_that_already_exists() -> None:
    overlay = {
        "version": 1,
        "custom_skills": [
            {
                "skill_name": "Python",
                "aliases": ["python language"],
            }
        ],
    }

    with pytest.raises(ValueError, match="already exists"):
        merge_taxonomies(_base_taxonomy(), overlay)


def test_merge_taxonomies_rejects_missing_alias_update_target() -> None:
    overlay = {
        "version": 1,
        "alias_updates": [
            {
                "target_skill_name": "Missing Skill",
                "aliases": ["missing alias"],
            }
        ],
    }

    with pytest.raises(ValueError, match="target skill not found"):
        merge_taxonomies(_base_taxonomy(), overlay)


def test_merge_taxonomies_rejects_ambiguous_aliases() -> None:
    overlay = {
        "version": 1,
        "custom_skills": [
            {
                "skill_name": "Job Scheduler",
                "aliases": ["Python"],
            }
        ],
    }

    with pytest.raises(ValueError, match="ambiguous"):
        merge_taxonomies(_base_taxonomy(), overlay)


def test_load_custom_taxonomy_overlay_validates_shape(tmp_path: Path) -> None:
    overlay_path = tmp_path / "custom_taxonomy.json"
    overlay_path.write_text(
        json.dumps(
            {
                "version": 1,
                "custom_skills": [
                    {
                        "skill_name": "  Prompt Engineering  ",
                        "category": "",
                        "aliases": ["prompt engineering"],
                    }
                ],
                "alias_updates": [],
            }
        ),
        encoding="utf-8",
    )

    overlay = load_custom_taxonomy_overlay(overlay_path)

    assert overlay["custom_skills"][0]["skill_name"] == "Prompt Engineering"
    assert overlay["custom_skills"][0]["category"] == DEFAULT_CUSTOM_CATEGORY


def test_load_custom_taxonomy_overlay_rejects_invalid_json(tmp_path: Path) -> None:
    overlay_path = tmp_path / "custom_taxonomy.json"
    overlay_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid custom taxonomy overlay JSON"):
        load_custom_taxonomy_overlay(overlay_path)


def test_save_merged_taxonomy_round_trip_with_loader(tmp_path: Path) -> None:
    output_path = tmp_path / "skills_merged.json"
    merged_taxonomy = merge_taxonomies(
        _base_taxonomy(),
        {
            "version": 1,
            "custom_skills": [
                {
                    "skill_name": "Carbon Footprint Analysis",
                    "aliases": ["carbon footprint analysis"],
                }
            ],
        },
    )

    saved_path = save_merged_taxonomy(merged_taxonomy, output_path)
    loaded_taxonomy = load_taxonomy(output_path)

    assert saved_path == str(output_path)
    assert loaded_taxonomy == merged_taxonomy
    assert not (tmp_path / "skills_merged.tmp.json").exists()


def test_build_taxonomy_merge_report_counts_changes() -> None:
    base_taxonomy = _base_taxonomy()
    overlay = {
        "version": 1,
        "custom_skills": [{"skill_name": "A/B Testing", "aliases": ["ab testing"]}],
        "alias_updates": [
            {"target_skill_name": "Python", "aliases": ["python programming"]}
        ],
    }
    merged_taxonomy = merge_taxonomies(base_taxonomy, overlay)

    report = build_taxonomy_merge_report(base_taxonomy, overlay, merged_taxonomy)

    assert report == {
        "base_skill_count": 2,
        "custom_skills_added": 1,
        "alias_updates_applied": 1,
        "merged_skill_count": 3,
        "added_skills": ["A/B Testing"],
        "updated_skills": ["Python"],
    }


def test_taxonomy_merge_cli_writes_merged_taxonomy(
    tmp_path: Path,
    capsys,
) -> None:
    base_path = tmp_path / "skills.json"
    custom_path = tmp_path / "custom_taxonomy.json"
    output_path = tmp_path / "skills_merged.json"
    base_path.write_text(json.dumps(_base_taxonomy()), encoding="utf-8")
    custom_path.write_text(
        json.dumps(
            {
                "version": 1,
                "custom_skills": [
                    {
                        "skill_name": "Carbon Footprint Analysis",
                        "aliases": ["carbon footprint analysis"],
                    }
                ],
                "alias_updates": [
                    {
                        "target_skill_name": "Face Recognition",
                        "aliases": ["nhan dien khuon mat"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    exit_code = taxonomy_merge_main(
        [
            "--base",
            str(base_path),
            "--custom",
            str(custom_path),
            "--output",
            str(output_path),
        ]
    )

    captured = capsys.readouterr()
    merged_taxonomy = load_taxonomy(output_path)

    assert exit_code == 0
    assert "Custom skills added: 1" in captured.out
    assert "Alias updates applied: 1" in captured.out
    assert "Carbon Footprint Analysis" in merged_taxonomy
    assert "nhan dien khuon mat" in merged_taxonomy["Face Recognition"]["aliases"]


def _base_taxonomy() -> dict:
    return {
        "Python": {
            "aliases": ["python"],
            "category": "Programming Language",
            "related": [],
            "transferable": [],
        },
        "Face Recognition": {
            "aliases": ["face recognition", "facial recognition"],
            "category": "Computer Vision",
            "related": ["Computer Vision"],
            "transferable": [],
        },
    }
