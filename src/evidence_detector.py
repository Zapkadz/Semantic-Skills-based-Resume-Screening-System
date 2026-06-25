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
DIRECT_EVIDENCE_PRIORITY = 3
SECONDARY_EVIDENCE_PRIORITY = 2
SYNTHESIZED_EVIDENCE_PRIORITY = 1
EVIDENCE_SOURCE_PREFERENCE = {
    "work_experience": 3,
    "projects": 2,
    "summary": 1,
    "headline": 1,
    "skills": 1,
    "certifications": 1,
    "none": 0,
}


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


def collect_evidence_candidates(resume_profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect searchable evidence text from a parsed resume profile."""
    return _collect_evidence_candidates(resume_profile)


def calculate_candidate_evidence_level(candidate: dict[str, Any]) -> int:
    """Calculate evidence strength for one evidence candidate."""
    return _calculate_evidence_level(candidate)


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
        candidate_priority = int(candidate.get("evidence_priority", 0))
        if _is_better_evidence_candidate(
            evidence_level,
            candidate_priority,
            candidate["source"],
            candidate["text"],
            best_evidence,
        ):
            best_evidence = {
                "evidence_level": evidence_level,
                "evidence_text": candidate["text"],
                "evidence_source": candidate["source"],
                "_evidence_priority": candidate_priority,
                "_text_length": len(candidate["text"]),
            }

    return _public_evidence(best_evidence)


def _collect_evidence_candidates(resume_profile: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect searchable evidence text from a parsed resume profile."""
    candidates: list[dict[str, Any]] = []

    for entry in resume_profile.get("work_experience", []):
        title = str(entry.get("title", "")).strip()
        company = str(entry.get("company", "")).strip()
        for description in entry.get("description", []):
            _append_candidate(
                candidates,
                "work_experience",
                description,
                DIRECT_EVIDENCE_PRIORITY,
            )
            _append_candidate(
                candidates,
                "work_experience",
                _join_context_parts(title, description),
                SYNTHESIZED_EVIDENCE_PRIORITY,
            )
            _append_candidate(
                candidates,
                "work_experience",
                _join_context_parts(title, company, description),
                SYNTHESIZED_EVIDENCE_PRIORITY,
            )

    for project in resume_profile.get("projects", []):
        project_name = str(project.get("name", "")).strip()
        technologies = [
            technology.strip()
            for technology in project.get("technologies", [])
            if isinstance(technology, str) and technology.strip()
        ]
        for description in project.get("description", []):
            _append_candidate(
                candidates,
                "projects",
                description,
                DIRECT_EVIDENCE_PRIORITY,
            )
            _append_candidate(
                candidates,
                "projects",
                _join_context_parts(project_name, description),
                SYNTHESIZED_EVIDENCE_PRIORITY,
            )
            if technologies:
                _append_candidate(
                    candidates,
                    "projects",
                    _join_context_parts(
                        description,
                        f"Technologies: {', '.join(technologies)}",
                    ),
                    SYNTHESIZED_EVIDENCE_PRIORITY,
                )

        if project_name and technologies:
            _append_candidate(
                candidates,
                "projects",
                _join_context_parts(project_name, f"Technologies: {', '.join(technologies)}"),
                SYNTHESIZED_EVIDENCE_PRIORITY,
            )

        for technology in technologies:
            _append_candidate(
                candidates,
                "projects",
                technology,
                SECONDARY_EVIDENCE_PRIORITY,
            )

    summary = resume_profile.get("summary", "")
    if summary:
        _append_candidate(candidates, "summary", summary, SECONDARY_EVIDENCE_PRIORITY)

    headline = resume_profile.get("headline", "")
    if headline:
        _append_candidate(candidates, "headline", headline, SECONDARY_EVIDENCE_PRIORITY)

    for skill in resume_profile.get("raw_skills", []):
        _append_candidate(candidates, "skills", skill, SECONDARY_EVIDENCE_PRIORITY)

    for certification in resume_profile.get("certifications", []):
        _append_candidate(
            candidates,
            "certifications",
            certification,
            SECONDARY_EVIDENCE_PRIORITY,
        )

    return _dedupe_evidence_candidates(candidates)


def _calculate_evidence_level(candidate: dict[str, Any]) -> int:
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
        "_evidence_priority": 0,
        "_text_length": 0,
    }


def _append_candidate(
    candidates: list[dict[str, Any]],
    source: str,
    text: str,
    evidence_priority: int,
) -> None:
    """Append one cleaned evidence candidate when text is non-empty."""
    if not isinstance(text, str):
        return

    clean_text = text.strip()
    if not clean_text:
        return

    candidates.append(
        {
            "source": source,
            "text": clean_text,
            "evidence_priority": evidence_priority,
        }
    )


def _join_context_parts(*parts: str) -> str:
    """Join context parts into one concise synthesized evidence string."""
    clean_parts = [part.strip() for part in parts if isinstance(part, str) and part.strip()]
    if not clean_parts:
        return ""

    combined = clean_parts[0]
    for part in clean_parts[1:]:
        if combined.endswith((".", "!", "?", ":")):
            combined = f"{combined} {part}"
        else:
            combined = f"{combined}. {part}"

    return combined


def _dedupe_evidence_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Deduplicate evidence candidates while keeping the stronger priority variant."""
    deduped: list[dict[str, Any]] = []
    index_by_key: dict[tuple[str, str], int] = {}

    for candidate in candidates:
        source = str(candidate.get("source", "")).strip()
        text = str(candidate.get("text", "")).strip()
        if not source or not text:
            continue

        key = (source, normalize_search_text(text))
        existing_index = index_by_key.get(key)
        if existing_index is None:
            index_by_key[key] = len(deduped)
            deduped.append(
                {
                    "source": source,
                    "text": text,
                    "evidence_priority": int(candidate.get("evidence_priority", 0)),
                }
            )
            continue

        if int(candidate.get("evidence_priority", 0)) > int(
            deduped[existing_index].get("evidence_priority", 0)
        ):
            deduped[existing_index] = {
                "source": source,
                "text": text,
                "evidence_priority": int(candidate.get("evidence_priority", 0)),
            }

    return deduped


def _is_better_evidence_candidate(
    evidence_level: int,
    evidence_priority: int,
    evidence_source: str,
    evidence_text: str,
    best_evidence: dict[str, Any],
) -> bool:
    """Choose stronger evidence while preferring concise direct text on ties."""
    current_tuple = (
        evidence_level,
        evidence_priority,
        EVIDENCE_SOURCE_PREFERENCE.get(evidence_source, 0),
        -len(evidence_text),
    )
    best_tuple = (
        int(best_evidence.get("evidence_level", 0)),
        int(best_evidence.get("_evidence_priority", 0)),
        EVIDENCE_SOURCE_PREFERENCE.get(
            str(best_evidence.get("evidence_source", "none")),
            0,
        ),
        -int(best_evidence.get("_text_length", 0)),
    )
    return current_tuple > best_tuple


def _public_evidence(evidence: dict[str, Any]) -> dict[str, Any]:
    """Strip internal ranking metadata before returning evidence."""
    return {
        "evidence_level": int(evidence.get("evidence_level", 0)),
        "evidence_text": str(evidence.get("evidence_text", "")),
        "evidence_source": str(evidence.get("evidence_source", "none")),
    }
