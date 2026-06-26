"""Technical intent inference for role-aware JD requirements."""

from __future__ import annotations

from typing import Any

from src.requirement_provenance import build_requirement_provenance_lookup
from src.requirement_types import CERTIFICATION_REQUIREMENT, TOOL_PLATFORM
from src.role_family import (
    BACKEND_ENGINEERING,
    COMPUTER_VISION_EKYC,
    DEVOPS_CLOUD,
    IT_SUPPORT_INFRA,
    SECURITY_GRC,
)
from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text


CORE_STACK = "CORE_STACK"
TOOLING_PLATFORM = "TOOLING_PLATFORM"
METHOD_CAPABILITY = "METHOD_CAPABILITY"
SECURITY_CONTROL = "SECURITY_CONTROL"
MODEL_TECHNIQUE = "MODEL_TECHNIQUE"
DEPLOYMENT_RUNTIME = "DEPLOYMENT_RUNTIME"
INFRA_IDENTITY_ADMIN = "INFRA_IDENTITY_ADMIN"
NETWORK_OPERATIONS = "NETWORK_OPERATIONS"
SYSTEM_OPERATIONS = "SYSTEM_OPERATIONS"
WORKPLACE_ADMIN = "WORKPLACE_ADMIN"
GENERIC_TECHNICAL = "GENERIC_TECHNICAL"

CORE_INTENT = "core"
SUPPORTING_INTENT = "supporting"
CONTEXTUAL_INTENT = "contextual"


def build_requirement_intent_summary(
    job_role_profile: dict[str, Any],
    required_skills: list[str],
    open_set_requirements: list[str],
    typed_requirements: list[dict[str, Any]] | None = None,
    requirement_provenance_summary: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build role-aware technical intent metadata for required/open-set items."""
    typed_lookup = {
        make_lookup_key(str(item.get("text", ""))): item
        for item in typed_requirements or []
        if str(item.get("text", "")).strip()
    }
    provenance_lookup = build_requirement_provenance_lookup(
        requirement_provenance_summary or []
    )
    role_family = str(job_role_profile.get("primary_role_family", "GENERIC_TECH"))
    summary: list[dict[str, Any]] = []

    for skill in required_skills:
        typed_requirement = typed_lookup.get(make_lookup_key(skill), {})
        provenance = provenance_lookup.get(make_lookup_key(skill), {})
        summary.append(
            {
                "text": skill,
                "taxonomy_status": "known",
                "role_family": role_family,
                **{
                    key: value
                    for key, value in provenance.items()
                    if key not in {"text"}
                },
                **infer_requirement_technical_intent(
                    skill,
                    role_family=role_family,
                    typed_requirement_type=str(typed_requirement.get("type", "")),
                ),
            }
        )

    for requirement in open_set_requirements:
        typed_requirement = typed_lookup.get(make_lookup_key(requirement), {})
        provenance = provenance_lookup.get(make_lookup_key(requirement), {})
        summary.append(
            {
                "text": requirement,
                "taxonomy_status": "unknown",
                "role_family": role_family,
                **{
                    key: value
                    for key, value in provenance.items()
                    if key not in {"text"}
                },
                **infer_requirement_technical_intent(
                    requirement,
                    role_family=role_family,
                    typed_requirement_type=str(typed_requirement.get("type", "")),
                ),
            }
        )

    return summary


def build_requirement_intent_lookup(
    requirement_intent_summary: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Build a lookup from normalized requirement text to intent metadata."""
    return {
        make_lookup_key(str(item.get("text", ""))): item
        for item in requirement_intent_summary
        if make_lookup_key(str(item.get("text", "")))
    }


def annotate_matches_with_requirement_intents(
    matches: list[dict[str, Any]],
    requirement_intent_summary: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Copy requirement intent metadata onto scored match objects."""
    intent_lookup = build_requirement_intent_lookup(requirement_intent_summary)
    annotated_matches: list[dict[str, Any]] = []
    for match in matches:
        requirement_key = make_lookup_key(str(match.get("required_skill", "")))
        annotated_matches.append(
            {
                **match,
                **{
                    key: value
                    for key, value in intent_lookup.get(requirement_key, {}).items()
                    if key
                    not in {
                        "text",
                    }
                },
            }
        )
    return annotated_matches


def infer_requirement_technical_intent(
    text: str,
    *,
    role_family: str,
    typed_requirement_type: str = "",
) -> dict[str, str]:
    """Infer intent type/strength for one technical requirement."""
    normalized_text = normalize_search_text(text)

    if role_family == COMPUTER_VISION_EKYC and any(
        phrase in normalized_text
        for phrase in (
            "face recognition",
            "face detection",
            "face matching",
            "face verification",
            "liveness detection",
            "anti spoofing",
            "anti-spoofing",
            "arcface",
            "landmark detection",
            "image normalization",
        )
    ):
        return _intent(MODEL_TECHNIQUE, CORE_INTENT, "computer_vision_core_signal")

    if role_family == SECURITY_GRC and any(
        phrase in normalized_text
        for phrase in (
            "qualys",
            "vulnerability management",
            "access control",
            "access governance",
            "iso 27001",
            "security operations",
            "security operation",
            "pam",
        )
    ):
        return _intent(SECURITY_CONTROL, CORE_INTENT, "security_control_signal")

    if role_family == BACKEND_ENGINEERING and any(
        phrase in normalized_text
        for phrase in (
            "java",
            "spring boot",
            "rest api",
            "sql",
            "microservice",
            "microservices",
        )
    ):
        return _intent(CORE_STACK, CORE_INTENT, "backend_core_stack_signal")

    if role_family == DEVOPS_CLOUD and any(
        phrase in normalized_text
        for phrase in (
            "aws",
            "azure",
            "gcp",
            "kubernetes",
            "terraform",
            "ci cd",
            "ci/cd",
            "jenkins",
            "monitoring",
            "docker",
        )
    ):
        return _intent(DEPLOYMENT_RUNTIME, CORE_INTENT, "devops_runtime_signal")

    if role_family == IT_SUPPORT_INFRA and any(
        phrase in normalized_text
        for phrase in (
            "active directory",
            "google workspace",
            "microsoft 365",
            "office 365",
            "user account",
            "access provisioning",
        )
    ):
        return _intent(
            INFRA_IDENTITY_ADMIN,
            CORE_INTENT,
            "infra_identity_admin_signal",
        )

    if role_family == IT_SUPPORT_INFRA and any(
        phrase in normalized_text
        for phrase in (
            "dns",
            "dhcp",
            "router",
            "switch",
            "vpn",
            "wifi",
            "wifi controller",
            "firewall",
        )
    ):
        return _intent(
            NETWORK_OPERATIONS,
            CORE_INTENT,
            "infra_network_operations_signal",
        )

    if role_family == IT_SUPPORT_INFRA and any(
        phrase in normalized_text
        for phrase in (
            "virtualization",
            "vmware",
            "hyper v",
            "hyper-v",
            "windows server",
            "linux administration",
            "server administration",
            "server",
        )
    ):
        return _intent(
            SYSTEM_OPERATIONS,
            SUPPORTING_INTENT,
            "infra_system_operations_signal",
        )

    if typed_requirement_type == CERTIFICATION_REQUIREMENT:
        return _intent(SECURITY_CONTROL, SUPPORTING_INTENT, "certification_requirement")

    if typed_requirement_type == TOOL_PLATFORM:
        return _intent(TOOLING_PLATFORM, SUPPORTING_INTENT, "tool_platform_requirement")

    if any(
        phrase in normalized_text
        for phrase in (
            "docker",
            "kubernetes",
            "onnx",
            "mobile inference",
            "edge",
            "deployment",
            "runtime",
        )
    ):
        return _intent(DEPLOYMENT_RUNTIME, SUPPORTING_INTENT, "deployment_runtime_signal")

    if any(
        phrase in normalized_text
        for phrase in (
            "python",
            "pytorch",
            "tensorflow",
            "linux",
            "oracle",
            "mysql",
            "postgres",
        )
    ):
        return _intent(TOOLING_PLATFORM, SUPPORTING_INTENT, "general_tooling_signal")

    if any(
        phrase in normalized_text
        for phrase in (
            "verification",
            "detection",
            "matching",
            "normalization",
            "classification",
            "integration",
            "optimization",
        )
    ):
        return _intent(METHOD_CAPABILITY, SUPPORTING_INTENT, "technical_capability_signal")

    return _intent(GENERIC_TECHNICAL, CONTEXTUAL_INTENT, "fallback_technical_intent")


def _intent(intent_type: str, intent_strength: str, intent_reason: str) -> dict[str, str]:
    """Build a stable intent payload."""
    return {
        "intent_type": intent_type,
        "intent_strength": intent_strength,
        "intent_reason": intent_reason,
    }
