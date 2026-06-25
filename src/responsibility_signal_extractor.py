"""Extract technical responsibility signals from JD description/responsibility lines."""

from __future__ import annotations

import re
from typing import Any

from src.requirement_types import DOMAIN_CONTEXT
from src.skill_extractor import extract_taxonomy_skills_from_text, merge_skill_lists
from src.text_normalization import normalize_search_text


TECHNICAL_TASK = "TECHNICAL_TASK"
TECHNICAL_CONTEXT = "TECHNICAL_CONTEXT"
DOMAIN_TASK = "DOMAIN_TASK"
OPERATIONAL_TASK = "OPERATIONAL_TASK"
GENERAL_TASK = "GENERAL_TASK"

SPECIFICITY_HIGH = "high"
SPECIFICITY_MEDIUM = "medium"
SPECIFICITY_LOW = "low"

RESPONSIBILITY_SECTIONS = {"description", "responsibilities"}
SUPPORTED_SIGNAL_TYPES = {TECHNICAL_TASK, TECHNICAL_CONTEXT}

TECHNICAL_ACTION_MARKERS = (
    "administer",
    "analyze",
    "automate",
    "build",
    "cai dat",
    "cau hinh",
    "configure",
    "deploy",
    "develop",
    "duy tri",
    "giam sat",
    "handle",
    "implement",
    "install",
    "integrate",
    "maintain",
    "manage",
    "monitor",
    "operate",
    "optimize",
    "setup",
    "support",
    "trien khai",
    "troubleshoot",
    "upgrade",
    "van hanh",
)

GENERIC_ACTION_MARKERS = (
    "collaborate",
    "communicate",
    "coordinate",
    "document",
    "liaise",
    "participate",
    "prepare",
    "report",
    "work with",
)

CURATED_TECHNICAL_TERMS = {
    "Active Directory": ("active directory", "ad ds"),
    "DNS": ("dns",),
    "DHCP": ("dhcp",),
    "Firewall": ("firewall", "firewalls"),
    "Google Workspace": ("google workspace", "workspace google"),
    "Linux": ("linux",),
    "Operating System": ("operating system", "os administration"),
    "Router": ("router", "routers"),
    "SAP": ("sap",),
    "Server": ("server", "servers"),
    "Switch": ("switch", "switches"),
    "VPN": ("vpn", "vpn connectivity"),
    "Virtualization": (
        "virtualization",
        "virtualisation",
        "virtual machine",
        "virtual machines",
        "virtualize server",
        "virtualize servers",
        "vmware",
        "hyper v",
        "hyper-v",
    ),
}


def build_responsibility_signal_metadata(
    typed_requirements: list[dict[str, Any]],
    taxonomy: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Extract technical responsibility signal objects and a flattened candidate pool."""
    responsibility_signals = extract_responsibility_signals(typed_requirements, taxonomy)
    technical_responsibility_candidates = extract_technical_responsibility_candidates(
        responsibility_signals
    )
    return {
        "responsibility_signals": responsibility_signals,
        "technical_responsibility_candidates": technical_responsibility_candidates,
    }


def extract_responsibility_signals(
    typed_requirements: list[dict[str, Any]],
    taxonomy: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build structured signal objects from description/responsibility requirement lines."""
    signals: list[dict[str, Any]] = []

    for requirement in typed_requirements:
        if str(requirement.get("ignored", "false")).casefold() == "true":
            continue

        section = str(requirement.get("section", ""))
        if section not in RESPONSIBILITY_SECTIONS:
            continue

        text = str(requirement.get("text", "")).strip()
        if not text:
            continue

        normalized_text = normalize_search_text(text)
        technical_terms = _extract_technical_terms(text, taxonomy)
        has_technical_action = any(
            marker in normalized_text for marker in TECHNICAL_ACTION_MARKERS
        )
        has_generic_action = any(
            marker in normalized_text for marker in GENERIC_ACTION_MARKERS
        )
        requirement_type = str(requirement.get("type", ""))

        signal_type = _classify_signal_type(
            requirement_type=requirement_type,
            technical_terms=technical_terms,
            has_technical_action=has_technical_action,
            has_generic_action=has_generic_action,
        )
        specificity = _classify_specificity(
            technical_terms=technical_terms,
            has_technical_action=has_technical_action,
        )

        signals.append(
            {
                "text": text,
                "normalized_text": normalized_text,
                "signal_type": signal_type,
                "technical_terms": technical_terms,
                "specificity": specificity,
                "section": section,
                "source_requirement_type": requirement_type,
            }
        )

    return signals


def extract_technical_responsibility_candidates(
    responsibility_signals: list[dict[str, Any]],
) -> list[str]:
    """Flatten high-signal technical responsibility terms into a candidate pool."""
    return merge_skill_lists(
        [
            term
            for signal in responsibility_signals
            if str(signal.get("signal_type", "")) in SUPPORTED_SIGNAL_TYPES
            and str(signal.get("specificity", "")) in {SPECIFICITY_HIGH, SPECIFICITY_MEDIUM}
            for term in signal.get("technical_terms", [])
        ]
    )


def _extract_technical_terms(
    text: str,
    taxonomy: dict[str, dict[str, Any]],
) -> list[str]:
    """Extract known or curated technical terms from one responsibility line."""
    normalized_text = normalize_search_text(text)
    taxonomy_terms = extract_taxonomy_skills_from_text(text, taxonomy)

    curated_terms = [
        canonical
        for canonical, aliases in CURATED_TECHNICAL_TERMS.items()
        if any(_contains_alias(normalized_text, alias) for alias in aliases)
    ]

    return merge_skill_lists(taxonomy_terms, curated_terms)


def _contains_alias(normalized_text: str, alias: str) -> bool:
    """Match an alias with normalized word boundaries."""
    normalized_alias = normalize_search_text(alias)
    if not normalized_alias:
        return False

    pattern = rf"(?<!\w){re.escape(normalized_alias)}(?!\w)"
    return bool(re.search(pattern, normalized_text))


def _classify_signal_type(
    *,
    requirement_type: str,
    technical_terms: list[str],
    has_technical_action: bool,
    has_generic_action: bool,
) -> str:
    """Assign a coarse signal type for one responsibility line."""
    if technical_terms:
        if has_technical_action:
            return TECHNICAL_TASK
        return TECHNICAL_CONTEXT

    if requirement_type == DOMAIN_CONTEXT:
        return DOMAIN_TASK

    if has_generic_action:
        return OPERATIONAL_TASK

    return GENERAL_TASK


def _classify_specificity(
    *,
    technical_terms: list[str],
    has_technical_action: bool,
) -> str:
    """Assign a simple specificity level for extracted responsibility terms."""
    if not technical_terms:
        return SPECIFICITY_LOW

    if len(technical_terms) >= 2 or has_technical_action:
        return SPECIFICITY_HIGH

    return SPECIFICITY_MEDIUM
