"""Build human-reviewed taxonomy suggestions from unknown requirements."""

from __future__ import annotations

from difflib import SequenceMatcher
import json
from collections import Counter
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.role_family import GENERIC_TECH
from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text, repair_mojibake


SUGGESTION_QUEUE_VERSION = 2
DEFAULT_MIN_FREQUENCY = 2
DEFAULT_GROUP_SIMILARITY_THRESHOLD = 0.86
DEFAULT_CATEGORY_SIMILARITY_THRESHOLD = 0.75
DEFAULT_TOP_NEAREST_SKILLS = 3
DEFAULT_MAX_ALIASES = 10
DEFAULT_MAX_EXAMPLES = 5
ALIAS_CANDIDATE_SIMILARITY_THRESHOLD = 0.90
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
    role_profile = job.get("job_role_profile", {})
    requirement_intent_lookup = _build_requirement_intent_lookup(
        job.get("requirement_intent_summary", [])
    )
    open_set_candidate_lookup = _build_open_set_candidate_lookup(
        [
            *job.get("open_set_candidates", []),
            *job.get("discarded_open_set_candidates", []),
        ]
    )

    observations_by_key: dict[str, dict[str, Any]] = {}
    for requirement in unknown_requirements:
        observation = _build_observation(
            phrase=requirement,
            job_id=job_id,
            job_title=job_title,
            source="job.taxonomy_coverage.unknown_requirements",
            context=requirement,
            **_resolve_observation_metadata(
                requirement,
                role_profile,
                requirement_intent_lookup,
                open_set_candidate_lookup,
            ),
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
                    **_resolve_observation_metadata(
                        phrase,
                        role_profile,
                        requirement_intent_lookup,
                        open_set_candidate_lookup,
                    ),
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
            -float(suggestion.get("governance_priority_score", 0.0)),
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
    job_role_family: str = "",
    job_role_family_confidence: float | None = None,
    intent_type: str = "",
    intent_strength: str = "",
    technical_candidate_status: str = "unknown",
    technical_confidence: float | None = None,
    keep_for_suggestion: bool = True,
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
        "job_role_family": str(job_role_family or "").strip(),
        "job_role_family_confidence": _round_float(job_role_family_confidence),
        "intent_type": str(intent_type or "").strip(),
        "intent_strength": str(intent_strength or "").strip(),
        "technical_candidate_status": str(technical_candidate_status or "unknown").strip(),
        "technical_confidence": _round_float(technical_confidence),
        "keep_for_suggestion": bool(keep_for_suggestion),
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
        if observation.get("keep_for_suggestion") is False:
            continue

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
    role_family_distribution = _distribution(
        [
            str(observation.get("job_role_family", "")).strip()
            for observation in group
            if str(observation.get("job_role_family", "")).strip()
        ]
    )
    dominant_role_family, dominant_role_family_ratio = _dominant_distribution_value(
        role_family_distribution,
        len(group),
    )
    intent_distribution = _distribution(
        [
            str(observation.get("intent_strength", "")).strip() or "unknown"
            for observation in group
        ]
    )
    dominant_intent_strength, _ = _dominant_distribution_value(
        intent_distribution,
        len(group),
    )
    evidence_support_count = sum(
        1
        for observation in group
        if str(observation.get("matched_evidence_text", "")).strip()
    )
    alias_candidate = _build_alias_candidate(
        suggested_canonical_name,
        nearest_existing_skills,
    )
    governance_priority_score = _calculate_governance_priority_score(
        group,
        dominant_role_family=dominant_role_family,
        dominant_role_family_ratio=dominant_role_family_ratio,
        dominant_intent_strength=dominant_intent_strength,
        evidence_support_count=evidence_support_count,
        alias_candidate=alias_candidate,
    )
    governance_priority = _priority_label(governance_priority_score)
    confidence = _calculate_confidence(
        frequency=len(group),
        dominant_role_family=dominant_role_family,
        dominant_role_family_ratio=dominant_role_family_ratio,
        dominant_intent_strength=dominant_intent_strength,
        evidence_support_count=evidence_support_count,
        has_nearest_skill=bool(nearest_existing_skills),
        alias_candidate=alias_candidate,
    )

    return {
        "suggestion_id": f"tax-sug-{_slugify(suggested_canonical_name)}",
        "suggested_canonical_name": suggested_canonical_name,
        "suggested_category": _suggest_category(taxonomy, nearest_existing_skills),
        "suggested_aliases": phrases[:DEFAULT_MAX_ALIASES],
        "frequency": len(group),
        "confidence": confidence,
        "nearest_existing_skills": nearest_existing_skills,
        "example_contexts": example_contexts,
        "example_evidence": example_evidence,
        "role_family_distribution": role_family_distribution,
        "dominant_role_family": dominant_role_family,
        "dominant_role_family_ratio": dominant_role_family_ratio,
        "intent_distribution": intent_distribution,
        "dominant_intent_strength": dominant_intent_strength,
        "evidence_support_count": evidence_support_count,
        "alias_candidate": alias_candidate,
        "governance_priority": governance_priority,
        "governance_priority_score": governance_priority_score,
        "review_reason": _build_review_reason(
            frequency=len(group),
            dominant_role_family=dominant_role_family,
            dominant_role_family_ratio=dominant_role_family_ratio,
            dominant_intent_strength=dominant_intent_strength,
            evidence_support_count=evidence_support_count,
            alias_candidate=alias_candidate,
        ),
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
    dominant_role_family: str,
    dominant_role_family_ratio: float,
    dominant_intent_strength: str,
    evidence_support_count: int,
    has_nearest_skill: bool,
    alias_candidate: dict[str, Any] | None,
) -> float:
    """Calculate a bounded heuristic confidence for a suggestion."""
    confidence = 0.45 + min(0.20, frequency * 0.05)
    if evidence_support_count > 0:
        confidence += 0.10
    if dominant_intent_strength == "core":
        confidence += 0.12
    elif dominant_intent_strength == "supporting":
        confidence += 0.07
    elif dominant_intent_strength == "contextual":
        confidence -= 0.05
    if dominant_role_family and dominant_role_family != GENERIC_TECH:
        confidence += 0.10 * dominant_role_family_ratio
    if has_nearest_skill:
        confidence += 0.05
    if alias_candidate:
        confidence += 0.05

    return round(max(0.10, min(confidence, 0.95)), 4)


def _build_requirement_intent_lookup(
    requirement_intent_summary: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a lookup from requirement phrase to role-aware intent metadata."""
    return {
        make_lookup_key(str(item.get("text", ""))): item
        for item in requirement_intent_summary
        if isinstance(item, dict) and make_lookup_key(str(item.get("text", "")))
    }


def _build_open_set_candidate_lookup(
    candidates: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a lookup from open-set candidate text variants to filter metadata."""
    lookup: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue

        for key in _candidate_lookup_keys(candidate):
            existing = lookup.get(key)
            if existing is None or _candidate_has_more_signal(candidate, existing):
                lookup[key] = candidate

    return lookup


def _candidate_lookup_keys(candidate: dict[str, Any]) -> set[str]:
    """Return stable lookup keys for one open-set candidate payload."""
    keys: set[str] = set()
    for value in (
        candidate.get("canonical_text"),
        candidate.get("text"),
        candidate.get("normalized_text"),
    ):
        key = make_lookup_key(str(value or ""))
        if key:
            keys.add(key)

    return keys


def _candidate_has_more_signal(
    candidate: dict[str, Any],
    existing: dict[str, Any],
) -> bool:
    """Prefer candidates that are kept for suggestion or have higher confidence."""
    candidate_keep = candidate.get("keep_for_suggestion") is True
    existing_keep = existing.get("keep_for_suggestion") is True
    if candidate_keep != existing_keep:
        return candidate_keep

    return float(candidate.get("technical_confidence", 0.0) or 0.0) > float(
        existing.get("technical_confidence", 0.0) or 0.0
    )


def _resolve_observation_metadata(
    phrase: str,
    role_profile: dict[str, Any],
    requirement_intent_lookup: dict[str, dict[str, Any]],
    open_set_candidate_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Resolve role-aware and governance metadata for one observation phrase."""
    key = make_lookup_key(phrase)
    intent_metadata = requirement_intent_lookup.get(key, {})
    candidate_metadata = open_set_candidate_lookup.get(key, {})

    return {
        "job_role_family": str(
            intent_metadata.get("role_family")
            or role_profile.get("primary_role_family")
            or ""
        ).strip(),
        "job_role_family_confidence": _coerce_float(role_profile.get("confidence")),
        "intent_type": str(intent_metadata.get("intent_type", "")).strip(),
        "intent_strength": str(intent_metadata.get("intent_strength", "")).strip(),
        "technical_candidate_status": str(
            candidate_metadata.get("status")
            or (
                "kept"
                if candidate_metadata.get("keep_for_matching") is True
                else "unknown"
            )
        ).strip(),
        "technical_confidence": _coerce_float(
            candidate_metadata.get("technical_confidence")
        ),
        "keep_for_suggestion": (
            bool(candidate_metadata.get("keep_for_suggestion"))
            if candidate_metadata
            else True
        ),
    }


def _distribution(values: list[str]) -> dict[str, int]:
    """Build a deterministic count distribution from a list of labels."""
    counts: Counter[str] = Counter(value for value in values if value)
    return {key: counts[key] for key in sorted(counts)}


def _dominant_distribution_value(
    distribution: dict[str, int],
    total_count: int,
) -> tuple[str, float]:
    """Return the most frequent label and its ratio over the group."""
    if not distribution or total_count <= 0:
        return "", 0.0

    best_label, best_count = max(
        distribution.items(),
        key=lambda item: (item[1], item[0]),
    )
    return best_label, round(best_count / total_count, 4)


def _build_alias_candidate(
    suggested_canonical_name: str,
    nearest_existing_skills: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Return likely-alias metadata when a phrase is very close to an existing skill."""
    if not nearest_existing_skills:
        return None

    nearest_skill = nearest_existing_skills[0]
    similarity = float(nearest_skill.get("similarity", 0.0) or 0.0)
    target_skill = str(nearest_skill.get("skill", "")).strip()
    if not target_skill or similarity < ALIAS_CANDIDATE_SIMILARITY_THRESHOLD:
        return None
    if not _looks_like_alias_variant(suggested_canonical_name, target_skill):
        return None

    return {
        "status": "likely_alias",
        "target_skill": target_skill,
        "similarity": round(similarity, 4),
    }


def _looks_like_alias_variant(left: str, right: str) -> bool:
    """Return True when two labels are lexically close enough to be alias variants."""
    left_normalized = normalize_search_text(left)
    right_normalized = normalize_search_text(right)
    left_compact = "".join(left_normalized.split())
    right_compact = "".join(right_normalized.split())
    if not left_compact or not right_compact:
        return False
    if left_compact == right_compact:
        return True
    if left_compact in right_compact or right_compact in left_compact:
        return min(len(left_compact), len(right_compact)) >= 5

    left_tokens = set(left_normalized.split())
    right_tokens = set(right_normalized.split())
    token_overlap = (
        len(left_tokens & right_tokens) / len(left_tokens | right_tokens)
        if left_tokens or right_tokens
        else 0.0
    )
    similarity_ratio = SequenceMatcher(None, left_compact, right_compact).ratio()
    return similarity_ratio >= 0.88 or (
        similarity_ratio >= 0.72 and token_overlap >= 0.50
    )


def _calculate_governance_priority_score(
    group: list[dict[str, Any]],
    *,
    dominant_role_family: str,
    dominant_role_family_ratio: float,
    dominant_intent_strength: str,
    evidence_support_count: int,
    alias_candidate: dict[str, Any] | None,
) -> float:
    """Calculate a role-aware priority score for admin review ordering."""
    frequency = len(group)
    frequency_bonus = min(0.24, max(0, frequency - 1) * 0.08)
    evidence_bonus = min(0.15, evidence_support_count * 0.05)
    confidence_values = [
        float(observation.get("technical_confidence", 0.0) or 0.0)
        for observation in group
        if isinstance(observation.get("technical_confidence"), (int, float))
    ]
    technical_confidence_bonus = (
        min(0.10, (sum(confidence_values) / len(confidence_values)) * 0.10)
        if confidence_values
        else 0.0
    )

    score = 0.30 + frequency_bonus + evidence_bonus + technical_confidence_bonus

    if dominant_role_family and dominant_role_family != GENERIC_TECH:
        score += 0.20 * dominant_role_family_ratio
    elif dominant_role_family_ratio:
        score += 0.08 * dominant_role_family_ratio

    if dominant_intent_strength == "core":
        score += 0.20
    elif dominant_intent_strength == "supporting":
        score += 0.12
    elif dominant_intent_strength == "contextual":
        score -= 0.05

    if alias_candidate:
        score += 0.05

    return round(max(0.0, min(score, 0.99)), 4)


def _priority_label(score: float) -> str:
    """Map a governance score to a stable review bucket."""
    if score >= 0.75:
        return "high"
    if score >= 0.55:
        return "medium"
    return "low"


def _build_review_reason(
    *,
    frequency: int,
    dominant_role_family: str,
    dominant_role_family_ratio: float,
    dominant_intent_strength: str,
    evidence_support_count: int,
    alias_candidate: dict[str, Any] | None,
) -> str:
    """Build one concise admin-facing reason for queue prioritization."""
    reasons: list[str] = [f"Observed {frequency} time(s)"]
    if dominant_role_family:
        reasons.append(
            f"{round(dominant_role_family_ratio * 100)}% from {dominant_role_family}"
        )
    if dominant_intent_strength:
        reasons.append(f"{dominant_intent_strength} technical intent")
    if evidence_support_count > 0:
        reasons.append(f"{evidence_support_count} evidence-backed observation(s)")
    if alias_candidate:
        reasons.append(
            f"likely alias of {alias_candidate.get('target_skill', 'existing skill')}"
        )

    return ". ".join(reasons) + "."


def _coerce_float(value: Any) -> float | None:
    """Convert numeric-like values to floats without raising."""
    if value is None or value == "":
        return None
    if not isinstance(value, (int, float)):
        return None
    return float(value)


def _round_float(value: float | None) -> float | None:
    """Round optional float values for stable JSON snapshots."""
    if value is None:
        return None
    return round(float(value), 4)


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
