"""Taxonomy-independent JD requirement extraction helpers."""

from __future__ import annotations

import re
from typing import Any

from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text, repair_mojibake, strip_list_marker


DEFAULT_REQUIREMENT_SOURCE = "requirements"
UNKNOWN_TAXONOMY_STATUS = "unknown"
KNOWN_TAXONOMY_STATUS = "known"
MAX_REQUIREMENT_WORDS = 8
MAX_REQUIREMENT_LENGTH = 80

HEADING_LABELS = {
    "qualification",
    "qualifications",
    "qualification experience",
    "qualifications experience",
    "skills",
    "professional requirements",
    "requirements",
    "job requirements",
    "yeu cau",
    "yeu cau cong viec",
}

SOFT_REQUIREMENT_KEYWORDS = {
    "ability to collaborate",
    "analytical",
    "communication",
    "detail oriented",
    "detail-oriented",
    "independently",
    "mindset",
    "process driven",
    "process-driven",
    "spoken english",
    "technical documentation",
    "user coordination",
    "written english",
}

LEADING_PATTERNS = (
    r"^professional requirements?\s*:\s*",
    r"^relevant certifications?\s*:\s*",
    r"^privacy certifications?\s*",
    r"^certifications?\s*:\s*",
    r"^proficiency in\s+",
    r"^strong expertise in\s+",
    r"^expertise in\s+",
    r"^knowledge of\s+",
    r"^understanding of\s+",
    r"^experience in\s+",
    r"^thành thạo\s+",
    r"^thanh thao\s+",
    r"^có kiến thức về\s+",
    r"^co kien thuc ve\s+",
    r"^có hiểu biết cơ bản về\s+",
    r"^co hieu biet co ban ve\s+",
    r"^có kinh nghiệm phát triển\s+",
    r"^co kinh nghiem phat trien\s+",
    r"^sử dụng ngôn ngữ\s+",
    r"^su dung ngon ngu\s+",
    r"^cơ sở dữ liệu\s+",
    r"^co so du lieu\s+",
    r"^at least\s+\d+\+?\s*(?:year|years|yr|yrs|yeear|năm|nam)\s+of\s+experience\s+in\s+",
    r"^ability to perform\s+",
)

TAIL_PATTERNS = (
    r"\bare an advantage\b.*$",
    r"\bis an advantage\b.*$",
    r"\bpreferably in\b.*$",
)

TRAILING_GENERIC_WORDS = {
    "certification",
    "certifications",
    "principle",
    "principles",
    "regulation",
    "regulations",
    "tool",
    "tools",
}

LOW_SIGNAL_UNITS = {
    "it",
    "privacy",
}

ACRONYM_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Z]{2,}/[A-Z0-9]+|[A-Z][A-Z0-9]*\+(?:/[A-Z0-9]+)?|[A-Z]{2,}(?:\s+\d{2,})?)"
    r"(?![A-Za-z0-9])"
)


def extract_requirement_units(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Extract concise requirement units without depending on taxonomy coverage."""
    requirement_lines = list(job_criteria.get("must_have_skills", []))
    extracted_units: list[dict[str, str]] = []
    seen_keys: set[str] = set()

    for line in requirement_lines:
        known_line_skills = extract_taxonomy_skills_from_text(str(line), taxonomy)
        for unit_text, method in _extract_units_from_line(str(line)):
            if _is_unit_covered_by_known_line_skill(unit_text, known_line_skills, taxonomy):
                continue

            taxonomy_status = _taxonomy_status(unit_text, taxonomy)
            if taxonomy_status == KNOWN_TAXONOMY_STATUS:
                continue

            lookup_key = make_lookup_key(unit_text)
            if not lookup_key or lookup_key in seen_keys:
                continue

            seen_keys.add(lookup_key)
            extracted_units.append(
                {
                    "text": unit_text,
                    "source": DEFAULT_REQUIREMENT_SOURCE,
                    "taxonomy_status": taxonomy_status,
                    "extraction_method": method,
                }
            )

    return extracted_units


def extract_unknown_requirement_texts(
    job_criteria: dict[str, Any],
    jd_text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Return only unknown requirement text values for open-set matching."""
    units = extract_requirement_units(job_criteria, jd_text, taxonomy)
    return merge_skill_lists([unit["text"] for unit in units])


def build_screening_confidence(
    known_requirements: list[str],
    open_set_requirements: list[str],
    embedding_matcher: Any | None,
) -> dict[str, Any]:
    """Build confidence metadata for taxonomy/open-set screening coverage."""
    embedding_enabled = embedding_matcher is not None
    warnings: list[str] = []

    if open_set_requirements and not embedding_enabled:
        warnings.append(
            "Open-set requirements detected but embedding matcher is disabled."
        )

    if open_set_requirements and not embedding_enabled:
        level = "low"
    elif open_set_requirements and not known_requirements:
        level = "medium"
    else:
        level = "high"

    return {
        "level": level,
        "known_requirement_count": len(known_requirements),
        "open_set_requirement_count": len(open_set_requirements),
        "embedding_enabled": embedding_enabled,
        "warnings": warnings,
    }


def _extract_units_from_line(line: str) -> list[tuple[str, str]]:
    """Extract concise requirement units from one JD requirement line."""
    clean_line = _clean_line(line)
    if not clean_line or _should_ignore_line(clean_line):
        return []

    explicit_terms = _extract_explicit_terms(clean_line)
    body = _strip_parentheses(clean_line)
    body = _remove_leading_patterns(body)
    body = _remove_tail_patterns(body)
    body_units = _split_requirement_body(body)

    units: list[tuple[str, str]] = []
    for term in explicit_terms:
        normalized_term = _normalize_unit(term)
        if _should_keep_unit(normalized_term):
            units.append((normalized_term, "explicit_term"))

    for unit in body_units:
        normalized_unit = _normalize_unit(unit)
        if _should_keep_unit(normalized_unit):
            units.append((normalized_unit, "pattern_split"))

    if not units:
        fallback_unit = _normalize_unit(clean_line)
        if _should_keep_unit(fallback_unit):
            units.append((fallback_unit, "fallback_line"))

    return _dedupe_units(units)


def _clean_line(line: str) -> str:
    """Repair encoding and remove bullets/noisy spaces."""
    repaired_line = repair_mojibake(line)
    cleaned = strip_list_marker(repaired_line).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip(" -")


def _should_ignore_line(line: str) -> bool:
    """Return True for headings and soft/general requirements."""
    normalized_line = normalize_search_text(line.rstrip(":"))
    if not normalized_line:
        return True
    if normalized_line in HEADING_LABELS:
        return True
    if line.rstrip().endswith(":") and len(normalized_line.split()) <= 4:
        return True
    if _is_experience_only_requirement(normalized_line):
        return True
    if any(keyword in normalized_line for keyword in SOFT_REQUIREMENT_KEYWORDS):
        return True

    return False


def _extract_explicit_terms(line: str) -> list[str]:
    """Extract explicit acronyms/certifications and e.g. terms."""
    terms: list[str] = []
    for parenthetical in re.findall(r"\(([^)]*)\)", line):
        parenthetical = re.sub(r"^(?:e\.g\.|eg|such as)\s*,?\s*", "", parenthetical, flags=re.IGNORECASE)
        terms.extend(_split_requirement_body(parenthetical))

    terms.extend(match.group(0) for match in ACRONYM_PATTERN.finditer(line))
    return terms


def _strip_parentheses(line: str) -> str:
    """Remove parenthetical details after extracting explicit terms."""
    return re.sub(r"\([^)]*\)", "", line)


def _remove_leading_patterns(line: str) -> str:
    """Remove common JD requirement lead-in phrases."""
    body = line.strip()
    changed = True
    while changed:
        changed = False
        for pattern in LEADING_PATTERNS:
            new_body = re.sub(pattern, "", body, flags=re.IGNORECASE).strip()
            if new_body != body:
                body = new_body
                changed = True

    return body


def _remove_tail_patterns(line: str) -> str:
    """Remove common non-skill trailing clauses."""
    body = line.strip()
    for pattern in TAIL_PATTERNS:
        body = re.sub(pattern, "", body, flags=re.IGNORECASE).strip()

    return body


def _split_requirement_body(body: str) -> list[str]:
    """Split comma/connector-separated requirement text into candidate units."""
    body = body.replace("&", ",")
    body = re.sub(r"\band/or\b", ",", body, flags=re.IGNORECASE)
    body = re.sub(r"\bor\b", ",", body, flags=re.IGNORECASE)
    body = re.sub(r"\band\b", ",", body, flags=re.IGNORECASE)
    return [part.strip() for part in re.split(r"[,;]", body) if part.strip()]


def _normalize_unit(unit: str) -> str:
    """Normalize one extracted requirement unit."""
    normalized = unit.strip()
    normalized = _remove_leading_patterns(normalized)
    normalized = re.sub(r"^(?:and|or|both|similar)\s+", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s+for\s+both\s+", " for ", normalized, flags=re.IGNORECASE)
    normalized = normalized.strip(" .;:-")
    normalized = _remove_trailing_generic_words(normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def _remove_trailing_generic_words(unit: str) -> str:
    """Remove generic suffix words such as tools/regulations."""
    words = unit.split()
    while len(words) > 1 and make_lookup_key(words[-1]) in TRAILING_GENERIC_WORDS:
        words.pop()

    return " ".join(words)


def _should_keep_unit(unit: str) -> bool:
    """Return True when a candidate unit is specific enough for open-set matching."""
    if not unit:
        return False

    normalized_unit = normalize_search_text(unit)
    if not normalized_unit or normalized_unit in HEADING_LABELS:
        return False
    if normalized_unit in LOW_SIGNAL_UNITS:
        return False
    if any(keyword in normalized_unit for keyword in SOFT_REQUIREMENT_KEYWORDS):
        return False
    if _is_experience_only_requirement(normalized_unit):
        return False
    if len(unit) > MAX_REQUIREMENT_LENGTH:
        return False
    if len(unit.split()) > MAX_REQUIREMENT_WORDS:
        return False

    return True


def _is_experience_only_requirement(normalized_text: str) -> bool:
    """Detect lines that only describe experience years."""
    if re.fullmatch(r"\d+\+?\s*(?:year|years|yr|yrs|nam|n m)", normalized_text):
        return True
    if "experience in" in normalized_text:
        return False

    return bool(re.search(r"\d+\+?\s*(?:year|years|yr|yrs|nam|năm|yeear)", normalized_text)) and (
        "experience" in normalized_text or "kinh nghiem" in normalized_text
    )


def _taxonomy_status(text: str, taxonomy: dict[str, dict[str, Any]]) -> str:
    """Return whether a requirement unit is already covered by taxonomy."""
    normalized = normalize_skills([text], taxonomy)
    if normalized and normalized[0] in taxonomy:
        return KNOWN_TAXONOMY_STATUS
    if extract_taxonomy_skills_from_text(text, taxonomy):
        return KNOWN_TAXONOMY_STATUS

    return UNKNOWN_TAXONOMY_STATUS


def _is_unit_covered_by_known_line_skill(
    unit_text: str,
    known_line_skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
) -> bool:
    """Return True when an extracted unit is only part of a known taxonomy skill."""
    unit_key = make_lookup_key(unit_text)
    if not unit_key:
        return True

    for skill in known_line_skills:
        skill_terms = [skill]
        skill_terms.extend(
            alias
            for alias in taxonomy.get(skill, {}).get("aliases", [])
            if isinstance(alias, str)
        )

        for term in skill_terms:
            term_key = make_lookup_key(term)
            if unit_key == term_key:
                return True
            if unit_key in term_key.split():
                return True

    return False


def _dedupe_units(units: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Deduplicate units while preserving extraction order."""
    deduped: list[tuple[str, str]] = []
    seen_keys: set[str] = set()

    for unit, method in units:
        lookup_key = make_lookup_key(unit)
        if not lookup_key or lookup_key in seen_keys:
            continue

        seen_keys.add(lookup_key)
        deduped.append((unit, method))

    return deduped
