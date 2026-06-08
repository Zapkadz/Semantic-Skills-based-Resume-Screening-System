"""Rule-based job description parser for Phase 03."""

from __future__ import annotations

import re
from typing import Any

from src.section_parser import (
    build_section_aliases,
    parse_section_heading as parse_known_section_heading,
    split_sections,
)
from src.text_normalization import normalize_search_text, repair_mojibake, strip_list_marker


RAW_SECTION_ALIASES = {
    "requirements": "requirements",
    "required skills": "requirements",
    "must have": "requirements",
    "must-have": "requirements",
    "qualifications": "requirements",
    "job requirements": "requirements",
    "required qualifications": "requirements",
    "yêu cầu": "requirements",
    "yeu cau": "requirements",
    "yêu cầu công việc": "requirements",
    "yeu cau cong viec": "requirements",
    "kỹ năng bắt buộc": "requirements",
    "ky nang bat buoc": "requirements",
    "yêu cầu ứng viên": "requirements",
    "yeu cau ung vien": "requirements",
    "nice to have": "nice_to_have",
    "nice-to-have": "nice_to_have",
    "preferred": "nice_to_have",
    "preferred skills": "nice_to_have",
    "plus": "nice_to_have",
    "bonus": "nice_to_have",
    "ưu tiên": "nice_to_have",
    "uu tien": "nice_to_have",
    "điểm cộng": "nice_to_have",
    "diem cong": "nice_to_have",
    "lợi thế": "nice_to_have",
    "loi the": "nice_to_have",
    "responsibilities": "responsibilities",
    "job responsibilities": "responsibilities",
    "job description": "responsibilities",
    "description": "responsibilities",
    "mô tả công việc": "responsibilities",
    "mo ta cong viec": "responsibilities",
    "trách nhiệm": "responsibilities",
    "trach nhiem": "responsibilities",
    "nhiệm vụ": "responsibilities",
    "nhiem vu": "responsibilities",
    "benefits": "benefits",
    "benefit": "benefits",
    "quyền lợi": "benefits",
    "quyen loi": "benefits",
    "phúc lợi": "benefits",
    "phuc loi": "benefits",
}

SECTION_ALIASES = build_section_aliases(RAW_SECTION_ALIASES)

EXPERIENCE_PATTERN = re.compile(
    r"(\d+)\+?\s*(?:year|years|yr|yrs|năm|nam)",
    re.IGNORECASE,
)


def parse_jd(text: str) -> dict[str, Any]:
    """Parse job description raw text into job criteria."""
    text = repair_mojibake(text)
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
    return split_sections(lines, SECTION_ALIASES)


def _parse_section_heading(line: str) -> tuple[str | None, str]:
    """Return normalized section name and optional inline content."""
    return parse_known_section_heading(line, SECTION_ALIASES)


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
    normalized_item = normalize_search_text(item)
    return bool(EXPERIENCE_PATTERN.search(item)) and any(
        keyword in normalized_item
        for keyword in ("experience", "kinh nghiem")
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

    if any(
        keyword in text
        for keyword in (
            "backend developer",
            "backend service",
            "rest api",
            "restful api",
            "api testing",
            "api development",
            "spring",
        )
    ):
        domains.append("Backend")
    if any(
        keyword in text
        for keyword in ("web", "rest api", "restful api", "api testing", "web application")
    ):
        domains.append("Web Application")
    if any(keyword in text for keyword in ("qa", "tester", "testing")):
        domains.append("Testing")
    if any(keyword in text for keyword in ("data analyst", "analytics", "dashboard")):
        domains.append("Data")
    if any(
        keyword in text
        for keyword in (
            "artificial intelligence",
            "machine learning",
            "deep learning",
            "model",
            "neural network",
            "tri tue nhan tao",
            "hoc may",
        )
    ):
        domains.append("AI/Machine Learning")
    if any(
        keyword in text
        for keyword in (
            "computer vision",
            "face recognition",
            "face detection",
            "image",
            "video",
            "opencv",
            "thi giac may tinh",
            "nhan dien khuon mat",
        )
    ):
        domains.append("Computer Vision")
    if any(
        keyword in text
        for keyword in (
            "ekyc",
            "biometric",
            "biometrics",
            "liveness",
            "anti spoofing",
            "face matching",
            "face verification",
            "xac thuc khuon mat",
            "chong gia mao",
        )
    ):
        domains.append("eKYC/Biometrics")
    if any(
        keyword in text
        for keyword in ("mobile", "android", "ios", "on device", "edge")
    ):
        domains.append("Mobile AI")

    return domains


def _strip_bullet(line: str) -> str:
    """Remove common bullet markers and surrounding whitespace."""
    return strip_list_marker(line)
