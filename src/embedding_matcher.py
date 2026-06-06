"""Optional embedding-based semantic similarity helpers for Phase 06."""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any


DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_SEMANTIC_THRESHOLD = 0.70


class SemanticEmbeddingMatcher:
    """Lazy embedding matcher with a safe fallback when models are unavailable."""

    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        threshold: float = DEFAULT_SEMANTIC_THRESHOLD,
        model: Any | None = None,
        model_loader: Callable[[str], Any] | None = None,
        auto_load: bool = False,
    ) -> None:
        self.model_name = model_name
        self.threshold = threshold
        self.model = model
        self.model_loader = model_loader
        self.unavailable_reason: str | None = None
        self._load_attempted = model is not None

        if auto_load:
            self.load_model()

    def load_model(self) -> bool:
        """Load the embedding model if possible and return availability."""
        if self.model is not None:
            return True

        if self._load_attempted:
            return False

        self._load_attempted = True
        try:
            loader = self.model_loader or _load_sentence_transformer
            self.model = loader(self.model_name)
        except Exception as exc:  # pragma: no cover - exact dependency errors vary
            self.unavailable_reason = str(exc)
            self.model = None
            return False

        return True

    def is_available(self) -> bool:
        """Return True when an embedding model is already loaded."""
        return self.model is not None

    def similarity(self, text_a: str, text_b: str) -> float | None:
        """Return cosine similarity for two texts, or None when unavailable."""
        if not _has_text(text_a) or not _has_text(text_b):
            return None

        if not self.load_model():
            return None

        try:
            embeddings = self.model.encode([text_a, text_b])
        except Exception as exc:  # pragma: no cover - model implementations vary
            self.unavailable_reason = str(exc)
            return None

        vector_a, vector_b = _split_two_embeddings(embeddings)
        return _cosine_similarity(vector_a, vector_b)

    def best_match(
        self,
        required_skill: str,
        candidate_skills: list[str],
    ) -> dict[str, Any] | None:
        """Return the best semantic match above threshold, if available."""
        best_candidate: str | None = None
        best_similarity: float | None = None

        for candidate_skill in candidate_skills:
            similarity = self.similarity(required_skill, candidate_skill)
            if similarity is None:
                continue

            if best_similarity is None or similarity > best_similarity:
                best_candidate = candidate_skill
                best_similarity = similarity

        if best_candidate is None or best_similarity is None:
            return None

        if best_similarity < self.threshold:
            return None

        return {
            "candidate_skill": best_candidate,
            "similarity": round(best_similarity, 4),
        }


def _load_sentence_transformer(model_name: str) -> Any:
    """Import sentence-transformers lazily so fallback remains lightweight."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def _has_text(value: str) -> bool:
    """Return True when a text value has non-whitespace content."""
    return isinstance(value, str) and bool(value.strip())


def _split_two_embeddings(embeddings: Any) -> tuple[list[float], list[float]]:
    """Convert model embeddings into two float lists."""
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()

    if len(embeddings) != 2:
        raise ValueError("Expected exactly two embeddings.")

    return _to_float_list(embeddings[0]), _to_float_list(embeddings[1])


def _to_float_list(vector: Any) -> list[float]:
    """Convert an embedding vector to a plain float list."""
    if hasattr(vector, "tolist"):
        vector = vector.tolist()

    return [float(value) for value in vector]


def _cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    """Calculate cosine similarity for two vectors."""
    if len(vector_a) != len(vector_b):
        raise ValueError("Embedding vectors must have the same length.")

    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)
