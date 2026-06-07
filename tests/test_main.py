import json
from pathlib import Path

from main import build_parser, main


def test_build_parser_parses_pipeline_arguments() -> None:
    parser = build_parser()

    args = parser.parse_args(
        [
            "--jd",
            "data/jobs/jd_backend_java.txt",
            "--cv-dir",
            "data/cvs",
            "--taxonomy",
            "data/taxonomy/skills.json",
            "--output-json",
            "outputs/ranking_results.json",
            "--output-dir",
            "outputs/reports",
            "--show-review-cards",
        ]
    )

    assert args.jd == "data/jobs/jd_backend_java.txt"
    assert args.cv_dir == "data/cvs"
    assert args.taxonomy == "data/taxonomy/skills.json"
    assert args.output_json == "outputs/ranking_results.json"
    assert args.output_dir == "outputs/reports"
    assert args.show_review_cards is True


def test_main_runs_pipeline_and_writes_requested_outputs(
    tmp_path: Path,
    capsys,
) -> None:
    output_json = tmp_path / "ranking_results.json"
    output_dir = tmp_path / "reports"

    exit_code = main(
        [
            "--jd",
            "data/jobs/jd_backend_java.txt",
            "--cv-dir",
            "data/cvs",
            "--output-json",
            str(output_json),
            "--output-dir",
            str(output_dir),
            "--show-review-cards",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Job: Backend Java Developer" in captured.out
    assert "1. Nguyen Van A - 87/100 - Strong Review" in captured.out
    assert "Saved JSON:" in captured.out
    assert "Saved review cards: 1 file(s)" in captured.out
    assert "# Nguyen Van A" in captured.out

    saved_result = json.loads(output_json.read_text(encoding="utf-8"))
    assert saved_result["candidates"][0]["candidate_name"] == "Nguyen Van A"

    saved_card = output_dir / "rank-01-nguyen-van-a.md"
    assert saved_card.exists()
    assert "Recommendation: Strong Review" in saved_card.read_text(encoding="utf-8")
