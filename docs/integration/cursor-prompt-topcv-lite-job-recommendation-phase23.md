# Cursor Prompt - Integrate Candidate-side AI Job Recommendation (Phase 23) into TOPCV Lite

Copy nguyen prompt duoi day vao Cursor trong project PHP `C:\xampp\htdocs\topcv_lite`.

```text
Ban dang code trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

Khong copy AI project vao trong web PHP.
Khong goi Python CLI cho feature nay.
Hay goi HTTP API noi bo dang chay tai:

http://127.0.0.1:8000

Muc tieu task nay:

Tich hop chuc nang candidate-side:

1 CV cua ung vien
  -> goi AI /recommend-jobs
  -> nhan Top 10 JD phu hop
  -> hien ly do phu hop
  -> hien skill-gap
  -> hien goi y nen bo sung/lam ro gi trong CV

Day la feature moi cho phia ung vien, KHONG thay the feature cu employer-side `/screening`.

==================================================
1. Hieu dung trang thai AI hien tai
==================================================

Python AI hien tai da co cung luc 2 endpoint:

1. POST /screening
   - Employer-side
   - 1 JD -> rank nhieu CV

2. POST /recommend-jobs
   - Candidate-side
   - 1 CV -> top matching JDs

Chi can 1 API server uvicorn dang chay.
Khong can tat endpoint nay de bat endpoint kia.
Ca 2 endpoint cung song song trong cung service.

Health check:

GET http://127.0.0.1:8000/health

Khi test, hay kiem tra:
- API dang chay
- phase dang dung
- embedding co dang bat khong neu local da cau hinh BGE-M3

==================================================
2. Nhung loi cu da tung gap - phai tranh lap lai
==================================================

Trong cac lan tich hop truoc, da co may loi lon:

1. Web gui JD dang HTML thang tu DB
   Vi du co:
   - <p>, <strong>, <ul>, <li>, &nbsp;
   - bullet HTML
   - xuong dong xau

   Hau qua:
   - AI parse requirement sai
   - score lech
   - open-set requirement bi nhiu

2. Web gui `cv_text` khong du sach hoac qua ngan
   Hau qua:
   - AI chi nhan ra title/years
   - skill evidence bi thieu
   - score thap hoac meo

3. Map sai candidate/job
   Vi du:
   - row tren web la ung vien A
   - payload gui CV cua ung vien B
   - hoac luu ket qua ve sai row DB

4. Web test tren API phase cu
   Hau qua:
   - web khong thay field moi
   - so sanh ket qua bi sai

5. UI doc nham field
   Vi du:
   - lay `recommendation` employer-side de hien cho candidate-side
   - trong khi candidate-side phai uu tien `fit_label`, `fit_summary`,
     `skill_gap_summary`, `next_best_actions`

Voi task nay, bat buoc phai:

- clean plain text truoc khi gui AI
- log request/response khi debug local
- map dung `candidate_id` / `job_id`
- doc dung contract response

==================================================
3. Feature can lam tren web
==================================================

Hay tich hop mot trang/luong candidate-side de ung vien co the:

- mo CV/ho so hien tai cua minh
- bam nut "AI goi y cong viec phu hop"
- web lay CV text cua ung vien
- web lay danh sach tat ca JD active/published con han
- gui sang POST /recommend-jobs
- nhan Top 10 jobs
- hien danh sach xep hang + giai thich

Neu project da co trang:
- candidate/profile
- candidate/cv
- candidate/dashboard
- jobs/list

hay inspect va chon diem dat feature hop ly nhat.

Khuyen nghi UX:

1. Dat CTA tai trang CV hoac Ho so ca nhan:
   "AI goi y cong viec phu hop"

2. Sau khi bam:
   - hoac render ngay trong cung trang
   - hoac chuyen sang mot trang ket qua rieng, vi du:
     `/candidate/job_recommendations.php`

==================================================
4. Dinh huong UI - thiet ke cho dung chat san pham
==================================================

Hay giu phong cach nhat quan voi TOPCV Lite hien co:
- sach
- de scan
- khong khoa trinh bay hoa my
- uu tien bang/list va modal/detail

Khong lam landing page.
Khong lam hero marketing.
Khong lam card trong card.

Khuyen nghi UI candidate-side:

### 4.1 Header block

- Tieu de: `AI goi y cong viec phu hop`
- Dong mo ta ngan:
  `Phan tich CV hien tai va goi y Top cong viec phu hop cung diem can cai thien.`
- Nut chinh:
  `Chay AI goi y`
- Badge nho:
  - so JD da xet
  - lan chay gan nhat
  - trang thai API

### 4.2 Summary strip

Sau khi co ket qua, hien 3-4 chi so ngan:

- `Top matches returned`
- `Strong/Good Fit count`
- `Jobs with missing must-have skills`
- `Jobs with optional growth only`

### 4.3 Results table or dense list

Moi job nen hien:

- Rank
- Job title
- Company name neu co trong DB
- Fit label
- Fit score
- Matched must-have count
- Missing must-have count
- Optional growth count
- Action: `Xem chi tiet`
- Action neu da co san web: `Xem tin` / `Ung tuyen`

Khuyen nghi label badge:

- `Strong Fit`
- `Good Fit`
- `Potential Fit`
- `Stretch`
- `Low Fit`

### 4.4 Detail modal / detail drawer

Khi bam `Xem chi tiet`, hien 4 nhom thong tin:

1. `Why this job fits`
   - render `why_fit`
   - render `fit_summary`

2. `Missing or weak areas`
   - `skill_gap_summary`
   - `skill_gaps.missing_must_have`
   - `skill_gaps.weak_evidence`
   - `skill_gaps.optional_growth`

3. `How to improve your CV`
   - `next_best_actions`
   - `cv_improvement_suggestions`

4. `Technical evidence`
   - `matched_must_have_skills`
   - `review_card.evidence_highlights`
   - chi hien co chon loc, khong dump raw JSON

### 4.5 Empty / warning states

Can co state than thien cho:

- chua co CV text
- khong co JD active
- API chua bat
- AI tra ve rong
- ket qua fit thap

Vi du:

- `CV hien tai chua du du lieu text de AI phan tich.`
- `Chua co tin tuyen dung active de goi y.`
- `Khong ket noi duoc AI service. Vui long thu lai sau.`

==================================================
5. Contract request - web phai gui nhu the nao
==================================================

Endpoint:

POST http://127.0.0.1:8000/recommend-jobs
Content-Type: application/json

Body:

{
  "candidate": {
    "candidate_id": 456,
    "candidate_name": "Nguyen Van A",
    "email": "candidate@example.com",
    "phone": "0900000000",
    "headline": "Backend Developer",
    "summary": "...",
    "skills": ["Java", "Spring Boot"],
    "work_experience": [...],
    "projects": [...],
    "education": [...],
    "certifications": [...],
    "cv_text": "plain text CV o day",
    "cv_file_path": "optional"
  },
  "jobs": [
    {
      "job_id": 10,
      "job_title": "Backend Java Developer",
      "requirements": [
        "Java",
        "Spring Boot",
        "REST API",
        "SQL"
      ],
      "nice_to_have": [
        "AWS"
      ],
      "responsibilities": [
        "Build RESTful APIs."
      ]
    }
  ],
  "options": {
    "top_k": 10,
    "retrieval_top_n": 50
  }
}

Notes quan trong:

1. `candidate.cv_text` la field quan trong nhat.
2. `jobs` nen la danh sach JOB ACTIVE/PUBLISHED/CON HAN.
3. Neu DB chua tach duoc `requirements`, `nice_to_have`, `responsibilities`,
   co the dung:
   - `title`
   - `job_description_text`
   nhung van phai clean plain text truoc.
4. AI support ca alias:
   - `job_title` hoac `title`
   - `cv_text` hoac `resume_text`
   - `job_description_text` hoac `raw_text` hoac `description`

==================================================
6. Cach clean JD/CV truoc khi gui AI
==================================================

Day la bat buoc.

Web khong duoc gui HTML tho vao AI.

Hay tao helper clean text, vi du:

- html_entity_decode(...)
- strip_tags(...)
- doi `<br>`, `</p>`, `</li>` thanh xuong dong truoc khi strip
- bo `&nbsp;`
- normalize multiple blank lines
- trim space tung dong
- giu bullet text thanh tung line

Yeu cau:

### 6.1 Clean JD text

Neu JD luu rich text HTML trong DB, phai convert ve plain text:

Khong gui:
`<p><strong>Requirements</strong></p><ul><li>Java</li>...`

Nen gui:

Requirements:
- Java
- Spring Boot

### 6.2 Clean CV text

Neu ung vien co CV online HTML/structured:
- build plain text co heading ro rang

Neu la extracted text tu PDF:
- normalize whitespace
- dam bao khong rong

Neu chi co mot vai field roi rac:
- tu build `cv_text` theo template co heading:

{candidate_name}
{headline}

Summary:
...

Skills:
- ...

Work Experience:
...

Projects:
...

Education:
...

==================================================
7. Contract response - web phai doc nhu the nao
==================================================

Response candidate-side hien tai co dang:

{
  "candidate": {
    "candidate_id": 456,
    "candidate_name": "Nguyen Van A",
    "source_file": "candidate-456.txt",
    "cv_file_path": ""
  },
  "top_jobs": [
    {
      "rank": 1,
      "job_id": 10,
      "job_title": "Backend Java Developer",
      "retrieval_rank": 1,
      "retrieval_score": 0.7183,
      "retrieval_reasons": [
        "Strong must-have skill overlap."
      ],
      "fit_score": 86,
      "fit_label": "Strong Fit",
      "fit_summary": "This role is a Strong Fit because ...",
      "base_score": 86,
      "recommendation": "Strong Review",
      "scores": {...},
      "hard_skill_gate": {...},
      "matched_must_have_skills": [...],
      "missing_must_have_skills": [...],
      "optional_strengths": [...],
      "why_fit": [...],
      "what_to_improve": [...],
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
      "cv_improvement_suggestions": [...],
      "next_best_actions": [...],
      "requirement_group_summary": {...},
      "taxonomy_coverage": {...},
      "screening_confidence": {...},
      "open_set_requirements": [...],
      "requirement_groups": {...},
      "review_card": {...}
    }
  ],
  "retrieval_stats": {
    "jobs_received": 3,
    "jobs_indexed": 3,
    "jobs_retrieved": 2,
    "jobs_reranked": 2,
    "top_k": 2,
    "retrieval_top_n": 2,
    "retrieval_applied": true
  }
}

Quy tac render:

### 7.1 Candidate-side field uu tien

Trong UI candidate-side, uu tien:

- `fit_label`
- `fit_score`
- `fit_summary`
- `why_fit`
- `skill_gap_summary`
- `skill_gaps`
- `next_best_actions`

### 7.2 Field employer-side chi de detail/debug

Khong dung `recommendation` employer-side lam label chinh cho candidate.
No van duoc giu lai de debug/noi bo.

Candidate-side phai hien `fit_label`, KHONG phai `recommendation`.

### 7.3 Dung `skill_gap_summary` de render badge/count nhanh

Vi du:
- Missing must-have: 2
- Weak evidence: 1
- Optional growth: 3

### 7.4 Dung `next_best_actions` cho list ngan

Khong dump full `cv_improvement_suggestions` len card compact.
Card/list chi nen show 2-4 actions tu `next_best_actions`.

==================================================
8. Logic lay du lieu jobs tu DB
==================================================

Hay inspect schema job hien co va chon job theo logic:

- published / active
- chua het han
- co the ung vien xem/ung tuyen duoc

Danh sach jobs gui sang AI nen la tap JDs dang mo.

Khong gui:
- draft
- deleted
- expired
- hidden

Neu so luong job rat lon, van co the gui danh sach active truoc.
MVP nay chap nhan gui nhieu job active, vi AI da co retrieval layer noi bo.

Khuyen nghi options:

- `top_k = 10`
- `retrieval_top_n = 50`

==================================================
9. Logging va debug local
==================================================

Can them debug local co the bat/tat bang config.

Toi thieu log:

- request timestamp
- candidate_id
- jobs_count
- top_k
- HTTP status
- response size
- top_jobs count
- top 3 job_id + fit_score + fit_label

Neu debug local bat:

- ghi request JSON vao file
- ghi response JSON vao file

Vi du folder:

C:\topcv_ai_runtime\api-debug\

Muc tieu la de doi chieu:
- web gui text da sach chua
- jobs list co dung khong
- response AI co dung contract khong

==================================================
10. Database / storage cho ket qua candidate-side
==================================================

Inspect project truoc khi chon cach luu.

Khuyen nghi:

Neu feature nay chi de show ket qua lan chay hien tai, co the:
- khong can luu DB ngay
- luu session/cache/log local

Neu muon co lich su goi y:
- tao bang rieng, vi du `ai_job_recommendation_runs`
- hoac `candidate_ai_job_matches`

Toi thieu co the luu:
- candidate_id
- request_snapshot_json
- response_json
- top_job_count
- created_at

Nhung MVP co the chua can luu DB neu project web chua can lich su.

Hay uu tien:
- feature chay duoc
- UI hien duoc ket qua
- debug de

==================================================
11. Canh bao nghiep vu - phai hien ro tren web
==================================================

Feature nay hien tai la Phase 23.
Nghia la:

- da co Top jobs theo CV
- da co skill-gap va CV improvement suggestions
- CHUA co preference-aware ranking

Vi vay web nen hien note ngan, vi du:

`Ket qua hien tai duoc xep hang dua tren muc do phu hop giua CV va JD. Chua tinh uu tien ca nhan nhu muc luong, dia diem, hinh thuc lam viec.`

Dieu nay rat quan trong de tranh user hieu nham.

==================================================
12. Acceptance criteria
==================================================

Sau khi lam xong:

1. Candidate co the bam nut chay AI goi y cong viec.
2. PHP build duoc `candidate.cv_text` plain text sach.
3. PHP lay duoc danh sach job active va build duoc `jobs[]`.
4. Web POST duoc toi `/recommend-jobs`.
5. Web hien duoc Top 10 jobs.
6. Moi job hien duoc:
   - fit label
   - fit score
   - why fit
   - missing/weak/optional gap counts
   - next best actions
7. Modal/detail hien duoc:
   - matched must-have skills
   - missing must-have skills
   - skill-gap details
   - CV improvement suggestions
8. Neu API loi, UI hien message than thien.
9. Neu CV text khong du, UI hien huong dan bo sung CV.
10. Khong gui HTML tho sang AI.

==================================================
13. Cach lam mong muon tu Cursor
==================================================

Hay:

1. Doc codebase va tim:
   - candidate profile / CV pages
   - job listing pages
   - schema DB lien quan candidate/jobs
   - helper config / cURL / logging hien co

2. De xuat file se sua/tao.

3. Implement toan bo luong candidate-side AI recommendation.

4. Them UI theo huong dense, de scan, nhat quan voi TOPCV Lite.

5. Bao ro:
   - file nao da sua
   - payload web gui sang AI co dang nao
   - response field nao dang render
   - cach test local

Neu gap cho nao schema web khong du de build `cv_text`, dung tu suy dien.
Hay chi ro field con thieu va de xuat fallback hop ly nhat.
```
