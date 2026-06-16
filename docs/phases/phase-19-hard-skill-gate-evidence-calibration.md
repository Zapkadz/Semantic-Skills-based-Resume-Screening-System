# Phase 19 - Hard-skill Gate and Evidence Calibration

## Goal

Phase 19 adds a minimum hard-skill evidence gate on top of the existing weighted
score. The weighted score still ranks candidates, but a candidate should not
receive `Review` or `Strong Review` when must-have technical skills are mostly
missing or only weakly evidenced.

This phase addresses a recruiter-facing concern:

- Experience and seniority are useful support signals.
- They should not override missing must-have technical evidence.
- The system should explain when a score is capped.

## Rationale

The project follows a scorecard-style screening flow:

```text
JD requirements
-> skill/taxonomy matching
-> evidence detection
-> weighted score
-> hard-skill gate
-> final score + recommendation + review card
```

The weighted score remains:

```text
skill_semantic: 40%
evidence:       20%
experience:     15%
seniority:      10%
domain:         10%
nice_to_have:    5%
```

Phase 19 does not replace that score. It adds a gate after scoring:

```text
base_score = weighted score
if base_score >= Review threshold and hard-skill evidence is weak:
    final_score = min(base_score, 69)
```

This keeps the formula transparent while preventing high experience/domain
scores from hiding hard-skill gaps.

## Gate Rules

For `Review` and above, cap the score at `69` when any of these is true:

- `skill_semantic < 0.55`
- `evidence < 0.50`
- confirmed hard-skill evidence coverage `< 0.60`

Confirmed coverage means:

```text
confirmed_match_count / total_must_have
```

A confirmed match is a positive must-have match with `evidence_level >= 2`.

For `Strong Review`, cap the score at `84` when:

- base score is at least `85`
- confirmed hard-skill evidence coverage is below `0.75`

## Output Contract

Candidate output keeps the old fields:

- `final_score`
- `recommendation`
- `scores`
- `matched_skills`
- `missing_skills`
- `review_card`

Phase 19 adds:

- `base_score`: weighted score before the hard-skill gate.
- `hard_skill_gate`: gate status, score cap, reasons, and coverage metrics.

Example:

```json
{
  "base_score": 72,
  "final_score": 69,
  "recommendation": "Maybe Review",
  "hard_skill_gate": {
    "passed": false,
    "applied": true,
    "score_cap": 69,
    "reasons": [
      {
        "code": "weak_evidence",
        "message": "Evidence strength is below the Review threshold."
      }
    ],
    "metrics": {
      "total_must_have": 16,
      "positive_match_count": 13,
      "confirmed_match_count": 5,
      "missing_count": 3,
      "confirmed_coverage": 0.3125
    }
  }
}
```

## Review Card Behavior

When the gate is applied, the review card explains that:

- the candidate may meet experience/domain expectations;
- the final recommendation was capped because hard-skill evidence is incomplete;
- missing and weakly evidenced must-have skills should be reviewed before
  shortlisting.

## Acceptance Criteria

- Existing strong demo candidate remains `Strong Review`.
- A high-experience candidate with weak hard-skill evidence is capped below
  `Review`.
- API output remains backward compatible for web fields already in use.
- Review card includes a clear hard-skill gate concern when the cap is applied.
- Full `pytest` passes.
