from src.embedding_matcher import (
    DEFAULT_EMBEDDING_MODEL,
    E5_QUERY_INSTRUCTION,
    MULTILINGUAL_E5_MODEL,
    SemanticEmbeddingMatcher,
    build_embedding_matcher,
    build_embedding_matcher_from_env,
    format_embedding_document,
    format_embedding_query,
)


class FakeEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "Backend API development": [1.0, 0.0],
            "Built RESTful services": [0.95, 0.05],
            "REST API": [0.90, 0.10],
            "React": [0.0, 1.0],
            "": [0.0, 0.0],
        }
        return [vectors[text] for text in texts]


class CountingEmbeddingModel:
    def __init__(self) -> None:
        self.encode_calls = 0

    def encode(self, texts: list[str]) -> list[list[float]]:
        self.encode_calls += 1
        vectors = {
            "face recognition": [1.0, 0.0],
            "nhận diện khuôn mặt": [0.95, 0.05],
            "accounting": [0.0, 1.0],
        }
        return [vectors[text] for text in texts]


def test_default_embedding_model_is_local_multilingual_bge_m3() -> None:
    matcher = build_embedding_matcher(enabled=True)

    assert matcher is not None
    assert matcher.model_name == DEFAULT_EMBEDDING_MODEL
    assert matcher.model_name == "BAAI/bge-m3"


def test_build_embedding_matcher_from_env_is_disabled_by_default(monkeypatch) -> None:
    monkeypatch.delenv("SEMANTIC_EMBEDDING_ENABLED", raising=False)

    assert build_embedding_matcher_from_env() is None


def test_build_embedding_matcher_from_env_reads_optional_config(monkeypatch) -> None:
    monkeypatch.setenv("SEMANTIC_EMBEDDING_ENABLED", "1")
    monkeypatch.setenv("SEMANTIC_EMBEDDING_MODEL", MULTILINGUAL_E5_MODEL)
    monkeypatch.setenv("SEMANTIC_EMBEDDING_THRESHOLD", "0.81")
    monkeypatch.setenv("SEMANTIC_EMBEDDING_LOCAL_ONLY", "1")

    matcher = build_embedding_matcher_from_env()

    assert matcher is not None
    assert matcher.model_name == MULTILINGUAL_E5_MODEL
    assert matcher.threshold == 0.81
    assert matcher.local_files_only is True
    assert matcher.is_available() is False


def test_similarity_returns_cosine_similarity_with_loaded_model() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeEmbeddingModel())

    similarity = matcher.similarity(
        "Backend API development",
        "Built RESTful services",
    )

    assert similarity is not None
    assert round(similarity, 4) == 0.9986


def test_embedding_query_formatting_adds_instruction_for_e5_only() -> None:
    assert format_embedding_query("face recognition", DEFAULT_EMBEDDING_MODEL) == (
        "face recognition"
    )
    assert format_embedding_document("nhận diện khuôn mặt", MULTILINGUAL_E5_MODEL) == (
        "nhận diện khuôn mặt"
    )
    assert format_embedding_query("face recognition", MULTILINGUAL_E5_MODEL) == (
        f"{E5_QUERY_INSTRUCTION}face recognition"
    )


def test_similarity_reuses_cached_embeddings() -> None:
    model = CountingEmbeddingModel()
    matcher = SemanticEmbeddingMatcher(model=model)

    first = matcher.similarity("face recognition", "nhận diện khuôn mặt")
    second = matcher.similarity("face recognition", "nhận diện khuôn mặt")

    assert first is not None
    assert round(first, 4) == 0.9986
    assert second == first
    assert model.encode_calls == 2


def test_similarity_returns_none_for_blank_text() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeEmbeddingModel())

    assert matcher.similarity("", "REST API") is None
    assert matcher.similarity("REST API", "   ") is None


def test_similarity_falls_back_when_model_loader_fails() -> None:
    def failing_loader(model_name: str) -> object:
        raise RuntimeError(f"Cannot load {model_name}")

    matcher = SemanticEmbeddingMatcher(
        model_name="unavailable-model",
        model_loader=failing_loader,
    )

    assert matcher.is_available() is False
    assert matcher.similarity("Backend API development", "REST API") is None
    assert matcher.is_available() is False
    assert matcher.unavailable_reason == "Cannot load unavailable-model"


def test_best_match_returns_candidate_above_threshold() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeEmbeddingModel(), threshold=0.70)

    match = matcher.best_match(
        "Backend API development",
        ["React", "REST API"],
    )

    assert match == {
        "candidate_skill": "REST API",
        "similarity": 0.9939,
    }


def test_best_match_returns_none_below_threshold() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeEmbeddingModel(), threshold=0.99)

    match = matcher.best_match("Backend API development", ["React"])

    assert match is None
