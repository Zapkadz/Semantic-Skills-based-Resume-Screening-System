"""CLI entry point for the Semantic Skills resume screening project."""

from __future__ import annotations

import argparse

from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    format_ranking_summary,
    run_screening_pipeline,
    save_pipeline_result_json,
    save_review_cards,
)
from src.review_card_generator import format_review_card_markdown


PROJECT_NAME = "Semantic Skills-based Resume Screening System"
CURRENT_PHASE = "Phase 10 - CLI Pipeline and Output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for the screening pipeline."""
    parser = argparse.ArgumentParser(
        description=(
            "Run the Semantic Skills-based Resume Screening System for one "
            "job description and a directory of text resumes."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version="semantic-skills-resume-screening 0.10.0-cli-pipeline",
    )
    parser.add_argument(
        "--jd",
        required=True,
        help="Path to the job description .txt file.",
    )
    parser.add_argument(
        "--cv-dir",
        required=True,
        help="Path to the directory containing resume .txt files.",
    )
    parser.add_argument(
        "--taxonomy",
        default=DEFAULT_TAXONOMY_PATH,
        help=f"Path to the skill taxonomy JSON file. Default: {DEFAULT_TAXONOMY_PATH}",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path to save the full ranking result as JSON.",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional directory to save Markdown review cards.",
    )
    parser.add_argument(
        "--show-review-cards",
        action="store_true",
        help="Print Markdown review cards after the ranking summary.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI screening pipeline."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = run_screening_pipeline(
            jd_path=args.jd,
            cv_dir=args.cv_dir,
            taxonomy_path=args.taxonomy,
        )
    except (FileNotFoundError, IsADirectoryError, NotADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    print(format_ranking_summary(result))

    if args.output_json:
        saved_path = save_pipeline_result_json(result, args.output_json)
        print(f"\nSaved JSON: {saved_path}")

    if args.output_dir:
        saved_paths = save_review_cards(result, args.output_dir)
        print(f"Saved review cards: {len(saved_paths)} file(s) in {args.output_dir}")

    if args.show_review_cards:
        _print_review_cards(result)

    return 0


def _print_review_cards(result: dict) -> None:
    """Print generated Markdown review cards to the terminal."""
    for candidate in result.get("candidates", []):
        review_card = candidate.get("review_card", {})
        print("\n---")
        print(format_review_card_markdown(review_card))


if __name__ == "__main__":
    raise SystemExit(main())
