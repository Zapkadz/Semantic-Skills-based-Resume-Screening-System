# Phase 08 Refactoring Plan - Scoring and Ranking

## 1. Current status

Phase 08 adds `src/scorer.py` as the scoring boundary for the MVP pipeline.

The module currently owns:

- Score weights.
- Evidence level score mapping.
- Recommendation thresholds.
- Candidate score calculation.
- Ranking.
- Baseline experience estimation.
- Baseline seniority detection.
- Baseline domain detection.

All Phase 08 tests pass with the current structure.

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 08.

The scorer is still small enough to keep in one module. Splitting too early into `experience_analyzer.py`, `seniority_detector.py`, and `domain_analyzer.py` would add files without reducing meaningful complexity yet.

## 3. What should stay stable

The following public functions should stay stable for Phase 09:

- `score_candidate`
- `rank_candidates`
- `calculate_final_score`
- `get_recommendation_label`
- `get_missing_skills`

Phase 09 review card generation should consume scorer output instead of recalculating scoring logic.

## 4. Candidate future refactors

Refactor only when one of these conditions happens:

- Experience parsing supports many date formats or overlapping jobs.
- Seniority detection needs more title normalization rules.
- Domain detection starts using taxonomy categories or structured project tags.
- Scoring weights become configurable.
- The Streamlit UI needs reusable explanations for each score component.

Possible future split:

```text
src/
|-- scorer.py
|-- experience_analyzer.py
|-- seniority_detector.py
`-- domain_analyzer.py
```

## 5. Risks to watch

- Double-counting experience if multiple roles overlap.
- Domain false positives from broad words like "testing" or "service".
- Seniority labels that conflict with experience years.
- Recommendation labels being treated as automatic hiring decisions.
- Score weights being changed without tests.

## 6. Next phase notes

Phase 09 should build the explainable review card from scorer output:

- Candidate name.
- Final score.
- Recommendation label.
- Score component breakdown.
- Matched skills.
- Missing skills.
- Evidence snippets.
- Nice-to-have matches.

Phase 09 should not duplicate scoring formulas.
