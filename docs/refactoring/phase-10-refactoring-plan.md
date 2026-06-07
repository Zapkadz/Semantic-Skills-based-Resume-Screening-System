# Phase 10 Refactoring Plan - CLI Pipeline and Output

## 1. Current status

Phase 10 adds `src/screening_pipeline.py` and upgrades `main.py` from a foundation placeholder to a real CLI adapter.

The pipeline currently owns:

- Loading JD and CV text files.
- Parsing JD and CV documents.
- Skill normalization.
- Must-have and nice-to-have matching.
- Evidence detection.
- Candidate scoring.
- Candidate ranking.
- Review card generation.
- JSON output writing.
- Markdown review card writing.
- Terminal ranking summary formatting.

All Phase 10 tests pass with the current structure.

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 10.

The current split is intentional:

- `src/screening_pipeline.py` owns orchestration.
- `main.py` owns CLI argument parsing and terminal-facing behavior.

This keeps `main.py` small and allows Phase 11 Streamlit work to reuse the same pipeline.

## 3. What should stay stable

The following public functions should stay stable for Phase 11:

- `run_screening_pipeline`
- `save_pipeline_result_json`
- `save_review_cards`
- `format_ranking_summary`

The Streamlit UI should call `run_screening_pipeline` instead of duplicating the module sequence.

## 4. Candidate future refactors

Refactor only when one of these conditions happens:

- Pipeline result schema grows too large.
- PDF/DOCX support introduces multiple document loader paths.
- Output saving needs multiple formats beyond JSON and Markdown.
- CLI needs subcommands.
- Streamlit needs a smaller API for uploaded in-memory files.

Possible future split:

```text
src/
|-- screening_pipeline.py
|-- output_writer.py
`-- cli_formatter.py
```

## 5. Risks to watch

- `main.py` growing into business logic.
- Runtime output accidentally being committed.
- Streamlit reimplementing the same pipeline.
- JSON schema changing without tests.
- CLI printing too much detail by default.
- Error handling becoming unclear when input paths are wrong.

## 6. Next phase notes

Phase 11 should build a simple Streamlit UI on top of the pipeline:

- Select or upload JD text.
- Select or upload CV text files.
- Run analysis.
- Show ranking table.
- Show review card for a selected candidate.

Phase 11 should not change scorer, matcher, evidence, or review card rules unless tests expose a bug.
