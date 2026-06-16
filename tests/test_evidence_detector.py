from src.document_loader import load_text_file
from src.evidence_detector import detect_all_evidence, detect_evidence
from src.jd_parser import parse_jd
from src.resume_parser import parse_resume
from src.semantic_matcher import match_skills
from src.skill_normalizer import normalize_skills
from src.skill_taxonomy import load_taxonomy


TAXONOMY_PATH = "data/taxonomy/skills.json"


def test_detect_evidence_returns_level_3_for_action_based_work_bullet() -> None:
    profile = {
        "raw_skills": ["Spring Boot"],
        "work_experience": [
            {
                "description": [
                    "Built REST APIs using Java and Spring Boot.",
                ]
            }
        ],
        "projects": [],
    }

    evidence = detect_evidence("Spring Boot", profile)

    assert evidence == {
        "skill": "Spring Boot",
        "evidence_level": 3,
        "evidence_text": "Built REST APIs using Java and Spring Boot.",
        "evidence_source": "work_experience",
    }


def test_detect_evidence_returns_level_3_for_action_based_project_bullet() -> None:
    profile = {
        "raw_skills": ["REST API"],
        "work_experience": [],
        "projects": [
            {
                "description": [
                    "Created RESTful APIs with Spring Boot and MySQL.",
                ],
                "technologies": [],
            }
        ],
    }

    evidence = detect_evidence("REST API", profile)

    assert evidence == {
        "skill": "REST API",
        "evidence_level": 3,
        "evidence_text": "Created RESTful APIs with Spring Boot and MySQL.",
        "evidence_source": "projects",
    }


def test_detect_evidence_returns_level_2_for_non_action_project_context() -> None:
    profile = {
        "raw_skills": [],
        "work_experience": [],
        "projects": [
            {
                "description": ["Backend service stack: Java, Spring Boot, MySQL."],
                "technologies": [],
            }
        ],
    }

    evidence = detect_evidence("MySQL", profile)

    assert evidence == {
        "skill": "MySQL",
        "evidence_level": 2,
        "evidence_text": "Backend service stack: Java, Spring Boot, MySQL.",
        "evidence_source": "projects",
    }


def test_detect_evidence_returns_level_1_for_skill_list_only() -> None:
    profile = {
        "summary": "",
        "headline": "",
        "raw_skills": ["Kafka"],
        "work_experience": [],
        "projects": [],
    }

    evidence = detect_evidence("Kafka", profile)

    assert evidence == {
        "skill": "Kafka",
        "evidence_level": 1,
        "evidence_text": "Kafka",
        "evidence_source": "skills",
    }


def test_detect_evidence_returns_level_1_for_summary_only() -> None:
    profile = {
        "summary": "Backend developer with Java experience.",
        "headline": "",
        "raw_skills": [],
        "work_experience": [],
        "projects": [],
    }

    evidence = detect_evidence("Java", profile)

    assert evidence["evidence_level"] == 1
    assert evidence["evidence_text"] == "Backend developer with Java experience."
    assert evidence["evidence_source"] == "summary"


def test_detect_evidence_returns_level_1_for_certification() -> None:
    profile = {
        "summary": "",
        "headline": "",
        "raw_skills": [],
        "work_experience": [],
        "projects": [],
        "certifications": ["ISO 27001 Lead Implementer"],
    }

    evidence = detect_evidence("ISO 27001", profile)

    assert evidence == {
        "skill": "ISO 27001",
        "evidence_level": 1,
        "evidence_text": "ISO 27001 Lead Implementer",
        "evidence_source": "certifications",
    }


def test_detect_evidence_returns_level_0_when_skill_is_missing() -> None:
    profile = {
        "summary": "Frontend developer.",
        "raw_skills": ["React"],
        "work_experience": [],
        "projects": [],
    }

    evidence = detect_evidence("Kafka", profile)

    assert evidence == {
        "skill": "Kafka",
        "evidence_level": 0,
        "evidence_text": "",
        "evidence_source": "none",
    }


def test_detect_all_evidence_enriches_matches_and_uses_candidate_skill() -> None:
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))
    matches = [
        {
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "score": 0.75,
        }
    ]

    enriched_matches = detect_all_evidence(matches, profile)

    assert enriched_matches == [
        {
            "required_skill": "SQL",
            "candidate_skill": "MySQL",
            "match_type": "related_match",
            "score": 0.75,
            "evidence_level": 3,
            "evidence_text": (
                "Designed MySQL database schemas for product and order modules."
            ),
            "evidence_source": "work_experience",
        }
    ]


def test_demo_pipeline_adds_strong_evidence_to_must_have_matches() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    profile = parse_resume(load_text_file("data/cvs/cv_strong.txt"))
    criteria = parse_jd(load_text_file("data/jobs/jd_backend_java.txt"))
    candidate_skills = normalize_skills(profile["raw_skills"], taxonomy)
    required_skills = normalize_skills(criteria["must_have_skills"], taxonomy)
    matches = match_skills(required_skills, candidate_skills, taxonomy)

    enriched_matches = detect_all_evidence(matches, profile)

    assert [match["evidence_level"] for match in enriched_matches] == [3, 3, 3, 3, 3]
    assert enriched_matches[0]["evidence_text"] == (
        "Built REST APIs using Java and Spring Boot."
    )
    assert enriched_matches[3]["required_skill"] == "SQL"
    assert enriched_matches[3]["candidate_skill"] == "MySQL"
    assert enriched_matches[3]["evidence_text"] == (
        "Designed MySQL database schemas for product and order modules."
    )


def test_detect_evidence_uses_vietnamese_aliases_and_action_verbs() -> None:
    taxonomy = load_taxonomy(TAXONOMY_PATH)
    profile = {
        "raw_skills": [],
        "work_experience": [],
        "projects": [
            {
                "description": [
                    "Xây dựng hệ thống nhận diện khuôn mặt cho quy trình eKYC.",
                ],
                "technologies": [],
            }
        ],
    }

    evidence = detect_evidence("Face Recognition", profile, taxonomy)

    assert evidence == {
        "skill": "Face Recognition",
        "evidence_level": 3,
        "evidence_text": "Xây dựng hệ thống nhận diện khuôn mặt cho quy trình eKYC.",
        "evidence_source": "projects",
    }
