"""CLI for exporting a merged runtime taxonomy from an Admin-approved overlay."""

from __future__ import annotations

import argparse
import sys

from src.screening_pipeline import DEFAULT_TAXONOMY_PATH
from src.skill_taxonomy import load_taxonomy
from src.taxonomy_merge import (
    build_taxonomy_merge_report,
    load_custom_taxonomy_overlay,
    merge_taxonomies,
    save_merged_taxonomy,
)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for taxonomy merge/export."""
    parser = argparse.ArgumentParser(
        description=(
            "Merge the base skill taxonomy with an Admin-approved custom taxonomy "
            "overlay and export one runtime taxonomy JSON file."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version="semantic-skills-taxonomy-merge 0.16.0",
    )
    parser.add_argument(
        "--base",
        default=DEFAULT_TAXONOMY_PATH,
        help=f"Path to the base taxonomy JSON file. Default: {DEFAULT_TAXONOMY_PATH}",
    )
    parser.add_argument(
        "--custom",
        required=True,
        help="Path to the Admin-approved custom taxonomy overlay JSON file.",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save the merged runtime taxonomy JSON file.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run taxonomy merge/export."""
    _configure_terminal_encoding()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        base_taxonomy = load_taxonomy(args.base)
        custom_overlay = load_custom_taxonomy_overlay(args.custom)
        merged_taxonomy = merge_taxonomies(base_taxonomy, custom_overlay)
        saved_path = save_merged_taxonomy(merged_taxonomy, args.output)
        report = build_taxonomy_merge_report(
            base_taxonomy,
            custom_overlay,
            merged_taxonomy,
        )
    except (FileNotFoundError, IsADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    print("Semantic Skills Taxonomy Merge")
    print(f"Base skills: {report['base_skill_count']}")
    print(f"Custom skills added: {report['custom_skills_added']}")
    print(f"Alias updates applied: {report['alias_updates_applied']}")
    print(f"Merged skills: {report['merged_skill_count']}")
    print(f"Output: {saved_path}")
    return 0


def _configure_terminal_encoding() -> None:
    """Prefer UTF-8 terminal output for bilingual taxonomy names."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue

        try:
            reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            continue


if __name__ == "__main__":
    raise SystemExit(main())
