"""Quality gate for candidate-side job recommendation."""

from __future__ import annotations

import re
from typing import Any

from src.text_normalization import html_to_plain_text, normalize_search_text


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

MIN_MEANINGFUL_CONTENT_WORDS = 12
MIN_SIGNAL_LINES_FOR_STRONG_QUALITY = 2
MIN_DESCRIPTION_ONLY_CONTENT_WORDS = 20
REQUIREMENT_HEADING_KEYS = {
    "condition bat buoc",
    "dieu kien bat buoc",
    "must have",
    "must-have",
    "qualification",
    "qualifications",
    "required",
    "required skills",
    "requirements",
    "yeu cau",
    "yeu cau bat buoc",
    "yeu cau cong viec",
}
EXPERIENCE_ONLY_PATTERN = re.compile(
    r"^\s*\d+\+?\s*(?:year|years|yr|yrs|nam|n m|yeear)\s*$",
    re.IGNORECASE,
)


def evaluate_job_quality(
    job_payload: dict[str, Any],
    job_criteria: dict[str, Any],
    jd_text: str,
    requirement_groups: dict[str, list[str]],
    must_have_skills: list[str],
    nice_to_have_skills: list[str],
    open_set_requirements: list[str],
) -> dict[str, Any]:
    """Evaluate whether one job has enough JD data for candidate-side recommendation."""
    job_title = str(
        job_criteria.get("job_title")
        or job_payload.get("job_title")
        or job_payload.get("title")
        or ""
    ).strip()
    normalized_title = normalize_search_text(job_title)
    source_lines = _source_lines(job_payload, jd_text)
    meaningful_source_lines = [
        line for line in source_lines if not _is_placeholder_line(line)
    ]
    meaningful_must_have_lines = _meaningful_lines(
        requirement_groups.get("must_have_technical", [])
    )
    meaningful_open_set_requirements = _meaningful_lines(open_set_requirements)
    meaningful_responsibilities = _meaningful_lines(
        requirement_groups.get("responsibilities", [])
    )
    meaningful_nice_to_have_lines = _meaningful_lines(
        requirement_groups.get("nice_to_have_technical", [])
    )
    meaningful_domain_context = _meaningful_lines(
        requirement_groups.get("domain_context", [])
    )
    structured_requirement_lines = _meaningful_lines(
        _extract_payload_lines(job_payload, ("requirements", "must_have_skills"))
    )
    structured_requirement_lines = [
        line
        for line in structured_requirement_lines
        if not _is_experience_only_line(line)
    ]
    structured_responsibility_lines = _meaningful_lines(
        _extract_payload_lines(job_payload, ("responsibilities",))
    )
    has_explicit_requirement_source = _has_explicit_requirement_source(job_payload)

    signal_lines = _unique_preserve_order(
        [
            *meaningful_must_have_lines,
            *meaningful_open_set_requirements,
            *meaningful_responsibilities,
            *meaningful_nice_to_have_lines,
            *meaningful_domain_context,
        ]
    )
    source_content_word_count = _word_count(" ".join(meaningful_source_lines))
    signal_word_count = _word_count(" ".join(signal_lines))
    placeholder_title = _is_placeholder_title(normalized_title)
    placeholder_content = bool(source_lines) and not meaningful_source_lines
    meaningful_technical_count = len(
        _unique_preserve_order(
            [*meaningful_must_have_lines, *meaningful_open_set_requirements]
        )
    )
    meaningful_responsibility_count = len(meaningful_responsibilities)
    signal_line_count = len(signal_lines)

    flags: list[str] = []
    reasons: list[str] = []
    quality_score = 100

    if placeholder_title:
        flags.append("placeholder_title")
        reasons.append("Job title looks like a placeholder.")
        quality_score -= 45

    if placeholder_content:
        flags.append("placeholder_content")
        reasons.append("JD content only contains placeholder-like text.")
        quality_score -= 35

    if source_content_word_count < MIN_MEANINGFUL_CONTENT_WORDS:
        flags.append("description_too_short")
        reasons.append("JD content is too short after cleaning.")
        quality_score -= 15

    if meaningful_technical_count == 0:
        flags.append("missing_requirements")
        reasons.append("No meaningful must-have requirements were detected.")
        quality_score -= 35

    if not has_explicit_requirement_source:
        flags.append("missing_explicit_requirements")
        reasons.append("JD does not include a clear candidate requirements section.")
        quality_score -= 20

    if meaningful_responsibility_count == 0:
        flags.append("missing_responsibilities")
        reasons.append("No meaningful responsibilities were detected.")
        quality_score -= 10

    if signal_line_count < MIN_SIGNAL_LINES_FOR_STRONG_QUALITY:
        flags.append("sparse_job_signal")
        reasons.append("JD has too few meaningful requirement or responsibility lines.")
        quality_score -= 10

    if signal_word_count < MIN_MEANINGFUL_CONTENT_WORDS:
        flags.append("low_signal_vocabulary")
        reasons.append("JD does not contain enough meaningful technical vocabulary.")
        quality_score -= 5

    recommendation_eligible = not _is_ineligible(
        placeholder_title=placeholder_title,
        placeholder_content=placeholder_content,
        has_explicit_requirement_source=has_explicit_requirement_source,
        meaningful_technical_count=meaningful_technical_count,
        meaningful_responsibility_count=meaningful_responsibility_count,
        structured_requirement_count=len(structured_requirement_lines),
        structured_responsibility_count=len(structured_responsibility_lines),
        source_content_word_count=source_content_word_count,
        signal_line_count=signal_line_count,
        quality_score=quality_score,
    )
    quality_score = max(0, min(100, int(round(quality_score))))

    if not recommendation_eligible:
        quality_label = "insufficient_jd_data"
    elif flags:
        quality_label = "eligible_with_warning"
    else:
        quality_label = "eligible"

    return {
        "quality_score": quality_score,
        "quality_label": quality_label,
        "recommendation_eligible": recommendation_eligible,
        "flags": _unique_preserve_order(flags),
        "reasons": _unique_preserve_order(reasons),
        "metrics": {
            "source_content_word_count": source_content_word_count,
            "signal_word_count": signal_word_count,
            "meaningful_must_have_count": len(meaningful_must_have_lines),
            "meaningful_open_set_count": len(meaningful_open_set_requirements),
            "meaningful_responsibility_count": meaningful_responsibility_count,
            "meaningful_nice_to_have_count": len(meaningful_nice_to_have_lines),
            "structured_requirement_count": len(structured_requirement_lines),
            "structured_responsibility_count": len(structured_responsibility_lines),
            "has_explicit_requirement_source": has_explicit_requirement_source,
            "signal_line_count": signal_line_count,
            "must_have_skill_count": len(must_have_skills),
            "nice_to_have_skill_count": len(nice_to_have_skills),
            "open_set_requirement_count": len(open_set_requirements),
        },
    }


def _is_ineligible(
    *,
    placeholder_title: bool,
    placeholder_content: bool,
    has_explicit_requirement_source: bool,
    meaningful_technical_count: int,
    meaningful_responsibility_count: int,
    structured_requirement_count: int,
    structured_responsibility_count: int,
    source_content_word_count: int,
    signal_line_count: int,
    quality_score: int | float,
) -> bool:
    """Return True when a JD should be excluded from recommendation."""
    if signal_line_count <= 0:
        return True
    if (
        meaningful_technical_count == 0
        and meaningful_responsibility_count == 0
        and source_content_word_count < MIN_MEANINGFUL_CONTENT_WORDS
    ):
        return True
    if placeholder_content and signal_line_count <= 1:
        return True
    if placeholder_title and meaningful_technical_count == 0:
        return True
    if (
        not has_explicit_requirement_source
        and structured_requirement_count == 0
        and source_content_word_count < MIN_DESCRIPTION_ONLY_CONTENT_WORDS
    ):
        return True
    if quality_score < 35:
        return True

    return False


def _source_lines(job_payload: dict[str, Any], jd_text: str) -> list[str]:
    """Collect cleaned payload lines that represent the original JD content."""
    lines: list[str] = []

    for field in ("raw_text", "job_description_text", "description"):
        lines.extend(_split_clean_lines(job_payload.get(field)))

    for field in (
        "requirements",
        "must_have_skills",
        "nice_to_have",
        "nice_to_have_skills",
        "responsibilities",
    ):
        value = job_payload.get(field)
        if isinstance(value, list):
            for item in value:
                lines.extend(_split_clean_lines(item))
        else:
            lines.extend(_split_clean_lines(value))

    if lines:
        return _unique_preserve_order(lines)

    return _split_clean_lines(jd_text)


def _split_clean_lines(value: Any) -> list[str]:
    """Convert one payload field into cleaned plain-text lines."""
    text = html_to_plain_text(str(value or "")).strip()
    if not text:
        return []

    return [
        line.strip(" -")
        for line in text.splitlines()
        if line.strip(" -")
    ]


def _extract_payload_lines(job_payload: dict[str, Any], fields: tuple[str, ...]) -> list[str]:
    """Extract cleaned lines from selected payload fields."""
    lines: list[str] = []
    for field in fields:
        value = job_payload.get(field)
        if isinstance(value, list):
            for item in value:
                lines.extend(_split_clean_lines(item))
        else:
            lines.extend(_split_clean_lines(value))

    return lines


def _meaningful_lines(lines: list[str]) -> list[str]:
    """Return non-placeholder lines with lightweight normalization."""
    cleaned_lines = []
    for line in lines:
        clean_line = html_to_plain_text(str(line or "")).strip()
        if not clean_line or _is_placeholder_line(clean_line):
            continue
        cleaned_lines.append(clean_line)

    return _unique_preserve_order(cleaned_lines)


def _is_placeholder_title(normalized_title: str) -> bool:
    """Detect short placeholder titles without overmatching real testing roles."""
    if not normalized_title:
        return True
    if normalized_title in PLACEHOLDER_TITLE_VALUES:
        return True

    words = normalized_title.split()
    return bool(words) and len(words) <= 4 and all(
        word in PLACEHOLDER_WORDS for word in words
    )


def _has_explicit_requirement_source(job_payload: dict[str, Any]) -> bool:
    """Return True when payload clearly provides a requirements section."""
    requirement_lines = [
        line
        for line in _meaningful_lines(
            _extract_payload_lines(job_payload, ("requirements", "must_have_skills"))
        )
        if not _is_experience_only_line(line)
    ]
    if requirement_lines:
        return True

    for field in ("raw_text", "job_description_text", "description"):
        lines = _split_clean_lines(job_payload.get(field))
        normalized_lines = {normalize_search_text(line.rstrip(":")) for line in lines}
        if normalized_lines & REQUIREMENT_HEADING_KEYS:
            return True

    return False


def _is_placeholder_line(value: str) -> bool:
    """Detect placeholder-like content lines such as 'test' or 'demo'."""
    normalized = normalize_search_text(value)
    if not normalized:
        return True
    if normalized in PLACEHOLDER_TITLE_VALUES:
        return True

    words = normalized.split()
    if not words:
        return True
    if len(words) <= 3 and all(word in PLACEHOLDER_WORDS for word in words):
        return True
    if len(set(words)) == 1 and words[0] in PLACEHOLDER_WORDS:
        return True
    if len(words) <= 4 and words[-1] in PLACEHOLDER_WORDS and any(
        prefix in normalized for prefix in ("mo ta", "description", "chi tiet")
    ):
        return True

    return False


def _is_experience_only_line(value: str) -> bool:
    """Return True for bare experience duration lines such as '1 năm'."""
    return bool(EXPERIENCE_ONLY_PATTERN.match(normalize_search_text(value)))


def _word_count(value: str) -> int:
    """Return normalized word count for one text segment."""
    normalized = normalize_search_text(value)
    return len(normalized.split()) if normalized else 0


def _unique_preserve_order(values: list[str]) -> list[str]:
    """Deduplicate strings while preserving their first appearance."""
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = normalize_search_text(value)
        if not key or key in seen:
            continue

        seen.add(key)
        deduped.append(value)

    return deduped
