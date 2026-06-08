"""Evidence detection for matched resume skills."""

from __future__ import annotations

import re
from typing import Any

from src.text_normalization import normalize_search_text


ACTION_VERBS = {
    "analyzed",
    "built",
    "configured",
    "created",
    "deployed",
    "designed",
    "developed",
    "implemented",
    "integrated",
    "maintained",
    "managed",
    "optimized",
    "tested",
    "used",
    "wrote",
    "ap dung",
    "cai dat",
    "cai thien",
    "danh gia",
    "huan luyen",
    "kiem thu",
    "phan tich",
    "phat hien",
    "phat trien",
    "su dung",
    "thiet ke",
    "theo doi",
    "tich hop",
    "toi uu",
    "trien khai",
    "xay dung",
}

ACTION_SOURCES = {"work_experience", "projects"}


def detect_evidence(
    skill: str,
    resume_profile: dict[str, Any],
    taxonomy: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Detect the strongest evidence for one skill in a parsed resume profile."""
    evidence = _find_best_evidence(_expand_search_terms([skill], taxonomy), resume_profile)
    return {
        "skill": skill,
        "evidence_level": evidence["evidence_level"],
        "evidence_text": evidence["evidence_text"],
        "evidence_source": evidence["evidence_source"],
    }


def detect_all_evidence(
    matches: list[dict[str, Any]],
    resume_profile: dict[str, Any],
    taxonomy: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Enrich match results with evidence fields from the resume profile."""
    enriched_matches: list[dict[str, Any]] = []

    for match in matches:
        search_terms = _expand_search_terms(_build_search_terms(match), taxonomy)
        evidence = _find_best_evidence(search_terms, resume_profile)

        enriched_match = {
            **match,
            "evidence_level": evidence["evidence_level"],
            "evidence_text": evidence["evidence_text"],
            "evidence_source": evidence["evidence_source"],
        }
        enriched_matches.append(enriched_match)

    return enriched_matches


def _build_search_terms(match: dict[str, Any]) -> list[str]:
    """Build evidence search terms from a match result."""
    terms: list[str] = []
    for key in ("candidate_skill", "required_skill"):
        value = match.get(key)
        if isinstance(value, str) and value.strip():
            terms.append(value.strip())

    return _dedupe_terms(terms)


def _expand_search_terms(
    terms: list[str],
    taxonomy: dict[str, dict[str, Any]] | None,
) -> list[str]:
    """Add taxonomy aliases for canonical skill search terms."""
    expanded_terms = list(terms)
    if not taxonomy:
        return _dedupe_terms(expanded_terms)

    for term in terms:
        metadata = taxonomy.get(term)
        if not metadata:
            continue

        expanded_terms.extend(
            alias
            for alias in metadata.get("aliases", [])
            if isinstance(alias, str) and alias.strip()
        )

    return _dedupe_terms(expanded_terms)


def _find_best_evidence(
    search_terms: list[str],
    resume_profile: dict[str, Any],
) -> dict[str, Any]:
    """Find the highest-level evidence across structured resume fields."""
    best_evidence = _empty_evidence()

    for candidate in _collect_evidence_candidates(resume_profile):
        if not _contains_any_skill(candidate["text"], search_terms):
            continue

        evidence_level = _calculate_evidence_level(candidate)
        if evidence_level > best_evidence["evidence_level"]:
            best_evidence = {
                "evidence_level": evidence_level,
                "evidence_text": candidate["text"],
                "evidence_source": candidate["source"],
            }

        if best_evidence["evidence_level"] == 3:
            break

    return best_evidence


def _collect_evidence_candidates(resume_profile: dict[str, Any]) -> list[dict[str, str]]:
    """Collect searchable evidence text from a parsed resume profile."""
    candidates: list[dict[str, str]] = []

    for entry in resume_profile.get("work_experience", []):
        for description in entry.get("description", []):
            candidates.append({"source": "work_experience", "text": description})

    for project in resume_profile.get("projects", []):
        for description in project.get("description", []):
            candidates.append({"source": "projects", "text": description})
        for technology in project.get("technologies", []):
            candidates.append({"source": "projects", "text": technology})

    summary = resume_profile.get("summary", "")
    if summary:
        candidates.append({"source": "summary", "text": summary})

    headline = resume_profile.get("headline", "")
    if headline:
        candidates.append({"source": "headline", "text": headline})

    for skill in resume_profile.get("raw_skills", []):
        candidates.append({"source": "skills", "text": skill})

    return [
        {"source": candidate["source"], "text": candidate["text"].strip()}
        for candidate in candidates
        if isinstance(candidate.get("text"), str) and candidate["text"].strip()
    ]


def _calculate_evidence_level(candidate: dict[str, str]) -> int:
    """Calculate evidence strength for one candidate text."""
    if candidate["source"] in ACTION_SOURCES:
        if _has_action_verb(candidate["text"]):
            return 3
        return 2

    return 1


def _contains_any_skill(text: str, search_terms: list[str]) -> bool:
    """Return True when text contains at least one skill term."""
    return any(_contains_skill(text, term) for term in search_terms)


def _contains_skill(text: str, skill: str) -> bool:
    """Match skill phrases case-insensitively with simple plural tolerance."""
    if not isinstance(skill, str) or not skill.strip():
        return False

    normalized_text = _normalize_for_search(text)
    normalized_skill = _normalize_for_search(skill)
    variants = _build_skill_variants(normalized_skill)

    return any(_phrase_exists(normalized_text, variant) for variant in variants)


def _build_skill_variants(skill: str) -> set[str]:
    """Build small phrase variants for common resume wording differences."""
    variants = {skill}

    if skill.endswith("api"):
        variants.add(f"{skill}s")
    if skill.endswith("apis"):
        variants.add(skill[:-1])
    if skill == "rest api":
        variants.update({"rest apis", "restful api", "restful apis"})
    if skill == "rest apis":
        variants.update({"rest api", "restful api", "restful apis"})

    return variants


def _phrase_exists(text: str, phrase: str) -> bool:
    """Check whether a normalized phrase exists with word boundaries."""
    if not phrase:
        return False

    pattern = rf"(?<!\w){re.escape(phrase)}(?!\w)"
    return bool(re.search(pattern, text))


def _has_action_verb(text: str) -> bool:
    """Detect whether evidence text contains an action verb."""
    normalized_text = _normalize_for_search(text)
    return any(_phrase_exists(normalized_text, verb) for verb in ACTION_VERBS)


def _normalize_for_search(value: str) -> str:
    """Normalize punctuation and whitespace for evidence searching."""
    return normalize_search_text(value)


def _dedupe_terms(terms: list[str]) -> list[str]:
    """Remove duplicate search terms while preserving order."""
    deduped_terms: list[str] = []
    seen: set[str] = set()

    for term in terms:
        normalized_term = _normalize_for_search(term)
        if not normalized_term or normalized_term in seen:
            continue

        seen.add(normalized_term)
        deduped_terms.append(term)

    return deduped_terms


def _empty_evidence() -> dict[str, Any]:
    """Return an empty evidence result."""
    return {
        "evidence_level": 0,
        "evidence_text": "",
        "evidence_source": "none",
    }
