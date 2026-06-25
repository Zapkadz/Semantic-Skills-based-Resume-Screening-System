"""Classify JD requirements into typed and scoring-aware groups."""

from __future__ import annotations

import re
from typing import Any

from src.requirement_types import (
    CERTIFICATION_REQUIREMENT,
    CONTEXT_PRIORITY,
    DOMAIN_CONTEXT,
    EDUCATION_REQUIREMENT,
    EXPERIENCE_REQUIREMENT,
    LANGUAGE_REQUIREMENT,
    MUST_HAVE_PRIORITY,
    NICE_TO_HAVE_PRIORITY,
    RESPONSIBILITY_CONTEXT,
    SOFT_SKILL,
    TECHNICAL_REQUIREMENT_TYPES,
    TECH_SKILL,
    TOOL_PLATFORM,
    UNKNOWN_REQUIREMENT,
)
from src.requirement_promotion import (
    build_promoted_requirements,
    build_scoring_requirement_entries,
)
from src.responsibility_signal_extractor import build_responsibility_signal_metadata
from src.skill_extractor import merge_skill_lists
from src.text_normalization import normalize_search_text, repair_mojibake, strip_list_marker


REQUIREMENT_GROUP_KEYS = (
    "must_have_technical",
    "nice_to_have_technical",
    "soft_skills",
    "education",
    "experience",
    "certifications",
    "language",
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

LANGUAGE_MARKERS = (
    "english",
    "spoken english",
    "writing english",
    "written english",
    "toeic",
    "ielts",
    "tieng anh",
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
    "trinh bay",
    "under pressure",
    "work independently",
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

TOOL_PLATFORM_MARKERS = (
    "aws",
    "azure",
    "cloud",
    "container",
    "database",
    "docker",
    "framework",
    "git",
    "gitlab",
    "gcp",
    "jenkins",
    "kubernetes",
    "library",
    "mysql",
    "oracle",
    "platform",
    "postgres",
    "pytorch",
    "qualys",
    "sap",
    "server",
    "spring boot",
    "tensorflow",
    "tool",
    "vmware",
)

EXPERIENCE_PATTERN = re.compile(
    r"\b\d+\+?\s*(?:year|years|yr|yrs|nam|n m|yeear)\b",
    re.IGNORECASE,
)
EXPERIENCE_ONLY_PATTERN = re.compile(
    r"^\s*\d+\+?\s*(?:year|years|yr|yrs|nam|n m|yeear)\s*$",
    re.IGNORECASE,
)


def classify_jd_requirements(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    """Classify parsed JD requirements into scoring-aware groups."""
    typed_requirements = build_typed_requirements(job_criteria, jd_text, taxonomy)
    groups = _empty_groups()
    for requirement in typed_requirements:
        _append_requirement_to_groups(requirement, groups)

    return {key: merge_skill_lists(groups[key]) for key in REQUIREMENT_GROUP_KEYS}


def build_typed_requirements(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Build typed requirement objects from JD sections and parsed fields."""
    sections = _extract_sections(job_criteria)
    typed_requirements: list[dict[str, str]] = []

    for section_name, priority in (
        ("requirements", MUST_HAVE_PRIORITY),
        ("qualifications", MUST_HAVE_PRIORITY),
        ("nice_to_have", NICE_TO_HAVE_PRIORITY),
    ):
        typed_requirements.extend(
            _build_typed_requirement_block(
                sections.get(section_name, []),
                section_name=section_name,
                priority=priority,
                taxonomy=taxonomy,
            )
        )

    for section_name in ("description", "responsibilities"):
        typed_requirements.extend(
            _build_typed_requirement_block(
                sections.get(section_name, []),
                section_name=section_name,
                priority=CONTEXT_PRIORITY,
                taxonomy=taxonomy,
            )
        )

    typed_requirements.extend(
        _build_typed_requirement_block(
            _extract_experience_lines(jd_text),
            section_name="requirements",
            priority=MUST_HAVE_PRIORITY,
            taxonomy=taxonomy,
        )
    )

    return _dedupe_typed_requirements(typed_requirements)


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


def enrich_job_criteria_with_requirement_metadata(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Attach typed requirements, groups, and responsibility signal metadata."""
    typed_requirements = build_typed_requirements(job_criteria, jd_text, taxonomy)
    requirement_groups = classify_jd_requirements(job_criteria, jd_text, taxonomy)
    responsibility_signal_metadata = build_responsibility_signal_metadata(
        typed_requirements,
        taxonomy,
    )
    enriched_job_criteria = {
        **job_criteria,
        "typed_requirements": typed_requirements,
        "requirement_groups": requirement_groups,
        **responsibility_signal_metadata,
    }
    scoring_requirement_entries = build_scoring_requirement_entries(enriched_job_criteria)
    promoted_requirements = build_promoted_requirements(enriched_job_criteria)
    return {
        **enriched_job_criteria,
        "promoted_requirements": promoted_requirements,
        "scoring_requirement_entries": scoring_requirement_entries,
    }


def _empty_groups() -> dict[str, list[str]]:
    """Create stable requirement groups."""
    return {key: [] for key in REQUIREMENT_GROUP_KEYS}


def _build_typed_requirement_block(
    lines: list[str],
    *,
    section_name: str,
    priority: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Classify an ordered section block into typed requirement objects."""
    typed_requirements: list[dict[str, str]] = []
    current_priority = priority
    for line in lines:
        clean_line = _clean_line(line)
        if not clean_line:
            continue

        heading_priority = _heading_priority(clean_line)
        if heading_priority:
            current_priority = heading_priority
            typed_requirements.append(
                _typed_requirement(
                    text=clean_line,
                    requirement_type=UNKNOWN_REQUIREMENT,
                    section_name=section_name,
                    priority=current_priority,
                    source_line=clean_line,
                    ignored=True,
                )
            )
            continue

        requirement_priority = _effective_priority(clean_line, current_priority)
        requirement_type = _classify_line_type(
            clean_line,
            section_name=section_name,
            priority=requirement_priority,
            taxonomy=taxonomy,
        )
        typed_requirements.append(
            _typed_requirement(
                text=clean_line,
                requirement_type=requirement_type,
                section_name=section_name,
                priority=requirement_priority,
                source_line=clean_line,
            )
        )

    return typed_requirements


def _classify_line_type(
    line: str,
    *,
    section_name: str,
    priority: str,
    taxonomy: dict[str, dict[str, Any]],
) -> str:
    """Classify one non-heading requirement line."""
    normalized = normalize_search_text(line)
    effective_priority = (
        NICE_TO_HAVE_PRIORITY if _has_preferred_marker(normalized) else priority
    )

    if _is_noise_line(normalized):
        return UNKNOWN_REQUIREMENT
    if section_name in {"description", "responsibilities"}:
        if _is_domain_context_line(normalized):
            return DOMAIN_CONTEXT
        return RESPONSIBILITY_CONTEXT
    if _is_experience_line(normalized):
        return EXPERIENCE_REQUIREMENT
    if _is_education_line(normalized):
        return EDUCATION_REQUIREMENT
    if _is_language_line(normalized):
        return LANGUAGE_REQUIREMENT
    if _is_soft_skill_line(normalized):
        return SOFT_SKILL
    if _is_domain_context_line(normalized):
        return DOMAIN_CONTEXT
    if _is_certification_line(normalized):
        return CERTIFICATION_REQUIREMENT
    if _looks_like_tool_platform_line(normalized, taxonomy):
        return TOOL_PLATFORM
    if effective_priority in {MUST_HAVE_PRIORITY, NICE_TO_HAVE_PRIORITY}:
        return TECH_SKILL

    return UNKNOWN_REQUIREMENT


def _heading_priority(line: str) -> str | None:
    """Return priority switch for known heading lines."""
    normalized = normalize_search_text(line.rstrip(":"))
    if normalized in REQUIRED_HEADING_KEYS:
        return MUST_HAVE_PRIORITY
    if normalized in PREFERRED_HEADING_KEYS:
        return NICE_TO_HAVE_PRIORITY
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
    if EXPERIENCE_ONLY_PATTERN.match(normalized):
        return True

    return bool(EXPERIENCE_PATTERN.search(normalized)) and (
        "experience" in normalized or "kinh nghiem" in normalized
    )


def _is_education_line(normalized: str) -> bool:
    """Detect education/degree requirements."""
    return any(marker in normalized for marker in EDUCATION_MARKERS)


def _is_language_line(normalized: str) -> bool:
    """Detect language/communication language requirements."""
    return any(marker in normalized for marker in LANGUAGE_MARKERS)


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


def _looks_like_tool_platform_line(
    normalized: str,
    taxonomy: dict[str, dict[str, Any]],
) -> bool:
    """Heuristically detect tool/platform/framework style requirements."""
    if any(marker in normalized for marker in TOOL_PLATFORM_MARKERS):
        return True

    taxonomy_categories = _matched_taxonomy_categories(normalized, taxonomy)
    if not taxonomy_categories:
        return False

    return all(
        any(
            keyword in category
            for keyword in (
                "framework",
                "library",
                "cloud",
                "database",
                "deployment",
                "runtime",
                "mobile",
                "messaging",
                "devops",
            )
        )
        for category in taxonomy_categories
    )


def _has_preferred_marker(normalized: str) -> bool:
    """Return True when a line itself marks an optional requirement."""
    return any(marker in normalized for marker in PREFERRED_MARKERS)


def _effective_priority(line: str, default_priority: str) -> str:
    """Allow per-line preferred markers to downgrade an optional requirement."""
    normalized = normalize_search_text(line)
    if _has_preferred_marker(normalized):
        return NICE_TO_HAVE_PRIORITY
    return default_priority


def _extract_experience_lines(jd_text: str) -> list[str]:
    """Extract explicit experience lines from raw JD text for metadata."""
    lines: list[str] = []
    for raw_line in repair_mojibake(jd_text).splitlines():
        clean_line = _clean_line(raw_line)
        if clean_line and _is_experience_line(normalize_search_text(clean_line)):
            lines.append(clean_line)
    return lines


def _extract_sections(job_criteria: dict[str, Any]) -> dict[str, list[str]]:
    """Read section-aware JD data with a fallback for older parser output."""
    sections = job_criteria.get("sections")
    if isinstance(sections, dict):
        return {
            "requirements": _string_list(sections.get("requirements", [])),
            "qualifications": _string_list(sections.get("qualifications", [])),
            "nice_to_have": _string_list(sections.get("nice_to_have", [])),
            "description": _string_list(sections.get("description", [])),
            "responsibilities": _string_list(sections.get("responsibilities", [])),
        }

    return {
        "requirements": _string_list(job_criteria.get("must_have_skills", [])),
        "qualifications": [],
        "nice_to_have": _string_list(job_criteria.get("nice_to_have_skills", [])),
        "description": _string_list(job_criteria.get("description_lines", [])),
        "responsibilities": _string_list(job_criteria.get("responsibilities", [])),
    }


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


def _typed_requirement(
    *,
    text: str,
    requirement_type: str,
    section_name: str,
    priority: str,
    source_line: str,
    ignored: bool = False,
) -> dict[str, str]:
    """Build one stable typed requirement object."""
    return {
        "text": text,
        "type": requirement_type,
        "section": section_name,
        "priority": priority,
        "source_line": source_line,
        "normalized_text": normalize_search_text(text),
        "ignored": "true" if ignored else "false",
    }


def _append_requirement_to_groups(
    requirement: dict[str, str],
    groups: dict[str, list[str]],
) -> None:
    """Map one typed requirement into scoring-aware requirement groups."""
    if requirement.get("ignored") == "true":
        groups["ignored"].append(requirement["text"])
        return

    requirement_type = requirement.get("type", UNKNOWN_REQUIREMENT)
    priority = requirement.get("priority", MUST_HAVE_PRIORITY)
    text = requirement.get("text", "")

    if requirement_type == EDUCATION_REQUIREMENT:
        groups["education"].append(text)
    elif requirement_type == EXPERIENCE_REQUIREMENT:
        groups["experience"].append(text)
    elif requirement_type == LANGUAGE_REQUIREMENT:
        groups["language"].append(text)
    elif requirement_type == SOFT_SKILL:
        groups["soft_skills"].append(text)
    elif requirement_type == DOMAIN_CONTEXT:
        groups["domain_context"].append(text)
    elif requirement_type == RESPONSIBILITY_CONTEXT:
        groups["responsibilities"].append(text)
    elif requirement_type == CERTIFICATION_REQUIREMENT:
        if priority == NICE_TO_HAVE_PRIORITY:
            groups["nice_to_have_technical"].append(text)
        else:
            groups["certifications"].append(text)
    elif requirement_type in TECHNICAL_REQUIREMENT_TYPES:
        if priority == NICE_TO_HAVE_PRIORITY:
            groups["nice_to_have_technical"].append(text)
        else:
            groups["must_have_technical"].append(text)
    else:
        groups["ignored"].append(text)


def _matched_taxonomy_categories(
    normalized_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Return taxonomy categories whose labels appear in a requirement line."""
    categories: list[str] = []
    for skill, metadata in taxonomy.items():
        skill_key = normalize_search_text(skill)
        if skill_key and skill_key in normalized_text:
            category = str(metadata.get("category", "")).strip().casefold()
            if category:
                categories.append(category)

        for alias in metadata.get("aliases", []):
            alias_key = normalize_search_text(str(alias))
            if alias_key and alias_key in normalized_text:
                category = str(metadata.get("category", "")).strip().casefold()
                if category:
                    categories.append(category)

    return categories


def _dedupe_typed_requirements(
    requirements: list[dict[str, str]],
) -> list[dict[str, str]]:
    """Deduplicate typed requirements while preserving first appearance."""
    deduped: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str, str, str]] = set()

    for requirement in requirements:
        key = (
            requirement.get("normalized_text", ""),
            requirement.get("type", ""),
            requirement.get("section", ""),
            requirement.get("priority", ""),
        )
        if not key[0] or key in seen_keys:
            continue

        seen_keys.add(key)
        deduped.append(requirement)

    return deduped
