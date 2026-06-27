import json
from pathlib import Path

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.job_recommendation_pipeline import run_job_recommendation_payload
from src.payload_pipeline import run_screening_payload


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "core_logic_benchmark"
MANIFEST_PATH = FIXTURE_ROOT / "manifests" / "core_logic_cases.json"


class FakeMultilingualEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "identity verification": [1.0, 0.0],
            "digital identity verification": [0.96, 0.04],
            "eKYC": [0.90, 0.10],
            "Identity Engineer": [0.0, 1.0],
        }
        return [vectors.get(text, [0.0, 1.0]) for text in texts]


def test_core_logic_benchmark_manifest_references_real_fixture_files() -> None:
    manifest = _load_manifest()

    assert manifest["version"] == 1
    assert manifest["cases"]

    for case in manifest["cases"]:
        if case.get("jd_file"):
            assert (FIXTURE_ROOT / case["jd_file"]).is_file()
        for cv_file in case.get("cv_files", []):
            assert (FIXTURE_ROOT / cv_file).is_file()
        if case.get("payload_file"):
            assert (FIXTURE_ROOT / case["payload_file"]).is_file()


def test_core_logic_benchmark_backend_strong_case() -> None:
    case = _case("screening_backend_strong")

    result = run_screening_payload(_screening_payload_from_case(case))

    candidate = result["candidates"][0]
    expected = case["expected"]

    assert candidate["final_score"] >= expected["min_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    assert candidate["missing_skills"] == expected["missing_skills"]
    assert result["job"]["must_have_skills"] == [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL",
        "Docker",
    ]
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_evidence_only_cv_still_scores_as_real_fit() -> None:
    case = _case("screening_backend_evidence_without_skills_section")

    result = run_screening_payload(_screening_payload_from_case(case))

    candidate = result["candidates"][0]
    expected = case["expected"]

    assert candidate["final_score"] >= expected["min_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    assert candidate["missing_skills"] == expected["missing_skills"]
    assert candidate["scores"]["evidence"] >= 0.9
    assert candidate["scores"]["skill_semantic"] == 1.0
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_hard_skill_deficit_is_not_overrated() -> None:
    case = _case("screening_backend_hard_skill_deficit")

    result = run_screening_payload(_screening_payload_from_case(case))

    candidate = result["candidates"][0]
    expected = case["expected"]

    assert candidate["final_score"] <= expected["max_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    for skill in expected["missing_skills_contains"]:
        assert skill in candidate["missing_skills"]
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_cross_lingual_case_keeps_semantic_signal() -> None:
    case = _case("screening_cross_lingual_cv")

    result = run_screening_payload(_screening_payload_from_case(case))

    candidate = result["candidates"][0]
    expected = case["expected"]

    assert result["job"]["must_have_skills"] == expected["required_skills"]
    assert candidate["final_score"] >= expected["min_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    assert candidate["missing_skills"] == []
    assert [
        (match["required_skill"], match["evidence_level"])
        for match in candidate["matched_skills"]
    ] == [
        ("Face Recognition", 3),
        ("Anti-Spoofing", 3),
        ("Python", 1),
    ]
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_placeholder_jobs_are_excluded_from_recommendation() -> None:
    case = _case("recommendation_placeholder_jobs_excluded")
    payload = _load_json(case["payload_file"])

    result = run_job_recommendation_payload(payload)
    expected = case["expected"]

    assert result["job_quality_stats"]["eligible_jobs"] == expected["eligible_jobs"]
    assert len(result["excluded_jobs"]) >= expected["excluded_jobs_min"]
    assert result["top_jobs"][0]["job_id"] == expected["top_job_id"]
    assert result["top_jobs"][0]["fit_label"] == expected["top_job_fit_label"]
    assert (
        result["top_jobs"][0]["decision_confidence"]["level"]
        == expected["top_job_decision_confidence_level"]
    )
    assert (
        result["top_jobs"][0]["job_confidence_guardrails"]["level"]
        == expected["top_job_guardrail_level"]
    )
    _assert_codes_include(
        result["top_jobs"][0]["decision_confidence"]["reason_codes"],
        expected["top_job_decision_reason_codes_contains"],
    )
    _assert_codes_include(
        result["top_jobs"][0]["job_confidence_guardrails"]["reason_codes"],
        expected["top_job_guardrail_reason_codes_contains"],
    )
    assert (
        result["diagnostics"]["runtime"]["top_job_decision_confidence_levels"]
        == expected["diagnostic_top_job_decision_confidence_levels"]
    )
    assert (
        result["diagnostics"]["runtime"]["top_job_guardrail_levels"]
        == expected["diagnostic_top_job_guardrail_levels"]
    )
    assert any("excluded" in warning.casefold() for warning in result["warnings"])


def test_core_logic_benchmark_soft_requirements_do_not_pollute_missing_skills() -> None:
    payload = {
        "job": {
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
    candidate = result["candidates"][0]

    assert groups["education"] == ["Tot nghiep Dai hoc nganh CNTT."]
    assert groups["soft_skills"] == [
        "Kha nang lam viec theo nhom, giao tiep, trinh bay."
    ]
    assert "Tot nghiep Dai hoc nganh CNTT." not in candidate["missing_skills"]
    assert (
        "Kha nang lam viec theo nhom, giao tiep, trinh bay."
        not in candidate["missing_skills"]
    )


def test_core_logic_benchmark_open_set_technical_requirement_is_preserved() -> None:
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeMultilingualEmbeddingModel(),
        threshold=0.70,
    )
    payload = {
        "job": {
            "job_title": "Identity Platform Specialist",
            "requirements": ["identity verification"],
        },
        "candidates": [
            {
                "candidate_name": "Digital ID Candidate",
                "cv_text": (
                    "Digital ID Candidate\n"
                    "Identity Engineer\n"
                    "\n"
                    "Skills:\n"
                    "- digital identity verification"
                ),
            }
        ],
    }

    result = run_screening_payload(payload, embedding_matcher=embedding_matcher)

    assert result["job"]["must_have_skills"] == []
    assert result["job"]["open_set_requirements"] == ["identity verification"]
    assert result["job"]["open_set_filter_summary"]["kept_count"] == 1
    assert result["job"]["taxonomy_coverage"]["unknown_count"] == 1

    match = result["candidates"][0]["matched_skills"][0]
    assert match["candidate_skill"] == "identity verification"
    assert match["match_type"] == "lexical_evidence_match"
    assert match["taxonomy_status"] == "unknown"
    assert match["evidence_text"] == "digital identity verification"


def test_core_logic_benchmark_sparse_infra_recovery_case_sets_guardrails() -> None:
    case = _case("screening_sparse_infra_recovery")

    result = run_screening_payload(_screening_payload_from_case(case))
    candidate = result["candidates"][0]
    expected = case["expected"]

    assert candidate["final_score"] <= expected["max_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    assert result["job"]["open_set_requirements"] == expected["open_set_requirements"]
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_open_set_identity_requirement_keeps_low_confidence_review() -> None:
    case = _case("screening_open_set_identity_requirement")
    embedding_matcher = SemanticEmbeddingMatcher(
        model=FakeMultilingualEmbeddingModel(),
        threshold=0.70,
    )

    result = run_screening_payload(
        _screening_payload_from_case(case),
        embedding_matcher=embedding_matcher,
    )
    candidate = result["candidates"][0]
    expected = case["expected"]

    assert candidate["final_score"] >= expected["min_final_score"]
    assert candidate["final_score"] <= expected["max_final_score"]
    assert candidate["recommendation"] == expected["recommendation"]
    assert result["job"]["open_set_requirements"] == expected["open_set_requirements"]
    _assert_screening_confidence_expectations(result, expected)


def test_core_logic_benchmark_context_split_evidence_is_recovered() -> None:
    payload = {
        "job": {
            "job_title": "Computer Vision Engineer",
            "requirements": ["Computer Vision", "PyTorch"],
        },
        "candidates": [
            {
                "candidate_name": "Context Candidate",
                "cv_text": (
                    "Context Candidate\n"
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


def test_core_logic_benchmark_responsibility_signal_foundation_is_exposed() -> None:
    payload = {
        "job": {
            "job_title": "IT Staff / IT Support / IT Helpdesk",
            "requirements": [
                "At least 3 years experience working in IT.",
                "Good at writing and speaking English.",
            ],
            "responsibilities": [
                "Manage Active Directory and troubleshoot DNS/DHCP issues.",
                "Support firewall, router, switch, VPN, and Google Workspace incidents.",
            ],
        },
        "candidates": [
            {
                "candidate_name": "Infra Candidate",
                "cv_text": "Infra Candidate\nIT Support Engineer\n\nSkills:\n- Active Directory",
            }
        ],
    }

    result = run_screening_payload(payload)

    assert result["job"]["must_have_skills"] == []
    assert result["job"]["open_set_requirements"] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
    ]
    assert result["job"]["technical_responsibility_candidates"] == [
        "Active Directory",
        "DNS",
        "DHCP",
        "Firewall",
        "Google Workspace",
        "Router",
        "Switch",
        "VPN",
    ]
    assert all(
        signal["signal_type"] == "TECHNICAL_TASK"
        for signal in result["job"]["responsibility_signals"]
    )


def _case(case_id: str) -> dict:
    manifest = _load_manifest()
    for case in manifest["cases"]:
        if case["case_id"] == case_id:
            return case

    raise KeyError(f"Unknown benchmark case: {case_id}")


def _load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _load_text(relative_path: str) -> str:
    return (FIXTURE_ROOT / relative_path).read_text(encoding="utf-8")


def _load_json(relative_path: str) -> dict:
    return json.loads((FIXTURE_ROOT / relative_path).read_text(encoding="utf-8"))


def _screening_payload_from_case(case: dict) -> dict:
    if case.get("payload_file"):
        return _load_json(case["payload_file"])

    return {
        "job": {
            "raw_text": _load_text(case["jd_file"]),
        },
        "candidates": [
            {
                "candidate_name": Path(cv_file).stem.replace("_", " "),
                "cv_text": _load_text(cv_file),
            }
            for cv_file in case["cv_files"]
        ],
    }


def _assert_screening_confidence_expectations(
    result: dict,
    expected: dict,
) -> None:
    job_guardrails = result["job"]["confidence_guardrails"]
    decision_confidence = result["candidates"][0]["decision_confidence"]

    assert job_guardrails["level"] == expected["job_confidence_level"]
    assert decision_confidence["level"] == expected["decision_confidence_level"]

    if "job_reason_codes_contains" in expected:
        _assert_codes_include(
            job_guardrails["reason_codes"],
            expected["job_reason_codes_contains"],
        )

    if "decision_reason_codes" in expected:
        assert decision_confidence["reason_codes"] == expected["decision_reason_codes"]

    if "decision_reason_codes_contains" in expected:
        _assert_codes_include(
            decision_confidence["reason_codes"],
            expected["decision_reason_codes_contains"],
        )


def _assert_codes_include(actual_codes: list[str], expected_codes: list[str]) -> None:
    for code in expected_codes:
        assert code in actual_codes
