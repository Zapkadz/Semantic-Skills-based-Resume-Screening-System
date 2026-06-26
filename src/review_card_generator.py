"""Explainable review card generation from scored candidates."""

from __future__ import annotations

from typing import Any


MAX_EVIDENCE_HIGHLIGHTS = 5
MAX_INTERVIEW_QUESTIONS = 5

SCORE_COMPONENT_ORDER = (
    "skill_semantic",
    "evidence",
    "experience",
    "seniority",
    "domain",
    "nice_to_have",
)

SCORE_COMPONENT_LABELS = {
    "skill_semantic": "Skill semantic",
    "evidence": "Evidence",
    "experience": "Experience",
    "seniority": "Seniority",
    "domain": "Domain",
    "nice_to_have": "Nice-to-have",
}


def generate_review_card(
    candidate_result: dict[str, Any],
    job_criteria: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create a structured recruiter review card from a scored candidate."""
    job_title = _get_job_title(job_criteria)
    matched_skills = list(candidate_result.get("matched_skills", []))
    missing_skills = list(candidate_result.get("missing_skills", []))
    nice_to_have_matches = list(candidate_result.get("nice_to_have_matches", []))
    score_breakdown = dict(candidate_result.get("scores", {}))
    hard_skill_gate = _get_hard_skill_gate(candidate_result)
    role_family_alignment = _get_role_family_alignment(candidate_result)
    role_alignment_impact = _get_role_alignment_impact(candidate_result)
    core_requirement_fit_summary = _get_core_requirement_fit_summary(candidate_result)
    requirement_groups = _get_requirement_groups(job_criteria)
    requirement_group_summary = dict(
        candidate_result.get("requirement_group_summary", {})
    )

    evidence_highlights = build_evidence_highlights(matched_skills)
    strengths = build_strengths(
        score_breakdown,
        evidence_highlights,
        role_family_alignment,
        core_requirement_fit_summary,
    )
    concerns = build_concerns(
        score_breakdown,
        missing_skills,
        nice_to_have_matches,
        matched_skills,
        hard_skill_gate,
        role_family_alignment,
        role_alignment_impact,
        core_requirement_fit_summary,
        candidate_result.get("source_alignment_impact", {}),
    )
    interview_questions = build_interview_questions(
        evidence_highlights,
        missing_skills,
        nice_to_have_matches,
    )

    return {
        "candidate_name": candidate_result.get("candidate_name", ""),
        "job_title": job_title,
        "final_score": candidate_result.get("final_score", 0),
        "recommendation": candidate_result.get("recommendation", ""),
        "summary": build_summary(candidate_result, job_title),
        "score_breakdown": score_breakdown,
        "raw_base_score": candidate_result.get("raw_base_score"),
        "role_calibrated_score": candidate_result.get("role_calibrated_score"),
        "role_score_adjustment": candidate_result.get("role_score_adjustment", 0),
        "source_calibrated_score": candidate_result.get("source_calibrated_score"),
        "source_score_adjustment": candidate_result.get("source_score_adjustment", 0),
        "base_score": candidate_result.get("base_score"),
        "hard_skill_gate": hard_skill_gate,
        "candidate_role_profile": dict(candidate_result.get("candidate_role_profile", {})),
        "role_family_alignment": role_family_alignment,
        "role_alignment_impact": role_alignment_impact,
        "core_requirement_fit_summary": core_requirement_fit_summary,
        "source_requirement_fit_summary": dict(
            candidate_result.get("source_requirement_fit_summary", {})
        ),
        "source_alignment_impact": dict(
            candidate_result.get("source_alignment_impact", {})
        ),
        "decision_confidence": dict(candidate_result.get("decision_confidence", {})),
        "seniority": candidate_result.get("seniority", ""),
        "experience_years": candidate_result.get("experience_years", 0),
        "domain": list(candidate_result.get("domain", [])),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "nice_to_have_matches": nice_to_have_matches,
        "requirement_groups": requirement_groups,
        "requirement_group_summary": requirement_group_summary,
        "requirement_notes": build_requirement_notes(
            requirement_groups,
            role_family_alignment,
        ),
        "evidence_highlights": evidence_highlights,
        "strengths": strengths,
        "concerns": concerns,
        "suggested_interview_questions": interview_questions,
    }


def format_review_card_markdown(review_card: dict[str, Any]) -> str:
    """Format a structured review card as readable Markdown."""
    candidate_name = review_card.get("candidate_name") or "Unknown Candidate"
    lines = [f"# {candidate_name}", ""]

    if review_card.get("job_title"):
        lines.extend([f"Role: {review_card['job_title']}", ""])

    lines.extend(
        [
            f"Score: {review_card.get('final_score', 0)}/100",
            f"Recommendation: {review_card.get('recommendation', '')}",
            "",
            "## Summary",
            review_card.get("summary", ""),
            "",
            "## Score Breakdown",
        ]
    )

    score_breakdown = review_card.get("score_breakdown", {})
    for component in SCORE_COMPONENT_ORDER:
        if component in score_breakdown:
            label = SCORE_COMPONENT_LABELS[component]
            lines.append(f"- {label}: {_format_score(score_breakdown[component])}")

    lines.extend(["", "## Strengths"])
    lines.extend(_format_bullets(review_card.get("strengths", [])))

    lines.extend(["", "## Concerns"])
    lines.extend(_format_bullets(review_card.get("concerns", [])))

    lines.extend(["", "## Evidence Highlights"])
    evidence_highlights = review_card.get("evidence_highlights", [])
    if evidence_highlights:
        for highlight in evidence_highlights:
            skill = highlight["skill"]
            level = highlight["evidence_level"]
            source = highlight["evidence_source"]
            text = highlight["evidence_text"]
            lines.append(f"- {skill} (level {level}, {source}): {text}")
    else:
        lines.append("- No strong evidence highlights found.")

    lines.extend(["", "## Missing Skills"])
    missing_skills = review_card.get("missing_skills", [])
    if missing_skills:
        lines.extend(f"- {skill}" for skill in missing_skills)
    else:
        lines.append("- None")

    requirement_notes = review_card.get("requirement_notes", [])
    if requirement_notes:
        lines.extend(["", "## Requirement Notes"])
        lines.extend(_format_bullets(requirement_notes))

    lines.extend(["", "## Suggested Interview Questions"])
    questions = review_card.get("suggested_interview_questions", [])
    if questions:
        lines.extend(
            f"{index}. {question}"
            for index, question in enumerate(questions, start=1)
        )
    else:
        lines.append("1. Can you walk through the project that best represents your fit for this role?")

    return "\n".join(lines).strip()


def build_summary(candidate_result: dict[str, Any], job_title: str = "") -> str:
    """Build a short recruiter-facing summary sentence."""
    candidate_name = candidate_result.get("candidate_name") or "This candidate"
    recommendation = candidate_result.get("recommendation", "Review")
    final_score = candidate_result.get("final_score", 0)
    base_score = candidate_result.get("base_score")
    raw_base_score = candidate_result.get("raw_base_score")
    role_calibrated_score = candidate_result.get("role_calibrated_score", base_score)
    role_score_adjustment = int(candidate_result.get("role_score_adjustment", 0) or 0)
    source_calibrated_score = candidate_result.get("source_calibrated_score", base_score)
    source_score_adjustment = int(
        candidate_result.get("source_score_adjustment", 0) or 0
    )
    role_alignment_impact = _get_role_alignment_impact(candidate_result)
    source_alignment_impact = _get_source_alignment_impact(candidate_result)
    hard_skill_gate = _get_hard_skill_gate(candidate_result)
    role_text = f" for {job_title}" if job_title else ""
    notes: list[str] = []

    if (
        role_score_adjustment != 0
        and raw_base_score is not None
        and role_calibrated_score is not None
    ):
        role_reason = _strip_sentence_end(str(role_alignment_impact.get("reason", "")).strip())
        role_note = (
            "Role-aware calibration adjusted the weighted score from "
            f"{raw_base_score}/100 to {role_calibrated_score}/100"
        )
        if role_reason:
            role_note += f" because {role_reason[:1].casefold() + role_reason[1:]}"
        role_note += "."
        notes.append(role_note)

    if (
        source_score_adjustment != 0
        and role_calibrated_score is not None
        and source_calibrated_score is not None
    ):
        source_reason = _strip_sentence_end(
            str(source_alignment_impact.get("reason", "")).strip()
        )
        source_note = (
            "Source-aware calibration adjusted the score from "
            f"{role_calibrated_score}/100 to {source_calibrated_score}/100"
        )
        if source_reason:
            source_note += f" because {source_reason[:1].casefold() + source_reason[1:]}"
        source_note += "."
        notes.append(source_note)

    if hard_skill_gate.get("applied") is True and base_score is not None:
        notes.append(
            f"The hard-skill gate capped the base score from {base_score}/100 "
            "because must-have skill evidence is incomplete."
        )

    summary = (
        f"{candidate_name} is a {recommendation} candidate{role_text} "
        f"with a final score of {final_score}/100."
    )
    if notes:
        summary += " " + " ".join(note.strip() for note in notes if note.strip())

    return summary


def build_evidence_highlights(
    matched_skills: list[dict[str, Any]],
    limit: int = MAX_EVIDENCE_HIGHLIGHTS,
) -> list[dict[str, Any]]:
    """Select strong evidence snippets from matched skill results."""
    highlights: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()

    for match in matched_skills:
        if match.get("match_type") == "no_match":
            continue
        if int(match.get("evidence_level", 0)) < 2:
            continue

        evidence_text = str(match.get("evidence_text", "")).strip()
        if not evidence_text:
            continue

        skill = _display_skill(match)
        seen_key = (_normalize_text(skill), _normalize_text(evidence_text))
        if seen_key in seen_keys:
            continue

        seen_keys.add(seen_key)
        highlights.append(
            {
                "skill": skill,
                "required_skill": match.get("required_skill", ""),
                "candidate_skill": match.get("candidate_skill"),
                "match_type": match.get("match_type", ""),
                "evidence_level": int(match.get("evidence_level", 0)),
                "evidence_text": evidence_text,
                "evidence_source": match.get("evidence_source", "none"),
            }
        )

        if len(highlights) >= limit:
            break

    return highlights


def build_strengths(
    score_breakdown: dict[str, float],
    evidence_highlights: list[dict[str, Any]],
    role_family_alignment: dict[str, Any] | None = None,
    core_requirement_fit_summary: dict[str, Any] | None = None,
) -> list[str]:
    """Build rule-based strengths from score components and evidence."""
    strengths: list[str] = []
    role_family_alignment = role_family_alignment or {}
    core_requirement_fit_summary = core_requirement_fit_summary or {}
    core_bucket = _requirement_fit_bucket(core_requirement_fit_summary, "core")

    if score_breakdown.get("skill_semantic", 0.0) >= 0.85:
        strengths.append("Strong must-have skill coverage.")
    elif score_breakdown.get("skill_semantic", 0.0) >= 0.70:
        strengths.append("Solid must-have skill coverage.")

    if score_breakdown.get("evidence", 0.0) >= 0.85:
        strengths.append("Strong evidence in work or project descriptions.")
    elif score_breakdown.get("evidence", 0.0) >= 0.60:
        strengths.append("Some practical evidence is present.")

    if score_breakdown.get("domain", 0.0) >= 0.85:
        strengths.append("Good domain alignment with the role.")

    if score_breakdown.get("seniority", 0.0) >= 0.85:
        strengths.append("Seniority appears aligned with the role.")

    if score_breakdown.get("experience", 0.0) >= 0.75:
        strengths.append("Experience level appears close to the requirement.")

    if role_family_alignment.get("status") == "strong_alignment":
        strengths.append("Role-family alignment appears strong for this position.")
    elif role_family_alignment.get("status") == "partial_alignment":
        strengths.append("The profile shows adjacent role-family overlap with this position.")

    if (
        int(core_bucket.get("total", 0)) >= 2
        and float(core_bucket.get("confirmed_coverage", 0.0)) >= 0.67
    ):
        strengths.append("Most core technical requirements have confirmed evidence.")

    highlight_skills = [highlight["skill"] for highlight in evidence_highlights]
    if highlight_skills:
        strengths.append(
            f"Clear evidence for {_join_readable_list(highlight_skills)}."
        )

    if not strengths:
        strengths.append("No strong positive signal stands out from the available data.")

    return strengths


def build_concerns(
    score_breakdown: dict[str, float],
    missing_skills: list[str],
    nice_to_have_matches: list[dict[str, Any]],
    matched_skills: list[dict[str, Any]] | None = None,
    hard_skill_gate: dict[str, Any] | None = None,
    role_family_alignment: dict[str, Any] | None = None,
    role_alignment_impact: dict[str, Any] | None = None,
    core_requirement_fit_summary: dict[str, Any] | None = None,
    source_alignment_impact: dict[str, Any] | None = None,
) -> list[str]:
    """Build rule-based concerns from missing skills and low score components."""
    concerns: list[str] = []
    matched_skills = matched_skills or []
    hard_skill_gate = hard_skill_gate or {}
    role_family_alignment = role_family_alignment or {}
    role_alignment_impact = role_alignment_impact or {}
    core_requirement_fit_summary = core_requirement_fit_summary or {}
    source_alignment_impact = source_alignment_impact or {}
    core_bucket = _requirement_fit_bucket(core_requirement_fit_summary, "core")

    if hard_skill_gate.get("applied") is True:
        concerns.append(_format_hard_skill_gate_concern(hard_skill_gate))
    elif _meets_experience_but_has_incomplete_hard_skill_evidence(
        score_breakdown,
        missing_skills,
        matched_skills,
    ):
        concerns.append(
            (
                "The candidate appears to meet the experience requirement, "
                "but hard-skill evidence is incomplete; review missing and "
                "weakly evidenced must-have skills before shortlisting."
            )
        )

    if (
        int(core_bucket.get("total", 0)) >= 2
        and float(core_bucket.get("confirmed_coverage", 0.0)) < 0.5
    ):
        concerns.append(
            "Core technical requirements are still missing or weakly evidenced."
        )

    if missing_skills:
        concerns.append(
            f"Missing must-have skills: {_join_readable_list(missing_skills)}."
        )

    if score_breakdown.get("evidence", 0.0) < 0.50:
        concerns.append("Evidence is weak or mostly keyword-level.")

    if score_breakdown.get("experience", 0.0) < 0.50:
        concerns.append("Experience may be below the job requirement.")

    if score_breakdown.get("domain", 0.0) < 0.50:
        concerns.append("Domain alignment may need recruiter review.")

    if score_breakdown.get("seniority", 0.0) < 0.65:
        concerns.append("Seniority may be below the job expectation.")

    nice_to_have_gaps = [
        str(match.get("required_skill", "")).strip()
        for match in nice_to_have_matches
        if match.get("match_type") == "no_match"
        and str(match.get("required_skill", "")).strip()
    ]
    if nice_to_have_gaps:
        concerns.append(
            f"Optional nice-to-have gaps: {_join_readable_list(nice_to_have_gaps)}."
        )

    semantic_only_requirements = [
        str(match.get("required_skill", "")).strip()
        for match in matched_skills
        if match.get("match_type") == "semantic_only_match"
        and str(match.get("required_skill", "")).strip()
    ]
    if semantic_only_requirements:
        concerns.append(
            (
                "Some requirements were evaluated with semantic-only evidence "
                f"outside the taxonomy: {_join_readable_list(semantic_only_requirements)}."
            )
        )

    if role_alignment_impact.get("applied") is True:
        impact_reason = str(role_alignment_impact.get("reason", "")).strip()
        if impact_reason:
            concerns.append(
                f"Role-aware calibration reduced the score: {impact_reason}"
            )

    if source_alignment_impact.get("applied") is True:
        impact_reason = str(source_alignment_impact.get("reason", "")).strip()
        if impact_reason:
            concerns.append(
                f"Source-aware calibration adjusted the score: {impact_reason}"
            )

    if (
        role_alignment_impact.get("applied") is not True
        and role_family_alignment.get("status") == "misaligned"
    ):
        concerns.append(
            str(role_family_alignment.get("note", "")).strip()
            or "The candidate's strongest technical profile appears misaligned with the JD role family."
        )
    elif (
        role_alignment_impact.get("applied") is not True
        and role_family_alignment.get("status") == "partial_alignment"
    ):
        concerns.append(
            str(role_family_alignment.get("note", "")).strip()
            or "The candidate only partially overlaps with the JD role family."
        )

    if not concerns:
        concerns.append("No major concerns detected from the available scoring signals.")

    return concerns


def _format_hard_skill_gate_concern(hard_skill_gate: dict[str, Any]) -> str:
    """Build a concise recruiter-facing concern for a score cap."""
    base_score = hard_skill_gate.get("base_score")
    final_score = hard_skill_gate.get("final_score")
    reasons = [
        str(reason.get("message", "")).strip()
        for reason in hard_skill_gate.get("reasons", [])
        if isinstance(reason, dict) and str(reason.get("message", "")).strip()
    ]
    reason_text = reasons[0] if reasons else "must-have skill evidence is incomplete"

    if base_score is not None and final_score is not None:
        return (
            "Hard-skill gate applied: the base score was capped from "
            f"{base_score}/100 to {final_score}/100. {reason_text}"
        )

    return f"Hard-skill gate applied: {reason_text}"


def _meets_experience_but_has_incomplete_hard_skill_evidence(
    score_breakdown: dict[str, float],
    missing_skills: list[str],
    matched_skills: list[dict[str, Any]],
) -> bool:
    """Flag candidates whose years/domain should not hide hard-skill gaps."""
    if score_breakdown.get("experience", 0.0) < 0.75:
        return False

    if score_breakdown.get("evidence", 0.0) < 0.50:
        return True

    if missing_skills:
        return True

    positive_matches = [
        match
        for match in matched_skills
        if float(match.get("score", 0.0)) > 0.0
        and match.get("match_type") not in {"no_match", "no_semantic_evidence"}
    ]
    if not positive_matches:
        return True

    weak_matches = [
        match
        for match in positive_matches
        if int(match.get("evidence_level", 0)) <= 1
    ]
    return len(weak_matches) / len(positive_matches) >= 0.50


def build_interview_questions(
    evidence_highlights: list[dict[str, Any]],
    missing_skills: list[str],
    nice_to_have_matches: list[dict[str, Any]],
    limit: int = MAX_INTERVIEW_QUESTIONS,
) -> list[str]:
    """Build deterministic interview questions from evidence and gaps."""
    questions: list[str] = []
    seen_questions: set[str] = set()
    seen_evidence_text: set[str] = set()

    for highlight in evidence_highlights:
        evidence_text = _strip_sentence_end(highlight["evidence_text"])
        evidence_key = _normalize_text(evidence_text)
        if evidence_key in seen_evidence_text:
            continue

        seen_evidence_text.add(evidence_key)
        _add_question(
            questions,
            seen_questions,
            (
                f"Can you explain how you used {highlight['skill']} "
                f"in this work example: {evidence_text}?"
            ),
            limit,
        )

    for skill in missing_skills:
        _add_question(
            questions,
            seen_questions,
            f"How would you handle {skill} in this role?",
            limit,
        )

    for match in nice_to_have_matches:
        if match.get("match_type") != "no_match":
            continue

        skill = str(match.get("required_skill", "")).strip()
        if not skill:
            continue

        _add_question(
            questions,
            seen_questions,
            f"Do you have production experience with {skill}?",
            limit,
        )

    if not questions:
        questions.append(
            "Can you walk through the project that best represents your fit for this role?"
        )

    return questions[:limit]


def build_requirement_notes(
    requirement_groups: dict[str, list[str]],
    role_family_alignment: dict[str, Any] | None = None,
) -> list[str]:
    """Build recruiter notes for non-technical JD requirement groups."""
    notes: list[str] = []
    role_family_alignment = role_family_alignment or {}

    education = requirement_groups.get("education", [])
    if education:
        education = [_strip_sentence_end(item) for item in education]
        notes.append(
            "Education requirements should be reviewed separately: "
            f"{_join_readable_list(education)}."
        )

    soft_skills = requirement_groups.get("soft_skills", [])
    if soft_skills:
        soft_skills = [_strip_sentence_end(item) for item in soft_skills]
        notes.append(
            "Soft skills should be verified during interview: "
            f"{_join_readable_list(soft_skills)}."
        )

    language = requirement_groups.get("language", [])
    if language:
        language = [_strip_sentence_end(item) for item in language]
        notes.append(
            "Language requirements should be reviewed separately: "
            f"{_join_readable_list(language)}."
        )

    domain_context = requirement_groups.get("domain_context", [])
    if domain_context:
        domain_context = [_strip_sentence_end(item) for item in domain_context]
        notes.append(
            "Domain context to consider: "
            f"{_join_readable_list(domain_context)}."
        )

    if role_family_alignment.get("status") in {"partial_alignment", "misaligned"}:
        role_note = str(role_family_alignment.get("note", "")).strip()
        if role_note:
            notes.append(f"Role-family note: {role_note}")

    return notes


def _get_job_title(job_criteria: dict[str, Any] | None) -> str:
    """Return a job title from optional job criteria."""
    if not job_criteria:
        return ""

    return str(job_criteria.get("job_title", "")).strip()


def _get_requirement_groups(job_criteria: dict[str, Any] | None) -> dict[str, list[str]]:
    """Return requirement groups from optional job criteria."""
    if not job_criteria:
        return {}

    groups = job_criteria.get("requirement_groups", {})
    return groups if isinstance(groups, dict) else {}


def _get_hard_skill_gate(candidate_result: dict[str, Any]) -> dict[str, Any]:
    """Return hard-skill gate metadata when available."""
    gate = candidate_result.get("hard_skill_gate", {})
    return gate if isinstance(gate, dict) else {}


def _get_role_family_alignment(candidate_result: dict[str, Any]) -> dict[str, Any]:
    """Return role-family alignment metadata when available."""
    alignment = candidate_result.get("role_family_alignment", {})
    return alignment if isinstance(alignment, dict) else {}


def _get_role_alignment_impact(candidate_result: dict[str, Any]) -> dict[str, Any]:
    """Return role-aware score impact metadata when available."""
    impact = candidate_result.get("role_alignment_impact", {})
    return impact if isinstance(impact, dict) else {}


def _get_core_requirement_fit_summary(candidate_result: dict[str, Any]) -> dict[str, Any]:
    """Return requirement-fit summary metadata when available."""
    summary = candidate_result.get("core_requirement_fit_summary", {})
    return summary if isinstance(summary, dict) else {}


def _get_source_alignment_impact(candidate_result: dict[str, Any]) -> dict[str, Any]:
    """Return source-aware score impact metadata when available."""
    impact = candidate_result.get("source_alignment_impact", {})
    return impact if isinstance(impact, dict) else {}


def _requirement_fit_bucket(summary: dict[str, Any], bucket_name: str) -> dict[str, Any]:
    """Return one nested requirement-fit bucket with safe defaults."""
    bucket = summary.get(bucket_name, {})
    return bucket if isinstance(bucket, dict) else {}


def _display_skill(match: dict[str, Any]) -> str:
    """Return a readable skill label for one matched skill."""
    required_skill = str(match.get("required_skill", "")).strip()
    candidate_skill = match.get("candidate_skill")

    if not isinstance(candidate_skill, str) or not candidate_skill.strip():
        return required_skill

    candidate_skill = candidate_skill.strip()
    if _normalize_text(candidate_skill) == _normalize_text(required_skill):
        return required_skill

    return f"{required_skill} via {candidate_skill}"


def _format_bullets(items: list[str]) -> list[str]:
    """Format list values as Markdown bullets."""
    if not items:
        return ["- None"]

    return [f"- {item}" for item in items]


def _format_score(value: Any) -> str:
    """Format numeric score values consistently."""
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def _join_readable_list(values: list[str]) -> str:
    """Join values into a short readable English list."""
    cleaned_values = [value for value in values if value]
    if not cleaned_values:
        return ""
    if len(cleaned_values) == 1:
        return cleaned_values[0]
    if len(cleaned_values) == 2:
        return f"{cleaned_values[0]} and {cleaned_values[1]}"

    return f"{', '.join(cleaned_values[:-1])}, and {cleaned_values[-1]}"


def _add_question(
    questions: list[str],
    seen_questions: set[str],
    question: str,
    limit: int,
) -> None:
    """Append a question if it is unique and the limit is not reached."""
    if len(questions) >= limit:
        return

    normalized_question = _normalize_text(question)
    if normalized_question in seen_questions:
        return

    seen_questions.add(normalized_question)
    questions.append(question)


def _strip_sentence_end(value: str) -> str:
    """Remove trailing punctuation before inserting text into a question."""
    return value.strip().rstrip(".!?")


def _normalize_text(value: str) -> str:
    """Normalize text for deduplication."""
    return " ".join(value.casefold().split())
