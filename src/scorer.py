"""Rule-based candidate scoring and ranking."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

from src.role_family import (
    GENERIC_TECH,
    calculate_role_family_alignment,
    infer_candidate_role_profile,
)
from src.technical_intent import CONTEXTUAL_INTENT, CORE_INTENT, SUPPORTING_INTENT
from src.text_normalization import normalize_search_text, repair_mojibake, strip_accents


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

NO_MATCH_TYPES = {"no_match", "no_semantic_evidence"}
REVIEW_SCORE_CAP = 69
STRONG_REVIEW_SCORE_CAP = 84
REVIEW_SCORE_THRESHOLD = 70
STRONG_REVIEW_SCORE_THRESHOLD = 85
MIN_REVIEW_SKILL_SEMANTIC_SCORE = 0.55
MIN_REVIEW_EVIDENCE_SCORE = 0.50
MIN_REVIEW_CONFIRMED_COVERAGE = 0.60
MIN_STRONG_REVIEW_CONFIRMED_COVERAGE = 0.75
MIN_REQUIREMENTS_FOR_COVERAGE_GATE = 3

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
    r"(?P<end_month>\d{1,2}|present|current|now|nay|hien tai)"
    r"/?(?P<end_year>\d{4})?",
    re.IGNORECASE,
)
EXPLICIT_EXPERIENCE_PATTERN = re.compile(
    r"(?:(?:over|more than|at least|minimum|hon|tren|toi thieu)\s+)?"
    r"(?P<years>\d+)\+?\s*(?:year|years|yr|yrs|nam)\s+"
    r"(?:of\s+)?(?:experience|kinh nghiem)"
)
INTENT_STRENGTHS = (
    CORE_INTENT,
    SUPPORTING_INTENT,
    CONTEXTUAL_INTENT,
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
    raw_base_score = calculate_final_score(scores)
    core_requirement_fit_summary = calculate_requirement_fit_summary(matches)
    candidate_role_profile = infer_candidate_role_profile(
        resume_profile,
        matches=matches,
    )
    role_family_alignment = calculate_role_family_alignment(
        job_criteria.get("job_role_profile", {}),
        candidate_role_profile,
    )
    role_alignment_impact = build_role_alignment_impact(
        role_family_alignment,
        matches,
        core_requirement_fit_summary,
    )
    role_score_adjustment = int(role_alignment_impact.get("adjustment", 0) or 0)
    role_calibrated_score = max(0, min(100, raw_base_score + role_score_adjustment))
    final_score, hard_skill_gate = apply_hard_skill_gate(
        role_calibrated_score,
        scores,
        matches,
    )

    return {
        "candidate_name": resume_profile.get("candidate_name", ""),
        "raw_base_score": raw_base_score,
        "role_calibrated_score": role_calibrated_score,
        "base_score": role_calibrated_score,
        "role_score_adjustment": role_score_adjustment,
        "final_score": final_score,
        "recommendation": get_recommendation_label(final_score),
        "scores": scores,
        "hard_skill_gate": hard_skill_gate,
        "matched_skills": matches,
        "missing_skills": get_missing_skills(matches),
        "nice_to_have_matches": nice_to_have_matches or [],
        "seniority": candidate_seniority,
        "experience_years": round(candidate_years, 2),
        "domain": candidate_domains,
        "core_requirement_fit_summary": core_requirement_fit_summary,
        "candidate_role_profile": candidate_role_profile,
        "role_family_alignment": {
            **role_family_alignment,
            "applied_adjustment": role_score_adjustment,
        },
        "role_alignment_impact": role_alignment_impact,
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


def calculate_requirement_fit_summary(
    matches: list[dict[str, Any]],
) -> dict[str, dict[str, int | float]]:
    """Summarize overall/core/supporting/contextual requirement coverage."""
    buckets = {
        strength: _new_requirement_fit_bucket()
        for strength in (*INTENT_STRENGTHS, "overall")
    }

    for match in matches:
        strength = _normalize_intent_strength(match.get("intent_strength"))
        bucket_names = ["overall", strength]
        positive_match = _is_positive_match(match)
        evidence_level = int(match.get("evidence_level", 0))
        semantic_only_match = match.get("match_type") == "semantic_only_match"

        for bucket_name in bucket_names:
            bucket = buckets[bucket_name]
            bucket["total"] += 1
            if positive_match:
                bucket["positive_match_count"] += 1
                if evidence_level >= 2:
                    bucket["confirmed_match_count"] += 1
                else:
                    bucket["weak_match_count"] += 1
                if semantic_only_match:
                    bucket["semantic_only_match_count"] += 1
            else:
                bucket["missing_count"] += 1

    for bucket in buckets.values():
        total = int(bucket["total"])
        positive = int(bucket["positive_match_count"])
        bucket["positive_coverage"] = _ratio_or_zero(positive, total)
        bucket["confirmed_coverage"] = _ratio_or_zero(
            int(bucket["confirmed_match_count"]),
            total,
        )
        bucket["weak_match_ratio"] = _ratio_or_zero(
            int(bucket["weak_match_count"]),
            positive,
        )
        bucket["semantic_only_ratio"] = _ratio_or_zero(
            int(bucket["semantic_only_match_count"]),
            positive,
        )

    return buckets


def build_role_alignment_impact(
    role_family_alignment: dict[str, Any],
    matches: list[dict[str, Any]],
    core_requirement_fit_summary: dict[str, dict[str, int | float]] | None = None,
) -> dict[str, Any]:
    """Build one explainable role-aware scoring adjustment payload."""
    fit_summary = core_requirement_fit_summary or calculate_requirement_fit_summary(matches)
    status = str(role_family_alignment.get("status", ""))
    adjustment_hint = int(role_family_alignment.get("adjustment_hint", 0) or 0)
    overall_bucket = fit_summary.get("overall", _new_requirement_fit_bucket())
    core_bucket = fit_summary.get(CORE_INTENT, _new_requirement_fit_bucket())
    semantic_only_ratio = float(overall_bucket.get("semantic_only_ratio", 0.0))
    core_total = int(core_bucket.get("total", 0))
    core_positive_coverage = float(core_bucket.get("positive_coverage", 0.0))
    core_confirmed_coverage = float(core_bucket.get("confirmed_coverage", 0.0))
    core_semantic_only_ratio = float(core_bucket.get("semantic_only_ratio", 0.0))

    adjustment = 0
    applied = False
    reason_code = "no_adjustment"
    reason = str(role_family_alignment.get("note", "")).strip()

    if status == "strong_alignment":
        reason_code = "strong_same_role_alignment"
        if core_total >= 2 and core_confirmed_coverage >= 0.67:
            reason = (
                "The candidate's strongest technical profile matches the JD role "
                "family and most core requirements have confirmed evidence."
            )
        else:
            reason = reason or (
                "The candidate's strongest technical profile aligns with the JD role family."
            )
    elif status == "generic_alignment":
        reason_code = "generic_candidate_role_signal"
        reason = reason or (
            "The candidate profile is still too generic for a strong role-aware adjustment."
        )
    elif status == "unknown_alignment":
        reason_code = "generic_job_role_signal"
        reason = reason or (
            "The JD role-family signal is too generic for role-aware calibration."
        )
    elif status == "partial_alignment":
        if core_total >= 1 and core_semantic_only_ratio >= 0.5 and core_confirmed_coverage < 0.5:
            adjustment = min(adjustment_hint, -4)
            applied = True
            reason_code = "adjacent_role_semantic_core_overlap"
            reason = (
                "The profile overlaps with an adjacent role family, but most core "
                "requirements are still semantic-only or weakly confirmed."
            )
        elif core_total >= 1 and core_positive_coverage >= 0.5 and core_confirmed_coverage < 0.5:
            adjustment = min(adjustment_hint, -3)
            applied = True
            reason_code = "adjacent_role_weak_core_overlap"
            reason = (
                "The profile is adjacent to the JD role family, but core "
                "requirements still need stronger direct evidence."
            )
        elif semantic_only_ratio >= 0.5 and adjustment_hint < 0:
            adjustment = adjustment_hint
            applied = True
            reason_code = "adjacent_role_semantic_overlap"
            reason = (
                "The profile overlaps with an adjacent role family, but several "
                "matches rely on semantic-only evidence."
            )
        else:
            reason_code = "adjacent_role_with_confirmed_overlap"
            reason = reason or (
                "The profile shows adjacent role-family overlap, but confirmed evidence keeps the calibration light."
            )
    elif status == "misaligned":
        if core_total >= 2 and core_semantic_only_ratio >= 0.5 and core_confirmed_coverage < 0.5:
            adjustment = min(adjustment_hint, -10)
            applied = True
            reason_code = "misaligned_semantic_core_overlap"
            reason = (
                "The JD is concentrated in one role family, but the candidate's "
                "core overlap is mostly semantic-only or weakly confirmed."
            )
        elif core_total >= 1 and core_positive_coverage >= 0.5 and core_confirmed_coverage == 0.0:
            adjustment = min(adjustment_hint, -8)
            applied = True
            reason_code = "misaligned_unconfirmed_core_overlap"
            reason = (
                "Some core overlap exists, but it is not backed by confirmed "
                "evidence inside the JD's primary role family."
            )
        elif semantic_only_ratio > 0.0 and adjustment_hint < 0:
            adjustment = max(adjustment_hint, -4)
            applied = True
            reason_code = "misaligned_partial_overlap"
            reason = (
                "Some technical overlap exists, but the candidate's strongest "
                "profile still points to a different primary role family."
            )
        else:
            reason_code = "misaligned_without_reliable_core_overlap"
            reason = reason or (
                "The candidate's strongest technical profile points to a different role family than the JD."
            )

    return {
        "status": status,
        "applied": applied,
        "adjustment": adjustment,
        "reason_code": reason_code,
        "reason": reason,
        "semantic_only_ratio": semantic_only_ratio,
        "core_total": core_total,
        "core_positive_coverage": core_positive_coverage,
        "core_confirmed_coverage": core_confirmed_coverage,
        "core_semantic_only_ratio": core_semantic_only_ratio,
    }


def apply_hard_skill_gate(
    base_score: int,
    scores: dict[str, float],
    matches: list[dict[str, Any]],
) -> tuple[int, dict[str, Any]]:
    """Cap high recommendations when must-have hard-skill evidence is weak."""
    gate = evaluate_hard_skill_gate(base_score, scores, matches)
    score_cap = gate.get("score_cap")
    final_score = min(base_score, int(score_cap)) if score_cap is not None else base_score

    gate["applied"] = final_score < base_score
    gate["base_score"] = base_score
    gate["final_score"] = final_score
    return final_score, gate


def evaluate_hard_skill_gate(
    base_score: int,
    scores: dict[str, float],
    matches: list[dict[str, Any]],
) -> dict[str, Any]:
    """Evaluate minimum hard-skill evidence needed for Review labels."""
    metrics = calculate_hard_skill_gate_metrics(matches)
    reasons: list[dict[str, str]] = []
    score_cap: int | None = None

    if base_score >= REVIEW_SCORE_THRESHOLD:
        if scores.get("skill_semantic", 0.0) < MIN_REVIEW_SKILL_SEMANTIC_SCORE:
            reasons.append(
                _gate_reason(
                    "low_skill_coverage",
                    "Must-have skill coverage is below the Review threshold.",
                )
            )
            score_cap = REVIEW_SCORE_CAP

        if scores.get("evidence", 0.0) < MIN_REVIEW_EVIDENCE_SCORE:
            reasons.append(
                _gate_reason(
                    "weak_evidence",
                    "Evidence strength is below the Review threshold.",
                )
            )
            score_cap = REVIEW_SCORE_CAP

        if (
            metrics["total_must_have"] >= MIN_REQUIREMENTS_FOR_COVERAGE_GATE
            and metrics["confirmed_coverage"] < MIN_REVIEW_CONFIRMED_COVERAGE
        ):
            reasons.append(
                _gate_reason(
                    "low_confirmed_coverage",
                    (
                        "Confirmed hard-skill evidence coverage is below the "
                        "Review threshold."
                    ),
                )
            )
            score_cap = REVIEW_SCORE_CAP

    if (
        score_cap is None
        and base_score >= STRONG_REVIEW_SCORE_THRESHOLD
        and metrics["total_must_have"] >= MIN_REQUIREMENTS_FOR_COVERAGE_GATE
        and metrics["confirmed_coverage"] < MIN_STRONG_REVIEW_CONFIRMED_COVERAGE
    ):
        reasons.append(
            _gate_reason(
                "strong_review_confirmed_coverage",
                (
                    "Confirmed hard-skill evidence coverage is below the "
                    "Strong Review threshold."
                ),
            )
        )
        score_cap = STRONG_REVIEW_SCORE_CAP

    return {
        "passed": score_cap is None,
        "score_cap": score_cap,
        "reasons": reasons,
        "metrics": metrics,
    }


def calculate_hard_skill_gate_metrics(
    matches: list[dict[str, Any]],
) -> dict[str, int | float]:
    """Summarize must-have skill evidence quality for gating."""
    total = len(matches)
    positive_matches = [
        match
        for match in matches
        if _is_positive_match(match)
    ]
    confirmed_matches = [
        match
        for match in positive_matches
        if int(match.get("evidence_level", 0)) >= 2
    ]
    weak_matches = [
        match
        for match in positive_matches
        if int(match.get("evidence_level", 0)) <= 1
    ]
    missing_matches = [
        match
        for match in matches
        if not _is_positive_match(match)
    ]

    return {
        "total_must_have": total,
        "positive_match_count": len(positive_matches),
        "confirmed_match_count": len(confirmed_matches),
        "weak_match_count": len(weak_matches),
        "missing_count": len(missing_matches),
        "positive_coverage": _coverage(len(positive_matches), total),
        "confirmed_coverage": _coverage(len(confirmed_matches), total),
        "weak_match_ratio": _coverage(len(weak_matches), len(positive_matches)),
    }


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
        if match.get("match_type") in NO_MATCH_TYPES
    ]


def estimate_experience_years(resume_profile: dict[str, Any]) -> float:
    """Estimate total experience years from parsed work experience durations."""
    total_months = 0
    for entry in resume_profile.get("work_experience", []):
        total_months += _duration_to_months(entry.get("duration", ""))

    duration_years = total_months / 12
    explicit_years = _extract_explicit_experience_years(resume_profile)
    return max(duration_years, explicit_years)


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
    if "lead" in profile_text or "truong nhom" in profile_text:
        return "Senior"

    if years >= 5:
        return "Senior"
    if years >= 2:
        return "Middle"
    if years >= 0.5 or any(
        keyword in profile_text
        for keyword in ("developer", "engineer", "ky su", "lap trinh vien")
    ):
        return "Junior"
    if "intern" in profile_text or "fresher" in profile_text or "thuc tap" in profile_text:
        return "Intern/Fresher"

    return "Not specified"


def detect_candidate_domains(resume_profile: dict[str, Any]) -> list[str]:
    """Infer candidate domains from parsed resume text."""
    profile_text = _profile_text(resume_profile)
    domains: list[str] = []

    if _contains_any_phrase(profile_text, ("backend", "api", "spring")):
        domains.append("Backend")
    if _contains_any_phrase(profile_text, ("web", "rest", "api", "web application")):
        domains.append("Web Application")
    if _contains_any_phrase(profile_text, ("qa", "tester", "api testing", "software testing")):
        domains.append("Testing")
    if _contains_any_phrase(profile_text, ("data analyst", "analytics")):
        domains.append("Data")
    if _contains_any_phrase(
        profile_text,
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
        profile_text,
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
        profile_text,
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
        profile_text,
        (
            "it security",
            "security operations",
            "governance",
            "compliance",
            "vulnerability management",
            "access management",
            "access governance",
            "risk management",
            "personal data protection",
            "audit",
            "iso 27001",
        ),
    ):
        domains.append("IT Security/GRC")
    if _contains_any_phrase(
        profile_text,
        ("mobile", "android", "ios", "on device", "edge ai", "edge device"),
    ):
        domains.append("Mobile AI")
    if not domains and any(
        keyword in profile_text
        for keyword in ("developer", "engineer", "software")
    ):
        domains.append("Software")

    return domains


def _semantic_only_ratio(matches: list[dict[str, Any]]) -> float:
    """Return the ratio of positive matches that depend on semantic-only evidence."""
    positive_matches = [match for match in matches if _is_positive_match(match)]
    if not positive_matches:
        return 0.0

    semantic_only_matches = [
        match
        for match in positive_matches
        if match.get("match_type") == "semantic_only_match"
    ]
    return _coverage(len(semantic_only_matches), len(positive_matches))


def _new_requirement_fit_bucket() -> dict[str, int | float]:
    """Create one zeroed requirement-fit bucket."""
    return {
        "total": 0,
        "positive_match_count": 0,
        "confirmed_match_count": 0,
        "weak_match_count": 0,
        "missing_count": 0,
        "semantic_only_match_count": 0,
        "positive_coverage": 0.0,
        "confirmed_coverage": 0.0,
        "weak_match_ratio": 0.0,
        "semantic_only_ratio": 0.0,
    }


def _normalize_intent_strength(value: Any) -> str:
    """Map arbitrary intent-strength values to stable known buckets."""
    normalized_value = str(value or "").strip().casefold()
    if normalized_value == CORE_INTENT:
        return CORE_INTENT
    if normalized_value == SUPPORTING_INTENT:
        return SUPPORTING_INTENT

    return CONTEXTUAL_INTENT


def _duration_to_months(duration: str) -> int:
    """Convert a simple duration string to inclusive months."""
    normalized_duration = _normalize_duration_text(duration)
    match = DATE_PATTERN.search(normalized_duration)
    if not match:
        return 0

    start_month = int(match.group("start_month"))
    start_year = int(match.group("start_year"))
    end_month_text = match.group("end_month")
    end_year_text = match.group("end_year")

    if normalize_search_text(end_month_text) in {
        "present",
        "current",
        "now",
        "nay",
        "hien tai",
    }:
        today = date.today()
        end_month = today.month
        end_year = today.year
    else:
        end_month = int(end_month_text)
        end_year = int(end_year_text or start_year)

    month_delta = (end_year - start_year) * 12 + (end_month - start_month) + 1
    return max(month_delta, 0)


def _normalize_duration_text(duration: str) -> str:
    """Normalize date ranges from English/Vietnamese CV text."""
    normalized = strip_accents(repair_mojibake(duration or "")).casefold()
    normalized = normalized.replace("–", "-").replace("—", "-")
    normalized = re.sub(r"\b(?:to|den|toi)\b", "-", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def _extract_explicit_experience_years(resume_profile: dict[str, Any]) -> float:
    """Extract explicit summary phrases like 'over 5 years of experience'."""
    text_parts = [
        str(resume_profile.get("headline", "")),
        str(resume_profile.get("summary", "")),
    ]
    for entry in resume_profile.get("work_experience", []):
        text_parts.append(str(entry.get("title", "")))
        text_parts.extend(str(item) for item in entry.get("description", []))

    normalized_text = normalize_search_text(" ".join(text_parts))
    matches = [
        int(match.group("years"))
        for match in EXPLICIT_EXPERIENCE_PATTERN.finditer(normalized_text)
    ]
    return float(max(matches)) if matches else 0.0


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

    return normalize_search_text(" ".join(part for part in text_parts if part))


def _normalize_label(value: str) -> str:
    """Normalize label-like text for comparison."""
    return " ".join(value.strip().casefold().split())


def _contains_any_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    """Return True when normalized text contains any phrase with boundaries."""
    return any(_contains_phrase(text, phrase) for phrase in phrases)


def _contains_phrase(text: str, phrase: str) -> bool:
    """Check phrase existence with word boundaries."""
    normalized_phrase = normalize_search_text(phrase)
    if not normalized_phrase:
        return False

    pattern = rf"(?<!\w){re.escape(normalized_phrase)}(?!\w)"
    return bool(re.search(pattern, text))


def _is_positive_match(match: dict[str, Any]) -> bool:
    """Return True when one must-have item has any positive matching signal."""
    return (
        float(match.get("score", 0.0)) > 0.0
        and match.get("match_type") not in NO_MATCH_TYPES
    )


def _coverage(count: int, total: int) -> float:
    """Return a rounded coverage ratio with zero-safe division."""
    if total <= 0:
        return 1.0

    return _round_score(count / total)


def _gate_reason(code: str, message: str) -> dict[str, str]:
    """Build a stable hard-skill gate reason object."""
    return {"code": code, "message": message}


def _ratio_or_zero(count: int, total: int) -> float:
    """Return a rounded ratio, but keep empty buckets at 0.0 instead of 1.0."""
    if total <= 0:
        return 0.0

    return _round_score(count / total)


def _round_score(value: float) -> float:
    """Round component scores consistently."""
    return round(value, 4)
