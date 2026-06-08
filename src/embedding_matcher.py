"""Optional embedding-based semantic similarity helpers."""

from __future__ import annotations

import math
import os
from collections.abc import Callable
from typing import Any


DEFAULT_EMBEDDING_MODEL = "BAAI/bge-m3"
LEGACY_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
MULTILINGUAL_E5_MODEL = "intfloat/multilingual-e5-large-instruct"
DEFAULT_SEMANTIC_THRESHOLD = 0.72
E5_QUERY_INSTRUCTION = (
    "Instruct: Given a job requirement, retrieve matching candidate resume evidence.\n"
    "Query: "
)

TRUTHY_ENV_VALUES = {"1", "true", "yes", "on", "enabled"}


class SemanticEmbeddingMatcher:
    """Lazy embedding matcher with a safe fallback when models are unavailable."""

    def __init__(
        self,
        model_name: str = DEFAULT_EMBEDDING_MODEL,
        threshold: float = DEFAULT_SEMANTIC_THRESHOLD,
        local_files_only: bool = False,
        model: Any | None = None,
        model_loader: Callable[[str], Any] | None = None,
        auto_load: bool = False,
    ) -> None:
        self.model_name = model_name
        self.threshold = threshold
        self.local_files_only = local_files_only
        self.model = model
        self.model_loader = model_loader
        self.unavailable_reason: str | None = None
        self._load_attempted = model is not None
        self._embedding_cache: dict[str, list[float]] = {}

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
            if self.model_loader is not None:
                self.model = self.model_loader(self.model_name)
            else:
                self.model = _load_sentence_transformer(
                    self.model_name,
                    local_files_only=self.local_files_only,
                )
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

        try:
            vector_a = self.encode_texts([text_a], role="query")[0]
            vector_b = self.encode_texts([text_b], role="document")[0]
        except Exception as exc:  # pragma: no cover - model implementations vary
            self.unavailable_reason = str(exc)
            return None

        return _cosine_similarity(vector_a, vector_b)

    def encode_texts(self, texts: list[str], role: str = "document") -> list[list[float]]:
        """Encode texts with small in-memory caching for one matcher instance."""
        if not texts:
            return []

        if not self.load_model():
            raise RuntimeError(self.unavailable_reason or "Embedding model unavailable.")

        vectors: list[list[float] | None] = []
        missing_texts: list[str] = []
        missing_indexes: list[int] = []

        for index, text in enumerate(texts):
            formatted_text = self._format_text(text, role)
            cache_key = self._cache_key(formatted_text)
            cached_vector = self._embedding_cache.get(cache_key)
            if cached_vector is None:
                vectors.append(None)
                missing_texts.append(formatted_text)
                missing_indexes.append(index)
                continue

            vectors.append(cached_vector)

        if missing_texts:
            embeddings = self.model.encode(missing_texts)
            encoded_vectors = _to_embedding_list(embeddings)
            if len(encoded_vectors) != len(missing_texts):
                raise ValueError("Embedding model returned an unexpected number of vectors.")

            for index, formatted_text, vector in zip(
                missing_indexes,
                missing_texts,
                encoded_vectors,
            ):
                cache_key = self._cache_key(formatted_text)
                self._embedding_cache[cache_key] = vector
                vectors[index] = vector

        return [vector for vector in vectors if vector is not None]

    def similarity_matrix(
        self,
        queries: list[str],
        documents: list[str],
    ) -> list[list[float]] | None:
        """Return query-document cosine similarities, or None when unavailable."""
        if not queries or not documents:
            return []

        if not all(_has_text(query) for query in queries):
            return None
        if not all(_has_text(document) for document in documents):
            return None

        try:
            query_vectors = self.encode_texts(queries, role="query")
            document_vectors = self.encode_texts(documents, role="document")
        except Exception as exc:  # pragma: no cover - model implementations vary
            self.unavailable_reason = str(exc)
            return None

        return [
            [
                _cosine_similarity(query_vector, document_vector)
                for document_vector in document_vectors
            ]
            for query_vector in query_vectors
        ]

    def best_match(
        self,
        required_skill: str,
        candidate_skills: list[str],
    ) -> dict[str, Any] | None:
        """Return the best semantic match above threshold, if available."""
        best_candidate: str | None = None
        best_similarity: float | None = None

        similarities = self.similarity_matrix([required_skill], candidate_skills)
        if not similarities:
            return None

        for candidate_skill, similarity in zip(candidate_skills, similarities[0]):
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

    def _format_text(self, text: str, role: str) -> str:
        """Format query/document text according to model family."""
        if role == "query":
            return format_embedding_query(text, self.model_name)

        return format_embedding_document(text, self.model_name)

    def _cache_key(self, formatted_text: str) -> str:
        """Build a cache key scoped to the selected model."""
        return f"{self.model_name}\0{formatted_text}"


def format_embedding_query(text: str, model_name: str = DEFAULT_EMBEDDING_MODEL) -> str:
    """Format query-side text for the selected embedding model."""
    clean_text = text.strip()
    if _is_e5_model(model_name):
        return f"{E5_QUERY_INSTRUCTION}{clean_text}"

    return clean_text


def format_embedding_document(
    text: str,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> str:
    """Format document-side text for the selected embedding model."""
    return text.strip()


def build_embedding_matcher(
    enabled: bool = False,
    model_name: str | None = None,
    threshold: float | None = None,
    local_files_only: bool = False,
    auto_load: bool = False,
) -> SemanticEmbeddingMatcher | None:
    """Build an optional embedding matcher from simple config values."""
    if not enabled:
        return None

    return SemanticEmbeddingMatcher(
        model_name=model_name or DEFAULT_EMBEDDING_MODEL,
        threshold=threshold if threshold is not None else DEFAULT_SEMANTIC_THRESHOLD,
        local_files_only=local_files_only,
        auto_load=auto_load,
    )


def build_embedding_matcher_from_env() -> SemanticEmbeddingMatcher | None:
    """Build an embedding matcher from environment variables when enabled."""
    enabled = _env_flag("SEMANTIC_EMBEDDING_ENABLED", default=False)
    if not enabled:
        return None

    return build_embedding_matcher(
        enabled=True,
        model_name=os.getenv("SEMANTIC_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        threshold=_env_float(
            "SEMANTIC_EMBEDDING_THRESHOLD",
            DEFAULT_SEMANTIC_THRESHOLD,
        ),
        local_files_only=_env_flag("SEMANTIC_EMBEDDING_LOCAL_ONLY", default=False),
        auto_load=False,
    )


def _load_sentence_transformer(
    model_name: str,
    local_files_only: bool = False,
) -> Any:
    """Import sentence-transformers lazily so fallback remains lightweight."""
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name, local_files_only=local_files_only)


def _has_text(value: str) -> bool:
    """Return True when a text value has non-whitespace content."""
    return isinstance(value, str) and bool(value.strip())


def _split_two_embeddings(embeddings: Any) -> tuple[list[float], list[float]]:
    """Convert model embeddings into two float lists."""
    embeddings = _to_embedding_list(embeddings)

    if len(embeddings) != 2:
        raise ValueError("Expected exactly two embeddings.")

    return embeddings[0], embeddings[1]


def _to_embedding_list(embeddings: Any) -> list[list[float]]:
    """Convert model embeddings into a list of float vectors."""
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()

    return [_to_float_list(vector) for vector in embeddings]


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


def _is_e5_model(model_name: str) -> bool:
    """Return True for multilingual E5 model names."""
    return "e5" in model_name.casefold()


def _env_flag(name: str, default: bool = False) -> bool:
    """Read a truthy/falsy environment flag."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    return raw_value.strip().casefold() in TRUTHY_ENV_VALUES


def _env_float(name: str, default: float) -> float:
    """Read a float environment variable with a safe fallback."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        return float(raw_value)
    except ValueError:
        return default
