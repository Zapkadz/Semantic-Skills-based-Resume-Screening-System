# Phase 17 Refactoring Plan - Taxonomy-independent Open-set Screening Core

## 1. Muc tieu refactor

Giam phu thuoc vao taxonomy khi JD thuoc nganh/chuc vu moi.

Truoc Phase 17:

```text
JD requirement phai vao taxonomy thi moi match/cham diem tot.
```

Sau Phase 17:

```text
Known taxonomy skills -> rule-based explainable matching
Unknown requirements -> open-set semantic evidence matching
```

## 2. Module moi

### 2.1 `src/requirement_extractor.py`

Trach nhiem:

- Tach requirement line dai thanh capability units ngan.
- Loc heading va soft requirement qua chung.
- Bo qua requirement da duoc taxonomy cover.
- Tao danh sach open-set requirements de semantic matcher xu ly.
- Tao `screening_confidence` metadata.

Vi du:

```text
Professional requirements: Proficiency in Linux, Nutanix administration, Commvault, and Qualys
```

Thanh:

```text
Linux
Nutanix administration
Commvault
Qualys
```

## 3. Module duoc cap nhat

### 3.1 `src/screening_pipeline.py`

- Dung `extract_unknown_requirement_texts`.
- Them `open_set_requirements` vao job output.
- Them `screening_confidence` vao job output.
- Van giu `must_have_skills` la known taxonomy skills.

### 3.2 `src/payload_pipeline.py`

- Giu `job_title` khi web gui ca `job_title` va `raw_text`.
- Dung chung open-set extraction voi CLI pipeline.
- Them `open_set_requirements` va `screening_confidence` vao API response.

### 3.3 `src/open_set_matcher.py`

- Dong bo threshold voi `SemanticEmbeddingMatcher.threshold` neu caller khong override.
- Uu tien exact phrase evidence khi evidence text chua dung requirement phrase.
- Neu similarity gan nhau, uu tien evidence source manh hon.

### 3.4 `src/evidence_detector.py`

- Them `certifications` vao evidence candidates.

### 3.5 `src/jd_parser.py`

- Them title fallback tu responsibility heading dau tien.
- Sua typo `yeear` cho minimum years parsing.
- Sua domain matching bang word-boundary phrase checks.
- Them domain `IT Security/GRC`.

### 3.6 `src/scorer.py`

- Sua candidate domain detection bang word-boundary phrase checks.
- Bo false positive tu cac tu chung nhu `service`/`application`.
- Them domain `IT Security/GRC`.

## 4. Compatibility

Khong doi CLI arguments.

Khong doi API endpoint.

Chi them field moi trong output:

```json
{
  "open_set_requirements": [],
  "screening_confidence": {}
}
```

Web cu van doc duoc `final_score`, `recommendation`, `review_card`.

Web moi nen hien them:

- taxonomy coverage.
- open-set requirements.
- confidence warning khi embedding disabled.

## 5. Test strategy

Them/cap nhat:

- `tests/test_requirement_extractor.py`
- `tests/test_payload_pipeline.py`
- `tests/test_jd_parser.py`
- `tests/test_scorer.py`
- `tests/test_evidence_detector.py`

Cover:

- Tach capability units tu long security JD.
- Skip known taxonomy phrases.
- Confidence warning khi embedding disabled.
- Open-set security role match duoc khi taxonomy rong va embedding available.
- JD title fallback.
- Domain matching khong match `edge` trong `knowledge`.
- Candidate security/GRC domain detection.
- Certification evidence.

## 6. Manual benchmark

Khong embedding:

```powershell
python main.py --jd data\jobs\JD_2.txt --cv-dir outputs\test_cv1_cv3 --output-json outputs\jd2_cv1_cv3_phase17_no_embedding.json
```

Ket qua:

```text
David Chen - 36/100 - Not Enough Evidence
Kevin Walker - 32/100 - Not Enough Evidence
```

Co BGE-M3:

```powershell
python main.py --jd data\jobs\JD_2.txt --cv-dir outputs\test_cv1_cv3 --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only --output-json outputs\jd2_cv1_cv3_phase17_bge.json
```

Ket qua:

```text
David Chen - 72/100 - Review
Kevin Walker - 36/100 - Not Enough Evidence
```

## 7. Risk

### 7.1 Over-extraction

Risk:

```text
Requirement extractor tach qua nhieu phrase.
```

Giam thieu:

- Gioi han length/word count.
- Loc headings.
- Loc soft requirements.
- Dedupe.

### 7.2 Semantic false positive

Risk:

```text
Embedding match gan nghia nhung sai intent.
```

Giam thieu:

- Mark `semantic_only_match`.
- Giu score semantic-only thap hon exact match.
- Output evidence text de recruiter verify.

### 7.3 Embedding disabled

Risk:

```text
Open-set requirements co nhung khong the semantic match.
```

Giam thieu:

- `screening_confidence.level = low`.
- Warning ro trong output.

