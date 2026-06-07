"""HTTP API entry point for web integration."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from src.api_models import ScreeningRequest
from src.payload_pipeline import run_screening_payload


API_PHASE = "Phase 11 - Python API Service"

app = FastAPI(
    title="Semantic Skills Resume Screening API",
    version="0.11.0",
)


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
        return run_screening_payload(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
