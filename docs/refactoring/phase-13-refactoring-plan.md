# Phase 13 Refactoring Plan - Local Multilingual Embedding

## 1. Current status

Phase 13 upgrades the optional embedding layer from Phase 06 into a local multilingual semantic signal.

Updated files:

- `src/embedding_matcher.py`
- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `main.py`
- `api.py`
- `tests/test_embedding_matcher.py`
- `tests/test_semantic_matcher.py`
- `tests/test_payload_pipeline.py`
- `tests/test_main.py`

The default recommended model is:

```text
BAAI/bge-m3
```

The E5 instruct alternative is supported through query formatting:

```text
intfloat/multilingual-e5-large-instruct
```

## 2. Refactoring decision

No behavior-changing refactor is needed at the end of Phase 13.

The current split is acceptable:

- `embedding_matcher.py` owns model loading, query/document formatting, caching, and cosine similarity.
- `semantic_matcher.py` owns rule priority and match result shape.
- `screening_pipeline.py` and `payload_pipeline.py` only pass an optional matcher into the shared matcher.
- `main.py` exposes CLI flags.
- `api.py` reads environment configuration without changing the JSON request schema.

This keeps embeddings optional and avoids spreading model-specific logic across the project.

## 3. What should stay stable

The following surfaces should stay stable:

- `SemanticEmbeddingMatcher.similarity`
- `SemanticEmbeddingMatcher.best_match`
- `SemanticEmbeddingMatcher.similarity_matrix`
- `format_embedding_query`
- `format_embedding_document`
- `build_embedding_matcher`
- `build_embedding_matcher_from_env`
- `match_skills(..., embedding_matcher=None)`
- `run_screening_pipeline(..., embedding_matcher=None)`
- `run_screening_payload(..., embedding_matcher=None)`

The API request/response body should stay backward compatible for TOPCV Lite.

## 4. Candidate future refactors

Refactor only when one of these conditions happens:

- Multiple API workers need shared model lifecycle management.
- Real model latency requires a queue/background job.
- Embedding cache needs to persist across requests.
- We add sentence-level semantic evidence retrieval.
- We add a vector database or FAISS/Chroma index.
- We import ESCO/O*NET/VSCO and need taxonomy-specific retrieval.

Possible future split:

```text
src/
|-- embeddings/
|   |-- config.py
|   |-- matcher.py
|   `-- cache.py
|-- matching/
|   |-- semantic_matcher.py
|   `-- evidence_retriever.py
```

Do not perform this split now. The current code is still small enough.

## 5. Risks to watch

- BGE-M3 is heavier than the old MiniLM default and may be slow on CPU.
- First model load may download from Hugging Face.
- Semantic match can create plausible but weak matches if threshold is too low.
- E5 instruct queries need instruction formatting; documents should not receive the same prefix.
- API embedding matcher is cached per process, not across multiple server processes.
- Tests should continue using fake models and must not download real models.

## 6. Next phase notes

Phase 14 can focus on external taxonomy and coverage:

- Vietnam VSCO 2020 for occupation classification.
- ESCO/O*NET-inspired occupation-skill structures.
- Coverage diagnostics such as `taxonomy_coverage`.
- Domain-specific taxonomy files to avoid one huge JSON.
- Clear warning when a JD appears outside the current taxonomy.
