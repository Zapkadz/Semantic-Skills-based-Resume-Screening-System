"""Rule-based job description parser for Phase 03 and later section-aware phases."""

from __future__ import annotations

import re
from typing import Any

from src.jd_section_parser import parse_jd_sections
from src.text_normalization import normalize_search_text, repair_mojibake


EXPERIENCE_PATTERN = re.compile(
    r"(\d+)\+?\s*(?:year|years|yeear|yr|yrs|nÄƒm|nam)",
    re.IGNORECASE,
)

EXPERIENCE_ONLY_PATTERN = re.compile(
    r"^\s*\d+\+?\s*(?:year|years|yeear|yr|yrs|nam)\s*$",
    re.IGNORECASE,
)


def parse_jd(text: str) -> dict[str, Any]:
    """Parse job description raw text into job criteria."""
    text = repair_mojibake(text)
    sections = parse_jd_sections(text)
    requirements = _parse_simple_list(
        [*sections.get("requirements", []), *sections.get("qualifications", [])]
    )
    nice_to_have = _parse_simple_list(sections.get("nice_to_have", []))
    description_lines = _parse_simple_list(sections.get("description", []))
    responsibility_lines = _parse_simple_list(sections.get("responsibilities", []))
    responsibilities = _merge_unique_lines(description_lines, responsibility_lines)
    job_title = _infer_job_title(sections, responsibilities)
    minimum_years = _extract_minimum_experience_years(requirements)

    return {
        "job_title": job_title,
        "description_lines": description_lines,
        "must_have_skills": [
            item for item in requirements if not _is_experience_requirement(item)
        ],
        "nice_to_have_skills": nice_to_have,
        "responsibilities": responsibilities,
        "minimum_experience_years": minimum_years,
        "seniority": _detect_seniority(job_title, minimum_years),
        "domain": _detect_domain(job_title, requirements, responsibilities),
        "sections": {
            **sections,
            "title": job_title,
        },
    }


def _parse_simple_list(lines: list[str]) -> list[str]:
    """Parse bullet or line-based section content into a clean list."""
    return [line.strip() for line in lines if line.strip()]


def _infer_job_title(
    sections: dict[str, Any],
    responsibilities: list[str],
) -> str:
    """Infer a JD title from intro text or the first responsibility heading."""
    title = str(sections.get("title", "")).strip()
    if title:
        return title

    intro_lines = list(sections.get("intro", []))
    if intro_lines:
        return intro_lines[0]

    for responsibility in responsibilities:
        clean_responsibility = responsibility.strip()
        if _looks_like_title_fallback(clean_responsibility):
            return clean_responsibility

    return ""


def _looks_like_title_fallback(value: str) -> bool:
    """Return True for short heading-like responsibility lines."""
    if not value or len(value) > 80:
        return False
    if value.endswith("."):
        return False
    if len(value.split()) > 8:
        return False

    normalized_value = normalize_search_text(value)
    if any(
        normalized_value.startswith(verb)
        for verb in ("build", "develop", "manage", "monitor", "perform", "support")
    ):
        return False

    return True


def _extract_minimum_experience_years(requirements: list[str]) -> int:
    """Extract the first minimum years value from requirement lines."""
    for requirement in requirements:
        normalized_requirement = normalize_search_text(requirement)
        match = EXPERIENCE_PATTERN.search(normalized_requirement)
        if match:
            return int(match.group(1))

    return 0


def _is_experience_requirement(item: str) -> bool:
    """Detect whether a requirement line describes experience instead of a skill."""
    normalized_item = normalize_search_text(item)
    if EXPERIENCE_ONLY_PATTERN.match(normalized_item):
        return True

    return bool(EXPERIENCE_PATTERN.search(normalized_item)) and any(
        keyword in normalized_item for keyword in ("experience", "kinh nghiem")
    )


def _detect_seniority(job_title: str, minimum_years: int) -> str:
    """Infer a simple seniority label from title and minimum years."""
    lower_title = normalize_search_text(job_title)

    if "senior" in lower_title:
        return "Senior"
    if "middle" in lower_title or "mid" in lower_title:
        return "Middle"
    if "junior" in lower_title:
        return "Junior"
    if "intern" in lower_title or "fresher" in lower_title or "thuc tap" in lower_title:
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
    text = normalize_search_text(text)
    domains: list[str] = []

    if _contains_any_phrase(
        text,
        (
            "backend developer",
            "backend service",
            "rest api",
            "restful api",
            "api testing",
            "api development",
            "spring",
        ),
    ):
        domains.append("Backend")
    if _contains_any_phrase(
        text,
        ("web", "rest api", "restful api", "api testing", "web application"),
    ):
        domains.append("Web Application")
    if _contains_any_phrase(text, ("qa", "tester", "testing")):
        domains.append("Testing")
    if _contains_any_phrase(text, ("data analyst", "analytics", "dashboard")):
        domains.append("Data")
    if _contains_any_phrase(
        text,
        (
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "model",
            "models",
            "neural network",
            "tri tue nhan tao",
            "hoc may",
        ),
    ):
        domains.append("AI/Machine Learning")
    if _contains_any_phrase(
        text,
        (
            "computer vision",
            "face recognition",
            "face detection",
            "image",
            "video",
            "opencv",
            "thi giac may tinh",
            "nhan dien khuon mat",
        ),
    ):
        domains.append("Computer Vision")
    if _contains_any_phrase(
        text,
        (
            "ekyc",
            "biometric",
            "biometrics",
            "liveness",
            "anti spoofing",
            "face matching",
            "face verification",
            "xac thuc khuon mat",
            "chong gia mao",
        ),
    ):
        domains.append("eKYC/Biometrics")
    if _contains_any_phrase(
        text,
        (
            "it security",
            "security operations",
            "governance",
            "compliance",
            "vulnerability management",
            "access management",
            "access control",
            "risk management",
            "personal data protection",
            "audit",
            "iso 27001",
        ),
    ):
        domains.append("IT Security/GRC")
    if _contains_any_phrase(
        text,
        ("mobile", "android", "ios", "on device", "edge ai", "edge device"),
    ):
        domains.append("Mobile AI")

    return domains


def _contains_any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    """Return True when normalized text contains any phrase with boundaries."""
    return any(_contains_phrase(text, phrase) for phrase in phrases)


def _contains_phrase(text: str, phrase: str) -> bool:
    """Check phrase existence with word boundaries to avoid substring hits."""
    normalized_phrase = normalize_search_text(phrase)
    if not normalized_phrase:
        return False

    pattern = rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"
    return bool(re.search(pattern, text))


def _merge_unique_lines(*collections: list[str]) -> list[str]:
    """Merge lists of lines while preserving first appearance."""
    merged: list[str] = []
    seen: set[str] = set()
    for collection in collections:
        for item in collection:
            key = normalize_search_text(item)
            if not key or key in seen:
                continue

            seen.add(key)
            merged.append(item)

    return merged
