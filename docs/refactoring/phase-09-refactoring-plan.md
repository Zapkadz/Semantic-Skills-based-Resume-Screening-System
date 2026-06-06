# Phase 09 Refactoring Plan - Explainable Review Card

## 1. Current status

Phase 09 adds `src/review_card_generator.py`.

The module currently owns:

- Structured review card generation.
- Markdown formatting.
- Evidence highlight selection.
- Strength generation.
- Concern generation.
- Interview question generation.

All Phase 09 tests pass with the current structure.

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 09.

The module is intentionally kept separate from `src/scorer.py` so review card generation does not duplicate or modify scoring formulas. This keeps the scoring boundary stable and makes explanation logic easier to test.

## 3. What should stay stable

The following public functions should stay stable for Phase 10:

- `generate_review_card`
- `format_review_card_markdown`

Phase 10 CLI work should consume these functions instead of reimplementing review card formatting in `main.py`.

## 4. Candidate future refactors

Refactor only when one of these conditions happens:

- Markdown formatting grows beyond simple terminal output.
- The Streamlit UI needs display-specific formatting.
- Interview question generation needs many role-specific templates.
- Review cards need export to JSON, HTML, PDF, or DOCX.
- Explanations need localization.

Possible future split:

```text
src/
|-- review_card_generator.py
|-- review_card_formatter.py
`-- interview_question_generator.py
```

## 5. Risks to watch

- Review card logic recalculating scores instead of reading scorer output.
- Concerns sounding like automatic rejection.
- Interview questions repeating because multiple skills share one evidence sentence.
- Review card becoming too long when a candidate has many matched skills.
- UI or CLI code duplicating review card generation rules.

## 6. Next phase notes

Phase 10 should wire the pipeline into CLI flow:

- Load one JD.
- Load all CV `.txt` files in a directory.
- Parse and normalize data.
- Match skills.
- Detect evidence.
- Score and rank candidates.
- Generate review cards.
- Print or save results.

Phase 10 should not change scoring or review card rules unless tests expose a bug.
