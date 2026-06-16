# Phase 23 Refactoring Plan - Skill-gap Explanation and CV Improvement Suggestions

## 1. Muc tieu refactor

Sau Phase 22, candidate-side recommendation da co retrieval va reranking, nhung
output van chua du chi tiet de ung vien biet can sua CV nhu the nao.

Muc tieu Phase 23:

```text
Top job recommendations
  -> tach ro missing skill va weak evidence
  -> them goi y cai thien CV
  -> giu output gon de web render de dang
```

## 2. Module moi

### 2.1 `src/skill_gap_explainer.py`

Trach nhiem:

- Doc candidate-vs-job result da duoc score.
- Tach gap thanh 4 nhom:
  - `missing_must_have`
  - `weak_evidence`
  - `optional_growth`
  - `presentation_gaps`
- Tao `skill_gap_summary`.
- Tao `cv_improvement_suggestions`.
- Cat gon thanh `next_best_actions` cho UI compact.

Nguyen tac:

- khong invent skill moi;
- khong khuyen them kinh nghiem ao;
- neu skill dang thieu thi dung wording
  `If you have real experience...`.

## 3. Module duoc cap nhat

### 3.1 `src/candidate_job_reranker.py`

- Goi `explain_skill_gaps(...)` sau khi score tung job.
- Dua them cac field moi vao moi `top_job`:
  - `skill_gap_summary`
  - `skill_gaps`
  - `cv_improvement_suggestions`
  - `next_best_actions`
- Dung `next_best_actions` lam `what_to_improve` de giu backward-compatible UI text.

### 3.2 `api.py`

- Nang `API_PHASE` len Phase 23.
- Nang version API len `0.23.0`.

### 3.3 Tests

Cap nhat:

- `tests/test_candidate_job_reranker.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`

Them moi:

- `tests/test_skill_gap_explainer.py`

## 4. Output contract

Moi `top_job` candidate-side co them:

```json
{
  "skill_gap_summary": {
    "missing_must_have_count": 0,
    "weak_evidence_count": 0,
    "optional_growth_count": 1,
    "presentation_gap_count": 0
  },
  "skill_gaps": {
    "missing_must_have": [],
    "weak_evidence": [],
    "optional_growth": [],
    "presentation_gaps": []
  },
  "cv_improvement_suggestions": [],
  "next_best_actions": []
}
```

Contract cu van giu:

- `fit_score`
- `fit_label`
- `fit_summary`
- `why_fit`
- `what_to_improve`

Nen web cu khong bi pha, con web moi co them field de render chi tiet hon.

## 5. Test strategy

Cover cac case:

- Missing must-have duoc dua vao dung nhom.
- Match co `evidence_level <= 1` duoc dua vao `weak_evidence`.
- Nice-to-have missing duoc dua vao `optional_growth`.
- Evidence score thap / gate applied sinh `presentation_gaps`.
- API `/recommend-jobs` tra ve cac field moi.
- `/screening` khong bi anh huong.

## 6. Manual check

Pipeline payload:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

```text
top_jobs[0].skill_gap_summary
top_jobs[0].skill_gaps
top_jobs[0].cv_improvement_suggestions
top_jobs[0].next_best_actions
```

## 7. Risk

### 7.1 Suggestion qua chung chung

Risk:

```text
Goi y CV nghe dung cho moi job, khong dua tren gap that.
```

Giam thieu:

- build tu requirement gap that;
- uu tien missing skill va weak evidence;
- gioi han `next_best_actions` ngan gon.

### 7.2 Suggestion khong trung thuc

Risk:

```text
He thong vo tinh khuyen ung vien them skill ma chua co that.
```

Giam thieu:

- wording co dieu kien:
  `If you have real experience...`
- khong sinh bullet noi dung ao.

### 7.3 Output qua dai cho web

Risk:

```text
Response nhieu text, card UI kho hien thi.
```

Giam thieu:

- dung `skill_gap_summary` cho badge/count;
- dung `next_best_actions` cho list ngan;
- de `cv_improvement_suggestions` cho modal/detail view.
