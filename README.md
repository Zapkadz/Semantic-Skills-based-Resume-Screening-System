# Semantic Skills-based Resume Screening System

## Overview

Semantic Skills-based Resume Screening System is an AI/NLP-assisted recruitment screening project. The system is designed to compare resumes with job descriptions through skills, evidence, experience, seniority, domain fit, and explainable review cards.

The project does not train a recruitment model from scratch. The MVP starts with rule-based processing, skill taxonomy, skill normalization, matching rules, evidence scoring, and explainable ranking. Optional semantic embedding is implemented as a fallback when the rule-based matcher cannot find a match.

## Current Phase

The project is currently in:

```text
Phase 15 - Human-in-the-loop Taxonomy Suggestion Queue
```

This phase turns repeated unknown requirements from open-set matching into a pending taxonomy suggestion queue. The AI project can suggest canonical skill names, aliases, frequency, example contexts, evidence snippets, and nearest existing taxonomy skills, but it does not automatically modify the taxonomy.

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
|-- api.py
|-- main.py
|-- taxonomy_suggest.py
|-- requirements.txt
|-- README.md
|-- PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md
|-- data/
|   |-- cvs/
|   |-- jobs/
|   `-- taxonomy/
|-- docs/
|   |-- integration/
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
- Optional embedding matcher wrapper.
- Semantic match fallback for no-match rule-based cases.
- Unit tests using mock embeddings, so tests do not require model downloads.
- Evidence detector for matched skills.
- Evidence levels from 0 to 3.
- Unit tests for keyword-only, project, work experience, and missing evidence.
- Rule-based candidate scorer.
- Weighted score components for skill match, evidence, experience, seniority, domain, and nice-to-have skills.
- Candidate ranking helper.
- Unit tests for scoring formulas, thresholds, demo pipeline scoring, and ranking order.
- Explainable review card generator.
- Markdown formatter for review cards.
- Rule-based strengths, concerns, evidence highlights, and interview questions.
- Unit tests for review card structure, Markdown output, and demo pipeline explanation.
- End-to-end screening pipeline.
- CLI arguments for JD path, CV directory, taxonomy path, JSON output, Markdown report output, and review card display.
- JSON ranking result writer.
- Markdown review card writer.
- Unit tests for pipeline output, file saving, and CLI behavior.
- FastAPI HTTP API service.
- JSON payload screening pipeline for web integration.
- Pydantic request models for job and candidate payloads.
- Health and screening endpoints.
- Unit tests for payload pipeline and API endpoints.
- Vietnamese-English JD and resume section parsing.
- Common mojibake repair for UTF-8 text misdecoded as Windows-1252.
- Taxonomy-based full-text skill extraction fallback.
- Expanded AI, Computer Vision, eKYC, biometrics, and model optimization taxonomy.
- Vietnamese skill aliases normalized to canonical English skill names.
- Vietnamese action verbs for evidence detection.
- AI/Computer Vision/eKYC/Mobile AI domain detection.
- Unit tests for bilingual parsing, skill extraction, Vietnamese aliases, and evidence.
- Local multilingual embedding configuration with `BAAI/bge-m3` as the recommended default.
- Optional `intfloat/multilingual-e5-large-instruct` query formatting support.
- Embedding cache for repeated query/document encoding inside one matcher instance.
- CLI flags and API environment variables for enabling embedding without changing default behavior.
- Unit tests for multilingual embedding config, formatting, caching, semantic matching, and injected payload matching.
- Open-set requirement matching for concise JD requirements outside the taxonomy.
- Taxonomy coverage output with known and unknown requirement counts.
- Semantic-only evidence matching for unknown requirements when embedding is enabled.
- Review card concerns that identify semantic-only matches outside the taxonomy.
- Unit tests for open-set requirement splitting, semantic evidence matching, coverage output, and review-card notes.
- Human-in-the-loop taxonomy suggestion builder for repeated unknown requirements.
- Versioned taxonomy suggestion queue JSON output.
- Standalone `taxonomy_suggest.py` CLI.
- Unit tests for observation collection, suggestion generation, save/load, and CLI output.

Not included yet:

- Full Streamlit UI.
- External taxonomy import from ESCO/O*NET/VSCO.
- Admin approval UI for taxonomy suggestions.
- Automatic taxonomy mutation.

## Run CLI Pipeline

```bash
python main.py --help
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Expected behavior in Phase 10: the command runs the full text-based screening pipeline and prints a ranking summary.

Save full JSON output:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

Save Markdown review cards:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-dir outputs/reports
```

Print review cards in the terminal:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --show-review-cards
```

Enable optional local multilingual embedding:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3
```

If the model has already been downloaded to the local Hugging Face cache, use local-only mode for stable offline/demo runs:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

For a fully offline demo after the model is cached, set `HF_HUB_OFFLINE=1` before running the command.

The embedding model is loaded lazily. If the model is unavailable, the system falls back to the rule-based taxonomy matcher.

When a JD contains a requirement outside the taxonomy, the output now includes coverage metadata:

```json
{
  "taxonomy_coverage": {
    "known_count": 2,
    "unknown_count": 1,
    "coverage_ratio": 0.6667,
    "known_requirements": ["Python", "SQL"],
    "unknown_requirements": ["carbon footprint analysis"]
  }
}
```

If embedding is enabled and the CV has semantically close evidence, an unknown requirement can produce:

```json
{
  "required_skill": "carbon footprint analysis",
  "candidate_skill": null,
  "match_type": "semantic_only_match",
  "taxonomy_status": "unknown",
  "score": 0.65,
  "similarity": 0.8421,
  "evidence_text": "Built carbon emission reports for ESG audits."
}
```

## Run Taxonomy Suggestion Queue

After saving a screening result JSON, generate pending taxonomy suggestions:

```bash
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Use a lower threshold for small demos:

```bash
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json --min-frequency 1
```

The suggestion queue is a local JSON artifact:

```json
{
  "version": 1,
  "suggestions": [
    {
      "suggested_canonical_name": "Carbon Footprint Analysis",
      "suggested_aliases": ["carbon footprint analysis"],
      "frequency": 2,
      "status": "pending_review"
    }
  ]
}
```

The Python project does not auto-update `data/taxonomy/skills.json`. Admin approval is expected in a later web/admin phase.

## Run Python API Service

Start the API server:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

Start the API with optional local multilingual embedding:

```bash
set SEMANTIC_EMBEDDING_ENABLED=1
set SEMANTIC_EMBEDDING_MODEL=BAAI/bge-m3
set SEMANTIC_EMBEDDING_THRESHOLD=0.72
set SEMANTIC_EMBEDDING_LOCAL_ONLY=1
uvicorn api:app --host 127.0.0.1 --port 8000
```

On PowerShell:

```powershell
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_THRESHOLD='0.72'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'
uvicorn api:app --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Run screening from a sample JSON payload:

```bash
curl -X POST http://127.0.0.1:8000/screening -H "Content-Type: application/json" -d @docs/integration/sample-screening-request.json
```

Expected screening response includes:

```text
candidate_name: Nguyen Van A
final_score: 87
recommendation: Strong Review
```

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

Vietnamese alias normalization:

```bash
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); print(normalize_skills(['nhận diện khuôn mặt', 'chong gia mao', 'Định danh điện tử'], taxonomy))"
```

Normalize parser output:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); print(normalize_skills(profile['raw_skills'], taxonomy))"
```

## Run Taxonomy Skill Extraction Check

Extract skills from Vietnamese text:

```bash
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_extractor import extract_taxonomy_skills_from_text; taxonomy=load_taxonomy('data/taxonomy/skills.json'); text='Xây dựng hệ thống nhận diện khuôn mặt và chống giả mạo trong quy trình eKYC bằng PyTorch.'; print(extract_taxonomy_skills_from_text(text, taxonomy))"
```

## Run Skill Matching Check

Match demo JD must-have skills with demo CV skills:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

## Run Embedding Fallback Check

Check that the optional embedding matcher can exist without a loaded model:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(auto_load=False); print(matcher.is_available())"
```

Expected output:

```text
False
```

Check local multilingual similarity when the model is available:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_name='BAAI/bge-m3', local_files_only=True); print(round(matcher.similarity('face recognition', 'nhận diện khuôn mặt') or 0, 4)); print(matcher.unavailable_reason)"
```

If the model is not downloaded yet or the machine is offline, this command can return `0` and an unavailable reason. That is expected fallback behavior.

Quick fallback check without contacting Hugging Face:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_loader=lambda name: (_ for _ in ()).throw(RuntimeError('model unavailable'))); print(matcher.similarity('face recognition', 'nhan dien khuon mat')); print(matcher.unavailable_reason)"
```

## Run Evidence Detection Check

Detect evidence for demo JD/CV matches:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); matches=match_skills(required, candidate, taxonomy); print(detect_all_evidence(matches, profile))"
```

## Run Scoring and Ranking Check

Score the demo candidate against the demo JD:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); nice_skills=normalize_skills(criteria['nice_to_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(nice_skills, candidate, taxonomy); print(score_candidate(criteria, profile, matches, nice))"
```

## Run Review Card Check

Generate a Markdown review card for the demo JD/CV:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; from src.review_card_generator import generate_review_card, format_review_card_markdown; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); nice_skills=normalize_skills(criteria['nice_to_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(nice_skills, candidate, taxonomy); result=score_candidate(criteria, profile, matches, nice); card=generate_review_card(result, criteria); print(format_review_card_markdown(card))"
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

In Phase 15, the app still shows a placeholder page because the functional UI is planned for a later phase.

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
Phase 16 - Admin Taxonomy Suggestion Review
```

That phase can add a web/Admin review workflow to approve, reject, or merge pending taxonomy suggestions before updating a custom taxonomy store.
