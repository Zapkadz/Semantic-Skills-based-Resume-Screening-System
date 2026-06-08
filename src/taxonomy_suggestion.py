"""Build human-reviewed taxonomy suggestions from unknown requirements."""

from __future__ import annotations

import json
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text, repair_mojibake


SUGGESTION_QUEUE_VERSION = 1
DEFAULT_MIN_FREQUENCY = 2
DEFAULT_GROUP_SIMILARITY_THRESHOLD = 0.86
DEFAULT_CATEGORY_SIMILARITY_THRESHOLD = 0.75
DEFAULT_TOP_NEAREST_SKILLS = 3
DEFAULT_MAX_ALIASES = 10
DEFAULT_MAX_EXAMPLES = 5
PENDING_REVIEW_STATUS = "pending_review"
PENDING_CLASSIFICATION_CATEGORY = "Pending Classification"


def collect_unknown_requirement_observations(
    screening_result: dict[str, Any],
) -> list[dict[str, Any]]:
    """Collect unknown requirement observations from one screening result."""
    job = screening_result.get("job", {})
    job_id = job.get("job_id")
    job_title = job.get("title") or job.get("job_title") or ""
    coverage = job.get("taxonomy_coverage", {})
    unknown_requirements = _string_list(coverage.get("unknown_requirements"))

    observations_by_key: dict[str, dict[str, Any]] = {}
    for requirement in unknown_requirements:
        observation = _build_observation(
            phrase=requirement,
            job_id=job_id,
            job_title=job_title,
            source="job.taxonomy_coverage.unknown_requirements",
            context=requirement,
        )
        observations_by_key[_observation_key(observation)] = observation

    for candidate in screening_result.get("candidates", []):
        for match in _candidate_open_set_matches(candidate):
            phrase = str(match.get("required_skill", "")).strip()
            if not phrase:
                continue

            key = make_lookup_key(phrase)
            observation = observations_by_key.get(key)
            if observation is None:
                observation = _build_observation(
                    phrase=phrase,
                    job_id=job_id,
                    job_title=job_title,
                    source="candidate.open_set_requirement_matches",
                    context=phrase,
                )
                observations_by_key[key] = observation

            _merge_match_into_observation(observation, match)

    return list(observations_by_key.values())


def collect_unknown_requirement_observations_from_results(
    screening_results: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collect observations from multiple screening results."""
    observations: list[dict[str, Any]] = []
    for result in screening_results:
        observations.extend(collect_unknown_requirement_observations(result))

    return observations


def build_taxonomy_suggestions(
    observations: list[dict[str, Any]],
    taxonomy: dict[str, dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
    min_frequency: int = DEFAULT_MIN_FREQUENCY,
    group_similarity_threshold: float = DEFAULT_GROUP_SIMILARITY_THRESHOLD,
) -> list[dict[str, Any]]:
    """Build pending taxonomy suggestions from unknown requirement observations."""
    groups = _group_observations(
        observations,
        embedding_matcher,
        group_similarity_threshold,
    )
    suggestions = [
        _build_suggestion(group, taxonomy, embedding_matcher)
        for group in groups
        if len(group) >= min_frequency
    ]
    return sorted(
        suggestions,
        key=lambda suggestion: (
            -int(suggestion.get("frequency", 0)),
            suggestion.get("suggested_canonical_name", ""),
        ),
    )


def load_screening_results(path: str | Path) -> list[dict[str, Any]]:
    """Load one or more screening results from JSON."""
    payload = _load_json(path)
    if isinstance(payload, list):
        return [result for result in payload if isinstance(result, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return [result for result in payload["results"] if isinstance(result, dict)]
    if isinstance(payload, dict):
        return [payload]

    raise ValueError(f"Unsupported screening result JSON structure: {path}")


def save_taxonomy_suggestions(
    suggestions: list[dict[str, Any]],
    output_path: str | Path,
) -> str:
    """Save taxonomy suggestions as a versioned JSON queue."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": SUGGESTION_QUEUE_VERSION,
        "suggestions": suggestions,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(path)


def load_taxonomy_suggestions(path: str | Path) -> list[dict[str, Any]]:
    """Load taxonomy suggestions from a versioned JSON queue."""
    payload = _load_json(path)
    if isinstance(payload, list):
        return [suggestion for suggestion in payload if isinstance(suggestion, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("suggestions"), list):
        return [
            suggestion
            for suggestion in payload["suggestions"]
            if isinstance(suggestion, dict)
        ]

    raise ValueError(f"Unsupported taxonomy suggestion JSON structure: {path}")


def _build_observation(
    phrase: str,
    job_id: Any = None,
    job_title: str = "",
    source: str = "",
    context: str = "",
) -> dict[str, Any]:
    """Build one normalized observation object."""
    clean_phrase = repair_mojibake(str(phrase)).strip()
    return {
        "phrase": clean_phrase,
        "job_id": job_id,
        "job_title": str(job_title or "").strip(),
        "source": source,
        "context": str(context or clean_phrase).strip(),
        "matched_evidence_text": "",
        "similarity": None,
    }


def _candidate_open_set_matches(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    """Return open-set matches from a candidate result."""
    explicit_matches = candidate.get("open_set_requirement_matches")
    if isinstance(explicit_matches, list):
        return [match for match in explicit_matches if isinstance(match, dict)]

    matches = candidate.get("matched_skills", [])
    return [
        match
        for match in matches
        if isinstance(match, dict)
        and match.get("taxonomy_status") == "unknown"
    ]


def _merge_match_into_observation(
    observation: dict[str, Any],
    match: dict[str, Any],
) -> None:
    """Merge candidate semantic evidence into a requirement observation."""
    evidence_text = str(match.get("evidence_text", "")).strip()
    if evidence_text and not observation.get("matched_evidence_text"):
        observation["matched_evidence_text"] = evidence_text

    similarity = match.get("similarity")
    if isinstance(similarity, (int, float)):
        existing_similarity = observation.get("similarity")
        if not isinstance(existing_similarity, (int, float)) or similarity > existing_similarity:
            observation["similarity"] = round(float(similarity), 4)


def _group_observations(
    observations: list[dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None,
    group_similarity_threshold: float,
) -> list[list[dict[str, Any]]]:
    """Group exact and optionally semantically similar observations."""
    groups: list[list[dict[str, Any]]] = []

    for observation in observations:
        phrase = str(observation.get("phrase", "")).strip()
        if not phrase:
            continue

        target_group = _find_observation_group(
            phrase,
            groups,
            embedding_matcher,
            group_similarity_threshold,
        )
        if target_group is None:
            groups.append([observation])
        else:
            target_group.append(observation)

    return groups


def _find_observation_group(
    phrase: str,
    groups: list[list[dict[str, Any]]],
    embedding_matcher: SemanticEmbeddingMatcher | None,
    group_similarity_threshold: float,
) -> list[dict[str, Any]] | None:
    """Find an existing group for one phrase."""
    phrase_key = make_lookup_key(phrase)
    for group in groups:
        representative = str(group[0].get("phrase", "")).strip()
        group_keys = {
            make_lookup_key(str(item.get("phrase", "")).strip())
            for item in group
        }
        if phrase_key in group_keys:
            return group

        if embedding_matcher is None or not representative:
            continue

        similarity = embedding_matcher.similarity(phrase, representative)
        if similarity is not None and similarity >= group_similarity_threshold:
            return group

    return None


def _build_suggestion(
    group: list[dict[str, Any]],
    taxonomy: dict[str, dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None,
) -> dict[str, Any]:
    """Build one pending taxonomy suggestion from a grouped observation list."""
    phrases = _dedupe_strings(
        [str(observation.get("phrase", "")).strip() for observation in group]
    )
    canonical_phrase = _choose_canonical_phrase(group)
    suggested_canonical_name = _to_canonical_name(canonical_phrase)
    nearest_existing_skills = _find_nearest_existing_skills(
        suggested_canonical_name,
        taxonomy,
        embedding_matcher,
    )
    example_contexts = _dedupe_strings(
        [str(observation.get("context", "")).strip() for observation in group]
    )[:DEFAULT_MAX_EXAMPLES]
    example_evidence = _dedupe_strings(
        [
            str(observation.get("matched_evidence_text", "")).strip()
            for observation in group
            if str(observation.get("matched_evidence_text", "")).strip()
        ]
    )[:DEFAULT_MAX_EXAMPLES]

    return {
        "suggestion_id": f"tax-sug-{_slugify(suggested_canonical_name)}",
        "suggested_canonical_name": suggested_canonical_name,
        "suggested_category": _suggest_category(taxonomy, nearest_existing_skills),
        "suggested_aliases": phrases[:DEFAULT_MAX_ALIASES],
        "frequency": len(group),
        "confidence": _calculate_confidence(
            frequency=len(group),
            has_evidence=bool(example_evidence),
            has_nearest_skill=bool(nearest_existing_skills),
        ),
        "nearest_existing_skills": nearest_existing_skills,
        "example_contexts": example_contexts,
        "example_evidence": example_evidence,
        "status": PENDING_REVIEW_STATUS,
    }


def _choose_canonical_phrase(group: list[dict[str, Any]]) -> str:
    """Choose the most frequent phrase in a group as canonical source."""
    phrases = [str(item.get("phrase", "")).strip() for item in group if item.get("phrase")]
    if not phrases:
        return "Unknown Skill"

    counts = Counter(make_lookup_key(phrase) for phrase in phrases)
    best_key, _ = counts.most_common(1)[0]
    for phrase in phrases:
        if make_lookup_key(phrase) == best_key:
            return phrase

    return phrases[0]


def _to_canonical_name(phrase: str) -> str:
    """Create a readable canonical skill name without using a generative model."""
    clean_phrase = repair_mojibake(phrase).strip().rstrip(".;:,")
    if not clean_phrase:
        return "Unknown Skill"
    if _is_ascii(clean_phrase):
        return " ".join(_title_token(token) for token in clean_phrase.split())

    return clean_phrase


def _find_nearest_existing_skills(
    suggested_canonical_name: str,
    taxonomy: dict[str, dict[str, Any]],
    embedding_matcher: SemanticEmbeddingMatcher | None,
    top_k: int = DEFAULT_TOP_NEAREST_SKILLS,
) -> list[dict[str, Any]]:
    """Find nearest existing taxonomy skills by embedding similarity."""
    if embedding_matcher is None or not taxonomy:
        return []

    skill_names = list(taxonomy)
    similarities = embedding_matcher.similarity_matrix(
        [suggested_canonical_name],
        skill_names,
    )
    if not similarities:
        return []

    ranked_skills = sorted(
        zip(skill_names, similarities[0]),
        key=lambda item: item[1],
        reverse=True,
    )
    return [
        {
            "skill": skill,
            "similarity": round(float(similarity), 4),
        }
        for skill, similarity in ranked_skills[:top_k]
    ]


def _suggest_category(
    taxonomy: dict[str, dict[str, Any]],
    nearest_existing_skills: list[dict[str, Any]],
) -> str:
    """Suggest a category from the nearest strong taxonomy skill."""
    if not nearest_existing_skills:
        return PENDING_CLASSIFICATION_CATEGORY

    nearest_skill = nearest_existing_skills[0]
    if nearest_skill.get("similarity", 0) < DEFAULT_CATEGORY_SIMILARITY_THRESHOLD:
        return PENDING_CLASSIFICATION_CATEGORY

    metadata = taxonomy.get(str(nearest_skill.get("skill", "")), {})
    category = metadata.get("category")
    if isinstance(category, str) and category.strip():
        return category

    return PENDING_CLASSIFICATION_CATEGORY


def _calculate_confidence(
    frequency: int,
    has_evidence: bool,
    has_nearest_skill: bool,
) -> float:
    """Calculate a bounded heuristic confidence for a suggestion."""
    confidence = 0.50 + min(0.30, frequency * 0.05)
    if has_evidence:
        confidence += 0.10
    if has_nearest_skill:
        confidence += 0.05

    return round(min(confidence, 0.95), 4)


def _load_json(path: str | Path) -> Any:
    """Load JSON with consistent validation errors."""
    json_path = Path(path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not json_path.is_file():
        raise IsADirectoryError(f"Expected JSON file, got directory: {json_path}")

    try:
        return json.loads(json_path.read_text(encoding="utf-8"))
    except JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {json_path}") from exc


def _observation_key(observation: dict[str, Any]) -> str:
    """Return the grouping key for an observation."""
    return make_lookup_key(str(observation.get("phrase", "")))


def _string_list(value: Any) -> list[str]:
    """Convert common values to a clean string list."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]

    return [str(value).strip()] if str(value).strip() else []


def _dedupe_strings(values: list[str]) -> list[str]:
    """Deduplicate strings while preserving order."""
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean_value = repair_mojibake(value).strip()
        key = make_lookup_key(clean_value)
        if not clean_value or key in seen:
            continue

        seen.add(key)
        deduped.append(clean_value)

    return deduped


def _slugify(value: str) -> str:
    """Build a stable ASCII-ish id slug."""
    slug = normalize_search_text(value).replace(" ", "-")
    return slug.strip("-") or "unknown-skill"


def _is_ascii(value: str) -> bool:
    """Return True when text is ASCII-only."""
    return all(ord(character) < 128 for character in value)


def _title_token(token: str) -> str:
    """Title-case a token while preserving all-caps/acronym-like values."""
    if token.isupper() or any(character.isdigit() for character in token):
        return token

    return token[:1].upper() + token[1:].lower()
