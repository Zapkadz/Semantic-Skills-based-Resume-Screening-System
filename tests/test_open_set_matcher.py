from src.embedding_matcher import SemanticEmbeddingMatcher
from src.open_set_matcher import (
    OPEN_SET_MATCH_SCORE,
    build_taxonomy_coverage,
    find_semantic_requirement_evidence,
    split_known_and_unknown_requirements,
)


class FakeOpenSetEmbeddingModel:
    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = {
            "carbon footprint analysis": [1.0, 0.0, 0.0],
            "Built carbon emission reports for ESG audits.": [0.96, 0.04, 0.0],
            "drone mission planning": [0.0, 1.0, 0.0],
            "Built REST APIs using Java.": [1.0, 0.0, 0.0],
            "Python": [0.0, 0.0, 1.0],
            "mobile ai deployment": [0.0, 0.8, 0.6],
            "Optimized liveness models for mobile devices.": [0.0, 1.0, 0.0],
            "ONNX Runtime Mobile": [0.0, 1.0, 0.0],
            "Optimized liveness models for mobile devices. Technologies: ONNX Runtime Mobile, PyTorch": [
                0.0,
                0.82,
                0.58,
            ],
        }
        return [vectors.get(text, [0.0, 0.0, 1.0]) for text in texts]


def test_split_known_and_unknown_requirements_keeps_unknown_skill_labels() -> None:
    taxonomy = _taxonomy()

    result = split_known_and_unknown_requirements(
        ["Python", "carbon footprint analysis", "3+ years experience"],
        ["Python"],
        taxonomy,
    )

    assert result == {
        "known_requirements": ["Python"],
        "unknown_requirements": ["carbon footprint analysis"],
    }


def test_build_taxonomy_coverage_reports_known_and_unknown_counts() -> None:
    coverage = build_taxonomy_coverage(
        ["Python", "SQL"],
        ["carbon footprint analysis"],
    )

    assert coverage == {
        "known_count": 2,
        "unknown_count": 1,
        "coverage_ratio": 0.6667,
        "known_requirements": ["Python", "SQL"],
        "unknown_requirements": ["carbon footprint analysis"],
    }


def test_find_semantic_requirement_evidence_returns_semantic_only_match() -> None:
    matcher = SemanticEmbeddingMatcher(
        model=FakeOpenSetEmbeddingModel(),
        threshold=0.70,
    )
    resume_profile = {
        "summary": "",
        "headline": "",
        "raw_skills": ["Python"],
        "work_experience": [],
        "projects": [
            {
                "name": "ESG Platform",
                "description": ["Built carbon emission reports for ESG audits."],
                "technologies": [],
            }
        ],
    }

    matches = find_semantic_requirement_evidence(
        ["carbon footprint analysis"],
        resume_profile,
        matcher,
        threshold=0.70,
    )

    assert matches == [
        {
            "required_skill": "carbon footprint analysis",
            "candidate_skill": None,
            "match_type": "semantic_only_match",
            "taxonomy_status": "unknown",
            "score": OPEN_SET_MATCH_SCORE,
            "similarity": 0.9991,
            "evidence_level": 3,
            "evidence_text": "Built carbon emission reports for ESG audits.",
            "evidence_source": "projects",
        }
    ]


def test_find_semantic_requirement_evidence_returns_no_semantic_evidence_below_threshold() -> None:
    matcher = SemanticEmbeddingMatcher(
        model=FakeOpenSetEmbeddingModel(),
        threshold=0.70,
    )
    resume_profile = {
        "summary": "",
        "headline": "",
        "raw_skills": [],
        "work_experience": [
            {
                "title": "Backend Developer",
                "company": "ABC",
                "duration": "",
                "description": ["Built REST APIs using Java."],
            }
        ],
        "projects": [],
    }

    matches = find_semantic_requirement_evidence(
        ["drone mission planning"],
        resume_profile,
        matcher,
        threshold=0.80,
    )

    assert matches == [
        {
            "required_skill": "drone mission planning",
            "candidate_skill": None,
            "match_type": "no_semantic_evidence",
            "taxonomy_status": "unknown",
            "score": 0.0,
            "similarity": None,
            "evidence_level": 0,
            "evidence_text": "",
            "evidence_source": "none",
        }
    ]


def test_find_semantic_requirement_evidence_skips_when_embedding_disabled() -> None:
    resume_profile = {
        "summary": "Built carbon emission reports.",
        "headline": "",
        "raw_skills": [],
        "work_experience": [],
        "projects": [],
    }

    assert (
        find_semantic_requirement_evidence(
            ["carbon footprint analysis"],
            resume_profile,
            embedding_matcher=None,
        )
        == []
    )


def test_find_semantic_requirement_evidence_uses_synthesized_project_context() -> None:
    matcher = SemanticEmbeddingMatcher(
        model=FakeOpenSetEmbeddingModel(),
        threshold=0.70,
    )
    resume_profile = {
        "summary": "",
        "headline": "",
        "raw_skills": [],
        "work_experience": [],
        "projects": [
            {
                "name": "Mobile Face SDK",
                "description": ["Optimized liveness models for mobile devices."],
                "technologies": ["ONNX Runtime Mobile", "PyTorch"],
            }
        ],
    }

    matches = find_semantic_requirement_evidence(
        ["mobile ai deployment"],
        resume_profile,
        matcher,
        threshold=0.70,
    )

    assert matches == [
        {
            "required_skill": "mobile ai deployment",
            "candidate_skill": None,
            "match_type": "semantic_only_match",
            "taxonomy_status": "unknown",
            "score": OPEN_SET_MATCH_SCORE,
            "similarity": 0.9996,
            "evidence_level": 3,
            "evidence_text": (
                "Optimized liveness models for mobile devices. Technologies: ONNX Runtime Mobile, PyTorch"
            ),
            "evidence_source": "projects",
        }
    ]


def _taxonomy() -> dict:
    return {
        "Python": {
            "aliases": ["python"],
            "category": "Programming Language",
            "related": [],
            "transferable": [],
        }
    }
