"""CLI for building pending taxonomy suggestions from screening results."""

from __future__ import annotations

import argparse
import sys

from src.embedding_matcher import (
    DEFAULT_EMBEDDING_MODEL,
    build_embedding_matcher,
)
from src.screening_pipeline import DEFAULT_TAXONOMY_PATH
from src.skill_taxonomy import load_taxonomy
from src.taxonomy_suggestion import (
    DEFAULT_MIN_FREQUENCY,
    build_taxonomy_suggestions,
    collect_unknown_requirement_observations_from_results,
    load_screening_results,
    save_taxonomy_suggestions,
)


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for taxonomy suggestion generation."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate a pending taxonomy suggestion queue from one or more "
            "screening result JSON files."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version="semantic-skills-taxonomy-suggest 0.15.0",
    )
    parser.add_argument(
        "--input-json",
        nargs="+",
        required=True,
        help="One or more screening result JSON files.",
    )
    parser.add_argument(
        "--output-json",
        required=True,
        help="Path to save the taxonomy suggestion queue JSON.",
    )
    parser.add_argument(
        "--taxonomy",
        default=DEFAULT_TAXONOMY_PATH,
        help=f"Path to the skill taxonomy JSON file. Default: {DEFAULT_TAXONOMY_PATH}",
    )
    parser.add_argument(
        "--min-frequency",
        type=int,
        default=DEFAULT_MIN_FREQUENCY,
        help=f"Minimum observation frequency for a suggestion. Default: {DEFAULT_MIN_FREQUENCY}",
    )
    parser.add_argument(
        "--enable-embedding",
        action="store_true",
        help=(
            "Enable optional embedding support for grouping and nearest-skill lookup. "
            "The command still works without embeddings."
        ),
    )
    parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help=f"Embedding model name. Default: {DEFAULT_EMBEDDING_MODEL}",
    )
    parser.add_argument(
        "--embedding-local-only",
        action="store_true",
        help="Load the embedding model from the local Hugging Face cache only.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run taxonomy suggestion generation."""
    _configure_terminal_encoding()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        taxonomy = load_taxonomy(args.taxonomy)
        screening_results = []
        for input_json in args.input_json:
            screening_results.extend(load_screening_results(input_json))

        observations = collect_unknown_requirement_observations_from_results(
            screening_results
        )
        embedding_matcher = build_embedding_matcher(
            enabled=args.enable_embedding,
            model_name=args.embedding_model,
            local_files_only=args.embedding_local_only,
        )
        suggestions = build_taxonomy_suggestions(
            observations,
            taxonomy,
            embedding_matcher=embedding_matcher,
            min_frequency=args.min_frequency,
        )
        saved_path = save_taxonomy_suggestions(suggestions, args.output_json)
    except (FileNotFoundError, IsADirectoryError, ValueError) as exc:
        parser.error(str(exc))

    print("Semantic Skills Taxonomy Suggestion Queue")
    print(f"Input files: {len(args.input_json)}")
    print(f"Unknown observations: {len(observations)}")
    print(f"Suggestions: {len(suggestions)}")
    print(f"Saved JSON: {saved_path}")
    return 0


def _configure_terminal_encoding() -> None:
    """Prefer UTF-8 terminal output for bilingual suggestion names."""
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
