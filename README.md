# Semantic Skills-based Resume Screening System

## Overview

Semantic Skills-based Resume Screening System is an AI/NLP-assisted recruitment screening project. The system is designed to compare resumes with job descriptions through skills, evidence, experience, seniority, domain fit, and explainable review cards.

The project does not train a recruitment model from scratch. The MVP starts with rule-based processing, skill taxonomy, skill normalization, matching rules, evidence scoring, and explainable ranking. Semantic embedding can be added in a later phase after the rule-based baseline is stable.

## Current Phase

The project is currently in:

```text
Phase 05 - Rule-based Skill Matching
```

This phase adds rule-based skill matching between normalized JD skills and normalized candidate skills. Evidence detection, final scoring, ranking, and review card generation will be implemented in later phases.

## Planned Processing Flow

```text
CV / JD text
  -> Document Loader
  -> Parser
  -> Skill Extraction
  -> Skill Normalization
  -> Skill Matching
  -> Evidence Detection
  -> Scoring
  -> Ranking
  -> Explainable Review Card
```

## Project Structure

```text
.
|-- app.py
|-- main.py
|-- requirements.txt
|-- README.md
|-- PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md
|-- data/
|   |-- cvs/
|   |-- jobs/
|   `-- taxonomy/
|-- docs/
|   |-- phases/
|   |-- refactoring/
|   `-- dev-learning-log.md
|-- outputs/
|   `-- reports/
|-- src/
`-- tests/
```

## Implemented Scope

Included:

- Repository foundation.
- Minimal CLI entry point.
- Minimal Streamlit entry point.
- Directory structure for data, source code, tests, outputs, and docs.
- Development learning log.
- TXT document loader.
- Minimal demo JD and CV text files.
- Unit tests for document loading.
- Rule-based resume parser.
- Rule-based JD parser.
- Unit tests for parser outputs.
- Skill taxonomy JSON.
- Skill taxonomy loader and alias map.
- Skill normalizer.
- Unit tests for taxonomy and normalization.
- Rule-based skill matcher.
- Unit tests for exact, related, transferable, and missing skill matches.

Not included yet:

- Evidence detection.
- Scoring and ranking.
- Review card generation.
- Full Streamlit UI.

## Run Minimal CLI

```bash
python main.py --help
python main.py
```

Expected behavior in Phase 05: the command confirms that the foundation is ready. The document loader, parsers, normalizer, and matcher are tested separately and are not wired into the CLI flow yet.

## Run Document Loader Tests

```bash
pytest
```

Manual loader check:

```bash
python -c "from src.document_loader import load_text_file; print(load_text_file('data/jobs/jd_backend_java.txt'))"
```

## Run Parser Checks

Resume parser:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; print(parse_resume(load_text_file('data/cvs/cv_strong.txt')))"
```

JD parser:

```bash
python -c "from src.document_loader import load_text_file; from src.jd_parser import parse_jd; print(parse_jd(load_text_file('data/jobs/jd_backend_java.txt')))"
```

## Run Skill Normalization Checks

Alias normalization:

```bash
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); print(normalize_skills(['JS', 'SpringBoot', 'Postgres'], taxonomy))"
```

Normalize parser output:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); print(normalize_skills(profile['raw_skills'], taxonomy))"
```

## Run Skill Matching Check

Match demo JD must-have skills with demo CV skills:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

## Run Minimal Streamlit Entry Point

Install dependencies first:

```bash
pip install -r requirements.txt
```

Then run:

```bash
streamlit run app.py
```

In Phase 05, the app still shows a placeholder page because the functional UI is planned for a later phase.

## Development Workflow

Work is organized by phase. Each phase should have:

- A branch named `phase/<number>-<short-name>`.
- A phase plan in `docs/phases/`.
- A development learning log entry in `docs/dev-learning-log.md`.
- A refactoring plan in `docs/refactoring/` after implementation.
- Manual testing notes before moving to the next phase.

## Next Phase

The next planned phase is:

```text
Phase 06 - Semantic Matching with Embeddings
```

That phase can add embedding-based semantic similarity after the rule-based baseline is stable.
