"""Rule-based job description parser for Phase 03."""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any


SECTION_ALIASES = {
    "requirements": "requirements",
    "required skills": "requirements",
    "must have": "requirements",
    "must-have": "requirements",
    "qualifications": "requirements",
    "nice to have": "nice_to_have",
    "nice-to-have": "nice_to_have",
    "preferred": "nice_to_have",
    "preferred skills": "nice_to_have",
    "responsibilities": "responsibilities",
    "job responsibilities": "responsibilities",
}

EXPERIENCE_PATTERN = re.compile(r"(\d+)\+?\s*(?:year|years|yr|yrs)", re.IGNORECASE)


def parse_jd(text: str) -> dict[str, Any]:
    """Parse job description raw text into job criteria."""
    lines = [line.rstrip() for line in text.splitlines()]
    intro_lines, sections = _split_sections(lines)
    non_empty_intro = [line.strip() for line in intro_lines if line.strip()]

    requirements = _parse_simple_list(sections.get("requirements", []))
    nice_to_have = _parse_simple_list(sections.get("nice_to_have", []))
    responsibilities = _parse_simple_list(sections.get("responsibilities", []))
    job_title = non_empty_intro[0] if non_empty_intro else ""
    minimum_years = _extract_minimum_experience_years(requirements)

    return {
        "job_title": job_title,
        "must_have_skills": [
            item for item in requirements if not _is_experience_requirement(item)
        ],
        "nice_to_have_skills": nice_to_have,
        "responsibilities": responsibilities,
        "minimum_experience_years": minimum_years,
        "seniority": _detect_seniority(job_title, minimum_years),
        "domain": _detect_domain(job_title, requirements, responsibilities),
    }


def _split_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """Split raw JD lines into intro lines and known JD sections."""
    intro_lines: list[str] = []
    sections: dict[str, list[str]] = OrderedDict()
    current_section: str | None = None

    for line in lines:
        section_name, inline_content = _parse_section_heading(line)
        if section_name:
            current_section = section_name
            sections.setdefault(current_section, [])
            if inline_content:
                sections[current_section].append(inline_content)
            continue

        if current_section:
            sections[current_section].append(line)
        else:
            intro_lines.append(line)

    return intro_lines, sections


def _parse_section_heading(line: str) -> tuple[str | None, str]:
    """Return normalized section name and optional inline content."""
    stripped = line.strip()
    if not stripped or ":" not in stripped:
        return None, ""

    heading, inline_content = stripped.split(":", 1)
    normalized_heading = heading.strip().lower()

    if normalized_heading not in SECTION_ALIASES:
        return None, ""

    return SECTION_ALIASES[normalized_heading], inline_content.strip()


def _parse_simple_list(lines: list[str]) -> list[str]:
    """Parse bullet or line-based section content into a clean list."""
    return [_strip_bullet(line) for line in lines if _strip_bullet(line)]


def _extract_minimum_experience_years(requirements: list[str]) -> int:
    """Extract the first minimum years value from requirement lines."""
    for requirement in requirements:
        match = EXPERIENCE_PATTERN.search(requirement)
        if match:
            return int(match.group(1))

    return 0


def _is_experience_requirement(item: str) -> bool:
    """Detect whether a requirement line describes experience instead of a skill."""
    lower_item = item.lower()
    return bool(EXPERIENCE_PATTERN.search(item)) and "experience" in lower_item


def _detect_seniority(job_title: str, minimum_years: int) -> str:
    """Infer a simple seniority label from title and minimum years."""
    lower_title = job_title.lower()

    if "senior" in lower_title:
        return "Senior"
    if "middle" in lower_title or "mid" in lower_title:
        return "Middle"
    if "junior" in lower_title:
        return "Junior"
    if "intern" in lower_title or "fresher" in lower_title:
        return "Intern/Fresher"

    if minimum_years >= 5:
        return "Senior"
    if minimum_years >= 2:
        return "Middle"
    if minimum_years >= 1:
        return "Junior"

    return "Not specified"


def _detect_domain(
    job_title: str,
    requirements: list[str],
    responsibilities: list[str],
) -> list[str]:
    """Infer simple job domains from title, requirements, and responsibilities."""
    text = " ".join([job_title, *requirements, *responsibilities]).lower()
    domains: list[str] = []

    if any(keyword in text for keyword in ("backend", "api", "service", "spring")):
        domains.append("Backend")
    if any(keyword in text for keyword in ("web", "rest", "api", "application")):
        domains.append("Web Application")
    if any(keyword in text for keyword in ("qa", "tester", "testing")):
        domains.append("Testing")
    if any(keyword in text for keyword in ("data analyst", "analytics", "dashboard")):
        domains.append("Data")

    return domains


def _strip_bullet(line: str) -> str:
    """Remove common bullet markers and surrounding whitespace."""
    stripped = line.strip()
    if stripped.startswith(("-", "*", "+")):
        return stripped[1:].strip()
    return stripped
