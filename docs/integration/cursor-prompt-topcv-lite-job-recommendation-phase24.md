# Cursor Prompt - Update TOPCV Lite Web for Candidate-side AI Recommendation Phase 24

Copy nguyen prompt duoi day vao Cursor trong project PHP `C:\xampp\htdocs\topcv_lite`.

```text
Ban dang code trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

Candidate-side AI recommendation da duoc nang cap len Phase 24.
Task nay CHI sua web PHP de tich hop dung response moi.
Khong sua code Python AI trong task nay.

==================================================
1. Boi canh quan trong
==================================================

AI Python hien tai co 2 endpoint:

1. POST /screening
   - employer-side
   - 1 JD -> rank nhieu CV

2. POST /recommend-jobs
   - candidate-side
   - 1 CV -> Top matching jobs

Task nay tap trung vao:

POST http://127.0.0.1:8000/recommend-jobs

Employer-side `/screening` KHONG doi contract nghiep vu trong task nay.
Candidate-side `/recommend-jobs` da co them Phase 24 metadata.

==================================================
2. Dieu gi da thay doi o Phase 24
==================================================

Truoc day, mot so job test / placeholder / gan nhu khong co noi dung van co the
xuat hien trong danh sach goi y voi:

- Low Fit
- 20-35 diem

Dieu nay gay hieu nham.

Phase 24 da bo sung:

- JD quality gate
- recommendation eligibility
- excluded_jobs
- job_quality_stats
- warnings
- job_quality cho tung job

Nghia la:

Job khong du du lieu de AI danh gia
KHONG duoc hien nhu mot ket qua "Low Fit" binh thuong nua.

Phai tach ro:

1. Job thuc su Low Fit
2. Job khong du du lieu JD

==================================================
3. Nhung loi cu phai tranh lap lai
==================================================

Da tung gap cac loi sau:

1. Web gui JD dang HTML tho tu DB
   (<p>, <strong>, &nbsp;, bullet HTML...)

2. Web gui cv_text qua ngan / khong du cau truc

3. Web dung nham field employer-side:
   - lay `recommendation`
   - thay vi `fit_label`

4. Web hien job test/rong nhu mot job "Low Fit" that

Task nay phai sua cho dung:

- van clean plain text truoc khi gui AI
- van dung `fit_label` lam nhan chinh candidate-side
- khong hien `excluded_jobs` trong danh sach fit jobs

==================================================
4. Muc tieu task web nay
==================================================

Hay cap nhat candidate-side UI/flow de:

1. goi `POST /recommend-jobs` nhu hien tai
2. render dung `top_jobs`
3. render them `excluded_jobs` theo mot nhom rieng
4. render `job_quality_stats`
5. render `warnings`
6. neu job bi excluded thi KHONG hien no nhu "Low Fit"

Neu web hien tai da co candidate-side recommendation page hoac component,
hay inspect codebase va cap nhat dung cho no.

==================================================
5. Request body web van gui nhu cu
==================================================

Web van gui:

{
  "candidate": {
    "candidate_id": 456,
    "candidate_name": "Nguyen Van A",
    "cv_text": "plain text CV sach",
    "headline": "...",
    "summary": "...",
    "skills": [...],
    "work_experience": [...],
    "projects": [...],
    "education": [...],
    "certifications": [...]
  },
  "jobs": [
    {
      "job_id": 10,
      "job_title": "Backend Java Developer",
      "requirements": [...],
      "nice_to_have": [...],
      "responsibilities": [...],
      "description": "plain text"
    }
  ],
  "options": {
    "top_k": 10,
    "retrieval_top_n": 50
  }
}

Van bat buoc:

- clean HTML -> plain text truoc khi gui
- khong gui rich text tho
- cv_text phai la plain text co heading ro rang

==================================================
6. Response moi can web doc
==================================================

Response Phase 24 co them:

{
  "candidate": {...},
  "top_jobs": [...],
  "excluded_jobs": [
    {
      "job_id": 99,
      "job_title": "Test",
      "job_quality": {
        "quality_score": 0,
        "quality_label": "insufficient_jd_data",
        "recommendation_eligible": false,
        "flags": [...],
        "reasons": [...]
      }
    }
  ],
  "retrieval_stats": {...},
  "job_quality_stats": {
    "jobs_received": 20,
    "eligible_jobs": 14,
    "excluded_jobs": 6
  },
  "warnings": [
    "6 jobs were excluded because the JD content was not strong enough for reliable AI recommendation."
  ]
}

Moi item trong `top_jobs` co them:

{
  "job_quality": {
    "quality_score": 78,
    "quality_label": "eligible_with_warning",
    "recommendation_eligible": true,
    "flags": [...],
    "reasons": [...]
  }
}

==================================================
7. Quy tac render candidate-side dung
==================================================

### 7.1 Danh sach job goi y chinh

Chi render `top_jobs` trong danh sach chinh.

KHONG dua `excluded_jobs` vao cung table/list fit jobs.

### 7.2 Nhan chinh candidate-side

Trong danh sach chinh, dung:

- `fit_label`
- `fit_score`
- `fit_summary`

Khong dung `recommendation` employer-side lam nhan chinh.

### 7.3 Hien canh bao chat luong JD

Neu `top_job.job_quality.quality_label == "eligible_with_warning"`:

- hien mot badge nho nhu:
  - `JD ngắn`
  - `JD cần xem lại`
  - `Dữ liệu JD hạn chế`

Chon wording ngon, trung tinh, khong qua gay gắt.

### 7.4 Hien excluded jobs o khu rieng

Them 1 section rieng, co the la collapse/accordion:

`Tin không đủ dữ liệu để AI đánh giá`

Trong do moi row hien:

- job_title
- company
- location neu co
- quality_label
- 1-2 ly do chinh tu `job_quality.reasons`
- button `Xem tin`

Khong hien fit score cho excluded jobs.

==================================================
8. Empty state va warning state moi
==================================================

Can bo sung 3 state quan trong:

### 8.1 top_jobs rong, excluded_jobs > 0

Hien thong diep:

`Hiện chưa có tin tuyển dụng đủ dữ liệu để AI gợi ý chính xác.`

va ben duoi co the hien:

`Một số tin đã bị loại vì mô tả tuyển dụng quá ngắn hoặc thiếu yêu cầu công việc.`

### 8.2 top_jobs > 0, excluded_jobs > 0

Hien top_jobs binh thuong.
Ben tren hien warning strip nho:

`Một số tin đã bị loại khỏi AI recommendation vì dữ liệu JD chưa đủ mạnh.`

### 8.3 top_jobs > 0, warning empty

Render binh thuong.

==================================================
9. UI de xuat cho dung phong cach TOPCV Lite
==================================================

Hay giu phong cach:

- sach
- bang/list de scan nhanh
- khong marketing style
- khong card trong card

Khuyen nghi layout:

### 9.1 Summary strip

Hien 3 chi so:

- `Jobs analyzed`
- `Eligible jobs`
- `Excluded jobs`

Lay tu `job_quality_stats`.

### 9.2 Main results table

Columns de xuat:

- `#`
- `Việc làm`
- `Độ phù hợp`
- `Thiếu hụt`
- `Thao tác`

Trong cot do phu hop:

- badge `fit_label`
- `fit_score`
- neu co, badge phu `JD ngắn`

Trong cot thieu hut:

- `missing_must_have_count`
- `optional_growth_count`
- `weak_evidence_count`

### 9.3 Excluded jobs section

Dat ben duoi danh sach chinh, collapse mac dinh dong.

Tieu de:

`Tin không đủ dữ liệu để AI đánh giá ({count})`

### 9.4 Detail modal

Voi `top_jobs`, modal van hien:

- why_fit
- skill_gap_summary
- skill_gaps
- next_best_actions
- review_card evidence highlights

Them 1 block nho:

`Chất lượng JD`
- quality_score
- quality_label
- reasons neu co

==================================================
10. Logging va debug
==================================================

Neu web da co che do debug local cho AI request/response, hay giu lai.

Can log them:

- top_jobs count
- excluded_jobs count
- warning count

Khi debug local:

- luu response JSON
- check xem excluded jobs da tach rieng chua

==================================================
11. Acceptance criteria
==================================================

Sau khi sua xong:

1. Web candidate-side van goi duoc `/recommend-jobs`.
2. Job that van hien trong `top_jobs`.
3. Job test / placeholder / rong khong hien nhu `Low Fit`.
4. `excluded_jobs` duoc render o section rieng.
5. Neu top_jobs rong vi toan bo job xau, UI hien empty state dung nghia.
6. UI dung `fit_label` lam nhan chinh candidate-side.
7. Web van clean plain text truoc khi gui AI.

==================================================
12. Cach lam mong muon
==================================================

Hay:

1. inspect codebase candidate-side recommendation hien tai
2. tim file render danh sach job AI goi y
3. cap nhat service/API parser theo contract Phase 24
4. cap nhat UI theo cac quy tac tren
5. bao ro:
   - file nao da sua
   - field nao dang dung tu response
   - cach test local

Neu web hien tai chua co section candidate-side recommendation ro rang,
hay de xuat diem dat feature hop ly nhat va implement luon theo huong toi uu UX.
```
