"""CLI entry point for the Semantic Skills resume screening project."""

from __future__ import annotations

import argparse
import sys

from src.embedding_matcher import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_SEMANTIC_THRESHOLD,
    build_embedding_matcher,
)
from src.review_card_generator import format_review_card_markdown
from src.screening_pipeline import (
    DEFAULT_TAXONOMY_PATH,
    format_ranking_summary,
    run_screening_pipeline,
    save_pipeline_result_json,
    save_review_cards,
)


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
        version="semantic-skills-resume-screening 0.13.0-local-multilingual-embedding",
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
    parser.add_argument(
        "--enable-embedding",
        action="store_true",
        help=(
            "Enable optional local multilingual embedding semantic matching. "
            "The pipeline falls back to rule-based matching if the model is unavailable."
        ),
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help=f"Embedding model name. Default: {DEFAULT_EMBEDDING_MODEL}",
    )
    parser.add_argument(
        "--embedding-threshold",
        type=float,
        default=DEFAULT_SEMANTIC_THRESHOLD,
        help=f"Semantic match threshold. Default: {DEFAULT_SEMANTIC_THRESHOLD}",
    )
    parser.add_argument(
        "--embedding-local-only",
        action="store_true",
        help=(
            "Load the embedding model from the local Hugging Face cache only. "
            "Use this after pre-downloading the model for offline or stable demos."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI screening pipeline."""
    _configure_terminal_encoding()
    parser = build_parser()
    args = parser.parse_args(argv)
    embedding_matcher = build_embedding_matcher(
        enabled=args.enable_embedding,
        model_name=args.embedding_model,
        threshold=args.embedding_threshold,
        local_files_only=args.embedding_local_only,
    )

    try:
        result = run_screening_pipeline(
            jd_path=args.jd,
            cv_dir=args.cv_dir,
            taxonomy_path=args.taxonomy,
            embedding_matcher=embedding_matcher,
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


def _configure_terminal_encoding() -> None:
    """Prefer UTF-8 terminal output for Vietnamese candidate names."""
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
