import json
from pathlib import Path

from src.embedding_matcher import SemanticEmbeddingMatcher
from src.taxonomy_suggestion import (
    build_taxonomy_suggestions,
    collect_unknown_requirement_observations,
    load_screening_results,
    load_taxonomy_suggestions,
    save_taxonomy_suggestions,
)
from taxonomy_suggest import main as taxonomy_suggest_main


class FakeSuggestionEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "carbon footprint analysis": [1.0, 0.0, 0.0],
            "CO2 emission reporting": [0.95, 0.05, 0.0],
            "Carbon Footprint Analysis": [1.0, 0.0, 0.0],
            "Data Analysis": [0.80, 0.20, 0.0],
            "Python": [0.0, 1.0, 0.0],
            "Machine Learning": [0.0, 0.0, 1.0],
        }
        return [vectors[text] for text in texts]


def test_collect_unknown_requirement_observations_merges_candidate_evidence() -> None:
    observations = collect_unknown_requirement_observations(_screening_result())

    assert observations == [
        {
            "phrase": "carbon footprint analysis",
            "job_id": 10,
            "job_title": "ESG Analyst",
            "source": "job.taxonomy_coverage.unknown_requirements",
            "context": "carbon footprint analysis",
            "matched_evidence_text": "Built carbon emission reports for ESG audits.",
            "similarity": 0.8421,
        },
        {
            "phrase": "ESG reporting",
            "job_id": 10,
            "job_title": "ESG Analyst",
            "source": "job.taxonomy_coverage.unknown_requirements",
            "context": "ESG reporting",
            "matched_evidence_text": "",
            "similarity": None,
        },
    ]


def test_build_taxonomy_suggestions_requires_minimum_frequency() -> None:
    observations = [
        _observation("carbon footprint analysis", job_id=1),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        min_frequency=2,
    )

    assert suggestions == []


def test_build_taxonomy_suggestions_creates_pending_suggestion() -> None:
    observations = [
        _observation(
            "carbon footprint analysis",
            job_id=1,
            evidence="Built carbon emission reports for ESG audits.",
        ),
        _observation("carbon footprint analysis", job_id=2),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        min_frequency=2,
    )

    assert suggestions == [
        {
            "suggestion_id": "tax-sug-carbon-footprint-analysis",
            "suggested_canonical_name": "Carbon Footprint Analysis",
            "suggested_category": "Pending Classification",
            "suggested_aliases": ["carbon footprint analysis"],
            "frequency": 2,
            "confidence": 0.7,
            "nearest_existing_skills": [],
            "example_contexts": ["carbon footprint analysis"],
            "example_evidence": ["Built carbon emission reports for ESG audits."],
            "status": "pending_review",
        }
    ]


def test_build_taxonomy_suggestions_groups_embedding_similar_phrases() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeSuggestionEmbeddingModel())
    observations = [
        _observation("carbon footprint analysis", job_id=1),
        _observation("CO2 emission reporting", job_id=2),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        embedding_matcher=matcher,
        min_frequency=2,
    )

    assert len(suggestions) == 1
    suggestion = suggestions[0]
    assert suggestion["suggested_aliases"] == [
        "carbon footprint analysis",
        "CO2 emission reporting",
    ]
    assert suggestion["nearest_existing_skills"] == [
        {"skill": "Data Analysis", "similarity": 0.9701},
        {"skill": "Python", "similarity": 0.0},
        {"skill": "Machine Learning", "similarity": 0.0},
    ]
    assert suggestion["suggested_category"] == "Analytics"


def test_save_and_load_taxonomy_suggestions_round_trip(tmp_path: Path) -> None:
    output_path = tmp_path / "taxonomy_suggestions.json"
    suggestions = [
        {
            "suggestion_id": "tax-sug-carbon-footprint-analysis",
            "suggested_canonical_name": "Carbon Footprint Analysis",
        }
    ]

    saved_path = save_taxonomy_suggestions(suggestions, output_path)
    loaded_suggestions = load_taxonomy_suggestions(output_path)

    assert saved_path == str(output_path)
    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "version": 1,
        "suggestions": suggestions,
    }
    assert loaded_suggestions == suggestions


def test_load_screening_results_accepts_single_result_and_results_wrapper(
    tmp_path: Path,
) -> None:
    single_path = tmp_path / "single.json"
    wrapper_path = tmp_path / "wrapper.json"
    single_path.write_text(json.dumps(_screening_result()), encoding="utf-8")
    wrapper_path.write_text(
        json.dumps({"results": [_screening_result()]}),
        encoding="utf-8",
    )

    assert load_screening_results(single_path) == [_screening_result()]
    assert load_screening_results(wrapper_path) == [_screening_result()]


def test_taxonomy_suggest_cli_writes_suggestion_queue(tmp_path: Path, capsys) -> None:
    input_path = tmp_path / "ranking_results.json"
    taxonomy_path = tmp_path / "skills.json"
    output_path = tmp_path / "taxonomy_suggestions.json"
    input_path.write_text(
        json.dumps(
            {
                "results": [
                    _screening_result(job_id=1),
                    _screening_result(job_id=2),
                ]
            }
        ),
        encoding="utf-8",
    )
    taxonomy_path.write_text(json.dumps(_taxonomy()), encoding="utf-8")

    exit_code = taxonomy_suggest_main(
        [
            "--input-json",
            str(input_path),
            "--output-json",
            str(output_path),
            "--taxonomy",
            str(taxonomy_path),
            "--min-frequency",
            "2",
        ]
    )

    captured = capsys.readouterr()
    output_payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert "Suggestions: 2" in captured.out
    assert output_payload["version"] == 1
    assert [
        suggestion["suggested_canonical_name"]
        for suggestion in output_payload["suggestions"]
    ] == ["Carbon Footprint Analysis", "ESG Reporting"]


def _screening_result(job_id: int = 10) -> dict:
    return {
        "job": {
            "job_id": job_id,
            "title": "ESG Analyst",
            "taxonomy_coverage": {
                "known_count": 1,
                "unknown_count": 2,
                "coverage_ratio": 0.3333,
                "known_requirements": ["Data Analysis"],
                "unknown_requirements": [
                    "carbon footprint analysis",
                    "ESG reporting",
                ],
            },
        },
        "candidates": [
            {
                "candidate_name": "Green Candidate",
                "open_set_requirement_matches": [
                    {
                        "required_skill": "carbon footprint analysis",
                        "match_type": "semantic_only_match",
                        "taxonomy_status": "unknown",
                        "similarity": 0.8421,
                        "evidence_text": "Built carbon emission reports for ESG audits.",
                    }
                ],
            }
        ],
    }


def _observation(
    phrase: str,
    job_id: int,
    evidence: str = "",
) -> dict:
    return {
        "phrase": phrase,
        "job_id": job_id,
        "job_title": "ESG Analyst",
        "source": "job.taxonomy_coverage.unknown_requirements",
        "context": phrase,
        "matched_evidence_text": evidence,
        "similarity": None,
    }


def _taxonomy() -> dict:
    return {
        "Data Analysis": {
            "aliases": ["data analysis"],
            "category": "Analytics",
            "related": [],
            "transferable": [],
        },
        "Python": {
            "aliases": ["python"],
            "category": "Programming Language",
            "related": [],
            "transferable": [],
        },
        "Machine Learning": {
            "aliases": ["machine learning"],
            "category": "AI/Machine Learning",
            "related": [],
            "transferable": [],
        },
    }
