from src.role_family import (
    BACKEND_ENGINEERING,
    COMPUTER_VISION_EKYC,
    DATA_AI_ENGINEERING,
    STRONG_ALIGNMENT,
    PARTIAL_ALIGNMENT,
    infer_candidate_role_profile,
    infer_job_role_profile,
    calculate_role_family_alignment,
)


def test_infer_job_role_profile_detects_backend_engineering() -> None:
    profile = infer_job_role_profile(
        job_title="Backend Java Developer",
        required_skills=["Java", "Spring Boot", "REST API", "SQL"],
        open_set_requirements=[],
        responsibilities=["Build backend services and REST APIs."],
        typed_requirements=[],
    )

    assert profile["primary_role_family"] == BACKEND_ENGINEERING
    assert profile["confidence"] >= 0.7


def test_infer_job_role_profile_detects_computer_vision_ekyc() -> None:
    profile = infer_job_role_profile(
        job_title="AI Computer Vision Engineer - eKYC",
        required_skills=["Python"],
        open_set_requirements=[
            "face recognition",
            "liveness detection",
            "anti-spoofing",
        ],
        responsibilities=["Deploy face verification models for mobile eKYC."],
        typed_requirements=[],
    )

    assert profile["primary_role_family"] == COMPUTER_VISION_EKYC
    assert profile["confidence"] >= 0.7


def test_infer_candidate_role_profile_detects_data_ai_engineering() -> None:
    resume_profile = {
        "headline": "Machine Learning Engineer",
        "summary": "Built model training and retrieval pipelines for AI products.",
        "raw_skills": ["Python", "PyTorch", "TensorFlow", "Machine Learning"],
        "work_experience": [
            {
                "title": "AI Engineer",
                "company": "ABC",
                "description": [
                    "Built model training pipelines and inference services."
                ],
            }
        ],
        "projects": [],
    }

    profile = infer_candidate_role_profile(resume_profile, matches=[])

    assert profile["primary_role_family"] == DATA_AI_ENGINEERING
    assert profile["confidence"] >= 0.65


def test_calculate_role_family_alignment_handles_strong_and_partial_alignment() -> None:
    strong = calculate_role_family_alignment(
        {
            "primary_role_family": BACKEND_ENGINEERING,
            "confidence": 0.85,
        },
        {
            "primary_role_family": BACKEND_ENGINEERING,
            "secondary_role_families": [],
            "confidence": 0.80,
        },
    )
    partial = calculate_role_family_alignment(
        {
            "primary_role_family": COMPUTER_VISION_EKYC,
            "confidence": 0.85,
        },
        {
            "primary_role_family": DATA_AI_ENGINEERING,
            "secondary_role_families": [COMPUTER_VISION_EKYC],
            "confidence": 0.80,
        },
    )

    assert strong["status"] == STRONG_ALIGNMENT
    assert strong["adjustment_hint"] == 0
    assert partial["status"] == PARTIAL_ALIGNMENT
    assert partial["adjustment_hint"] == -2
