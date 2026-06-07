# Phase 11 Refactoring Plan - Python API Service

## 1. Current status

Phase 11 adds a FastAPI HTTP API service for web integration.

New files:

- `api.py`
- `src/api_models.py`
- `src/payload_pipeline.py`
- `tests/test_api.py`
- `tests/test_payload_pipeline.py`
- `docs/integration/sample-screening-request.json`

The existing CLI entry point `main.py` remains unchanged.

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 11.

The current split is intentional:

- `main.py` is the CLI adapter.
- `api.py` is the HTTP adapter.
- `src/screening_pipeline.py` handles file-based pipeline input.
- `src/payload_pipeline.py` handles JSON payload input.
- Parser, matcher, evidence, scorer, and review card modules remain shared core logic.

This avoids duplicating scoring or matching logic in the API layer.

## 3. What should stay stable

The following public surfaces should stay stable:

- `GET /health`
- `POST /screening`
- `run_screening_payload`
- `build_jd_text_from_payload`
- `build_cv_document_from_payload`
- Existing CLI command:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

PHP integration should depend on `POST /screening` and not call lower-level scorer modules directly.

## 4. Candidate future refactors

Refactor only when one of these conditions happens:

- File-based and payload-based pipelines start duplicating too much orchestration code.
- API response schema needs versioning.
- Web integration needs authentication or API keys.
- The API needs background jobs for large CV batches.
- PDF/DOCX extraction is added to the API.
- PHP sends uploaded files instead of `cv_text`.

Possible future split:

```text
src/
|-- screening_engine.py
|-- screening_pipeline.py
|-- payload_pipeline.py
|-- api_models.py
`-- response_models.py
```

## 5. Risks to watch

- API endpoint becoming business logic.
- CLI and API behavior drifting apart.
- Response losing `application_id`, making PHP DB mapping harder.
- Payload schema changing without updating integration docs.
- Server process left running during tests/manual checks.
- Candidate CV payload missing text but not failing clearly.

## 6. Next phase notes

Next work can go in one of two directions:

- Integrate TOPCV Lite PHP with `POST /screening`.
- Build a Streamlit UI for local demo use.

Whichever path is chosen, it should call the API or shared pipeline instead of duplicating parser/matcher/scorer logic.
