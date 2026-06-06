# Semantic Skills-based Resume Screening System

## Overview

Semantic Skills-based Resume Screening System is an AI/NLP-assisted recruitment screening project. The system is designed to compare resumes with job descriptions through skills, evidence, experience, seniority, domain fit, and explainable review cards.

The project does not train a recruitment model from scratch. The MVP starts with rule-based processing, skill taxonomy, skill normalization, matching rules, evidence scoring, and explainable ranking. Semantic embedding can be added in a later phase after the rule-based baseline is stable.

## Current Phase

The project is currently in:

```text
Phase 01 - Project Foundation
```

This phase only prepares the repository structure and minimal entry points. Business logic such as document loading, resume parsing, skill extraction, matching, evidence detection, scoring, and review card generation will be implemented in later phases.

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

## Phase 01 Scope

Included:

- Repository foundation.
- Minimal CLI entry point.
- Minimal Streamlit entry point.
- Directory structure for data, source code, tests, outputs, and docs.
- Development learning log.

Not included yet:

- TXT document loading.
- Resume/JD parsing.
- Skill taxonomy content.
- Skill matching.
- Evidence detection.
- Scoring and ranking.
- Review card generation.
- Full Streamlit UI.

## Run Minimal CLI

```bash
python main.py --help
python main.py
```

Expected behavior in Phase 01: the command only confirms that the foundation is ready and explains that business logic starts in later phases.

## Run Minimal Streamlit Entry Point

Install dependencies first:

```bash
pip install -r requirements.txt
```

Then run:

```bash
streamlit run app.py
```

In Phase 01, the app only shows a placeholder page.

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
Phase 02 - Document Loader and Text Input
```

That phase will implement reading `.txt` files for JD and CV inputs.
