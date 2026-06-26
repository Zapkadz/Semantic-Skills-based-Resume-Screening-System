"""Filter open-set JD requirement units down to technical matching candidates."""

from __future__ import annotations

import re
from typing import Any

from src.skill_taxonomy import make_lookup_key
from src.text_normalization import normalize_search_text, repair_mojibake


KEPT_STATUS = "kept"
DISCARDED_STATUS = "discarded"

DEFAULT_TECHNICAL_CONFIDENCE_THRESHOLD = 0.55

TECHNICAL_PRODUCT_TOKENS = {
    "dhcp",
    "dns",
    "angular",
    "api",
    "apis",
    "arcface",
    "aws",
    "azure",
    "ci",
    "commvault",
    "cuda",
    "cudnn",
    "devops",
    "docker",
    "edge",
    "eks",
    "etl",
    "gcp",
    "firewall",
    "git",
    "gitlab",
    "gpu",
    "grafana",
    "grpc",
    "hadoop",
    "jenkins",
    "kafka",
    "kubernetes",
    "linux",
    "llm",
    "monolithic",
    "microservice",
    "microservices",
    "mobile",
    "mongodb",
    "mysql",
    "nutanix",
    "ocr",
    "onnx",
    "oracle",
    "pytorch",
    "postgres",
    "postgresql",
    "prometheus",
    "python",
    "pyspark",
    "qualys",
    "rabbitmq",
    "react",
    "redis",
    "router",
    "sdk",
    "spark",
    "switch",
    "spring",
    "sql",
    "tensorflow",
    "terraform",
    "typescript",
    "vpn",
    "vmware",
    "windows",
}

TECHNICAL_CAPABILITY_TOKENS = {
    "administration",
    "alignment",
    "anti",
    "augmentation",
    "classification",
    "control",
    "debugging",
    "deployment",
    "detection",
    "distillation",
    "encoding",
    "encryption",
    "evaluation",
    "fine",
    "generalization",
    "hardening",
    "indexing",
    "inference",
    "integration",
    "liveness",
    "matching",
    "monitoring",
    "normalization",
    "optimization",
    "orchestration",
    "parsing",
    "pipeline",
    "pipelines",
    "preprocessing",
    "pruning",
    "quantization",
    "recognition",
    "reranking",
    "retrieval",
    "scanning",
    "segmentation",
    "spoofing",
    "tuning",
    "verification",
}

TECHNICAL_SIGNAL_PHRASES = {
    "active directory",
    "access control",
    "computer vision",
    "data pipeline",
    "data pipelines",
    "face matching",
    "face recognition",
    "google workspace",
    "identity verification",
    "image normalization",
    "landmark detection",
    "liveness detection",
    "model deployment",
    "model inference",
    "micro service",
    "micro services",
    "patch upgrades",
    "vulnerability management",
}

DISCARDED_EXACT_PHRASES = {
    "compliance",
    "governance",
    "it governance",
    "it security operations",
    "operations",
    "personal data protection",
    "security operations",
}

DOMAIN_OR_REGULATORY_MARKERS = {
    "banking",
    "compliance",
    "domain",
    "finance",
    "governance",
    "policy",
    "policies",
    "privacy",
    "regulation",
    "regulations",
    "regulatory",
}

GENERIC_CONTEXT_TOKENS = {
    "ability",
    "business",
    "communication",
    "coordination",
    "detail",
    "experience",
    "knowledge",
    "mindset",
    "operations",
    "process",
    "teamwork",
    "working",
}

ACRONYM_OR_CERT_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Z]{2,}/[A-Z0-9]+|[A-Z][A-Z0-9]*\+(?:/[A-Z0-9]+)?|[A-Z]{2,}(?:\s+\d{2,})?)"
    r"(?![A-Za-z0-9])"
)
CAMEL_OR_BRAND_PATTERN = re.compile(r"[A-Z][a-z]+[A-Z][A-Za-z0-9]*")
LOW_SIGNAL_ACRONYMS = {"it"}


def filter_open_set_requirement_candidates(
    candidates: list[dict[str, Any]],
    *,
    known_requirement_labels: list[str] | None = None,
    threshold: float = DEFAULT_TECHNICAL_CONFIDENCE_THRESHOLD,
) -> list[dict[str, Any]]:
    """Score and label unknown requirement units for technical open-set matching."""
    known_requirement_keys = {
        make_lookup_key(label)
        for label in known_requirement_labels or []
        if make_lookup_key(label)
    }
    filtered_by_key: dict[str, dict[str, Any]] = {}

    for candidate in candidates:
        text = repair_mojibake(str(candidate.get("text", ""))).strip()
        if not text:
            continue

        canonical_text = _canonicalize_requirement_text(text)
        normalized_text = normalize_search_text(canonical_text)
        if not normalized_text:
            continue

        filtered_candidate = {
            **candidate,
            "text": text,
            "canonical_text": canonical_text,
            "normalized_text": normalized_text,
        }

        if make_lookup_key(canonical_text) in known_requirement_keys:
            filtered_candidate.update(
                {
                    "status": DISCARDED_STATUS,
                    "reason": "known_requirement_duplicate",
                    "technical_confidence": 0.0,
                    "keep_for_matching": False,
                    "keep_for_suggestion": False,
                }
            )
        else:
            filtered_candidate.update(
                _assess_open_set_technical_candidate(
                    canonical_text,
                    threshold=threshold,
                )
            )

        existing = filtered_by_key.get(normalized_text)
        if existing is None or _should_replace_candidate(filtered_candidate, existing):
            filtered_by_key[normalized_text] = filtered_candidate

    return list(filtered_by_key.values())


def build_open_set_filter_summary(
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Summarize open-set filter decisions for diagnostics and UI."""
    candidate_count = len(candidates)
    kept_candidates = [
        candidate for candidate in candidates if candidate.get("status") == KEPT_STATUS
    ]
    discarded_candidates = [
        candidate
        for candidate in candidates
        if candidate.get("status") == DISCARDED_STATUS
    ]
    discarded_reason_counts: dict[str, int] = {}
    for candidate in discarded_candidates:
        reason = str(candidate.get("reason", "")).strip() or "discarded"
        discarded_reason_counts[reason] = discarded_reason_counts.get(reason, 0) + 1

    return {
        "candidate_count": candidate_count,
        "kept_count": len(kept_candidates),
        "discarded_count": len(discarded_candidates),
        "kept_for_matching_count": sum(
            1 for candidate in candidates if candidate.get("keep_for_matching") is True
        ),
        "kept_for_suggestion_count": sum(
            1 for candidate in candidates if candidate.get("keep_for_suggestion") is True
        ),
        "discarded_reason_counts": discarded_reason_counts,
    }


def _assess_open_set_technical_candidate(
    text: str,
    *,
    threshold: float,
) -> dict[str, Any]:
    """Classify one unknown requirement as technical-enough or not."""
    normalized_text = normalize_search_text(text)
    tokens = normalized_text.split()

    if normalized_text in DISCARDED_EXACT_PHRASES:
        return _discard("generic_context_only", confidence=0.05)

    if _is_regulatory_or_domain_phrase(normalized_text, tokens):
        return _discard("domain_context_only", confidence=0.15)

    if _is_single_generic_token(tokens):
        return _discard("low_technical_specificity", confidence=0.10)

    confidence = 0.0
    reason = "low_technical_specificity"

    if _has_explicit_acronym_or_cert_signal(text):
        confidence = 0.95
        reason = "explicit_tool_signal"
    elif _has_product_or_platform_signal(tokens, normalized_text):
        confidence = 0.88
        reason = "explicit_tool_signal"
    elif _has_technical_signal_phrase(normalized_text):
        confidence = 0.82
        reason = "technical_capability_phrase"
    elif _has_technical_capability_shape(tokens):
        confidence = 0.74
        reason = "technical_capability_phrase"
    elif _looks_like_brand_or_framework_name(text, tokens):
        confidence = 0.66
        reason = "explicit_tool_signal"

    if confidence < threshold:
        return _discard(reason, confidence=round(confidence, 4))

    return {
        "status": KEPT_STATUS,
        "reason": reason,
        "technical_confidence": round(confidence, 4),
        "keep_for_matching": True,
        "keep_for_suggestion": True,
    }


def _canonicalize_requirement_text(text: str) -> str:
    """Apply lightweight canonicalization without guessing new skills."""
    clean_text = repair_mojibake(text).strip().strip(" .;:-")
    if not clean_text:
        return clean_text

    normalized_text = normalize_search_text(clean_text)
    preferred_casing = {
        "ci cd": "CI/CD",
        "commvault": "Commvault",
        "devops": "DevOps",
        "linux": "Linux",
        "micro service": "Micro-service",
        "nutanix administration": "Nutanix administration",
        "onnx": "ONNX",
        "oop": "OOP",
        "oracle": "Oracle",
        "pytorch": "PyTorch",
        "qualys": "Qualys",
        "security+": "Security+",
        "sql": "SQL",
        "tensorflow": "TensorFlow",
        "windows": "Windows",
    }
    return preferred_casing.get(normalized_text, clean_text)


def _discard(reason: str, *, confidence: float) -> dict[str, Any]:
    """Build a stable discarded-candidate decision."""
    return {
        "status": DISCARDED_STATUS,
        "reason": reason,
        "technical_confidence": round(confidence, 4),
        "keep_for_matching": False,
        "keep_for_suggestion": False,
    }


def _has_explicit_acronym_or_cert_signal(text: str) -> bool:
    """Return True for explicit acronym/certification-style tokens."""
    normalized_text = normalize_search_text(text)
    if normalized_text in {"ceh", "cipp e", "cipm", "ci cd", "iso 27001", "oop"}:
        return True
    if text.endswith("+"):
        return True

    for match in ACRONYM_OR_CERT_PATTERN.findall(text):
        if normalize_search_text(match) not in LOW_SIGNAL_ACRONYMS:
            return True

    return False


def _has_product_or_platform_signal(tokens: list[str], normalized_text: str) -> bool:
    """Return True for clear tool/platform/product-like requirement phrases."""
    return any(token in TECHNICAL_PRODUCT_TOKENS for token in tokens)


def _has_technical_signal_phrase(normalized_text: str) -> bool:
    """Return True for strong multi-word technical capability phrases."""
    return any(phrase in normalized_text for phrase in TECHNICAL_SIGNAL_PHRASES)


def _has_technical_capability_shape(tokens: list[str]) -> bool:
    """Return True for concise technical phrases such as 'identity verification'."""
    if len(tokens) < 2 or len(tokens) > 5:
        return False
    if any(token in DOMAIN_OR_REGULATORY_MARKERS for token in tokens):
        return False

    return any(token in TECHNICAL_CAPABILITY_TOKENS for token in tokens)


def _looks_like_brand_or_framework_name(text: str, tokens: list[str]) -> bool:
    """Heuristically keep concise product/framework names not yet in the taxonomy."""
    if len(tokens) != 1:
        return False
    if tokens[0] in GENERIC_CONTEXT_TOKENS:
        return False
    if CAMEL_OR_BRAND_PATTERN.search(text):
        return True

    return bool(re.search(r"[A-Za-z]+[-/][A-Za-z0-9]+", text))


def _is_regulatory_or_domain_phrase(normalized_text: str, tokens: list[str]) -> bool:
    """Return True for phrases that mostly describe context/compliance domains."""
    if normalized_text in DISCARDED_EXACT_PHRASES:
        return True

    if len(tokens) <= 4 and all(
        token in DOMAIN_OR_REGULATORY_MARKERS or token in {"data", "it", "personal"}
        for token in tokens
    ):
        return True

    return (
        any(token in DOMAIN_OR_REGULATORY_MARKERS for token in tokens)
        and not any(token in TECHNICAL_PRODUCT_TOKENS for token in tokens)
        and not any(token in TECHNICAL_CAPABILITY_TOKENS for token in tokens)
    )


def _is_single_generic_token(tokens: list[str]) -> bool:
    """Return True for very short generic phrases that are too broad to match."""
    if len(tokens) != 1:
        return False

    token = tokens[0]
    if token in TECHNICAL_PRODUCT_TOKENS or token in TECHNICAL_CAPABILITY_TOKENS:
        return False

    return token in {
        "compliance",
        "governance",
        "operations",
        "privacy",
        "security",
        "support",
    }


def _should_replace_candidate(
    candidate: dict[str, Any],
    existing: dict[str, Any],
) -> bool:
    """Prefer kept or higher-confidence candidates when canonical keys collide."""
    candidate_status = str(candidate.get("status", ""))
    existing_status = str(existing.get("status", ""))
    if candidate_status == KEPT_STATUS and existing_status != KEPT_STATUS:
        return True
    if candidate_status != KEPT_STATUS and existing_status == KEPT_STATUS:
        return False

    return float(candidate.get("technical_confidence", 0.0)) > float(
        existing.get("technical_confidence", 0.0)
    )
