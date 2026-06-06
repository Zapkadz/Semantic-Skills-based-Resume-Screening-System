"""Rule-based and optional embedding semantic skill matching."""

from __future__ import annotations

from typing import Any

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.skill_taxonomy import build_alias_map, make_lookup_key


MATCH_SCORES = {
    "exact_match": 1.0,
    "related_match": 0.75,
    "transferable_match": 0.55,
    "semantic_match": 0.85,
    "no_match": 0.0,
}

MATCH_PRIORITY = ("exact_match", "related_match", "transferable_match")


def match_skills(
    job_skills: list[str],
    candidate_skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> list[dict[str, Any]]:
    """Match required job skills using rules and optional embedding fallback."""
    alias_map = build_alias_map(taxonomy)
    normalized_job_skills = _canonicalize_skills(job_skills, alias_map)
    normalized_candidate_skills = _canonicalize_skills(candidate_skills, alias_map)

    return [
        _match_single_skill(
            required_skill,
            normalized_candidate_skills,
            taxonomy,
            embedding_matcher,
        )
        for required_skill in normalized_job_skills
    ]


def get_missing_skills(matches: list[dict[str, Any]]) -> list[str]:
    """Return required skills that did not receive a candidate match."""
    return [
        match["required_skill"]
        for match in matches
        if match["match_type"] == "no_match"
    ]


def _match_single_skill(
    required_skill: str,
    candidate_skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> dict[str, Any]:
    """Find the best rule-based or semantic match for one required skill."""
    for match_type in MATCH_PRIORITY:
        candidate_skill = _find_candidate_match(
            required_skill,
            candidate_skills,
            taxonomy,
            match_type,
        )
        if candidate_skill:
            return _build_match_result(required_skill, candidate_skill, match_type)

    semantic_match = _find_semantic_match(
        required_skill,
        candidate_skills,
        embedding_matcher,
    )
    if semantic_match:
        return _build_match_result(
            required_skill,
            semantic_match["candidate_skill"],
            "semantic_match",
            similarity=semantic_match["similarity"],
        )

    return _build_match_result(required_skill, None, "no_match")


def _find_candidate_match(
    required_skill: str,
    candidate_skills: list[str],
    taxonomy: dict[str, dict[str, Any]],
    match_type: str,
) -> str | None:
    """Find the first candidate skill matching a required skill for one rule."""
    for candidate_skill in candidate_skills:
        if _is_match(required_skill, candidate_skill, taxonomy, match_type):
            return candidate_skill

    return None


def _is_match(
    required_skill: str,
    candidate_skill: str,
    taxonomy: dict[str, dict[str, Any]],
    match_type: str,
) -> bool:
    """Check whether two canonical skills match by one rule type."""
    if match_type == "exact_match":
        return make_lookup_key(required_skill) == make_lookup_key(candidate_skill)

    if match_type == "related_match":
        return _skills_are_connected(
            required_skill,
            candidate_skill,
            taxonomy,
            relationship_key="related",
        )

    if match_type == "transferable_match":
        return _skills_are_connected(
            required_skill,
            candidate_skill,
            taxonomy,
            relationship_key="transferable",
        )

    return False


def _skills_are_connected(
    required_skill: str,
    candidate_skill: str,
    taxonomy: dict[str, dict[str, Any]],
    relationship_key: str,
) -> bool:
    """Check a relationship in both taxonomy directions."""
    required_connections = _get_relationships(
        required_skill,
        taxonomy,
        relationship_key,
    )
    candidate_connections = _get_relationships(
        candidate_skill,
        taxonomy,
        relationship_key,
    )

    candidate_key = make_lookup_key(candidate_skill)
    required_key = make_lookup_key(required_skill)

    return (
        candidate_key in required_connections
        or required_key in candidate_connections
    )


def _get_relationships(
    skill: str,
    taxonomy: dict[str, dict[str, Any]],
    relationship_key: str,
) -> set[str]:
    """Return normalized relationship values for one skill."""
    metadata = taxonomy.get(skill, {})
    relationships = metadata.get(relationship_key, [])
    return {
        make_lookup_key(relationship)
        for relationship in relationships
        if isinstance(relationship, str) and relationship.strip()
    }


def _find_semantic_match(
    required_skill: str,
    candidate_skills: list[str],
    embedding_matcher: SemanticEmbeddingMatcher | None,
) -> dict[str, Any] | None:
    """Find a semantic embedding match when the optional matcher is available."""
    if embedding_matcher is None:
        return None

    return embedding_matcher.best_match(required_skill, candidate_skills)


def _canonicalize_skills(skills: list[str], alias_map: dict[str, str]) -> list[str]:
    """Canonicalize skill names and remove duplicates while preserving order."""
    canonical_skills: list[str] = []
    seen_keys: set[str] = set()

    for skill in skills:
        canonical_skill = _canonicalize_skill(skill, alias_map)
        if not canonical_skill:
            continue

        lookup_key = make_lookup_key(canonical_skill)
        if lookup_key in seen_keys:
            continue

        seen_keys.add(lookup_key)
        canonical_skills.append(canonical_skill)

    return canonical_skills


def _canonicalize_skill(skill: str, alias_map: dict[str, str]) -> str:
    """Map aliases to canonical names and keep unknown skills unchanged."""
    if not isinstance(skill, str):
        raise TypeError("Skill must be a string.")

    clean_skill = skill.strip()
    if not clean_skill:
        return ""

    return alias_map.get(make_lookup_key(clean_skill), clean_skill)


def _build_match_result(
    required_skill: str,
    candidate_skill: str | None,
    match_type: str,
    similarity: float | None = None,
) -> dict[str, Any]:
    """Build one stable match result dictionary."""
    result = {
        "required_skill": required_skill,
        "candidate_skill": candidate_skill,
        "match_type": match_type,
        "score": MATCH_SCORES[match_type],
    }

    if similarity is not None:
        result["similarity"] = similarity

    return result
