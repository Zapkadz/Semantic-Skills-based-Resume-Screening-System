"""Open-set requirement matching for skills outside the taxonomy."""

from __future__ import annotations

import re
from typing import Any

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.evidence_detector import (
    calculate_candidate_evidence_level,
    collect_evidence_candidates,
)
from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text


DEFAULT_OPEN_SET_SIMILARITY_THRESHOLD = 0.74
OPEN_SET_MATCH_SCORE = 0.65
SEMANTIC_ONLY_MATCH_TYPE = "semantic_only_match"
LEXICAL_EVIDENCE_MATCH_TYPE = "lexical_evidence_match"
NO_SEMANTIC_EVIDENCE_MATCH_TYPE = "no_semantic_evidence"
UNKNOWN_TAXONOMY_STATUS = "unknown"

MAX_UNKNOWN_REQUIREMENT_WORDS = 10
MAX_UNKNOWN_REQUIREMENT_LENGTH = 120
MIN_EVIDENCE_TEXT_LENGTH = 4
EVIDENCE_SIMILARITY_TOLERANCE = 0.15


def split_known_and_unknown_requirements(
    raw_requirements: list[str],
    known_skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
) -> dict[str, list[str]]:
    """Split parsed JD requirements into known taxonomy skills and unknown items."""
    normalized_requirements = normalize_skills(raw_requirements, taxonomy)
    known_requirement_keys = {make_lookup_key(skill) for skill in known_skills}
    unknown_requirements: list[str] = []

    for raw_requirement, normalized_requirement in zip(
        raw_requirements,
        normalized_requirements,
    ):
        if not normalized_requirement:
            continue

        requirement_key = make_lookup_key(normalized_requirement)
        if normalized_requirement in taxonomy or requirement_key in known_requirement_keys:
            continue

        extracted_skills = extract_taxonomy_skills_from_text(raw_requirement, taxonomy)
        if _is_covered_by_known_skills(extracted_skills, known_requirement_keys):
            continue

        if not _looks_like_unknown_requirement(normalized_requirement):
            continue

        unknown_requirements = merge_skill_lists(
            unknown_requirements,
            [normalized_requirement],
        )

    return {
        "known_requirements": list(known_skills),
        "unknown_requirements": unknown_requirements,
    }


def build_taxonomy_coverage(
    known_requirements: list[str],
    unknown_requirements: list[str],
) -> dict[str, Any]:
    """Build an explainable taxonomy coverage summary for one JD."""
    known_count = len(known_requirements)
    unknown_count = len(unknown_requirements)
    total_count = known_count + unknown_count
    coverage_ratio = 1.0 if total_count == 0 else round(known_count / total_count, 4)

    return {
        "known_count": known_count,
        "unknown_count": unknown_count,
        "coverage_ratio": coverage_ratio,
        "known_requirements": list(known_requirements),
        "unknown_requirements": list(unknown_requirements),
    }


def find_semantic_requirement_evidence(
    unknown_requirements: list[str],
    resume_profile: dict[str, Any],
    embedding_matcher: SemanticEmbeddingMatcher | None,
    threshold: float = DEFAULT_OPEN_SET_SIMILARITY_THRESHOLD,
) -> list[dict[str, Any]]:
    """Match unknown JD requirements against resume evidence sentences."""
    if not unknown_requirements:
        return []

    evidence_candidates = _collect_open_set_evidence_candidates(resume_profile)
    if not evidence_candidates:
        return [
            _build_no_semantic_evidence_match(requirement)
            for requirement in unknown_requirements
        ]

    effective_threshold = (
        getattr(embedding_matcher, "threshold", threshold)
        if embedding_matcher is not None
        and threshold == DEFAULT_OPEN_SET_SIMILARITY_THRESHOLD
        else threshold
    )
    evidence_texts = [candidate["text"] for candidate in evidence_candidates]
    similarities = (
        embedding_matcher.similarity_matrix(
            unknown_requirements,
            evidence_texts,
        )
        if embedding_matcher is not None
        else None
    )

    matches: list[dict[str, Any]] = []
    for index, requirement in enumerate(unknown_requirements):
        exact_candidate = _best_exact_evidence_candidate(
            requirement,
            evidence_candidates,
        )
        if exact_candidate is not None:
            matches.append(_build_lexical_evidence_match(requirement, exact_candidate))
            continue

        if similarities is None:
            matches.append(_build_no_semantic_evidence_match(requirement))
            continue

        requirement_similarities = similarities[index]
        best_candidate = _best_evidence_candidate(
            requirement,
            requirement_similarities,
            evidence_candidates,
            effective_threshold,
        )
        if best_candidate is None or (
            best_candidate["similarity"] < effective_threshold
            and not best_candidate.get("contains_requirement")
        ):
            matches.append(_build_no_semantic_evidence_match(requirement))
            continue

        matches.append(
            _build_semantic_only_match(
                requirement,
                best_candidate,
            )
        )

    return matches


def _is_covered_by_known_skills(
    extracted_skills: list[str],
    known_requirement_keys: set[str],
) -> bool:
    """Return True when a raw requirement is already represented by known skills."""
    if not extracted_skills:
        return False

    extracted_keys = {make_lookup_key(skill) for skill in extracted_skills}
    return bool(extracted_keys & known_requirement_keys)


def _looks_like_unknown_requirement(value: str) -> bool:
    """Keep concise requirement labels and avoid broad paragraphs."""
    clean_value = value.strip()
    if not clean_value:
        return False
    if clean_value.rstrip().endswith(":"):
        return False

    words = clean_value.split()
    if len(words) > MAX_UNKNOWN_REQUIREMENT_WORDS:
        return False
    if len(clean_value) > MAX_UNKNOWN_REQUIREMENT_LENGTH:
        return False

    normalized_value = normalize_search_text(clean_value)
    if any(
        keyword in normalized_value
        for keyword in (
            "year experience",
            "years experience",
            "kinh nghiem",
            "responsible for",
            "collaborate with",
        )
    ):
        return False

    return True


def _collect_open_set_evidence_candidates(
    resume_profile: dict[str, Any],
) -> list[dict[str, str]]:
    """Collect evidence candidates suitable for semantic requirement matching."""
    candidates = collect_evidence_candidates(resume_profile)
    filtered_candidates: list[dict[str, str]] = []
    seen_texts: set[str] = set()

    for candidate in candidates:
        text = candidate["text"].strip()
        if len(text) < MIN_EVIDENCE_TEXT_LENGTH:
            continue

        normalized_text = normalize_search_text(text)
        if normalized_text in seen_texts:
            continue

        seen_texts.add(normalized_text)
        filtered_candidates.append(candidate)

    return filtered_candidates


def _best_evidence_candidate(
    requirement: str,
    similarities: list[float],
    evidence_candidates: list[dict[str, str]],
    threshold: float,
) -> dict[str, Any] | None:
    """Return the best evidence candidate balancing similarity and evidence strength."""
    all_candidates = [
        {
            **candidate,
            "similarity": round(similarity, 4),
            "evidence_level": calculate_candidate_evidence_level(candidate),
            "contains_requirement": _contains_requirement_phrase(
                candidate["text"],
                requirement,
            ),
        }
        for similarity, candidate in zip(similarities, evidence_candidates)
    ]
    exact_candidates = [
        candidate for candidate in all_candidates if candidate["contains_requirement"]
    ]
    if exact_candidates:
        return max(
            exact_candidates,
            key=lambda candidate: (
                candidate["evidence_level"],
                candidate["similarity"],
            ),
        )

    ranked_candidates = [
        candidate for candidate in all_candidates if candidate["similarity"] >= threshold
    ]
    if not ranked_candidates:
        return None

    best_similarity = max(candidate["similarity"] for candidate in ranked_candidates)
    similarity_floor = max(threshold, best_similarity - EVIDENCE_SIMILARITY_TOLERANCE)
    eligible_candidates = [
        candidate
        for candidate in ranked_candidates
        if candidate["similarity"] >= similarity_floor
    ]

    return max(
        eligible_candidates,
        key=lambda candidate: (
            candidate["evidence_level"],
            candidate["similarity"],
        ),
    )


def _best_exact_evidence_candidate(
    requirement: str,
    evidence_candidates: list[dict[str, str]],
) -> dict[str, Any] | None:
    """Return the strongest exact lexical evidence candidate for one requirement."""
    exact_candidates = [
        {
            **candidate,
            "similarity": 1.0,
            "evidence_level": calculate_candidate_evidence_level(candidate),
        }
        for candidate in evidence_candidates
        if _contains_requirement_phrase(candidate["text"], requirement)
    ]
    if not exact_candidates:
        return None

    return max(
        exact_candidates,
        key=lambda candidate: (
            candidate["evidence_level"],
            candidate["similarity"],
        ),
    )


def _contains_requirement_phrase(text: str, requirement: str) -> bool:
    """Return True when evidence text contains the open-set requirement phrase."""
    normalized_text = normalize_search_text(text)
    normalized_requirement = normalize_search_text(requirement)
    if not normalized_text or not normalized_requirement:
        return False

    pattern = rf"(?<!\w){re.escape(normalized_requirement)}(?!\w)"
    return bool(re.search(pattern, normalized_text))


def _build_semantic_only_match(
    requirement: str,
    evidence_candidate: dict[str, Any],
) -> dict[str, Any]:
    """Build a scored semantic-only match for an unknown requirement."""
    return {
        "required_skill": requirement,
        "candidate_skill": None,
        "match_type": SEMANTIC_ONLY_MATCH_TYPE,
        "taxonomy_status": UNKNOWN_TAXONOMY_STATUS,
        "score": OPEN_SET_MATCH_SCORE,
        "similarity": evidence_candidate["similarity"],
        "evidence_level": evidence_candidate["evidence_level"],
        "evidence_text": evidence_candidate["text"],
        "evidence_source": evidence_candidate["source"],
    }


def _build_lexical_evidence_match(
    requirement: str,
    evidence_candidate: dict[str, Any],
) -> dict[str, Any]:
    """Build a scored exact-evidence match for an unknown requirement."""
    return {
        "required_skill": requirement,
        "candidate_skill": requirement,
        "match_type": LEXICAL_EVIDENCE_MATCH_TYPE,
        "taxonomy_status": UNKNOWN_TAXONOMY_STATUS,
        "score": OPEN_SET_MATCH_SCORE,
        "similarity": 1.0,
        "evidence_level": evidence_candidate["evidence_level"],
        "evidence_text": evidence_candidate["text"],
        "evidence_source": evidence_candidate["source"],
    }


def _build_no_semantic_evidence_match(requirement: str) -> dict[str, Any]:
    """Build an unmatched open-set requirement result."""
    return {
        "required_skill": requirement,
        "candidate_skill": None,
        "match_type": NO_SEMANTIC_EVIDENCE_MATCH_TYPE,
        "taxonomy_status": UNKNOWN_TAXONOMY_STATUS,
        "score": 0.0,
        "similarity": None,
        "evidence_level": 0,
        "evidence_text": "",
        "evidence_source": "none",
    }
