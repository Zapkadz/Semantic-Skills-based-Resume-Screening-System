"""Structured candidate-side skill-gap explanation and CV suggestions."""

from __future__ import annotations

from typing import Any


MAX_IMPROVEMENT_SUGGESTIONS = 8
MAX_NEXT_BEST_ACTIONS = 4


def explain_skill_gaps(
    candidate_result: dict[str, Any],
    job_output: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build structured skill-gap output for one candidate-vs-job result."""
    matched_skills = list(candidate_result.get("matched_skills", []))
    missing_skills = list(candidate_result.get("missing_skills", []))
    nice_to_have_matches = list(candidate_result.get("nice_to_have_matches", []))
    score_breakdown = dict(candidate_result.get("scores", {}))
    hard_skill_gate = dict(candidate_result.get("hard_skill_gate", {}))
    role_alignment_impact = dict(candidate_result.get("role_alignment_impact", {}))
    core_requirement_fit_summary = dict(
        candidate_result.get("core_requirement_fit_summary", {})
    )
    job_output = job_output or {}

    skill_gaps = {
        "missing_must_have": build_missing_must_have_gaps(missing_skills),
        "weak_evidence": build_weak_evidence_gaps(matched_skills),
        "optional_growth": build_optional_growth_gaps(nice_to_have_matches),
        "presentation_gaps": build_presentation_gaps(
            score_breakdown,
            hard_skill_gate,
            matched_skills,
            job_output,
            role_alignment_impact,
            core_requirement_fit_summary,
        ),
    }
    skill_gap_summary = build_skill_gap_summary(skill_gaps)
    cv_improvement_suggestions = build_cv_improvement_suggestions(skill_gaps)
    next_best_actions = build_next_best_actions(cv_improvement_suggestions)

    return {
        "skill_gap_summary": skill_gap_summary,
        "skill_gaps": skill_gaps,
        "cv_improvement_suggestions": cv_improvement_suggestions,
        "next_best_actions": next_best_actions,
    }


def build_missing_must_have_gaps(missing_skills: list[str]) -> list[dict[str, Any]]:
    """Build structured missing must-have skill gaps."""
    return [
        {
            "skill": skill,
            "gap_type": "missing_must_have",
        }
        for skill in missing_skills
        if isinstance(skill, str) and skill.strip()
    ]


def build_weak_evidence_gaps(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build weak-evidence gaps for matched must-have items with shallow evidence."""
    weak_gaps: list[dict[str, Any]] = []
    seen_skills: set[str] = set()

    for match in matches:
        if match.get("match_type") in {"no_match", "no_semantic_evidence"}:
            continue

        evidence_level = int(match.get("evidence_level", 0))
        if evidence_level > 1:
            continue

        skill = str(match.get("required_skill", "")).strip()
        if not skill or skill in seen_skills:
            continue

        seen_skills.add(skill)
        weak_gaps.append(
            {
                "skill": skill,
                "gap_type": "weak_evidence",
                "current_evidence_level": evidence_level,
                "match_type": match.get("match_type", ""),
            }
        )

    return weak_gaps


def build_optional_growth_gaps(
    nice_to_have_matches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build optional growth gaps from missing nice-to-have matches."""
    optional_gaps: list[dict[str, Any]] = []
    seen_skills: set[str] = set()

    for match in nice_to_have_matches:
        if match.get("match_type") != "no_match":
            continue

        skill = str(match.get("required_skill", "")).strip()
        if not skill or skill in seen_skills:
            continue

        seen_skills.add(skill)
        optional_gaps.append(
            {
                "skill": skill,
                "gap_type": "optional_growth",
            }
        )

    return optional_gaps


def build_presentation_gaps(
    score_breakdown: dict[str, float],
    hard_skill_gate: dict[str, Any],
    matched_skills: list[dict[str, Any]],
    job_output: dict[str, Any] | None = None,
    role_alignment_impact: dict[str, Any] | None = None,
    core_requirement_fit_summary: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Build CV presentation gaps when skills may exist but evidence is under-surfaced."""
    presentation_gaps: list[dict[str, Any]] = []
    job_output = job_output or {}
    role_alignment_impact = role_alignment_impact or {}
    core_requirement_fit_summary = core_requirement_fit_summary or {}
    core_bucket = _requirement_fit_bucket(core_requirement_fit_summary, "core")

    if float(score_breakdown.get("evidence", 0.0)) < 0.50:
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Add project or work bullets with technologies, responsibilities, "
                    "and measurable outcomes to strengthen evidence."
                ),
            }
        )

    if hard_skill_gate.get("applied") is True:
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Make must-have technical evidence more explicit so the role is not capped by the hard-skill gate."
                ),
            }
        )

    if _has_many_weak_matches(matched_skills):
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Several matched skills are still keyword-level; rewrite them as concrete experience or project bullets."
                ),
            }
        )

    if (
        int(core_bucket.get("total", 0)) >= 2
        and float(core_bucket.get("confirmed_coverage", 0.0)) < 0.5
    ):
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Prioritize concrete bullets for the job's core technical requirements before adding extra optional skills."
                ),
            }
        )

    if role_alignment_impact.get("applied") is True:
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Show more direct evidence for the target role family so the match is not driven mainly by adjacent-role or semantic overlap."
                ),
            }
        )

    domain_context = list(
        job_output.get("requirement_groups", {}).get("domain_context", [])
    )
    if domain_context and float(score_breakdown.get("domain", 0.0)) >= 0.50:
        presentation_gaps.append(
            {
                "gap_type": "presentation",
                "message": (
                    "Mention the business or domain context more explicitly so the job fit is easier to detect."
                ),
            }
        )

    return _dedupe_gap_messages(presentation_gaps)


def build_skill_gap_summary(skill_gaps: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    """Summarize structured skill-gap counts for compact UI rendering."""
    return {
        "missing_must_have_count": len(skill_gaps.get("missing_must_have", [])),
        "weak_evidence_count": len(skill_gaps.get("weak_evidence", [])),
        "optional_growth_count": len(skill_gaps.get("optional_growth", [])),
        "presentation_gap_count": len(skill_gaps.get("presentation_gaps", [])),
    }


def build_cv_improvement_suggestions(
    skill_gaps: dict[str, list[dict[str, Any]]],
) -> list[str]:
    """Build ordered candidate-facing CV improvement suggestions."""
    suggestions: list[str] = []

    for gap in skill_gaps.get("missing_must_have", []):
        skill = str(gap.get("skill", "")).strip()
        if skill:
            suggestions.append(
                f"If you have real experience with {skill}, add it explicitly in your Skills section and mention one concrete usage example in work or projects."
            )

    for gap in skill_gaps.get("weak_evidence", []):
        skill = str(gap.get("skill", "")).strip()
        if skill:
            suggestions.append(
                f"Move {skill} from a keyword-only mention into a work or project bullet with technologies, responsibilities, and outcomes."
            )

    for gap in skill_gaps.get("optional_growth", []):
        skill = str(gap.get("skill", "")).strip()
        if skill:
            suggestions.append(
                f"If you have real exposure to {skill}, add it as an optional growth strength for similar roles."
            )

    for gap in skill_gaps.get("presentation_gaps", []):
        message = str(gap.get("message", "")).strip()
        if message:
            suggestions.append(message)

    return _dedupe_suggestions(suggestions)[:MAX_IMPROVEMENT_SUGGESTIONS]


def build_next_best_actions(
    cv_improvement_suggestions: list[str],
) -> list[str]:
    """Pick the most useful next actions for compact UI rendering."""
    return cv_improvement_suggestions[:MAX_NEXT_BEST_ACTIONS]


def _has_many_weak_matches(matches: list[dict[str, Any]]) -> bool:
    """Return True when weak evidence dominates the positive skill matches."""
    positive_matches = [
        match
        for match in matches
        if match.get("match_type") not in {"no_match", "no_semantic_evidence"}
    ]
    if not positive_matches:
        return False

    weak_matches = [
        match
        for match in positive_matches
        if int(match.get("evidence_level", 0)) <= 1
    ]
    return len(weak_matches) >= 2 and len(weak_matches) / len(positive_matches) >= 0.5


def _dedupe_suggestions(suggestions: list[str]) -> list[str]:
    """Deduplicate suggestion strings while preserving order."""
    deduped: list[str] = []
    seen: set[str] = set()
    for suggestion in suggestions:
        normalized = " ".join(suggestion.casefold().split())
        if not suggestion or normalized in seen:
            continue

        seen.add(normalized)
        deduped.append(suggestion)

    return deduped


def _dedupe_gap_messages(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Deduplicate presentation gap messages while preserving order."""
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for gap in gaps:
        message = str(gap.get("message", "")).strip()
        normalized = " ".join(message.casefold().split())
        if not message or normalized in seen:
            continue

        seen.add(normalized)
        deduped.append(gap)

    return deduped


def _requirement_fit_bucket(summary: dict[str, Any], bucket_name: str) -> dict[str, Any]:
    """Return one nested requirement-fit bucket with safe defaults."""
    bucket = summary.get(bucket_name, {})
    return bucket if isinstance(bucket, dict) else {}
