"""CLI entry point for the Semantic Skills resume screening project.

Phase 01 only verifies that the project foundation is ready.
Business logic starts in later phases.
"""

from __future__ import annotations

import argparse


PROJECT_NAME = "Semantic Skills-based Resume Screening System"
CURRENT_PHASE = "Phase 01 - Project Foundation"


def build_parser() -> argparse.ArgumentParser:
    """Build the minimal CLI parser for the project foundation phase."""
    parser = argparse.ArgumentParser(
        description=(
            "Project foundation CLI for the Semantic Skills-based Resume "
            "Screening System."
        )
    )
    parser.add_argument(
        "--version",
        action="version",
        version="semantic-skills-resume-screening 0.1.0-foundation",
    )
    return parser


def main() -> None:
    """Run the minimal foundation command."""
    parser = build_parser()
    parser.parse_args()

    print(PROJECT_NAME)
    print(CURRENT_PHASE)
    print("Foundation is ready. Business logic starts in Phase 02.")


if __name__ == "__main__":
    main()
