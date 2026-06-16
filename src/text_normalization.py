"""Shared text normalization helpers for parsers and matchers."""

from __future__ import annotations

import html
import re
import unicodedata


MOJIBAKE_MARKERS = ("Ã", "Â", "â", "Ä", "Æ", "á»", "áº", "á»", "€", "™")

LIST_MARKER_PATTERN = re.compile(
    r"^\s*(?:[-*+•–—?]\s*|\d+[\.)]\s*|[A-Za-z][\.)]\s*)"
)


def repair_mojibake(text: str) -> str:
    """Repair common UTF-8 text that was decoded as Windows-1252."""
    if not isinstance(text, str) or not text:
        return text

    if not any(marker in text for marker in MOJIBAKE_MARKERS):
        return text

    try:
        repaired = text.encode("cp1252").decode("utf-8")
    except UnicodeError:
        return text

    if _mojibake_marker_count(repaired) <= _mojibake_marker_count(text):
        return repaired

    return text


def html_to_plain_text(text: str) -> str:
    """Convert light HTML/editor content into parser-friendly plain text."""
    if not isinstance(text, str) or not text:
        return text

    decoded = html.unescape(repair_mojibake(text)).replace("\xa0", " ")
    decoded = re.sub(r"(?i)<\s*br\s*/?\s*>", "\n", decoded)
    decoded = re.sub(r"(?i)<\s*li[^>]*>", "\n- ", decoded)
    decoded = re.sub(
        r"(?i)</\s*(p|div|li|ul|ol|h[1-6]|tr|table|section)\s*>",
        "\n",
        decoded,
    )
    decoded = re.sub(r"(?i)<\s*(p|div|ul|ol|h[1-6]|tr|table|section)[^>]*>", "\n", decoded)
    decoded = re.sub(r"<[^>]+>", " ", decoded)
    decoded = html.unescape(decoded).replace("\xa0", " ")
    decoded = re.sub(r"[ \t\f\v]+", " ", decoded)
    decoded = re.sub(r" *\n *", "\n", decoded)
    decoded = re.sub(r"\n{3,}", "\n\n", decoded)
    return decoded.strip()


def strip_accents(text: str) -> str:
    """Remove Vietnamese accents while preserving the base characters."""
    repaired_text = repair_mojibake(text)
    repaired_text = repaired_text.replace("đ", "d").replace("Đ", "D")
    normalized = unicodedata.normalize("NFD", repaired_text)
    return "".join(
        character
        for character in normalized
        if unicodedata.category(character) != "Mn"
    )


def normalize_lookup_text(text: str) -> str:
    """Normalize text for case-insensitive and accent-insensitive lookup."""
    return " ".join(strip_accents(text).strip().casefold().split())


def normalize_search_text(text: str) -> str:
    """Normalize text for phrase searching with simple word boundaries."""
    normalized = strip_accents(text).casefold()
    normalized = normalized.replace(".", " ")
    normalized = normalized.replace("/", " ")
    normalized = re.sub(r"[^a-z0-9+#]+", " ", normalized)
    return " ".join(normalized.split())


def normalize_heading_text(text: str) -> str:
    """Normalize a section heading for alias lookup."""
    stripped = strip_list_marker(text).strip().rstrip(":").strip()
    normalized = strip_accents(stripped).casefold()
    normalized = re.sub(r"[^a-z0-9+#]+", " ", normalized)
    return " ".join(normalized.split())


def strip_list_marker(line: str) -> str:
    """Remove common bullet, numbering, and letter list markers."""
    return LIST_MARKER_PATTERN.sub("", line, count=1).strip()


def _mojibake_marker_count(text: str) -> int:
    """Count characters that commonly appear in mojibake strings."""
    return sum(text.count(marker) for marker in MOJIBAKE_MARKERS)
