# Refactoring Plan - Phase 06

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 06 da them optional embedding matcher, semantic fallback va tests bang fake embedding model. Rule-based matcher van la baseline chinh.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring final vi Phase 06 chua co final scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Khong co duplication dang ke. `embedding_matcher.py` tach rieng phan model/similarity, `semantic_matcher.py` chi goi optional fallback.

### 3.2 Oversized files

`src/embedding_matcher.py` con nho va co trach nhiem ro:

- Lazy load model.
- Tinh cosine similarity.
- Tim best semantic match tren threshold.
- Fallback khi model unavailable.

`src/semantic_matcher.py` van vua phai vi rule-based logic con nho.

### 3.3 Naming

Ten function/class ro rang:

- `SemanticEmbeddingMatcher`
- `DEFAULT_EMBEDDING_MODEL`
- `DEFAULT_SEMANTIC_THRESHOLD`
- `similarity`
- `best_match`
- `semantic_match`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Cosine similarity bang fake embedding model.
- Blank text fallback.
- Model loader failure fallback.
- Best match tren threshold.
- Best match duoi threshold.
- Semantic match khi rule-based no match.
- Rule-based priority cao hon semantic.
- No match khi embedding unavailable.

Co the them test cho model thật trong manual testing, nhung khong nen dua vao automated tests vi can internet/model cache.

### 3.5 API compatibility

Public API hien tai:

```python
SemanticEmbeddingMatcher(...)
SemanticEmbeddingMatcher.similarity(text_a, text_b) -> float | None
SemanticEmbeddingMatcher.best_match(required_skill, candidate_skills) -> dict | None
match_skills(job_skills, candidate_skills, taxonomy, embedding_matcher=None) -> list[dict]
```

Tham so `embedding_matcher` la optional nen call site Phase 05 van chay nhu cu.

## 4. De xuat refactor

### De xuat 1 - Chua tach vector math ra module rieng

- File lien quan: `src/embedding_matcher.py`
- Van de: cosine similarity hien nam trong cung file.
- Cach refactor: co the tach sang `src/vector_utils.py` neu sau nay co nhieu model/vector logic.
- Rui ro: tach som lam project nhieu file hon khi logic con gon.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua refactor.

### De xuat 2 - Chua cache embedding

- File lien quan: `src/embedding_matcher.py`
- Van de: moi lan similarity goi model encode rieng.
- Cach refactor: co the cache embedding theo text neu matching nhieu CV.
- Rui ro: cache som co the lam tang state va kho giai thich hon.
- Cach test sau refactor: chay `pytest` va manual semantic similarity.
- Co thay doi behavior khong? Khong.

Ket luan: de sau khi co ranking nhieu CV.

### De xuat 3 - Khong dua model thật vao automated tests

- File lien quan: `tests/test_embedding_matcher.py`
- Van de: test model thật can internet/cache va chay cham.
- Cach refactor: khong lam; tiep tuc dung fake model.
- Rui ro: neu test that model, CI/may khac co the fail vi network.
- Cach test sau refactor: manual command voi model that.
- Co thay doi behavior khong? Khong.

Ket luan: giu tests bang fake model.

## 5. Pham vi refactor

Phase 06 khong thuc hien refactor code them.

Khong refactor:

- Khong tach vector utils.
- Khong cache embeddings.
- Khong them model thật vao automated tests.
- Khong thay threshold mac dinh.
- Khong wire vao CLI/UI.
- Khong them final scoring.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(auto_load=False); print(matcher.is_available())"
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(); print(matcher.similarity('Built RESTful services', 'Backend API development')); print(matcher.unavailable_reason)"
```

Ket qua mong doi:

- Tat ca tests pass.
- Fallback check in `False`.
- Model thật neu kha dung tra similarity float hoac tra `None` kem unavailable reason, nhung khong crash.

## 7. Ghi chu cho bao cao

Sau Phase 06, du an co buoc review refactor de dam bao embedding matching van la thanh phan bo sung, khong thay the rule-based baseline. Viec dung fake model trong automated tests giup test on dinh, con model thật duoc kiem tra thu cong de tranh phu thuoc vao internet hoac cache model trong quy trinh CI.
