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
            "Py torch": [0.0, 0.99, 0.01],
            "Py Torch": [0.0, 0.99, 0.01],
            "PyTorch": [0.0, 1.0, 0.0],
            "face anti spoofing": [0.05, 0.20, 0.97],
            "Face Anti Spoofing": [0.05, 0.20, 0.97],
            "model optimization": [0.20, 0.95, 0.10],
            "Model Optimization": [0.20, 0.95, 0.10],
            "Liveness Detection": [0.04, 0.22, 0.97],
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
            "job_role_family": "DATA_AI_ENGINEERING",
            "job_role_family_confidence": 0.81,
            "intent_type": "METHOD_CAPABILITY",
            "intent_strength": "supporting",
            "technical_candidate_status": "kept",
            "technical_confidence": 0.88,
            "keep_for_suggestion": True,
        },
        {
            "phrase": "ESG reporting",
            "job_id": 10,
            "job_title": "ESG Analyst",
            "source": "job.taxonomy_coverage.unknown_requirements",
            "context": "ESG reporting",
            "matched_evidence_text": "",
            "similarity": None,
            "job_role_family": "DATA_AI_ENGINEERING",
            "job_role_family_confidence": 0.81,
            "intent_type": "GENERIC_TECHNICAL",
            "intent_strength": "contextual",
            "technical_candidate_status": "discarded",
            "technical_confidence": 0.15,
            "keep_for_suggestion": False,
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
            role_family="DATA_AI_ENGINEERING",
            intent_type="METHOD_CAPABILITY",
            intent_strength="supporting",
            technical_confidence=0.88,
        ),
        _observation(
            "carbon footprint analysis",
            job_id=2,
            role_family="DATA_AI_ENGINEERING",
            intent_type="METHOD_CAPABILITY",
            intent_strength="supporting",
            technical_confidence=0.88,
        ),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        min_frequency=2,
    )

    assert len(suggestions) == 1
    suggestion = suggestions[0]
    assert suggestion["suggestion_id"] == "tax-sug-carbon-footprint-analysis"
    assert suggestion["suggested_canonical_name"] == "Carbon Footprint Analysis"
    assert suggestion["suggested_category"] == "Pending Classification"
    assert suggestion["suggested_aliases"] == ["carbon footprint analysis"]
    assert suggestion["frequency"] == 2
    assert suggestion["confidence"] == 0.82
    assert suggestion["nearest_existing_skills"] == []
    assert suggestion["example_contexts"] == ["carbon footprint analysis"]
    assert suggestion["example_evidence"] == [
        "Built carbon emission reports for ESG audits."
    ]
    assert suggestion["role_family_distribution"] == {"DATA_AI_ENGINEERING": 2}
    assert suggestion["dominant_role_family"] == "DATA_AI_ENGINEERING"
    assert suggestion["dominant_role_family_ratio"] == 1.0
    assert suggestion["intent_distribution"] == {"supporting": 2}
    assert suggestion["dominant_intent_strength"] == "supporting"
    assert suggestion["evidence_support_count"] == 1
    assert suggestion["alias_candidate"] is None
    assert suggestion["governance_priority"] == "high"
    assert suggestion["governance_priority_score"] == 0.838
    assert suggestion["review_reason"] == (
        "Observed 2 time(s). 100% from DATA_AI_ENGINEERING. "
        "supporting technical intent. 1 evidence-backed observation(s)."
    )
    assert suggestion["status"] == "pending_review"


def test_build_taxonomy_suggestions_groups_embedding_similar_phrases() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeSuggestionEmbeddingModel())
    observations = [
        _observation(
            "carbon footprint analysis",
            job_id=1,
            role_family="DATA_AI_ENGINEERING",
            intent_type="METHOD_CAPABILITY",
            intent_strength="supporting",
            technical_confidence=0.88,
        ),
        _observation(
            "CO2 emission reporting",
            job_id=2,
            role_family="DATA_AI_ENGINEERING",
            intent_type="METHOD_CAPABILITY",
            intent_strength="supporting",
            technical_confidence=0.88,
        ),
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
    assert suggestion["nearest_existing_skills"][0] == {
        "skill": "Data Analysis",
        "similarity": 0.9701,
    }
    assert suggestion["suggested_category"] == "Analytics"
    assert suggestion["alias_candidate"] is None
    assert suggestion["governance_priority"] == "high"


def test_build_taxonomy_suggestions_marks_likely_alias_candidates() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeSuggestionEmbeddingModel())
    observations = [
        _observation(
            "Py torch",
            job_id=1,
            role_family="DATA_AI_ENGINEERING",
            intent_type="TOOLING_PLATFORM",
            intent_strength="supporting",
            technical_confidence=0.95,
        ),
        _observation(
            "Py torch",
            job_id=2,
            evidence="Built model training pipelines with Py torch.",
            role_family="DATA_AI_ENGINEERING",
            intent_type="TOOLING_PLATFORM",
            intent_strength="supporting",
            technical_confidence=0.95,
        ),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        embedding_matcher=matcher,
        min_frequency=2,
    )

    suggestion = suggestions[0]
    assert suggestion["alias_candidate"] == {
        "status": "likely_alias",
        "target_skill": "PyTorch",
        "similarity": 0.9999,
    }
    assert suggestion["suggested_category"] == "Deep Learning"
    assert suggestion["governance_priority"] == "high"
    assert "likely alias of PyTorch" in suggestion["review_reason"]


def test_build_taxonomy_suggestions_prioritizes_role_concentrated_core_items() -> None:
    matcher = SemanticEmbeddingMatcher(model=FakeSuggestionEmbeddingModel())
    observations = [
        _observation(
            "model optimization",
            job_id=1,
            role_family="GENERIC_TECH",
            intent_type="GENERIC_TECHNICAL",
            intent_strength="contextual",
            technical_confidence=0.66,
        ),
        _observation(
            "model optimization",
            job_id=2,
            role_family="GENERIC_TECH",
            intent_type="GENERIC_TECHNICAL",
            intent_strength="contextual",
            technical_confidence=0.66,
        ),
        _observation(
            "face anti spoofing",
            job_id=3,
            evidence="Built anti-spoofing checks for eKYC face verification.",
            role_family="COMPUTER_VISION_EKYC",
            intent_type="MODEL_TECHNIQUE",
            intent_strength="core",
            technical_confidence=0.88,
        ),
        _observation(
            "face anti spoofing",
            job_id=4,
            role_family="COMPUTER_VISION_EKYC",
            intent_type="MODEL_TECHNIQUE",
            intent_strength="core",
            technical_confidence=0.88,
        ),
    ]

    suggestions = build_taxonomy_suggestions(
        observations,
        _taxonomy(),
        embedding_matcher=matcher,
        min_frequency=2,
    )

    assert [suggestion["suggested_canonical_name"] for suggestion in suggestions] == [
        "Face Anti Spoofing",
        "Model Optimization",
    ]
    assert (
        suggestions[0]["governance_priority_score"]
        > suggestions[1]["governance_priority_score"]
    )
    assert suggestions[0]["dominant_role_family"] == "COMPUTER_VISION_EKYC"
    assert suggestions[1]["dominant_intent_strength"] == "contextual"


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
        "version": 2,
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
    assert "Suggestions: 1" in captured.out
    assert output_payload["version"] == 2
    assert [
        suggestion["suggested_canonical_name"]
        for suggestion in output_payload["suggestions"]
    ] == ["Carbon Footprint Analysis"]


def _screening_result(job_id: int = 10) -> dict:
    return {
        "job": {
            "job_id": job_id,
            "title": "ESG Analyst",
            "job_role_profile": {
                "primary_role_family": "DATA_AI_ENGINEERING",
                "confidence": 0.81,
            },
            "requirement_intent_summary": [
                {
                    "text": "carbon footprint analysis",
                    "taxonomy_status": "unknown",
                    "role_family": "DATA_AI_ENGINEERING",
                    "intent_type": "METHOD_CAPABILITY",
                    "intent_strength": "supporting",
                },
                {
                    "text": "ESG reporting",
                    "taxonomy_status": "unknown",
                    "role_family": "DATA_AI_ENGINEERING",
                    "intent_type": "GENERIC_TECHNICAL",
                    "intent_strength": "contextual",
                },
            ],
            "open_set_candidates": [
                {
                    "text": "carbon footprint analysis",
                    "canonical_text": "carbon footprint analysis",
                    "normalized_text": "carbon footprint analysis",
                    "status": "kept",
                    "reason": "technical_capability_phrase",
                    "technical_confidence": 0.88,
                    "keep_for_matching": True,
                    "keep_for_suggestion": True,
                },
                {
                    "text": "ESG reporting",
                    "canonical_text": "ESG reporting",
                    "normalized_text": "esg reporting",
                    "status": "discarded",
                    "reason": "domain_context_only",
                    "technical_confidence": 0.15,
                    "keep_for_matching": False,
                    "keep_for_suggestion": False,
                },
            ],
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
    role_family: str = "",
    intent_type: str = "",
    intent_strength: str = "",
    technical_confidence: float | None = None,
    keep_for_suggestion: bool = True,
) -> dict:
    return {
        "phrase": phrase,
        "job_id": job_id,
        "job_title": "ESG Analyst",
        "source": "job.taxonomy_coverage.unknown_requirements",
        "context": phrase,
        "matched_evidence_text": evidence,
        "similarity": None,
        "job_role_family": role_family,
        "job_role_family_confidence": None,
        "intent_type": intent_type,
        "intent_strength": intent_strength,
        "technical_candidate_status": "kept" if keep_for_suggestion else "discarded",
        "technical_confidence": technical_confidence,
        "keep_for_suggestion": keep_for_suggestion,
    }


def _taxonomy() -> dict:
    return {
        "Data Analysis": {
            "aliases": ["data analysis"],
            "category": "Analytics",
            "related": [],
            "transferable": [],
        },
        "PyTorch": {
            "aliases": ["py torch"],
            "category": "Deep Learning",
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
        "Liveness Detection": {
            "aliases": ["liveness detection"],
            "category": "Computer Vision",
            "related": [],
            "transferable": [],
        },
    }
