"""Role-family inference and alignment helpers for technical screening."""

from __future__ import annotations

import re
from typing import Any

from src.text_normalization import normalize_search_text


BACKEND_ENGINEERING = "BACKEND_ENGINEERING"
FRONTEND_ENGINEERING = "FRONTEND_ENGINEERING"
FULLSTACK_ENGINEERING = "FULLSTACK_ENGINEERING"
DATA_AI_ENGINEERING = "DATA_AI_ENGINEERING"
COMPUTER_VISION_EKYC = "COMPUTER_VISION_EKYC"
SECURITY_GRC = "SECURITY_GRC"
DEVOPS_CLOUD = "DEVOPS_CLOUD"
IT_SUPPORT_INFRA = "IT_SUPPORT_INFRA"
MOBILE_ENGINEERING = "MOBILE_ENGINEERING"
QA_AUTOMATION = "QA_AUTOMATION"
GENERIC_TECH = "GENERIC_TECH"

ROLE_FAMILIES = (
    BACKEND_ENGINEERING,
    FRONTEND_ENGINEERING,
    FULLSTACK_ENGINEERING,
    DATA_AI_ENGINEERING,
    COMPUTER_VISION_EKYC,
    SECURITY_GRC,
    DEVOPS_CLOUD,
    IT_SUPPORT_INFRA,
    MOBILE_ENGINEERING,
    QA_AUTOMATION,
    GENERIC_TECH,
)

STRONG_ALIGNMENT = "strong_alignment"
PARTIAL_ALIGNMENT = "partial_alignment"
GENERIC_ALIGNMENT = "generic_alignment"
MISALIGNED = "misaligned"
UNKNOWN_ALIGNMENT = "unknown_alignment"

ROLE_FAMILY_DEFINITIONS = {
    BACKEND_ENGINEERING: {
        "title_terms": {
            "backend",
            "backend developer",
            "backend engineer",
            "java developer",
            "api developer",
        },
        "core_terms": {
            "java",
            "spring boot",
            "rest api",
            "sql",
            "microservice",
            "microservices",
            "hibernate",
            "backend services",
        },
        "supporting_terms": {
            "docker",
            "mysql",
            "postgres",
            "oracle",
            "relational database",
        },
    },
    FRONTEND_ENGINEERING: {
        "title_terms": {
            "frontend",
            "frontend developer",
            "frontend engineer",
            "ui engineer",
        },
        "core_terms": {
            "react",
            "angular",
            "vue",
            "javascript",
            "typescript",
            "css",
            "html",
            "frontend",
        },
        "supporting_terms": {
            "ui",
            "ux",
            "responsive",
            "web app",
        },
    },
    FULLSTACK_ENGINEERING: {
        "title_terms": {
            "fullstack",
            "full stack",
            "fullstack developer",
            "full stack developer",
        },
        "core_terms": {
            "fullstack",
            "full stack",
            "frontend",
            "backend",
            "react",
            "angular",
            "node",
            "spring boot",
            "rest api",
        },
        "supporting_terms": {
            "database",
            "docker",
            "javascript",
            "sql",
        },
    },
    DATA_AI_ENGINEERING: {
        "title_terms": {
            "data scientist",
            "ai engineer",
            "machine learning engineer",
            "ml engineer",
            "data engineer",
        },
        "core_terms": {
            "machine learning",
            "deep learning",
            "model training",
            "feature engineering",
            "data pipeline",
            "data pipelines",
            "llm",
            "retrieval",
            "rag",
            "pytorch",
            "tensorflow",
        },
        "supporting_terms": {
            "python",
            "analytics",
            "data analysis",
            "inference",
            "fine tuning",
        },
    },
    COMPUTER_VISION_EKYC: {
        "title_terms": {
            "computer vision",
            "computer vision engineer",
            "vision engineer",
            "ekyc",
            "biometric",
        },
        "core_terms": {
            "computer vision",
            "face recognition",
            "face detection",
            "face matching",
            "face verification",
            "liveness detection",
            "anti spoofing",
            "anti-spoofing",
            "arcface",
            "opencv",
            "landmark detection",
            "facial landmark",
            "image normalization",
            "ekyc",
            "biometric",
            "deepfake",
        },
        "supporting_terms": {
            "python",
            "onnx",
            "mobile inference",
            "edge",
            "on device",
            "alignment",
        },
    },
    SECURITY_GRC: {
        "title_terms": {
            "security",
            "security officer",
            "it security",
            "governance",
            "grc",
            "compliance",
            "risk",
        },
        "core_terms": {
            "qualys",
            "vulnerability management",
            "access control",
            "access governance",
            "governance",
            "compliance",
            "risk management",
            "iso 27001",
            "security operations",
            "security operation",
            "personal data protection",
            "pam",
            "audit",
        },
        "supporting_terms": {
            "security+",
            "ceh",
            "cipp/e",
            "cipm",
            "regulatory",
            "it security",
        },
    },
    DEVOPS_CLOUD: {
        "title_terms": {
            "devops",
            "site reliability engineer",
            "sre",
            "platform engineer",
            "cloud engineer",
        },
        "core_terms": {
            "devops",
            "aws",
            "azure",
            "gcp",
            "terraform",
            "kubernetes",
            "docker",
            "jenkins",
            "ci/cd",
            "monitoring",
            "prometheus",
            "grafana",
        },
        "supporting_terms": {
            "linux",
            "helm",
            "cloud",
            "deployment",
            "infrastructure",
        },
    },
    IT_SUPPORT_INFRA: {
        "title_terms": {
            "desktop support",
            "help desk",
            "helpdesk",
            "infrastructure engineer",
            "it helpdesk",
            "it infrastructure",
            "it staff",
            "it support",
            "it support engineer",
            "it support specialist",
            "network support",
            "sysadmin",
            "system administrator",
        },
        "core_terms": {
            "active directory",
            "dhcp",
            "dns",
            "end user support",
            "firewall",
            "google workspace",
            "hyper-v",
            "incident support",
            "linux administration",
            "microsoft 365",
            "office 365",
            "router",
            "server administration",
            "support engineer",
            "switch",
            "troubleshooting",
            "virtualization",
            "vmware",
            "vpn",
            "windows server",
        },
        "supporting_terms": {
            "access provisioning",
            "hardware",
            "monitoring",
            "printer",
            "sap",
            "software installation",
            "ticketing",
            "user account",
            "wifi controller",
            "workplace support",
        },
    },
    MOBILE_ENGINEERING: {
        "title_terms": {
            "mobile",
            "android",
            "ios",
            "mobile engineer",
            "android developer",
            "ios developer",
        },
        "core_terms": {
            "android",
            "ios",
            "swift",
            "kotlin",
            "flutter",
            "react native",
            "mobile",
        },
        "supporting_terms": {
            "on device",
            "mobile inference",
            "sdk",
            "edge",
        },
    },
    QA_AUTOMATION: {
        "title_terms": {
            "qa",
            "tester",
            "test engineer",
            "automation tester",
            "qa engineer",
        },
        "core_terms": {
            "test automation",
            "automation testing",
            "selenium",
            "cypress",
            "api testing",
            "qa",
            "test cases",
        },
        "supporting_terms": {
            "quality assurance",
            "postman",
            "regression testing",
        },
    },
}

RELATED_ROLE_FAMILIES = {
    BACKEND_ENGINEERING: {FULLSTACK_ENGINEERING, DEVOPS_CLOUD},
    FRONTEND_ENGINEERING: {FULLSTACK_ENGINEERING, MOBILE_ENGINEERING},
    FULLSTACK_ENGINEERING: {BACKEND_ENGINEERING, FRONTEND_ENGINEERING},
    DATA_AI_ENGINEERING: {COMPUTER_VISION_EKYC},
    COMPUTER_VISION_EKYC: {DATA_AI_ENGINEERING, MOBILE_ENGINEERING},
    SECURITY_GRC: set(),
    DEVOPS_CLOUD: {BACKEND_ENGINEERING},
    IT_SUPPORT_INFRA: {DEVOPS_CLOUD, SECURITY_GRC, GENERIC_TECH},
    MOBILE_ENGINEERING: {FRONTEND_ENGINEERING, COMPUTER_VISION_EKYC},
    QA_AUTOMATION: {BACKEND_ENGINEERING, FRONTEND_ENGINEERING},
    GENERIC_TECH: set(),
}


def infer_job_role_profile(
    *,
    job_title: str,
    required_skills: list[str],
    open_set_requirements: list[str],
    responsibilities: list[str] | None = None,
    typed_requirements: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Infer the dominant role-family of one JD from technical signals."""
    title_text = normalize_search_text(job_title)
    required_text = normalize_search_text(" ".join(required_skills))
    open_set_text = normalize_search_text(" ".join(open_set_requirements))
    responsibility_text = normalize_search_text(" ".join(responsibilities or []))
    typed_text = normalize_search_text(
        " ".join(
            str(item.get("text", "")).strip()
            for item in typed_requirements or []
            if str(item.get("ignored", "false")).casefold() != "true"
        )
    )
    sources = {
        "title": title_text,
        "required": required_text,
        "open_set": open_set_text,
        "responsibilities": responsibility_text,
        "typed": typed_text,
    }
    return _infer_role_profile_from_sources(sources, profile_kind="job")


def infer_candidate_role_profile(
    resume_profile: dict[str, Any],
    matches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Infer the dominant role-family signals present in one CV."""
    work_text = []
    for entry in resume_profile.get("work_experience", []):
        work_text.extend(
            [
                str(entry.get("title", "")),
                str(entry.get("company", "")),
                " ".join(str(item) for item in entry.get("description", [])),
            ]
        )
    project_text = []
    for project in resume_profile.get("projects", []):
        project_text.extend(
            [
                str(project.get("name", "")),
                " ".join(str(item) for item in project.get("description", [])),
                " ".join(str(item) for item in project.get("technologies", [])),
            ]
        )
    evidence_text = " ".join(
        str(match.get("evidence_text", "")).strip()
        for match in matches or []
        if str(match.get("evidence_text", "")).strip()
    )
    sources = {
        "title": normalize_search_text(
            " ".join(
                [
                    str(resume_profile.get("headline", "")),
                    " ".join(str(entry.get("title", "")) for entry in resume_profile.get("work_experience", [])),
                ]
            )
        ),
        "required": normalize_search_text(
            " ".join(str(skill) for skill in resume_profile.get("raw_skills", []))
        ),
        "open_set": normalize_search_text(evidence_text),
        "responsibilities": normalize_search_text(" ".join([*work_text, *project_text])),
        "typed": normalize_search_text(str(resume_profile.get("summary", ""))),
    }
    return _infer_role_profile_from_sources(sources, profile_kind="candidate")


def calculate_role_family_alignment(
    job_role_profile: dict[str, Any],
    candidate_role_profile: dict[str, Any],
) -> dict[str, Any]:
    """Calculate role-family alignment metadata between one JD and one CV."""
    job_primary = str(job_role_profile.get("primary_role_family", GENERIC_TECH))
    candidate_primary = str(
        candidate_role_profile.get("primary_role_family", GENERIC_TECH)
    )
    job_confidence = float(job_role_profile.get("confidence", 0.0) or 0.0)
    candidate_confidence = float(candidate_role_profile.get("confidence", 0.0) or 0.0)
    candidate_secondary = set(candidate_role_profile.get("secondary_role_families", []))

    if job_primary == GENERIC_TECH or job_confidence < 0.60:
        return _alignment_payload(
            UNKNOWN_ALIGNMENT,
            job_primary,
            candidate_primary,
            0,
            "The JD role-family signal is still too generic for role-aware calibration.",
        )

    if candidate_primary == job_primary:
        return _alignment_payload(
            STRONG_ALIGNMENT,
            job_primary,
            candidate_primary,
            0,
            "The candidate's strongest technical profile aligns with the JD role family.",
        )

    if job_primary in candidate_secondary or _is_related_role_family(
        job_primary,
        candidate_primary,
    ):
        return _alignment_payload(
            PARTIAL_ALIGNMENT,
            job_primary,
            candidate_primary,
            -2,
            "The candidate shows adjacent role-family overlap, but not as the primary profile.",
        )

    if candidate_primary == GENERIC_TECH or candidate_confidence < 0.55:
        return _alignment_payload(
            GENERIC_ALIGNMENT,
            job_primary,
            candidate_primary,
            0,
            "The candidate profile is too generic to confirm or reject strong role alignment.",
        )

    return _alignment_payload(
        MISALIGNED,
        job_primary,
        candidate_primary,
        -8,
        "The candidate's strongest technical profile points to a different role family than the JD.",
    )


def role_family_label(role_family: str) -> str:
    """Return a readable English label for one role-family code."""
    return role_family.replace("_", " ").title()


def _infer_role_profile_from_sources(
    sources: dict[str, str],
    *,
    profile_kind: str,
) -> dict[str, Any]:
    """Infer role-family scores from normalized text sources."""
    raw_scores: dict[str, float] = {role_family: 0.0 for role_family in ROLE_FAMILIES}
    matched_indicators: dict[str, list[str]] = {role_family: [] for role_family in ROLE_FAMILIES}

    source_weights = {
        "title": (4.0, 2.5, 0.0),
        "required": (3.0, 1.5, 0.0),
        "open_set": (2.5, 1.5, 0.0),
        "responsibilities": (2.0, 1.0, 0.0),
        "typed": (1.5, 0.75, 0.0),
    }

    for role_family, definition in ROLE_FAMILY_DEFINITIONS.items():
        for source_name, text in sources.items():
            if not text:
                continue

            title_weight, core_weight, supporting_weight = source_weights[source_name]
            matched_title_terms = _match_terms(text, definition["title_terms"])
            matched_core_terms = _match_terms(text, definition["core_terms"])
            matched_supporting_terms = _match_terms(text, definition["supporting_terms"])

            raw_scores[role_family] += len(matched_title_terms) * title_weight
            raw_scores[role_family] += len(matched_core_terms) * core_weight
            raw_scores[role_family] += len(matched_supporting_terms) * supporting_weight

            matched_indicators[role_family].extend(
                [
                    *[f"{source_name}:{term}" for term in matched_title_terms],
                    *[f"{source_name}:{term}" for term in matched_core_terms],
                    *[f"{source_name}:{term}" for term in matched_supporting_terms],
                ]
            )

    positive_scores = {
        role_family: score
        for role_family, score in raw_scores.items()
        if score > 0.0 and role_family != GENERIC_TECH
    }
    if not positive_scores:
        return {
            "profile_kind": profile_kind,
            "primary_role_family": GENERIC_TECH,
            "secondary_role_families": [],
            "confidence": 0.35,
            "signals": {GENERIC_TECH: 1.0},
            "matched_indicators": [],
        }

    total_score = sum(positive_scores.values())
    sorted_scores = sorted(
        positive_scores.items(),
        key=lambda item: (-item[1], item[0]),
    )
    primary_role_family, primary_score = sorted_scores[0]
    signals = {
        role_family: round(score / total_score, 4)
        for role_family, score in sorted_scores
    }
    confidence = round(min(0.95, 0.45 + 0.50 * (primary_score / total_score)), 4)
    secondary_role_families = [
        role_family
        for role_family, score in sorted_scores[1:]
        if score >= primary_score * 0.45
    ]

    return {
        "profile_kind": profile_kind,
        "primary_role_family": primary_role_family,
        "secondary_role_families": secondary_role_families,
        "confidence": confidence,
        "signals": signals,
        "matched_indicators": matched_indicators[primary_role_family][:10],
    }


def _match_terms(text: str, terms: set[str]) -> list[str]:
    """Return matched terms with stable ordering."""
    matched_terms: list[str] = []
    for term in sorted(terms):
        if _contains_term(text, term):
            matched_terms.append(term)
    return matched_terms


def _contains_term(text: str, term: str) -> bool:
    """Check whether normalized text contains one normalized term."""
    normalized_term = normalize_search_text(term)
    if not normalized_term:
        return False
    pattern = rf"(?<!\w){re.escape(normalized_term)}(?!\w)"
    return bool(re.search(pattern, text))


def _is_related_role_family(job_role_family: str, candidate_role_family: str) -> bool:
    """Return True for adjacent role families that should not be treated as fully wrong."""
    return candidate_role_family in RELATED_ROLE_FAMILIES.get(job_role_family, set())


def _alignment_payload(
    status: str,
    job_role_family: str,
    candidate_primary_role_family: str,
    adjustment_hint: int,
    note: str,
) -> dict[str, Any]:
    """Build a stable alignment payload."""
    return {
        "status": status,
        "job_role_family": job_role_family,
        "candidate_primary_role_family": candidate_primary_role_family,
        "adjustment_hint": adjustment_hint,
        "note": note,
        "job_role_family_label": role_family_label(job_role_family),
        "candidate_role_family_label": role_family_label(candidate_primary_role_family),
    }
