# Phase 25 Refactoring Plan - Web Payload Quality Hardening and Runtime Diagnostics

## 1. Muc tieu refactor

Sau Phase 24, candidate-side recommendation da loai duoc job test / placeholder
ra khoi `top_jobs`. Tuy nhien, khi dua vao web that, van de con lai la:

```text
Khong phai luc nao diem "la" cung do scorer.
Rat nhieu luc payload web gui sang AI chua sach hoac qua ngan.
```

Muc tieu Phase 25:

```text
Bo sung diagnostics co cau truc
de tach ro input issue, parsing issue, va matching issue.
```

## 2. Module moi

### 2.1 `src/payload_diagnostics.py`

Trach nhiem:

- Danh gia chat luong payload JD truoc khi parse.
- Danh gia chat luong payload CV truoc khi parse.
- Tao `flags`, `warnings`, `metrics`, `source`.
- Tong hop diagnostics theo candidate list hoac job list.

### 2.2 `src/runtime_diagnostics.py`

Trach nhiem:

- Tao `trace_id`.
- Build top-level `diagnostics` cho `/screening`.
- Build top-level `diagnostics` cho `/recommend-jobs`.
- Gom payload summary va runtime summary vao mot contract on dinh.

## 3. Module duoc cap nhat

### 3.1 `src/payload_pipeline.py`

- Tao `trace_id` cho moi screening request.
- Chay payload diagnostics cho job va candidate payloads.
- Them `job_quality` vao diagnostics employer-side.
- Tra them `diagnostics` va `trace_id` o top-level response.

### 3.2 `src/job_catalog_loader.py`

- Danh gia `payload_diagnostics` cho tung job trong catalog.
- Luu metadata nay de candidate-side runtime co the tong hop lai.

### 3.3 `src/job_recommendation_pipeline.py`

- Tao `trace_id` cho moi recommendation request.
- Danh gia diagnostics cho candidate payload.
- Tong hop diagnostics tren toan bo job catalog.
- Dua `payload_diagnostics` vao `excluded_jobs`.

### 3.4 `api.py`

- Nang phase len Phase 25.
- Nang version API len `0.25.0`.

## 4. Output contract

Ca hai endpoint deu co them:

```json
{
  "trace_id": "screening-abc123",
  "diagnostics": {
    "endpoint": "screening",
    "trace_id": "screening-abc123",
    "payload": {},
    "runtime": {}
  }
}
```

### 4.1 `/screening`

Them:

- `diagnostics.payload.job`
- `diagnostics.payload.candidates`
- `diagnostics.runtime.job_quality`

### 4.2 `/recommend-jobs`

Them:

- `diagnostics.payload.candidate`
- `diagnostics.payload.jobs`
- `diagnostics.runtime.top_job_ids`
- `diagnostics.runtime.excluded_job_ids`

## 5. Test strategy

Them/cap nhat:

- `tests/test_payload_diagnostics.py`
- `tests/test_runtime_diagnostics.py`
- `tests/test_payload_pipeline.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`

Cover:

- JD placeholder / qua ngan -> co payload flags
- CV qua ngan / qua sparse -> co payload flags
- response co `trace_id`
- response co `diagnostics`
- diagnostics tong hop dung so luong candidate/job bi flag
- full regression khong gay cac phase truoc

## 6. Manual check

Screening:

```powershell
$body = Get-Content docs\integration\sample-screening-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/screening -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

```text
trace_id
diagnostics.payload.job
diagnostics.payload.candidates
diagnostics.runtime.job_quality
```

Recommendation:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

```text
trace_id
diagnostics.payload.candidate
diagnostics.payload.jobs
diagnostics.runtime.top_job_ids
diagnostics.runtime.excluded_job_ids
```

## 7. Risk

### 7.1 Diagnostics qua noisy

Risk:

```text
Response bi qua dai, web kho doc.
```

Giam thieu:

- chi tong hop metrics can thiet;
- giu `warnings` san pham rieng;
- diagnostics chu yeu phuc vu debug/admin.

### 7.2 Flag qua nhay

Risk:

```text
Job/CV that nhung viet ngan van bi canh bao.
```

Giam thieu:

- diagnostics chi canh bao, khong auto fail screening;
- Phase 24 quality gate van la lop quyet dinh chinh cho candidate-side exclusion.

### 7.3 Web bo qua diagnostics moi

Risk:

```text
Backend da tra diagnostics nhung web khong dung.
```

Giam thieu:

- contract backward-compatible;
- co the viet them Cursor prompt tich hop web sau phase nay.
