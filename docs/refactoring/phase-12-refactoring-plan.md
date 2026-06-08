# Phase 12 Refactoring Plan - Vietnamese-English Parser, Taxonomy, and Evidence Foundation

## 1. Current status

Phase 12 improves the input understanding layer before local multilingual embedding is added.

New files:

- `src/text_normalization.py`
- `src/section_parser.py`
- `src/skill_extractor.py`
- `tests/test_skill_extractor.py`

Major updated files:

- `src/jd_parser.py`
- `src/resume_parser.py`
- `src/evidence_detector.py`
- `src/scorer.py`
- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `data/taxonomy/skills.json`

The CLI and FastAPI API interfaces remain unchanged.

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 12.

The new split is intentional:

- `text_normalization.py` owns encoding repair and accent/search normalization.
- `section_parser.py` owns reusable section heading parsing.
- `skill_extractor.py` owns taxonomy skill extraction from raw text.
- JD/resume parsers still own structured profile parsing.
- Pipeline modules own the decision to merge parsed skills with raw-text extracted skills.

This keeps parser schema stable while improving recall for messy bilingual input.

## 3. What should stay stable

The following public surfaces should stay stable:

- `parse_jd(text)`
- `parse_resume(text)`
- `extract_taxonomy_skills_from_text(text, taxonomy)`
- `merge_skill_lists`
- `detect_evidence(skill, resume_profile, taxonomy=None)`
- `detect_all_evidence(matches, resume_profile, taxonomy=None)`
- `run_screening_pipeline`
- `run_screening_payload`
- `GET /health`
- `POST /screening`

The API request/response schema should not change for TOPCV Lite integration.

## 4. Candidate future refactors

Refactor only when one of these conditions appears:

- JD/resume parsers need many more shared block parsing rules.
- Taxonomy grows large enough that JSON becomes hard to review manually.
- Skill extraction needs phrase-level confidence, source spans, or section-aware weights.
- API needs to expose extraction diagnostics for debugging web integration.
- Multilingual embedding introduces sentence chunking that should be shared by matcher and evidence modules.

Possible future split:

```text
src/
|-- parsing/
|   |-- section_parser.py
|   |-- jd_parser.py
|   `-- resume_parser.py
|-- skills/
|   |-- taxonomy.py
|   |-- normalizer.py
|   `-- extractor.py
`-- matching/
    |-- semantic_matcher.py
    `-- multilingual_embedding_matcher.py
```

Do not perform this split now; the current module count is still manageable.

## 5. Risks to watch

- Full-text extraction can create false positives if aliases are too broad.
- Acronyms like `FAR`, `FRR`, and `AUC` should remain case-sensitive in extraction.
- Generic aliases like `CV` should not be used for `Computer Vision` because it can mean resume/CV.
- Mojibake repair is best-effort and should not replace correct text extraction in web/PDF pipelines.
- Adding too many unknown short requirement labels can pollute `must_have_skills`.
- Domain detection should not let weak words like `ai` inside Vietnamese syllables trigger AI domain.

## 6. Next phase notes

Phase 13 should add local multilingual embedding as an optional semantic signal:

- Start with a local model wrapper that can be unavailable without breaking tests.
- Compare `BAAI/bge-m3` and `intfloat/multilingual-e5-large`.
- Keep taxonomy/rule matching as the explainable backbone.
- Use embedding to improve cross-language semantic equivalence, not to replace evidence.
- Add tests with fake embedding models so CI does not download large models.
