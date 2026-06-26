import pytest

from src.payload_pipeline import (
    build_cv_document_from_payload,
    build_jd_text_from_payload,
    run_screening_payload,
)
from src.embedding_matcher import SemanticEmbeddingMatcher


class FakeMultilingualEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "identity verification": [1.0, 0.0],
            "digital identity verification": [0.96, 0.04],
            "eKYC": [0.90, 0.10],
            "Identity Engineer": [0.0, 1.0],
        }
        return [vectors.get(text, [0.0, 1.0]) for text in texts]


class FakeSecurityEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        concepts = [
            ("linux", ("linux",)),
            ("qualys", ("qualys",)),
            ("vulnerability", ("vulnerability",)),
            ("access", ("access", "pam")),
            ("data_protection", ("personal data protection", "data protection")),
            ("governance", ("governance",)),
            ("compliance", ("compliance", "iso 27001")),
            ("security", ("security operations", "it security", "security+")),
            ("ceh", ("ceh", "certified ethical hacker")),
        ]
        vectors: list[list[float]] = []
        for text in texts:
            normalized_text = text.casefold()
            vector = [
                1.0 if any(alias in normalized_text for alias in aliases) else 0.0
                for _, aliases in concepts
            ]
            vectors.append(vector if any(vector) else [0.0 for _ in concepts])

        return vectors


def test_build_jd_text_from_payload_uses_structured_sections() -> None:
    job = {
        "job_title": "Backend Java Developer",
        "requirements": ["Java", "Spring Boot"],
        "nice_to_have": ["AWS"],
        "responsibilities": ["Build REST APIs."],
        "minimum_experience_years": 1,
    }

    text = build_jd_text_from_payload(job)

    assert text == (
        "Backend Java Developer\n"
        "\n"
        "Requirements:\n"
        "- Java\n"
        "- Spring Boot\n"
        "- 1+ year experience\n"
        "\n"
        "Nice to have:\n"
        "- AWS\n"
        "\n"
        "Responsibilities:\n"
        "- Build REST APIs."
    )


def test_build_jd_text_from_payload_prefers_raw_text() -> None:
    raw_text = "QA Tester\n\nRequirements:\n- API testing"

    assert build_jd_text_from_payload({"raw_text": raw_text}) == raw_text


def test_build_jd_text_from_payload_accepts_title_and_job_description_text() -> None:
    text = build_jd_text_from_payload(
        {
            "title": "Identity Platform Specialist",
            "job_description_text": "Requirements:\n- identity verification",
        }
    )

    assert text == (
        "Identity Platform Specialist\n"
        "\n"
        "Requirements:\n"
        "- identity verification"
    )


def test_build_jd_text_from_payload_strips_php_editor_html() -> None:
    job = {
        "job_title": "IT Security & IT Governance Officer",
        "requirements": [
            (
                "<p><strong>1. Qualifications &amp; Experience</strong></p>"
                "<p>•&nbsp;<strong>Professional requirements: Proficiency in Linux</strong>, "
                "Nutanix administration, Commvault, and Qualys.</p>"
                "<p>• At least 3 yeear of experience in "
                "<strong>IT Security Operations, Governance, Compliance, "
                "Personal Data Protection</strong>.</p>"
            )
        ],
        "responsibilities": [
            (
                "<p><strong>1. IT Security Operations</strong></p>"
                "<p>• Manage and monitor Qualys vulnerability scanning platform.</p>"
            )
        ],
    }

    text = build_jd_text_from_payload(job)

    assert "<p>" not in text
    assert "&nbsp;" not in text
    assert "- Professional requirements: Proficiency in Linux" in text
    assert "- At least 3 yeear of experience in IT Security Operations" in text
    assert "- Manage and monitor Qualys vulnerability scanning platform." in text


def test_build_cv_document_from_payload_uses_cv_text_and_ids() -> None:
    candidate = {
        "application_id": 123,
        "candidate_id": 456,
        "candidate_name": "Nguyen Van A",
        "email": "candidate@example.com",
        "cv_text": "Nguyen Van A\nBackend Developer\n\nSkills:\n- Java",
    }

    document = build_cv_document_from_payload(candidate)

    assert document == {
        "filename": "application-123__candidate-456.txt",
        "path": "",
        "text": "Nguyen Van A\nBackend Developer\n\nSkills:\n- Java",
        "application_id": 123,
        "candidate_id": 456,
        "email": "candidate@example.com",
        "phone": "",
        "applied_at": "",
        "cv_file_path": "",
        "candidate_name": "Nguyen Van A",
    }


def test_build_cv_document_from_payload_accepts_resume_text_alias() -> None:
    candidate = {
        "candidate_id": "cand-01",
        "candidate_name": "Digital ID Candidate",
        "resume_text": "Digital ID Candidate\nIdentity Engineer\n\nSkills:\n- identity verification",
    }

    document = build_cv_document_from_payload(candidate)

    assert document["filename"] == "candidate-cand-01.txt"
    assert document["text"] == (
        "Digital ID Candidate\nIdentity Engineer\n\nSkills:\n- identity verification"
    )


def test_build_cv_document_from_payload_can_build_structured_cv_text() -> None:
    candidate = {
        "application_id": 123,
        "candidate_id": 456,
        "candidate_name": "Nguyen Van A",
        "headline": "Backend Developer",
        "summary": "Backend developer with Java experience.",
        "skills": ["Java", "Spring Boot"],
        "work_experience": [
            {
                "title": "Backend Developer Intern",
                "company": "ABC Tech",
                "duration": "06/2024 - 12/2024",
                "description": ["Built REST APIs using Java."],
            }
        ],
        "projects": [
            {
                "name": "E-commerce API",
                "description": ["Created RESTful APIs."],
                "technologies": ["Java", "Spring Boot"],
            }
        ],
        "education": ["Bachelor of Software Engineering"],
    }

    document = build_cv_document_from_payload(candidate)

    assert document["filename"] == "application-123__candidate-456.txt"
    assert document["text"] == (
        "Nguyen Van A\n"
        "Backend Developer\n"
        "\n"
        "Summary:\n"
        "Backend developer with Java experience.\n"
        "\n"
        "Skills:\n"
        "- Java\n"
        "- Spring Boot\n"
        "\n"
        "Work Experience:\n"
        "Backend Developer Intern - ABC Tech\n"
        "06/2024 - 12/2024\n"
        "- Built REST APIs using Java.\n"
        "\n"
        "Projects:\n"
        "E-commerce API\n"
        "- Created RESTful APIs.\n"
        "Technologies: Java, Spring Boot\n"
        "\n"
        "Education:\n"
        "Bachelor of Software Engineering"
    )


def test_run_screening_payload_returns_ranked_candidates_with_web_ids() -> None:
    result = run_screening_payload(_demo_screening_payload())

    assert result["trace_id"].startswith("screening-")
    assert result["job"]["job_id"] == 10
    assert result["job"]["title"] == "Backend Java Developer"
    assert result["job"]["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    assert result["job"]["open_set_requirements"] == []
    assert result["job"]["open_set_filter_summary"] == {
        "candidate_count": 0,
        "kept_count": 0,
        "discarded_count": 0,
        "kept_for_matching_count": 0,
        "kept_for_suggestion_count": 0,
        "discarded_reason_counts": {},
    }
    assert result["job"]["taxonomy_coverage"] == {
        "known_count": 5,
        "unknown_count": 0,
        "coverage_ratio": 1.0,
        "known_requirements": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
        "unknown_requirements": [],
    }
    assert result["job"]["screening_confidence"] == {
        "level": "high",
        "known_requirement_count": 5,
        "open_set_requirement_count": 0,
        "embedding_enabled": False,
        "warnings": [],
    }
    assert result["job"]["job_role_profile"]["primary_role_family"] == "BACKEND_ENGINEERING"
    assert any(
        item["text"] == "Java" and item["intent_type"] == "CORE_STACK"
        for item in result["job"]["requirement_intent_summary"]
    )

    candidate = result["candidates"][0]
    assert candidate["rank"] == 1
    assert candidate["application_id"] == 123
    assert candidate["candidate_id"] == 456
    assert candidate["candidate_name"] == "Nguyen Van A"
    assert candidate["source_file"] == "application-123__candidate-456.txt"
    assert candidate["final_score"] == 87
    assert candidate["recommendation"] == "Strong Review"
    assert candidate["raw_base_score"] == 87
    assert candidate["role_calibrated_score"] == 87
    assert candidate["source_calibrated_score"] == 87
    assert candidate["role_score_adjustment"] == 0
    assert candidate["source_score_adjustment"] == 0
    assert candidate["candidate_role_profile"]["primary_role_family"] == "BACKEND_ENGINEERING"
    assert candidate["role_family_alignment"]["status"] == "strong_alignment"
    assert candidate["role_alignment_impact"]["reason_code"] == "strong_same_role_alignment"
    assert candidate["source_alignment_impact"]["reason_code"] in {
        "explicit_requirements_well_covered",
        "explicit_core_requirements_confirmed",
    }
    assert candidate["core_requirement_fit_summary"]["core"]["total"] == 4
    assert candidate["source_requirement_fit_summary"]["explicit_requirement"]["total"] == 5
    assert candidate["review_card"]["job_title"] == "Backend Java Developer"
    assert candidate["review_card"]["concerns"] == [
        "Optional nice-to-have gaps: AWS and Kafka."
    ]
    assert result["diagnostics"]["trace_id"] == result["trace_id"]
    assert result["diagnostics"]["payload"]["job"]["flags"] == []
    assert result["diagnostics"]["payload"]["candidates"]["flagged_count"] == 0
    assert result["diagnostics"]["runtime"]["job_quality"]["recommendation_eligible"] is True


def test_run_screening_payload_rejects_missing_job_text() -> None:
    payload = {"job": {}, "candidates": []}

    with pytest.raises(ValueError, match="Job payload must include"):
        run_screening_payload(payload)


def test_run_screening_payload_rejects_candidate_without_cv_data() -> None:
    payload = {
        "job": {"job_title": "Backend Java Developer", "requirements": ["Java"]},
        "candidates": [{"application_id": 123, "candidate_name": "No CV"}],
    }

    with pytest.raises(ValueError, match="Candidate payload must include"):
        run_screening_payload(payload)


def test_run_screening_payload_matches_english_jd_with_vietnamese_cv() -> None:
    payload = {
        "job": {
            "job_id": 20,
            "raw_text": (
                "Computer Vision Engineer\n"
                "\n"
                "Requirements\n"
                "- Experience with face recognition and anti-spoofing.\n"
                "- Python"
            ),
        },
        "candidates": [
            {
                "application_id": 555,
                "candidate_name": "Le Van AI",
                "cv_text": (
                    "Le Van AI\n"
                    "AI Engineer\n"
                    "\n"
                    "Kỹ năng\n"
                    "Python\n"
                    "\n"
                    "Dự án\n"
                    "Tên dự án: eKYC Face System\n"
                    "Mô tả:\n"
                    "- Xây dựng hệ thống nhận diện khuôn mặt và chống giả mạo."
                ),
            }
        ],
    }

    result = run_screening_payload(payload)

    assert result["job"]["must_have_skills"] == [
        "Face Recognition",
        "Anti-Spoofing",
        "Python",
    ]
    assert result["job"]["job_role_profile"]["primary_role_family"] == "COMPUTER_VISION_EKYC"
    candidate = result["candidates"][0]
    assert candidate["candidate_name"] == "Le Van AI"
    assert candidate["final_score"] >= 70
    assert candidate["missing_skills"] == []
    assert [
        (match["required_skill"], match["evidence_level"])
        for match in candidate["matched_skills"]
    ] == [
        ("Face Recognition", 3),
        ("Anti-Spoofing", 3),
        ("Python", 1),
    ]


def test_run_screening_payload_applies_role_family_penalty_for_semantic_only_mismatch(
    tmp_path,
) -> None:
    taxonomy_path = tmp_path / "empty_taxonomy.json"
    taxonomy_path.write_text("{}", encoding="utf-8")
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeMultilingualEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_id": 60,
            "job_title": "AI Computer Vision Engineer - eKYC",
            "requirements": [
                "identity verification",
            ],
            "responsibilities": [
                "Design face recognition and liveness detection pipelines.",
            ],
        },
        "candidates": [
            {
                "candidate_name": "Generic ML Candidate",
                "cv_text": (
                    "Generic ML Candidate\n"
                    "Machine Learning Engineer\n"
                    "\n"
                    "Summary:\n"
                    "Built machine learning retrieval pipelines and recommendation models.\n"
                    "\n"
                    "Skills:\n"
                    "- Python\n"
                    "- Machine Learning\n"
                    "- eKYC"
                ),
            }
        ],
    }

    result = run_screening_payload(
        payload,
        taxonomy_path=str(taxonomy_path),
        embedding_matcher=embedding_matcher,
    )

    candidate = result["candidates"][0]
    assert result["job"]["job_role_profile"]["primary_role_family"] == "COMPUTER_VISION_EKYC"
    assert candidate["candidate_role_profile"]["primary_role_family"] == "DATA_AI_ENGINEERING"
    assert candidate["role_family_alignment"]["status"] in {
        "partial_alignment",
        "misaligned",
    }
    assert candidate["base_score"] <= candidate["raw_base_score"]
    assert candidate["role_score_adjustment"] < 0


def test_run_screening_payload_can_use_injected_multilingual_embedding_matcher() -> None:
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeMultilingualEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_id": 30,
            "job_title": "Identity Platform Specialist",
            "requirements": ["identity verification"],
        },
        "candidates": [
            {
                "application_id": 777,
                "candidate_name": "Digital ID Candidate",
                "cv_text": (
                "Digital ID Candidate\n"
                "Identity Engineer\n"
                "\n"
                "Skills:\n"
                "- eKYC"
            ),
        }
    ],
}

    result = run_screening_payload(payload, embedding_matcher=embedding_matcher)

    match = result["candidates"][0]["matched_skills"][0]
    assert match["required_skill"] == "identity verification"
    assert match["candidate_skill"] is None
    assert match["match_type"] == "semantic_only_match"
    assert match["taxonomy_status"] == "unknown"
    assert match["evidence_text"] == "eKYC"
    assert match["evidence_source"] == "skills"
    assert match["similarity"] == 0.9939
    assert match["requirement_source_kind"] == "explicit_requirement"
    assert result["job"]["must_have_skills"] == []
    assert result["job"]["taxonomy_coverage"] == {
        "known_count": 0,
        "unknown_count": 1,
        "coverage_ratio": 0.0,
        "known_requirements": [],
        "unknown_requirements": ["identity verification"],
    }
    assert result["job"]["open_set_requirements"] == ["identity verification"]
    assert result["job"]["open_set_filter_summary"]["kept_count"] == 1
    assert result["job"]["screening_confidence"] == {
        "level": "medium",
        "known_requirement_count": 0,
        "open_set_requirement_count": 1,
        "embedding_enabled": True,
        "warnings": [],
    }


def test_run_screening_payload_open_set_security_role_without_taxonomy(
    tmp_path,
) -> None:
    taxonomy_path = tmp_path / "empty_taxonomy.json"
    taxonomy_path.write_text("{}", encoding="utf-8")
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeSecurityEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_id": 40,
            "job_title": "IT Security & IT Governance Officer",
            "requirements": [
                "Professional requirements: Proficiency in Linux and Qualys.",
                "At least 3 yeear of experience in IT Security Operations, Governance, Compliance, Personal Data Protection.",
                "Knowledge of vulnerability management tools and access control principles.",
                "Relevant certifications: Security+, CEH, ISO 27001 are an advantage.",
            ],
        },
        "candidates": [
            {
                "application_id": 888,
                "candidate_name": "David Chen",
                "cv_text": (
                    "David Chen\n"
                    "Senior IT Security & Governance Officer\n"
                    "\n"
                    "Summary:\n"
                    "IT Security and Governance professional with experience in vulnerability management, access governance, compliance, personal data protection, and Qualys.\n"
                    "\n"
                    "Skills:\n"
                    "- Qualys\n"
                    "- Linux Administration\n"
                    "- Access Management\n"
                    "- Vulnerability Management\n"
                    "- Personal Data Protection\n"
                    "- IT Governance\n"
                    "- Compliance Management\n"
                    "\n"
                    "Work Experience:\n"
                    "Senior IT Security Officer - Global Banking Technology\n"
                    "01/2021 - Present\n"
                    "- Managed enterprise vulnerability management using Qualys.\n"
                    "- Reviewed access requests according to PAM procedures.\n"
                    "- Supported ISO 27001 compliance and regulatory audits.\n"
                    "- Ensured compliance with Personal Data Protection regulations.\n"
                    "\n"
                    "Certifications:\n"
                    "CompTIA Security+\n"
                    "Certified Ethical Hacker (CEH)\n"
                    "ISO 27001 Lead Implementer"
                ),
            }
        ],
    }

    result = run_screening_payload(
        payload,
        taxonomy_path=str(taxonomy_path),
        embedding_matcher=embedding_matcher,
    )

    assert result["job"]["must_have_skills"] == []
    assert "Qualys" in result["job"]["open_set_requirements"]
    assert "vulnerability management" in result["job"]["open_set_requirements"]
    assert "Governance" not in result["job"]["open_set_requirements"]
    assert "Compliance" not in result["job"]["open_set_requirements"]
    assert "Personal Data Protection" not in result["job"]["open_set_requirements"]
    assert "open_set_filter_summary" in result["job"]
    assert result["job"]["screening_confidence"]["level"] == "medium"
    assert result["job"]["domain"] == ["IT Security/GRC"]

    candidate = result["candidates"][0]
    assert candidate["candidate_name"] == "David Chen"
    assert candidate["final_score"] >= 70
    assert candidate["recommendation"] in {"Review", "Strong Review"}
    assert any(
        match["match_type"] == "semantic_only_match"
        for match in candidate["open_set_requirement_matches"]
    )


def test_run_screening_payload_separates_soft_education_and_nice_to_have() -> None:
    payload = {
        "job": {
            "job_id": 50,
            "job_title": "Fullstack Developer",
            "requirements": [
                "Dieu kien bat buoc:",
                "Tot nghiep Dai hoc nganh CNTT.",
                "Thanh thao Java, Spring Boot, Angular, Javascript.",
                "Toi thieu 02 nam kinh nghiem phat trien ung dung.",
                "Kha nang lam viec theo nhom, giao tiep, trinh bay.",
                "Dieu kien uu tien:",
                "Co kinh nghiem su dung Git, GitLab, Docker container.",
            ],
        },
        "candidates": [
            {
                "application_id": 999,
                "candidate_name": "Fullstack Candidate",
                "cv_text": (
                    "Fullstack Candidate\n"
                    "Backend Developer\n"
                    "\n"
                    "Skills:\n"
                    "- Java\n"
                    "- Spring Boot\n"
                    "- Docker\n"
                    "\n"
                    "Work Experience:\n"
                    "Backend Developer - ABC\n"
                    "01/2020 - Present\n"
                    "- Built Java Spring Boot APIs."
                ),
            }
        ],
    }

    result = run_screening_payload(payload)

    groups = result["job"]["requirement_groups"]
    assert groups["education"] == ["Tot nghiep Dai hoc nganh CNTT."]
    assert groups["soft_skills"] == [
        "Kha nang lam viec theo nhom, giao tiep, trinh bay."
    ]
    assert groups["experience"] == [
        "Toi thieu 02 nam kinh nghiem phat trien ung dung."
    ]
    assert groups["nice_to_have_technical"] == [
        "Co kinh nghiem su dung Git, GitLab, Docker container."
    ]

    candidate = result["candidates"][0]
    assert "Tot nghiep Dai hoc nganh CNTT." not in candidate["missing_skills"]
    assert (
        "Kha nang lam viec theo nhom, giao tiep, trinh bay."
        not in candidate["missing_skills"]
    )
    assert "Co kinh nghiem su dung Git" not in " ".join(candidate["missing_skills"])
    assert candidate["review_card"]["requirement_notes"] == [
        "Education requirements should be reviewed separately: Tot nghiep Dai hoc nganh CNTT.",
        "Soft skills should be verified during interview: Kha nang lam viec theo nhom, giao tiep, trinh bay.",
        "Role-family note: The candidate shows adjacent role-family overlap, but not as the primary profile.",
    ]


def test_run_screening_payload_handles_html_jd_from_php_editor(
    tmp_path,
) -> None:
    taxonomy_path = tmp_path / "empty_taxonomy.json"
    taxonomy_path.write_text("{}", encoding="utf-8")
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeSecurityEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_id": 18,
            "job_title": "IT Security & IT Governance Officer",
            "requirements": [
                (
                    "<p><strong>1. Qualifications &amp; Experience</strong></p>"
                    "<p>•&nbsp;<strong>Professional requirements: Proficiency in Linux</strong>, "
                    "Nutanix administration, Commvault, and Qualys; ability to perform "
                    "patch upgrades for both Windows and Linux.</p>"
                    "<p>• At least 3 yeear of experience in "
                    "<strong>IT Security Operations, Governance, Compliance, "
                    "Personal Data Protection</strong>, preferably in banking/finance.</p>"
                    "<p>• Knowledge of vulnerability management tools (e.g., Qualys) "
                    "and access control principles.</p>"
                    "<p>• Relevant certifications: Security+, CEH, ISO 27001 are an advantage.</p>"
                )
            ],
            "responsibilities": [
                (
                    "<p><strong>1. IT Security Operations</strong></p>"
                    "<p>• Manage and monitor Qualys vulnerability scanning platform.</p>"
                    "<p>• Review and approve system access requests based on security matrices.</p>"
                )
            ],
        },
        "candidates": [
            {
                "application_id": 15,
                "candidate_id": 4,
                "candidate_name": "Phan Thanh Kiet",
                "cv_text": (
                    "Phan Thanh Kiet\n"
                    "IT Security & Governance Officer\n"
                    "\n"
                    "Summary:\n"
                    "IT Security and Governance professional with over 5 years of experience "
                    "in security operations, vulnerability management, access governance, "
                    "compliance, personal data protection, and IT risk management. "
                    "Experienced with Qualys and Linux administration.\n"
                    "\n"
                    "Skills:\n"
                    "- Qualys\n"
                    "- Vulnerability Management\n"
                    "- Access Management\n"
                    "- Linux Administration\n"
                    "- Personal Data Protection\n"
                    "- IT Governance\n"
                    "- Compliance Management\n"
                    "\n"
                    "Work Experience:\n"
                    "IT Security Analyst - Asia Financial Services\n"
                    "07/2018 - 12/2020\n"
                    "- Managed user access lifecycle and security audits.\n"
                    "\n"
                    "Senior IT Security & Governance Officer - Global Banking Technology\n"
                    "01/2021 – Hien tai\n"
                    "- Manage enterprise vulnerability management using Qualys.\n"
                    "- Review access requests according to security matrices and PAM procedures.\n"
                    "- Support ISO 27001 compliance and regulatory audits.\n"
                    "- Ensure compliance with Personal Data Protection regulations.\n"
                    "\n"
                    "Certifications:\n"
                    "CompTIA Security+\n"
                    "Certified Ethical Hacker (CEH)\n"
                    "ISO 27001 Lead Implementer"
                ),
            }
        ],
    }

    result = run_screening_payload(
        payload,
        taxonomy_path=str(taxonomy_path),
        embedding_matcher=embedding_matcher,
    )

    assert "Qualys" in result["job"]["open_set_requirements"]
    assert "vulnerability management" in result["job"]["open_set_requirements"]
    assert "Governance" not in result["job"]["open_set_requirements"]
    assert "Compliance" not in result["job"]["open_set_requirements"]
    assert result["job"]["screening_confidence"]["open_set_requirement_count"] > 1
    assert "open_set_filter_summary" in result["job"]

    candidate = result["candidates"][0]
    assert candidate["experience_years"] >= 5
    assert candidate["final_score"] >= 55
    assert candidate["recommendation"] in {"Maybe Review", "Review", "Strong Review"}


def test_run_screening_payload_recovers_context_split_evidence_from_cv() -> None:
    payload = {
        "job": {
            "job_id": 77,
            "job_title": "Computer Vision Engineer",
            "requirements": [
                "Computer Vision",
                "PyTorch",
            ],
        },
        "candidates": [
            {
                "candidate_name": "Tran Van A",
                "cv_text": (
                    "Tran Van A\n"
                    "AI Engineer\n"
                    "\n"
                    "Work Experience\n"
                    "Computer Vision Engineer - Vision Labs\n"
                    "01/2022 - Present\n"
                    "- Built eKYC onboarding and liveness workflows for mobile apps.\n"
                    "\n"
                    "Projects\n"
                    "Project name: Mobile Face SDK\n"
                    "Description:\n"
                    "Optimized face verification pipelines for production deployment.\n"
                    "Technologies:\n"
                    "PyTorch\n"
                    "ONNX\n"
                ),
            }
        ],
    }

    result = run_screening_payload(payload)
    candidate = result["candidates"][0]

    assert candidate["missing_skills"] == []
    assert [
        (match["required_skill"], match["evidence_level"], match["evidence_source"])
        for match in candidate["matched_skills"]
    ] == [
        ("Computer Vision", 3, "work_experience"),
        ("PyTorch", 3, "projects"),
    ]
    assert candidate["scores"]["evidence"] == 1.0
    assert candidate["final_score"] >= 80


def test_run_screening_payload_exposes_responsibility_signal_metadata_without_changing_scoring_input() -> None:
    payload = {
        "job": {
            "job_id": 22,
            "job_title": "IT Staff / IT Support / IT Helpdesk",
            "requirements": [
                "At least 3 years experience working in IT.",
                "Good at writing and speaking English.",
                "Enthusiastic and eager to learn.",
                "Have experience in SAP or program is an advantage.",
            ],
            "responsibilities": [
                "Manage Active Directory and troubleshoot DNS/DHCP issues.",
                "Support firewall, router, switch, VPN, and Google Workspace incidents.",
            ],
        },
        "candidates": [
            {
                "application_id": 1,
                "candidate_name": "Infra Candidate",
                "cv_text": "Infra Candidate\nIT Support Engineer\n\nSkills:\n- Active Directory",
            }
        ],
    }

    result = run_screening_payload(payload)
    job = result["job"]

    assert job["job_role_profile"]["primary_role_family"] == "IT_SUPPORT_INFRA"
    assert job["must_have_skills"] == []
    assert job["explicit_technical_recovery_summary"] == {
        "raw_explicit_technical_count": 0,
        "usable_explicit_technical_count": 0,
        "explicit_technical_contamination_count": 0,
        "usable_explicit_technical_lines": [],
        "contaminated_explicit_technical_lines": [],
        "supported_high_specificity_signal_count": 2,
        "technical_responsibility_candidate_count": 8,
        "recovery_triggered": True,
        "recovery_reason": "sparse_explicit_technical_requirements",
    }
    assert job["open_set_requirements"] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
    ]
    assert job["technical_responsibility_candidates"] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
        "Google Workspace",
        "Router",
        "Switch",
        "VPN",
    ]
    assert len(job["responsibility_signals"]) == 2
    assert [item["text"] for item in job["promoted_requirements"]] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
    ]
    assert job["requirement_provenance_summary"] == [
        {
            "text": "Active Directory",
            "requirement_source_kind": "promoted_responsibility",
            "requirement_source_text": "Active Directory",
            "requirement_priority": "must_have",
            "taxonomy_status": "unknown",
        },
        {
            "text": "DNS",
            "requirement_source_kind": "promoted_responsibility",
            "requirement_source_text": "DNS",
            "requirement_priority": "must_have",
            "taxonomy_status": "unknown",
        },
        {
            "text": "DHCP",
            "requirement_source_kind": "promoted_responsibility",
            "requirement_source_text": "DHCP",
            "requirement_priority": "must_have",
            "taxonomy_status": "unknown",
        },
        {
            "text": "Firewall",
            "requirement_source_kind": "promoted_responsibility",
            "requirement_source_text": "Firewall",
            "requirement_priority": "must_have",
            "taxonomy_status": "unknown",
        },
    ]
    assert all(
        signal["signal_type"] == "TECHNICAL_TASK"
        for signal in job["responsibility_signals"]
    )

    candidate = result["candidates"][0]
    lexical_match = next(
        match
        for match in candidate["open_set_requirement_matches"]
        if match["required_skill"] == "Active Directory"
    )
    assert lexical_match["candidate_skill"] == "Active Directory"
    assert lexical_match["match_type"] == "lexical_evidence_match"
    assert lexical_match["taxonomy_status"] == "unknown"
    assert lexical_match["score"] == 0.65
    assert lexical_match["similarity"] == 1.0
    assert lexical_match["evidence_level"] == 1
    assert lexical_match["evidence_text"] == "Active Directory"
    assert lexical_match["evidence_source"] == "skills"
    assert lexical_match["intent_type"] == "INFRA_IDENTITY_ADMIN"
    assert lexical_match["intent_strength"] == "core"
    assert lexical_match["intent_reason"] == "infra_identity_admin_signal"
    assert lexical_match["role_family"] == "IT_SUPPORT_INFRA"
    assert lexical_match["requirement_source_kind"] == "promoted_responsibility"
    assert lexical_match["requirement_source_text"] == "Active Directory"
    assert lexical_match["requirement_priority"] == "must_have"


def _demo_screening_payload() -> dict:
    return {
        "job": {
            "job_id": 10,
            "job_title": "Backend Java Developer",
            "requirements": [
                "Java",
                "Spring Boot",
                "REST API",
                "SQL",
                "Basic Docker",
                "1+ year backend experience",
            ],
            "nice_to_have": ["AWS", "Kafka", "Kubernetes"],
            "responsibilities": [
                "Develop backend services.",
                "Build RESTful APIs.",
                "Work with relational databases.",
            ],
        },
        "candidates": [
            {
                "application_id": 123,
                "candidate_id": 456,
                "candidate_name": "Nguyen Van A",
                "email": "candidate@example.com",
                "cv_text": (
                    "Nguyen Van A\n"
                    "Backend Developer\n"
                    "\n"
                    "Summary:\n"
                    "Backend developer with experience building Java Spring Boot services and REST APIs.\n"
                    "\n"
                    "Skills:\n"
                    "- Java\n"
                    "- Spring Boot\n"
                    "- REST API\n"
                    "- MySQL\n"
                    "- Docker\n"
                    "\n"
                    "Work Experience:\n"
                    "Backend Developer Intern - ABC Tech\n"
                    "06/2024 - 12/2024\n"
                    "- Built REST APIs using Java and Spring Boot.\n"
                    "- Designed MySQL database schemas for product and order modules.\n"
                    "- Used Docker Compose for local development and testing.\n"
                    "\n"
                    "Projects:\n"
                    "E-commerce API\n"
                    "- Developed authentication and order management modules.\n"
                    "- Implemented JWT login for backend services.\n"
                    "- Created RESTful APIs with Spring Boot and MySQL.\n"
                    "\n"
                    "Education:\n"
                    "Bachelor of Software Engineering"
                ),
            }
        ],
    }
