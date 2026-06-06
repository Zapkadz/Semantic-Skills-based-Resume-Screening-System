"""Rule-based resume parser for Phase 03."""

from __future__ import annotations

import re
from collections import OrderedDict
from typing import Any


SECTION_ALIASES = {
    "summary": "summary",
    "profile": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "work experience": "work_experience",
    "experience": "work_experience",
    "employment history": "work_experience",
    "projects": "projects",
    "project": "projects",
    "education": "education",
    "certifications": "certifications",
    "certification": "certifications",
}

DURATION_PATTERN = re.compile(
    r"(\d{1,2}/\d{4})|(\d{4})|(present|current|now)",
    re.IGNORECASE,
)


def parse_resume(text: str) -> dict[str, Any]:
    """Parse resume raw text into a candidate profile dictionary."""
    lines = [line.rstrip() for line in text.splitlines()]
    intro_lines, sections = _split_sections(lines)
    non_empty_intro = [line for line in intro_lines if line.strip()]

    return {
        "candidate_name": non_empty_intro[0].strip() if non_empty_intro else "",
        "headline": non_empty_intro[1].strip() if len(non_empty_intro) > 1 else "",
        "summary": _join_section_text(sections.get("summary", [])),
        "raw_skills": _parse_simple_list(sections.get("skills", [])),
        "work_experience": _parse_work_experience(sections.get("work_experience", [])),
        "projects": _parse_projects(sections.get("projects", [])),
        "education": _parse_simple_list(sections.get("education", [])),
        "certifications": _parse_simple_list(sections.get("certifications", [])),
    }


def _split_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """Split raw lines into intro lines and known resume sections."""
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


def _join_section_text(lines: list[str]) -> str:
    """Join non-empty section lines into a readable one-line summary."""
    return " ".join(_strip_bullet(line) for line in lines if _strip_bullet(line))


def _parse_simple_list(lines: list[str]) -> list[str]:
    """Parse bullet or line-based section content into a clean list."""
    return [_strip_bullet(line) for line in lines if _strip_bullet(line)]


def _parse_work_experience(lines: list[str]) -> list[dict[str, Any]]:
    """Parse MVP work experience blocks."""
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in lines:
        clean_line = _strip_bullet(line)
        if not clean_line:
            continue

        if _is_bullet(line):
            if current is None:
                current = _empty_work_entry()
            current["description"].append(clean_line)
            continue

        if _looks_like_duration(clean_line):
            if current is None:
                current = _empty_work_entry()
            current["duration"] = clean_line
            continue

        if current and (current["title"] or current["description"]):
            entries.append(current)

        title, company = _split_title_company(clean_line)
        current = {
            "title": title,
            "company": company,
            "duration": "",
            "description": [],
        }

    if current and (current["title"] or current["description"]):
        entries.append(current)

    return entries


def _parse_projects(lines: list[str]) -> list[dict[str, Any]]:
    """Parse MVP project blocks."""
    projects: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in lines:
        clean_line = _strip_bullet(line)
        if not clean_line:
            continue

        if _is_bullet(line):
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current["description"].append(clean_line)
            continue

        if current and (current["name"] or current["description"]):
            projects.append(current)

        current = {"name": clean_line, "description": [], "technologies": []}

    if current and (current["name"] or current["description"]):
        projects.append(current)

    return projects


def _empty_work_entry() -> dict[str, Any]:
    """Create an empty work experience entry with stable keys."""
    return {"title": "", "company": "", "duration": "", "description": []}


def _split_title_company(line: str) -> tuple[str, str]:
    """Split a work header into title and company when possible."""
    if " - " not in line:
        return line, ""

    title, company = line.split(" - ", 1)
    return title.strip(), company.strip()


def _looks_like_duration(line: str) -> bool:
    """Detect simple date or duration lines."""
    return bool(DURATION_PATTERN.search(line))


def _is_bullet(line: str) -> bool:
    """Return True when a line starts with a common plain-text bullet marker."""
    return line.lstrip().startswith(("-", "*", "+"))


def _strip_bullet(line: str) -> str:
    """Remove common bullet markers and surrounding whitespace."""
    stripped = line.strip()
    if stripped.startswith(("-", "*", "+")):
        return stripped[1:].strip()
    return stripped
