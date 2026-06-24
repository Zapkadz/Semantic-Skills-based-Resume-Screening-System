import json
from pathlib import Path

from src.payload_pipeline import run_screening_payload
from src.screening_pipeline import run_screening_pipeline


FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "core_logic_benchmark"


def test_cli_and_payload_pipelines_match_for_backend_strong_case(tmp_path: Path) -> None:
    jd_path = FIXTURE_ROOT / "jds" / "backend_java_strong.txt"
    cv_fixture_path = FIXTURE_ROOT / "cvs" / "backend_java_strong.txt"
    cv_dir = tmp_path / "cvs"
    cv_dir.mkdir()
    copied_cv_path = cv_dir / cv_fixture_path.name
    copied_cv_path.write_text(cv_fixture_path.read_text(encoding="utf-8"), encoding="utf-8")

    cli_result = run_screening_pipeline(jd_path, cv_dir)
    payload_result = run_screening_payload(_load_json("payloads/screening_backend_strong.json"))

    cli_candidate = cli_result["candidates"][0]
    payload_candidate = payload_result["candidates"][0]

    assert cli_result["job"]["must_have_skills"] == payload_result["job"]["must_have_skills"]
    assert cli_result["job"]["taxonomy_coverage"] == payload_result["job"]["taxonomy_coverage"]
    assert cli_candidate["candidate_name"] == payload_candidate["candidate_name"]
    assert cli_candidate["final_score"] == payload_candidate["final_score"]
    assert cli_candidate["recommendation"] == payload_candidate["recommendation"]
    assert cli_candidate["missing_skills"] == payload_candidate["missing_skills"]


def test_cli_and_payload_pipelines_keep_same_cross_lingual_skills(tmp_path: Path) -> None:
    jd_path = FIXTURE_ROOT / "jds" / "computer_vision_en.txt"
    cv_fixture_path = FIXTURE_ROOT / "cvs" / "computer_vision_vi.txt"
    cv_dir = tmp_path / "cvs"
    cv_dir.mkdir()
    copied_cv_path = cv_dir / cv_fixture_path.name
    copied_cv_path.write_text(cv_fixture_path.read_text(encoding="utf-8"), encoding="utf-8")

    cli_result = run_screening_pipeline(jd_path, cv_dir)
    payload_result = run_screening_payload(
        {
            "job": {"raw_text": jd_path.read_text(encoding="utf-8")},
            "candidates": [
                {
                    "candidate_name": "Le Van AI",
                    "cv_text": cv_fixture_path.read_text(encoding="utf-8"),
                }
            ],
        }
    )

    assert cli_result["job"]["must_have_skills"] == payload_result["job"]["must_have_skills"]
    assert cli_result["candidates"][0]["final_score"] == payload_result["candidates"][0]["final_score"]
    assert cli_result["candidates"][0]["missing_skills"] == payload_result["candidates"][0]["missing_skills"]


def _load_json(relative_path: str) -> dict:
    return json.loads((FIXTURE_ROOT / relative_path).read_text(encoding="utf-8"))
