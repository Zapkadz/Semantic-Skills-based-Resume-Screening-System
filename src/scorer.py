"""Rule-based candidate scoring and ranking."""

from __future__ import annotations

import re
from datetime import date
from typing import Any


SCORE_WEIGHTS = {
    "skill_semantic": 0.40,
    "evidence": 0.20,
    "experience": 0.15,
    "seniority": 0.10,
    "domain": 0.10,
    "nice_to_have": 0.05,
}

EVIDENCE_LEVEL_SCORES = {
    0: 0.0,
    1: 0.4,
    2: 0.7,
    3: 1.0,
}

RECOMMENDATION_THRESHOLDS = [
    (85, "Strong Review"),
    (70, "Review"),
    (55, "Maybe Review"),
    (40, "Low Priority"),
    (0, "Not Enough Evidence"),
]

SENIORITY_ORDER = {
    "Intern/Fresher": 0,
    "Junior": 1,
    "Middle": 2,
    "Senior": 3,
}

DATE_PATTERN = re.compile(
    r"(?P<start_month>\d{1,2})/(?P<start_year>\d{4})\s*-\s*"
    r"(?P<end_month>\d{1,2}|present|current|now)/?(?P<end_year>\d{4})?",
    re.IGNORECASE,
)


def score_candidate(
    job_criteria: dict[str, Any],
    resume_profile: dict[str, Any],
    matches: list[dict[str, Any]],
    nice_to_have_matches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Score one candidate with transparent rule-based components."""
    candidate_years = estimate_experience_years(resume_profile)
    candidate_seniority = detect_candidate_seniority(resume_profile, candidate_years)
    candidate_domains = detect_candidate_domains(resume_profile)

    scores = {
        "skill_semantic": calculate_skill_semantic_score(matches),
        "evidence": calculate_evidence_score(matches),
        "experience": calculate_experience_score(
            candidate_years,
            job_criteria.get("minimum_experience_years", 0),
        ),
        "seniority": calculate_seniority_score(
            job_criteria.get("seniority", "Not specified"),
            candidate_seniority,
        ),
        "domain": calculate_domain_score(
            job_criteria.get("domain", []),
            candidate_domains,
        ),
        "nice_to_have": calculate_nice_to_have_score(nice_to_have_matches),
    }
    final_score = calculate_final_score(scores)

    return {
        "candidate_name": resume_profile.get("candidate_name", ""),
        "final_score": final_score,
        "recommendation": get_recommendation_label(final_score),
        "scores": scores,
        "matched_skills": matches,
        "missing_skills": get_missing_skills(matches),
        "nice_to_have_matches": nice_to_have_matches or [],
        "seniority": candidate_seniority,
        "experience_years": round(candidate_years, 2),
        "domain": candidate_domains,
    }


def rank_candidates(candidate_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort candidate results by final score and add rank numbers."""
    ranked_results = sorted(
        candidate_results,
        key=lambda result: (
            -result.get("final_score", 0),
            -result.get("scores", {}).get("evidence", 0),
            result.get("candidate_name", ""),
        ),
    )

    return [
        {
            "rank": index,
            **result,
        }
        for index, result in enumerate(ranked_results, start=1)
    ]


def calculate_skill_semantic_score(matches: list[dict[str, Any]]) -> float:
    """Average match scores across must-have skill matches."""
    if not matches:
        return 0.0

    return _round_score(
        sum(float(match.get("score", 0.0)) for match in matches) / len(matches)
    )


def calculate_evidence_score(matches: list[dict[str, Any]]) -> float:
    """Average evidence scores across must-have skill matches."""
    if not matches:
        return 0.0

    evidence_scores = [
        EVIDENCE_LEVEL_SCORES.get(int(match.get("evidence_level", 0)), 0.0)
        for match in matches
    ]
    return _round_score(sum(evidence_scores) / len(evidence_scores))


def calculate_experience_score(
    candidate_years: float,
    required_years: int | float,
) -> float:
    """Score candidate experience against a minimum years requirement."""
    if required_years <= 0:
        return 1.0

    if candidate_years >= required_years:
        return 1.0
    if candidate_years >= 0.75 * required_years:
        return 0.75
    if candidate_years >= 0.5 * required_years:
        return 0.5

    return 0.25


def calculate_seniority_score(
    required_seniority: str,
    candidate_seniority: str,
) -> float:
    """Score seniority fit using a small transparent mapping."""
    if required_seniority == "Not specified" or candidate_seniority == "Not specified":
        return 0.75

    required_level = SENIORITY_ORDER.get(required_seniority, 1)
    candidate_level = SENIORITY_ORDER.get(candidate_seniority, 1)
    difference = candidate_level - required_level

    if difference == 0:
        return 1.0
    if difference == -1:
        return 0.65
    if difference <= -2:
        return 0.25
    if difference == 1:
        return 0.85

    return 0.70


def calculate_domain_score(
    job_domains: list[str],
    candidate_domains: list[str],
) -> float:
    """Score domain fit by overlap between job and candidate domains."""
    if not job_domains:
        return 1.0
    if not candidate_domains:
        return 0.25

    job_domain_keys = {_normalize_label(domain) for domain in job_domains}
    candidate_domain_keys = {_normalize_label(domain) for domain in candidate_domains}

    if job_domain_keys & candidate_domain_keys:
        return 1.0
    if "software" in candidate_domain_keys:
        return 0.5

    return 0.0


def calculate_nice_to_have_score(
    nice_to_have_matches: list[dict[str, Any]] | None,
) -> float:
    """Score nice-to-have coverage as matched items over total items."""
    if not nice_to_have_matches:
        return 0.5

    matched_count = sum(
        1
        for match in nice_to_have_matches
        if match.get("match_type") != "no_match"
    )
    return _round_score(matched_count / len(nice_to_have_matches))


def calculate_final_score(scores: dict[str, float]) -> int:
    """Calculate the weighted final score on a 0-100 scale."""
    weighted_score = sum(
        scores.get(component, 0.0) * weight
        for component, weight in SCORE_WEIGHTS.items()
    )
    return round(weighted_score * 100)


def get_recommendation_label(final_score: int | float) -> str:
    """Map a final score to a recruiter-facing recommendation label."""
    for threshold, label in RECOMMENDATION_THRESHOLDS:
        if final_score >= threshold:
            return label

    return "Not Enough Evidence"


def get_missing_skills(matches: list[dict[str, Any]]) -> list[str]:
    """Return required skills with no match."""
    return [
        match["required_skill"]
        for match in matches
        if match.get("match_type") == "no_match"
    ]


def estimate_experience_years(resume_profile: dict[str, Any]) -> float:
    """Estimate total experience years from parsed work experience durations."""
    total_months = 0
    for entry in resume_profile.get("work_experience", []):
        total_months += _duration_to_months(entry.get("duration", ""))

    return total_months / 12


def detect_candidate_seniority(
    resume_profile: dict[str, Any],
    candidate_years: float | None = None,
) -> str:
    """Infer candidate seniority from profile text and estimated years."""
    years = candidate_years
    if years is None:
        years = estimate_experience_years(resume_profile)

    profile_text = _profile_text(resume_profile)
    if "senior" in profile_text:
        return "Senior"
    if "middle" in profile_text or " mid " in f" {profile_text} ":
        return "Middle"

    if years >= 5:
        return "Senior"
    if years >= 2:
        return "Middle"
    if years >= 0.5 or "developer" in profile_text or "engineer" in profile_text:
        return "Junior"
    if "intern" in profile_text or "fresher" in profile_text:
        return "Intern/Fresher"

    return "Not specified"


def detect_candidate_domains(resume_profile: dict[str, Any]) -> list[str]:
    """Infer candidate domains from parsed resume text."""
    profile_text = _profile_text(resume_profile)
    domains: list[str] = []

    if any(
        keyword in profile_text
        for keyword in ("backend", "api", "service", "spring")
    ):
        domains.append("Backend")
    if any(
        keyword in profile_text
        for keyword in ("web", "rest", "api", "application")
    ):
        domains.append("Web Application")
    if any(
        keyword in profile_text
        for keyword in ("qa", "tester", "api testing", "software testing")
    ):
        domains.append("Testing")
    if any(keyword in profile_text for keyword in ("data analyst", "analytics")):
        domains.append("Data")
    if not domains and any(
        keyword in profile_text
        for keyword in ("developer", "engineer", "software")
    ):
        domains.append("Software")

    return domains


def _duration_to_months(duration: str) -> int:
    """Convert a simple duration string to inclusive months."""
    match = DATE_PATTERN.search(duration or "")
    if not match:
        return 0

    start_month = int(match.group("start_month"))
    start_year = int(match.group("start_year"))
    end_month_text = match.group("end_month")
    end_year_text = match.group("end_year")

    if end_month_text.casefold() in {"present", "current", "now"}:
        today = date.today()
        end_month = today.month
        end_year = today.year
    else:
        end_month = int(end_month_text)
        end_year = int(end_year_text or start_year)

    month_delta = (end_year - start_year) * 12 + (end_month - start_month) + 1
    return max(month_delta, 0)


def _profile_text(resume_profile: dict[str, Any]) -> str:
    """Flatten selected resume profile fields into searchable lowercase text."""
    text_parts: list[str] = [
        resume_profile.get("headline", ""),
        resume_profile.get("summary", ""),
        " ".join(resume_profile.get("raw_skills", [])),
    ]

    for entry in resume_profile.get("work_experience", []):
        text_parts.extend(
            [
                entry.get("title", ""),
                entry.get("company", ""),
                " ".join(entry.get("description", [])),
            ]
        )

    for project in resume_profile.get("projects", []):
        text_parts.extend(
            [
                project.get("name", ""),
                " ".join(project.get("description", [])),
                " ".join(project.get("technologies", [])),
            ]
        )

    return " ".join(part for part in text_parts if part).casefold()


def _normalize_label(value: str) -> str:
    """Normalize label-like text for comparison."""
    return " ".join(value.strip().casefold().split())


def _round_score(value: float) -> float:
    """Round component scores consistently."""
    return round(value, 4)
