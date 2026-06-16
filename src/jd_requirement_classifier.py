"""Classify JD requirements into scoring-aware groups."""

from __future__ import annotations

import re
from typing import Any

from src.skill_extractor import merge_skill_lists
from src.text_normalization import normalize_search_text, repair_mojibake, strip_list_marker


REQUIREMENT_GROUP_KEYS = (
    "must_have_technical",
    "nice_to_have_technical",
    "soft_skills",
    "education",
    "experience",
    "certifications",
    "domain_context",
    "responsibilities",
    "ignored",
)

REQUIRED_HEADING_KEYS = {
    "condition bat buoc",
    "dieu kien bat buoc",
    "required",
    "required skills",
    "requirements",
    "must have",
    "must-have",
    "qualification",
    "qualifications",
    "yeu cau",
    "yeu cau bat buoc",
    "yeu cau cong viec",
}

PREFERRED_HEADING_KEYS = {
    "advantage",
    "bonus",
    "diem cong",
    "dieu kien uu tien",
    "la loi the",
    "loi the",
    "nice to have",
    "nice-to-have",
    "plus",
    "preferred",
    "preferred skills",
    "uu tien",
}

PREFERRED_MARKERS = (
    "advantage",
    "are an advantage",
    "bonus",
    "diem cong",
    "is an advantage",
    "la loi the",
    "loi the",
    "nice to have",
    "plus",
    "preferred",
    "uu tien",
)

EDUCATION_MARKERS = (
    "bachelor",
    "cao dang",
    "dai hoc",
    "degree",
    "dien tu vien thong",
    "graduate",
    "major",
    "nganh cntt",
    "toan tin",
    "tot nghiep",
    "university",
)

SOFT_SKILL_MARKERS = (
    "analytical",
    "chiu ap luc",
    "communication",
    "dam me hoc hoi",
    "detail oriented",
    "detail-oriented",
    "doc lap",
    "giao tiep",
    "lam viec doc lap",
    "lam viec nhom",
    "mindset",
    "nhiet tinh",
    "presentation",
    "problem solving",
    "process driven",
    "process-driven",
    "teamwork",
    "thuyet trinh",
    "tieng anh",
    "trinh bay",
    "under pressure",
    "work independently",
    "written english",
)

DOMAIN_MARKERS = (
    "banking",
    "domain",
    "finance",
    "linh vuc",
    "ngan hang",
    "tai chinh",
)

CERTIFICATION_MARKERS = (
    "certificate",
    "certification",
    "certified",
    "chung chi",
    "cipp",
    "ceh",
    "iso",
    "security+",
)

EXPERIENCE_PATTERN = re.compile(
    r"\b\d+\+?\s*(?:year|years|yr|yrs|nam|n m|yeear)\b",
    re.IGNORECASE,
)


def classify_jd_requirements(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    """Classify parsed JD requirements into scoring-aware groups."""
    groups = _empty_groups()
    required_lines = _string_list(job_criteria.get("must_have_skills", []))
    nice_to_have_lines = _string_list(job_criteria.get("nice_to_have_skills", []))
    responsibilities = _string_list(job_criteria.get("responsibilities", []))

    _classify_sequence(required_lines, "required", taxonomy, groups)
    _classify_sequence(nice_to_have_lines, "preferred", taxonomy, groups)

    groups["responsibilities"] = merge_skill_lists(responsibilities)
    groups["experience"] = merge_skill_lists(
        groups["experience"],
        _extract_experience_lines(jd_text),
    )

    return {key: merge_skill_lists(groups[key]) for key in REQUIREMENT_GROUP_KEYS}


def build_scoring_requirement_lines(
    requirement_groups: dict[str, list[str]],
) -> tuple[list[str], list[str]]:
    """Return must-have and nice-to-have lines for skill/open-set scoring."""
    must_have = merge_skill_lists(
        requirement_groups.get("must_have_technical", []),
        requirement_groups.get("certifications", []),
    )
    nice_to_have = merge_skill_lists(
        requirement_groups.get("nice_to_have_technical", []),
    )
    return must_have, nice_to_have


def _empty_groups() -> dict[str, list[str]]:
    """Create stable requirement groups."""
    return {key: [] for key in REQUIREMENT_GROUP_KEYS}


def _classify_sequence(
    lines: list[str],
    default_priority: str,
    taxonomy: dict[str, dict[str, Any]],
    groups: dict[str, list[str]],
) -> None:
    """Classify an ordered sequence while honoring nested headings."""
    priority = default_priority
    for line in lines:
        clean_line = _clean_line(line)
        if not clean_line:
            continue

        heading_priority = _heading_priority(clean_line)
        if heading_priority:
            priority = heading_priority
            groups["ignored"].append(clean_line)
            continue

        group = _classify_line(clean_line, priority, taxonomy)
        groups[group].append(clean_line)


def _classify_line(
    line: str,
    priority: str,
    taxonomy: dict[str, dict[str, Any]],
) -> str:
    """Classify one non-heading requirement line."""
    normalized = normalize_search_text(line)
    effective_priority = "preferred" if _has_preferred_marker(normalized) else priority

    if _is_noise_line(normalized):
        return "ignored"
    if _is_experience_line(normalized):
        return "experience"
    if _is_education_line(normalized):
        return "education"
    if _is_soft_skill_line(normalized):
        return "soft_skills"
    if _is_domain_context_line(normalized):
        return "domain_context"
    if _is_certification_line(normalized):
        return (
            "nice_to_have_technical"
            if effective_priority == "preferred"
            else "certifications"
        )

    return (
        "nice_to_have_technical"
        if effective_priority == "preferred"
        else "must_have_technical"
    )


def _heading_priority(line: str) -> str | None:
    """Return priority switch for known heading lines."""
    normalized = normalize_search_text(line.rstrip(":"))
    if normalized in REQUIRED_HEADING_KEYS:
        return "required"
    if normalized in PREFERRED_HEADING_KEYS:
        return "preferred"
    return None


def _is_noise_line(normalized: str) -> bool:
    """Detect headings and empty low-signal lines."""
    if not normalized:
        return True
    if normalized in REQUIRED_HEADING_KEYS or normalized in PREFERRED_HEADING_KEYS:
        return True
    if normalized in {"skills", "ky nang", "qualification experience"}:
        return True
    return False


def _is_experience_line(normalized: str) -> bool:
    """Detect lines that specify experience amount."""
    return bool(EXPERIENCE_PATTERN.search(normalized)) and (
        "experience" in normalized or "kinh nghiem" in normalized
    )


def _is_education_line(normalized: str) -> bool:
    """Detect education/degree requirements."""
    return any(marker in normalized for marker in EDUCATION_MARKERS)


def _is_soft_skill_line(normalized: str) -> bool:
    """Detect soft/transversal skill requirements."""
    return any(marker in normalized for marker in SOFT_SKILL_MARKERS)


def _is_domain_context_line(normalized: str) -> bool:
    """Detect domain context statements rather than technical skill requirements."""
    return any(marker in normalized for marker in DOMAIN_MARKERS) and not any(
        marker in normalized for marker in ("api", "java", "spring", "sql")
    )


def _is_certification_line(normalized: str) -> bool:
    """Detect certification requirements."""
    return any(marker in normalized for marker in CERTIFICATION_MARKERS)


def _has_preferred_marker(normalized: str) -> bool:
    """Return True when a line itself marks an optional requirement."""
    return any(marker in normalized for marker in PREFERRED_MARKERS)


def _extract_experience_lines(jd_text: str) -> list[str]:
    """Extract explicit experience lines from raw JD text for metadata."""
    lines: list[str] = []
    for raw_line in repair_mojibake(jd_text).splitlines():
        clean_line = _clean_line(raw_line)
        if clean_line and _is_experience_line(normalize_search_text(clean_line)):
            lines.append(clean_line)
    return lines


def _string_list(value: Any) -> list[str]:
    """Convert common parsed values into clean strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean_line(item) for item in value if _clean_line(item)]
    return [_clean_line(value)] if _clean_line(value) else []


def _clean_line(value: Any) -> str:
    """Normalize one JD line without losing its display text."""
    cleaned = strip_list_marker(repair_mojibake(str(value or ""))).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -")
