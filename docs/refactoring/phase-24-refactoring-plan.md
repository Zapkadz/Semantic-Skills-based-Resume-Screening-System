# Phase 24 Refactoring Plan - JD Quality Gate and Recommendation Eligibility

## 1. Muc tieu refactor

Sau Phase 23, candidate-side recommendation da co retrieval, reranking va
skill-gap explanation. Tuy nhien, du lieu web that co nhieu tin test / placeholder
lam ket qua goi y bi nhieu.

Muc tieu Phase 24:

```text
Danh gia chat luong JD truoc
roi moi cho job tham gia recommendation.
```

## 2. Module moi

### 2.1 `src/job_quality_gate.py`

Trach nhiem:

- Phat hien title placeholder.
- Phat hien content qua ngan sau khi clean.
- Kiem tra job co yeu cau ky thuat co y nghia khong.
- Kiem tra responsibilities co y nghia khong.
- Tao `job_quality` metadata va `recommendation_eligible`.

## 3. Module duoc cap nhat

### 3.1 `src/job_catalog_loader.py`

- Goi `evaluate_job_quality(...)` cho tung normalized job card.
- Luu `job_quality` vao catalog.

### 3.2 `src/job_recommendation_pipeline.py`

- Tach `eligible_job_catalog` va `excluded_jobs`.
- Chi build retrieval index tren eligible jobs.
- Them `job_quality_stats` va `warnings` vao response.

### 3.3 `src/candidate_job_reranker.py`

- Dua `job_quality` vao tung `top_job`.

### 3.4 `api.py`

- Nang phase len Phase 24.
- Nang version API len `0.24.0`.

## 4. Output contract

Response candidate-side co them:

```json
{
  "excluded_jobs": [],
  "job_quality_stats": {},
  "warnings": []
}
```

Moi `top_job` co them:

```json
{
  "job_quality": {
    "quality_score": 0,
    "quality_label": "eligible",
    "recommendation_eligible": true,
    "flags": [],
    "reasons": []
  }
}
```

## 5. Test strategy

Them/cap nhat:

- `tests/test_job_quality_gate.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`

Cover:

- job `Test` + `test` -> ineligible
- job that co requirements that -> eligible
- placeholder job khong xuat hien trong `top_jobs`
- placeholder job xuat hien trong `excluded_jobs`
- top-level response co `job_quality_stats` va `warnings`

## 6. Manual check

Payload co 1 job that + 1 job test:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

```text
top_jobs
excluded_jobs
job_quality_stats
warnings
```

## 7. Risk

### 7.1 Loai nham JD ngan nhung that

Risk:

```text
Mot so job viet ngan nhung van hop le.
```

Giam thieu:

- khong chi dua vao 1 rule duy nhat;
- cho phep `eligible_with_warning`;
- hard exclusion chi ap dung khi ket hop nhieu co xau.

### 7.2 Over-match title placeholder

Risk:

```text
`Test Engineer` bi hieu nham la job test.
```

Giam thieu:

- chi flag title placeholder khi title ngan va toan tu placeholder;
- khong bat substring may moc.

### 7.3 Web payload chua clean

Risk:

```text
HTML ban tu web lam quality gate nhan dinh sai.
```

Giam thieu:

- tiep tuc clean payload trong Python;
- tiep tuc yeu cau web gui plain text sach;
- giu debug request/response cho integration.
