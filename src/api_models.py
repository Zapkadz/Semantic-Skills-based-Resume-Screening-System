"""Pydantic models for the HTTP API payloads."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class JobPayload(BaseModel):
    """Input job payload sent by a web application."""

    model_config = ConfigDict(extra="allow")

    job_id: int | str | None = None
    job_title: str = ""
    title: str = ""
    requirements: list[str] = Field(default_factory=list)
    must_have_skills: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    nice_to_have_skills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    minimum_experience_years: int | None = None
    raw_text: str = ""
    job_description_text: str = ""
    description: str = ""


class CandidatePayload(BaseModel):
    """Input candidate/CV payload sent by a web application."""

    model_config = ConfigDict(extra="allow")

    application_id: int | str | None = None
    candidate_id: int | str | None = None
    candidate_name: str = ""
    email: str = ""
    phone: str = ""
    headline: str = ""
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    work_experience: list[dict[str, Any]] = Field(default_factory=list)
    projects: list[dict[str, Any]] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    cv_text: str = ""
    resume_text: str = ""
    cv_file_path: str = ""
    applied_at: str = ""


class RecommendationOptions(BaseModel):
    """Optional controls for candidate-side job recommendation."""

    model_config = ConfigDict(extra="allow")

    top_k: int = Field(default=10, ge=1, le=100)
    retrieval_top_n: int = Field(default=50, ge=1, le=500)


class ScreeningRequest(BaseModel):
    """Request body for the screening endpoint."""

    model_config = ConfigDict(extra="allow")

    job: JobPayload
    candidates: list[CandidatePayload]
    taxonomy_path: str = "data/taxonomy/skills.json"


class JobRecommendationRequest(BaseModel):
    """Request body for candidate-side job recommendation."""

    model_config = ConfigDict(extra="allow")

    candidate: CandidatePayload
    jobs: list[JobPayload]
    options: RecommendationOptions = Field(default_factory=RecommendationOptions)
    taxonomy_path: str = "data/taxonomy/skills.json"
