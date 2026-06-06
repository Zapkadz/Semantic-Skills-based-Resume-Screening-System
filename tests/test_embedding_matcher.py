from src.embedding_matcher import SemanticEmbeddingMatcher


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


def test_similarity_returns_cosine_similarity_with_loaded_model() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeEmbeddingModel())

    similarity = matcher.similarity(
        "Backend API development",
        "Built RESTful services",
    )

    assert similarity is not None
    assert round(similarity, 4) == 0.9986


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
