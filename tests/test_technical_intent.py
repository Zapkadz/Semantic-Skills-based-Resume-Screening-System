from src.role_family import BACKEND_ENGINEERING, COMPUTER_VISION_EKYC, SECURITY_GRC
from src.technical_intent import (
    CORE_INTENT,
    CORE_STACK,
    MODEL_TECHNIQUE,
    SECURITY_CONTROL,
    build_requirement_intent_summary,
    infer_requirement_technical_intent,
)


def test_infer_requirement_technical_intent_detects_backend_core_stack() -> None:
    intent = infer_requirement_technical_intent(
        "Spring Boot",
        role_family=BACKEND_ENGINEERING,
    )

    assert intent == {
        "intent_type": CORE_STACK,
        "intent_strength": CORE_INTENT,
        "intent_reason": "backend_core_stack_signal",
    }


def test_infer_requirement_technical_intent_detects_computer_vision_model_technique() -> None:
    intent = infer_requirement_technical_intent(
        "face recognition",
        role_family=COMPUTER_VISION_EKYC,
    )

    assert intent == {
        "intent_type": MODEL_TECHNIQUE,
        "intent_strength": CORE_INTENT,
        "intent_reason": "computer_vision_core_signal",
    }


def test_build_requirement_intent_summary_marks_security_control_open_set() -> None:
    summary = build_requirement_intent_summary(
        {
            "primary_role_family": SECURITY_GRC,
        },
        required_skills=[],
        open_set_requirements=["Qualys", "vulnerability management"],
        typed_requirements=[],
    )

    assert summary == [
        {
            "text": "Qualys",
            "taxonomy_status": "unknown",
            "role_family": SECURITY_GRC,
            "intent_type": SECURITY_CONTROL,
            "intent_strength": CORE_INTENT,
            "intent_reason": "security_control_signal",
        },
        {
            "text": "vulnerability management",
            "taxonomy_status": "unknown",
            "role_family": SECURITY_GRC,
            "intent_type": SECURITY_CONTROL,
            "intent_strength": CORE_INTENT,
            "intent_reason": "security_control_signal",
        },
    ]
