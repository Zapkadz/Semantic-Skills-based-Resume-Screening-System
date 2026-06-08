"""HTTP API entry point for web integration."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from src.api_models import ScreeningRequest
from src.embedding_matcher import (
    SemanticEmbeddingMatcher,
    build_embedding_matcher_from_env,
)
from src.payload_pipeline import run_screening_payload


API_PHASE = "Phase 11 - Python API Service"

app = FastAPI(
    title="Semantic Skills Resume Screening API",
    version="0.11.0",
)

_API_EMBEDDING_MATCHER: SemanticEmbeddingMatcher | None = None


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return API health information."""
    return {
        "status": "ok",
        "service": "semantic-skills-resume-screening",
        "phase": API_PHASE,
    }


@app.post("/screening")
def screen_candidates(request: ScreeningRequest) -> dict:
    """Screen candidate CV payloads against one job payload."""
    try:
        return run_screening_payload(
            request,
            embedding_matcher=_get_api_embedding_matcher(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


def _get_api_embedding_matcher() -> SemanticEmbeddingMatcher | None:
    """Return one cached API embedding matcher when env config enables it."""
    global _API_EMBEDDING_MATCHER

    if _API_EMBEDDING_MATCHER is None:
        _API_EMBEDDING_MATCHER = build_embedding_matcher_from_env()

    return _API_EMBEDDING_MATCHER
