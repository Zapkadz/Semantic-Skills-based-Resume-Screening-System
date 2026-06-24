"""Payload quality diagnostics for web-facing AI endpoints."""

from __future__ import annotations

import re
from typing import Any

from src.text_normalization import html_to_plain_text, normalize_search_text


SHORT_CV_WORD_THRESHOLD = 20
SHORT_JD_WORD_THRESHOLD = 20
HTML_HEAVY_TAG_THRESHOLD = 6
PLACEHOLDER_TITLE_VALUES = {
    "abc",
    "demo",
    "job test",
    "sample",
    "test",
    "test migrate",
    "test xoa tin",
    "tin test",
    "untitled job",
}
PLACEHOLDER_WORDS = {
    "abc",
    "demo",
    "job",
    "mau",
    "migrate",
    "placeholder",
    "post",
    "sample",
    "test",
    "tin",
    "xoa",
}


def diagnose_job_payload(
    job_payload: dict[str, Any],
    jd_text: str,
) -> dict[str, Any]:
    """Assess raw job payload quality before matching/scoring."""
    title = str(job_payload.get("job_title") or job_payload.get("title") or "").strip()
    description = _clean_text(
        job_payload.get("description") or job_payload.get("job_description_text")
    )
    requirements = _extract_lines(job_payload.get("requirements") or job_payload.get("must_have_skills"))
    responsibilities = _extract_lines(job_payload.get("responsibilities"))
    nice_to_have = _extract_lines(job_payload.get("nice_to_have") or job_payload.get("nice_to_have_skills"))
    html_tag_count = _payload_html_tag_count(
        [
            job_payload.get("raw_text"),
            job_payload.get("job_description_text"),
            job_payload.get("description"),
            *_as_raw_values(job_payload.get("requirements")),
            *_as_raw_values(job_payload.get("must_have_skills")),
            *_as_raw_values(job_payload.get("responsibilities")),
            *_as_raw_values(job_payload.get("nice_to_have")),
            *_as_raw_values(job_payload.get("nice_to_have_skills")),
        ]
    )
    jd_word_count = _word_count(jd_text)

    flags: list[str] = []
    if not title:
        flags.append("job_title_missing")
    elif _is_placeholder_title(title):
        flags.append("job_title_placeholder")

    if jd_word_count < SHORT_JD_WORD_THRESHOLD:
        flags.append("jd_text_too_short")
    if not requirements:
        flags.append("jd_missing_requirements_input")
    if not responsibilities:
        flags.append("jd_missing_responsibilities_input")
    if html_tag_count >= HTML_HEAVY_TAG_THRESHOLD and jd_word_count < SHORT_JD_WORD_THRESHOLD:
        flags.append("html_cleaning_changed_text_heavily")

    return {
        "flags": flags,
        "warnings": [_job_warning_message(flag) for flag in flags],
        "quality_label": _quality_label_from_flags(flags),
        "source": {
            "used_raw_text": bool(_clean_text(job_payload.get("raw_text"))),
            "used_job_description_text": bool(
                _clean_text(job_payload.get("job_description_text"))
            ),
            "used_structured_sections": bool(requirements or responsibilities or nice_to_have),
        },
        "metrics": {
            "title_word_count": _word_count(title),
            "jd_word_count": jd_word_count,
            "description_word_count": _word_count(description),
            "requirements_count": len(requirements),
            "responsibilities_count": len(responsibilities),
            "nice_to_have_count": len(nice_to_have),
            "html_tag_count": html_tag_count,
        },
    }


def diagnose_candidate_payload(
    candidate_payload: dict[str, Any],
    candidate_document: dict[str, Any],
) -> dict[str, Any]:
    """Assess raw candidate payload quality before matching/scoring."""
    candidate_name = str(candidate_payload.get("candidate_name", "")).strip()
    headline = str(candidate_payload.get("headline", "")).strip()
    skills = _extract_lines(candidate_payload.get("skills"))
    work_experience = list(candidate_payload.get("work_experience") or [])
    projects = list(candidate_payload.get("projects") or [])
    education = _extract_lines(candidate_payload.get("education"))
    certifications = _extract_lines(candidate_payload.get("certifications"))
    source_mode = _candidate_source_mode(candidate_payload)
    document_text = str(candidate_document.get("text", "")).strip()
    cv_word_count = _word_count(document_text)
    html_tag_count = _payload_html_tag_count(
        [candidate_payload.get("cv_text"), candidate_payload.get("resume_text")]
    )

    flags: list[str] = []
    if not candidate_name:
        flags.append("candidate_name_missing")
    if cv_word_count < SHORT_CV_WORD_THRESHOLD:
        flags.append("cv_text_too_short")
    if (
        not skills
        and not work_experience
        and not projects
        and cv_word_count < SHORT_CV_WORD_THRESHOLD * 2
    ):
        flags.append("candidate_profile_sparse")
    if html_tag_count >= HTML_HEAVY_TAG_THRESHOLD and cv_word_count < SHORT_CV_WORD_THRESHOLD:
        flags.append("html_cleaning_changed_text_heavily")

    warnings = [_candidate_warning_message(flag) for flag in flags]
    if not headline and source_mode == "structured_cv":
        warnings.append("Structured CV payload does not include a headline.")

    return {
        "flags": flags,
        "warnings": warnings,
        "quality_label": _quality_label_from_flags(flags),
        "source": {
            "source_mode": source_mode,
            "used_structured_profile": source_mode == "structured_cv",
        },
        "metrics": {
            "cv_word_count": cv_word_count,
            "headline_word_count": _word_count(headline),
            "skill_count": len(skills),
            "work_experience_count": len(work_experience),
            "project_count": len(projects),
            "education_count": len(education),
            "certification_count": len(certifications),
            "html_tag_count": html_tag_count,
        },
    }


def summarize_candidate_payload_diagnostics(
    diagnostics: list[dict[str, Any]],
    candidates: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Aggregate candidate payload diagnostics into one compact summary."""
    candidates = candidates or [{} for _ in diagnostics]
    flagged_candidates = []
    flag_counts = _flag_counts(diagnostics)
    word_counts = [int(item.get("metrics", {}).get("cv_word_count", 0)) for item in diagnostics]

    for candidate_payload, diag in zip(candidates, diagnostics):
        if not diag.get("flags"):
            continue
        flagged_candidates.append(
            {
                "application_id": candidate_payload.get("application_id"),
                "candidate_id": candidate_payload.get("candidate_id"),
                "candidate_name": candidate_payload.get("candidate_name", ""),
                "flags": list(diag.get("flags", [])),
                "quality_label": diag.get("quality_label", "ok"),
                "metrics": {
                    "cv_word_count": diag.get("metrics", {}).get("cv_word_count", 0),
                    "source_mode": diag.get("source", {}).get("source_mode", ""),
                },
            }
        )

    warnings: list[str] = []
    if flag_counts.get("cv_text_too_short", 0):
        warnings.append(
            f"{flag_counts['cv_text_too_short']} candidate payloads look too short for reliable AI parsing."
        )
    if flag_counts.get("candidate_profile_sparse", 0):
        warnings.append(
            f"{flag_counts['candidate_profile_sparse']} candidate payloads contain very sparse profile data."
        )

    return {
        "received_count": len(diagnostics),
        "flagged_count": len(flagged_candidates),
        "flag_counts": flag_counts,
        "flagged_candidates": flagged_candidates,
        "warnings": warnings,
        "metrics": {
            "min_cv_word_count": min(word_counts) if word_counts else 0,
            "max_cv_word_count": max(word_counts) if word_counts else 0,
            "avg_cv_word_count": round(sum(word_counts) / len(word_counts), 1)
            if word_counts
            else 0.0,
        },
    }


def summarize_job_payload_diagnostics(
    diagnostics: list[dict[str, Any]],
    jobs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Aggregate job payload diagnostics into one compact summary."""
    jobs = jobs or [{} for _ in diagnostics]
    flagged_jobs = []
    flag_counts = _flag_counts(diagnostics)
    jd_word_counts = [int(item.get("metrics", {}).get("jd_word_count", 0)) for item in diagnostics]

    for job_payload, diag in zip(jobs, diagnostics):
        if not diag.get("flags"):
            continue
        flagged_jobs.append(
            {
                "job_id": job_payload.get("job_id"),
                "job_title": job_payload.get("job_title") or job_payload.get("title", ""),
                "flags": list(diag.get("flags", [])),
                "quality_label": diag.get("quality_label", "ok"),
                "metrics": {
                    "jd_word_count": diag.get("metrics", {}).get("jd_word_count", 0),
                    "requirements_count": diag.get("metrics", {}).get("requirements_count", 0),
                    "responsibilities_count": diag.get("metrics", {}).get(
                        "responsibilities_count",
                        0,
                    ),
                },
            }
        )

    warnings: list[str] = []
    if flag_counts.get("job_title_placeholder", 0):
        warnings.append(
            f"{flag_counts['job_title_placeholder']} jobs use placeholder-like titles."
        )
    if flag_counts.get("jd_missing_requirements_input", 0):
        warnings.append(
            f"{flag_counts['jd_missing_requirements_input']} jobs do not provide explicit requirement lines."
        )
    if flag_counts.get("jd_text_too_short", 0):
        warnings.append(
            f"{flag_counts['jd_text_too_short']} jobs look too short for reliable AI analysis."
        )

    return {
        "received_count": len(diagnostics),
        "flagged_count": len(flagged_jobs),
        "flag_counts": flag_counts,
        "flagged_jobs": flagged_jobs,
        "warnings": warnings,
        "metrics": {
            "min_jd_word_count": min(jd_word_counts) if jd_word_counts else 0,
            "max_jd_word_count": max(jd_word_counts) if jd_word_counts else 0,
            "avg_jd_word_count": round(sum(jd_word_counts) / len(jd_word_counts), 1)
            if jd_word_counts
            else 0.0,
        },
    }


def _candidate_source_mode(candidate_payload: dict[str, Any]) -> str:
    """Return the dominant source used to build the candidate document."""
    if _clean_text(candidate_payload.get("cv_text")):
        return "cv_text"
    if _clean_text(candidate_payload.get("resume_text")):
        return "resume_text"
    return "structured_cv"


def _clean_text(value: Any) -> str:
    """Convert HTML-like payload text into cleaned plain text."""
    return html_to_plain_text(str(value or "")).strip()


def _extract_lines(value: Any) -> list[str]:
    """Extract cleaned non-empty lines from payload values."""
    if value is None:
        return []
    if isinstance(value, list):
        lines: list[str] = []
        for item in value:
            lines.extend(_extract_lines(item))
        return lines

    text = _clean_text(value)
    return [line.strip(" -") for line in text.splitlines() if line.strip(" -")]


def _payload_html_tag_count(values: list[Any]) -> int:
    """Count HTML tags across raw payload fields."""
    return sum(len(re.findall(r"<[^>]+>", str(value or ""))) for value in values)


def _as_raw_values(value: Any) -> list[Any]:
    """Return one field as a flat raw-value list for diagnostics counting."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _word_count(value: str) -> int:
    """Count normalized words in a string."""
    normalized = normalize_search_text(value)
    return len(normalized.split()) if normalized else 0


def _is_placeholder_title(title: str) -> bool:
    """Detect placeholder-like titles."""
    normalized_title = normalize_search_text(title)
    if not normalized_title:
        return True
    if normalized_title in PLACEHOLDER_TITLE_VALUES:
        return True

    words = normalized_title.split()
    return bool(words) and len(words) <= 4 and all(
        word in PLACEHOLDER_WORDS for word in words
    )


def _quality_label_from_flags(flags: list[str]) -> str:
    """Map payload flags into a compact quality label."""
    if not flags:
        return "ok"
    if any(
        flag in flags
        for flag in (
            "job_title_placeholder",
            "jd_text_too_short",
            "cv_text_too_short",
            "candidate_profile_sparse",
        )
    ):
        return "warning"
    return "info"


def _flag_counts(diagnostics: list[dict[str, Any]]) -> dict[str, int]:
    """Count flags across multiple diagnostic objects."""
    counts: dict[str, int] = {}
    for diag in diagnostics:
        for flag in diag.get("flags", []):
            counts[flag] = counts.get(flag, 0) + 1
    return counts


def _job_warning_message(flag: str) -> str:
    """Map a job payload flag to a stable warning message."""
    messages = {
        "job_title_missing": "Job payload is missing a title.",
        "job_title_placeholder": "Job title looks like placeholder content.",
        "jd_text_too_short": "Job text looks too short for reliable AI analysis.",
        "jd_missing_requirements_input": "Job payload does not include explicit requirements.",
        "jd_missing_responsibilities_input": "Job payload does not include explicit responsibilities.",
        "html_cleaning_changed_text_heavily": "HTML cleaning appears to have removed most visible JD content.",
    }
    return messages.get(flag, flag)


def _candidate_warning_message(flag: str) -> str:
    """Map a candidate payload flag to a stable warning message."""
    messages = {
        "candidate_name_missing": "Candidate payload is missing a display name.",
        "cv_text_too_short": "Candidate CV text looks too short for reliable AI parsing.",
        "candidate_profile_sparse": "Candidate payload contains very sparse profile information.",
        "html_cleaning_changed_text_heavily": "HTML cleaning appears to have removed most visible CV content.",
    }
    return messages.get(flag, flag)
