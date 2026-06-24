"""Section-aware parser for plain-text job descriptions."""

from __future__ import annotations

from typing import Any

from src.section_parser import build_section_aliases, split_sections
from src.text_normalization import repair_mojibake, strip_list_marker


RAW_JD_SECTION_ALIASES = {
    "requirements": "requirements",
    "required skills": "requirements",
    "must have": "requirements",
    "must-have": "requirements",
    "job requirements": "requirements",
    "required qualifications": "requirements",
    "required": "requirements",
    "condition bat buoc": "requirements",
    "dieu kien bat buoc": "requirements",
    "yeu cau": "requirements",
    "yeu cau cong viec": "requirements",
    "yeu cau ung vien": "requirements",
    "ky nang bat buoc": "requirements",
    "skills": "requirements",
    "qualifications": "qualifications",
    "qualification": "qualifications",
    "qualification experience": "qualifications",
    "qualifications experience": "qualifications",
    "professional requirements": "qualifications",
    "qualifications & experience": "qualifications",
    "nice to have": "nice_to_have",
    "nice-to-have": "nice_to_have",
    "preferred": "nice_to_have",
    "preferred skills": "nice_to_have",
    "plus": "nice_to_have",
    "bonus": "nice_to_have",
    "uu tien": "nice_to_have",
    "dieu kien uu tien": "nice_to_have",
    "diem cong": "nice_to_have",
    "loi the": "nice_to_have",
    "description": "description",
    "job description": "description",
    "mo ta cong viec": "description",
    "chi tiet tin tuyen dung": "description",
    "responsibilities": "responsibilities",
    "job responsibilities": "responsibilities",
    "trach nhiem": "responsibilities",
    "nhiem vu": "responsibilities",
    "benefits": "benefits",
    "benefit": "benefits",
    "quyen loi": "benefits",
    "phuc loi": "benefits",
}

SECTION_ALIASES = build_section_aliases(RAW_JD_SECTION_ALIASES)

SECTION_KEYS = (
    "title",
    "intro",
    "description",
    "requirements",
    "qualifications",
    "responsibilities",
    "nice_to_have",
    "benefits",
)


def parse_jd_sections(text: str) -> dict[str, Any]:
    """Parse a raw JD text blob into named sections."""
    repaired_text = repair_mojibake(text)
    lines = [line.rstrip() for line in repaired_text.splitlines()]
    intro_lines, sections = split_sections(lines, SECTION_ALIASES)
    cleaned_intro = _clean_lines(intro_lines)
    title = cleaned_intro[0] if cleaned_intro else ""

    return {
        "title": title,
        "intro": cleaned_intro[1:] if cleaned_intro else [],
        "description": _clean_lines(sections.get("description", [])),
        "requirements": _clean_lines(sections.get("requirements", [])),
        "qualifications": _clean_lines(sections.get("qualifications", [])),
        "responsibilities": _clean_lines(sections.get("responsibilities", [])),
        "nice_to_have": _clean_lines(sections.get("nice_to_have", [])),
        "benefits": _clean_lines(sections.get("benefits", [])),
    }


def empty_jd_sections() -> dict[str, Any]:
    """Return an empty JD sections object with stable keys."""
    return {key: ([] if key != "title" else "") for key in SECTION_KEYS}


def _clean_lines(lines: list[str]) -> list[str]:
    """Strip bullets and empty lines while preserving order."""
    cleaned: list[str] = []
    for line in lines:
        stripped = strip_list_marker(line).strip()
        if stripped:
            cleaned.append(stripped)

    return cleaned
