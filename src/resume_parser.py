"""Rule-based resume parser for Phase 03."""

from __future__ import annotations

import re
from typing import Any

from src.section_parser import (
    build_section_aliases,
    parse_section_heading as parse_known_section_heading,
    split_sections,
)
from src.text_normalization import (
    normalize_heading_text,
    repair_mojibake,
    strip_list_marker,
)


RAW_SECTION_ALIASES = {
    "summary": "summary",
    "profile": "summary",
    "objective": "summary",
    "career objective": "summary",
    "tóm tắt": "summary",
    "tom tat": "summary",
    "mục tiêu nghề nghiệp": "summary",
    "muc tieu nghe nghiep": "summary",
    "skills": "skills",
    "technical skills": "skills",
    "kỹ năng": "skills",
    "ky nang": "skills",
    "kỹ năng chuyên môn": "skills",
    "ky nang chuyen mon": "skills",
    "work experience": "work_experience",
    "experience": "work_experience",
    "employment history": "work_experience",
    "professional experience": "work_experience",
    "kinh nghiệm": "work_experience",
    "kinh nghiem": "work_experience",
    "kinh nghiệm làm việc": "work_experience",
    "kinh nghiem lam viec": "work_experience",
    "projects": "projects",
    "project": "projects",
    "dự án": "projects",
    "du an": "projects",
    "dự án tiêu biểu": "projects",
    "du an tieu bieu": "projects",
    "education": "education",
    "học vấn": "education",
    "hoc van": "education",
    "trình độ học vấn": "education",
    "trinh do hoc van": "education",
    "certifications": "certifications",
    "certification": "certifications",
    "chứng chỉ": "certifications",
    "chung chi": "certifications",
    "nghiên cứu": "research",
    "nghien cuu": "research",
    "sở thích": "interests",
    "so thich": "interests",
}

SECTION_ALIASES = build_section_aliases(RAW_SECTION_ALIASES)

DURATION_PATTERN = re.compile(
    r"(\d{1,2}/\d{4})|(\d{4})|(present|current|now|nay|hiện tại|hien tai)",
    re.IGNORECASE,
)


def parse_resume(text: str) -> dict[str, Any]:
    """Parse resume raw text into a candidate profile dictionary."""
    text = repair_mojibake(text)
    lines = [line.rstrip() for line in text.splitlines()]
    intro_lines, sections = _split_sections(lines)
    non_empty_intro = [line for line in intro_lines if line.strip()]

    return {
        "candidate_name": non_empty_intro[0].strip() if non_empty_intro else "",
        "headline": non_empty_intro[1].strip() if len(non_empty_intro) > 1 else "",
        "summary": _join_section_text(sections.get("summary", [])),
        "raw_skills": _parse_skill_list(sections.get("skills", [])),
        "work_experience": _parse_work_experience(sections.get("work_experience", [])),
        "projects": _parse_projects(sections.get("projects", [])),
        "education": _parse_simple_list(sections.get("education", [])),
        "certifications": _parse_simple_list(sections.get("certifications", [])),
    }


def _split_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    """Split raw lines into intro lines and known resume sections."""
    return split_sections(lines, SECTION_ALIASES)


def _parse_section_heading(line: str) -> tuple[str | None, str]:
    """Return normalized section name and optional inline content."""
    return parse_known_section_heading(line, SECTION_ALIASES)


def _join_section_text(lines: list[str]) -> str:
    """Join non-empty section lines into a readable one-line summary."""
    return " ".join(_strip_bullet(line) for line in lines if _strip_bullet(line))


def _parse_simple_list(lines: list[str]) -> list[str]:
    """Parse bullet or line-based section content into a clean list."""
    return [_strip_bullet(line) for line in lines if _strip_bullet(line)]


def _parse_skill_list(lines: list[str]) -> list[str]:
    """Parse a skill section into individual skill labels."""
    skills: list[str] = []
    for line in lines:
        clean_line = _strip_bullet(line)
        if not clean_line:
            continue

        skills.extend(_split_inline_values(clean_line))

    return skills


def _parse_work_experience(lines: list[str]) -> list[dict[str, Any]]:
    """Parse MVP work experience blocks."""
    entries: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line in lines:
        clean_line = _strip_bullet(line)
        if not clean_line:
            continue

        label, value = _split_label_value(clean_line)
        if label in {"mo ta", "description"} and not value:
            continue
        if label in {"cong ty", "company"}:
            if current is None:
                current = _empty_work_entry()
            current["company"] = value
            continue

        if _is_bullet(line):
            if current is None:
                current = _empty_work_entry()
            current["description"].append(clean_line)
            continue

        if _looks_like_duration(clean_line):
            if current and current["title"] and not current["duration"] and not current["description"]:
                current["duration"] = clean_line
                continue

            if current and (current["title"] or current["description"]):
                entries.append(current)
                current = _empty_work_entry()
            if current is None:
                current = _empty_work_entry()
            current["duration"] = clean_line
            continue

        if current is None:
            title, company = _split_title_company(clean_line)
            current = {
                "title": title,
                "company": company,
                "duration": "",
                "description": [],
            }
            continue

        if current.get("duration") and not current.get("title"):
            current["title"] = clean_line
            continue

        if current.get("title") and not current.get("company") and not current["description"]:
            current["company"] = clean_line
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
    current_mode = "description"

    for line in lines:
        clean_line = _strip_bullet(line)
        if not clean_line:
            continue

        label, value = _split_label_value(clean_line)
        if label in {"ten du an", "project name"}:
            if current and (current["name"] or current["description"] or current["technologies"]):
                projects.append(current)
            current = {"name": value, "description": [], "technologies": []}
            current_mode = "description"
            continue
        if label in {"vai tro", "role"}:
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current_mode = "description"
            if value:
                current["description"].append(f"Role: {value}")
            continue
        if label in {"mo ta", "description"}:
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current_mode = "description"
            if value:
                current["description"].append(value)
            continue
        if label in {"cong nghe", "technologies", "technology"}:
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current_mode = "technologies"
            if value:
                current["technologies"].extend(_split_inline_values(value))
            continue
        if label in {"ket qua", "result", "results"}:
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current_mode = "description"
            if value:
                current["description"].append(value)
            continue

        if current_mode == "technologies":
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current["technologies"].extend(_split_inline_values(clean_line))
            continue

        if _is_bullet(line):
            if current is None:
                current = {"name": "", "description": [], "technologies": []}
            current["description"].append(clean_line)
            continue

        if _looks_like_duration(clean_line):
            if current and (current["name"] or current["description"] or current["technologies"]):
                projects.append(current)
            current = {"name": "", "description": [], "technologies": []}
            current_mode = "description"
            continue

        if current and current_mode == "description" and current["name"]:
            current["description"].append(clean_line)
            continue

        if current and (current["name"] or current["description"] or current["technologies"]):
            projects.append(current)

        current = {"name": clean_line, "description": [], "technologies": []}

    if current and (current["name"] or current["description"] or current["technologies"]):
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
    stripped = line.lstrip()
    return stripped.startswith(("-", "*", "+", "•", "–", "—"))


def _strip_bullet(line: str) -> str:
    """Remove common bullet markers and surrounding whitespace."""
    return strip_list_marker(line)


def _split_label_value(line: str) -> tuple[str, str]:
    """Split common label/value lines and normalize the label."""
    if ":" not in line:
        return "", ""

    label, value = line.split(":", 1)
    return normalize_heading_text(label), value.strip()


def _split_inline_values(value: str) -> list[str]:
    """Split comma/semicolon/pipe separated values."""
    values = re.split(r"[,;|]", value)
    return [item.strip() for item in values if item.strip()]
