"""Reusable section splitting helpers for plain-text JD and resume parsers."""

from __future__ import annotations

from collections import OrderedDict

from src.text_normalization import normalize_heading_text, strip_list_marker


def build_section_aliases(raw_aliases: dict[str, str]) -> dict[str, str]:
    """Build normalized section aliases from human-readable alias text."""
    return {
        normalize_heading_text(alias): section_name
        for alias, section_name in raw_aliases.items()
    }


def split_sections(
    lines: list[str],
    section_aliases: dict[str, str],
) -> tuple[list[str], dict[str, list[str]]]:
    """Split raw lines into intro lines and named sections."""
    intro_lines: list[str] = []
    sections: dict[str, list[str]] = OrderedDict()
    current_section: str | None = None

    for line in lines:
        section_name, inline_content = parse_section_heading(line, section_aliases)
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


def parse_section_heading(
    line: str,
    section_aliases: dict[str, str],
) -> tuple[str | None, str]:
    """Return normalized section name and optional inline content."""
    stripped = strip_list_marker(line).strip()
    if not stripped:
        return None, ""

    if ":" in stripped:
        heading, inline_content = stripped.split(":", 1)
        section_name = section_aliases.get(normalize_heading_text(heading))
        if section_name:
            return section_name, inline_content.strip()

    if _can_be_bare_heading(stripped):
        section_name = section_aliases.get(normalize_heading_text(stripped))
        if section_name:
            return section_name, ""

    return None, ""


def _can_be_bare_heading(value: str) -> bool:
    """Avoid treating long prose lines as section headings."""
    stripped = value.strip()
    if len(stripped) > 80:
        return False
    if stripped.endswith((".", "!", "?")):
        return False

    return True
