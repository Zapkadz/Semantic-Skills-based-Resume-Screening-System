# Phase 22 - Candidate-side Reranking with the Core Scorer

## 1. Muc tieu phase

Phase 21 da giai quyet duoc bai toan retrieval:

```text
1 CV
  -> build candidate query profile
  -> retrieve top-N jobs
```

Nhung hien tai candidate-side pipeline van dang rerank theo mot cach "dung duoc" nhung chua tach bach ro rang:

- retrieval da co;
- fit score da co;
- nhung logic candidate-side reranking van nam chen trong pipeline;
- label va output van con dam employer-side flavor.

Muc tieu cua Phase 22 la:

```text
tach candidate-side reranking thanh mot lop rieng,
van tai su dung core scorer hien co,
nhung chuyen output thanh fit-centric thay vi recruiter-centric.
```

Noi ngan gon:

```text
Phase 21 = lay dung top-N jobs kha nang
Phase 22 = cham ky va xep hang lai top-N do cho dung voi ung vien
```

## 2. Van de can giai quyet

Sau Phase 21, candidate-side flow da co:

```text
retrieval_score
fit_score
```

nhung van con 4 van de:

### 2.1 Reranking chua thanh mot module rieng

Hien tai viec score tung job va sort fit score dang nam trong
`src/job_recommendation_pipeline.py`.

Dieu nay co nhung bat cap:

- kho test rieng cho candidate-side reranking;
- kho mo rong logic label/fit band;
- kho giai thich ro retrieval vs reranking khi bao ve.

### 2.2 Label van mang huong employer-side

Core scorer hien tai sinh label:

- `Strong Review`
- `Review`
- `Maybe Review`
- `Low Priority`
- `Not Enough Evidence`

Nhung voi candidate-side, nguoi dung khong doc theo goc nhin nha tuyen dung.
Ung vien can nhin theo huong:

- `Strong Fit`
- `Good Fit`
- `Potential Fit`
- `Stretch`
- `Low Fit`

### 2.3 Chua tach ro retrieval signal va fit signal trong final ordering

Retrieval score chi nen giup:

```text
loc tap JD kha nang
```

khong nen "len tieng" qua manh trong final ranking.

Phase 22 can chot ro:

```text
retrieval = shortlist
reranking = final top_k ordering
```

### 2.4 Chua co candidate-side fit explanation du ban chat

Ung vien khong chi can biet:

```text
job nay duoc xep top 1
```

ma con can biet:

- vi sao no phu hop;
- no la "strong fit" hay "career stretch";
- neu thieu, thieu o tang nao:
  - hard skills;
  - evidence;
  - seniority;
  - domain;
  - experience.

## 3. Nguyen tac thiet ke

### 3.1 Khong viet AI moi

Phase 22 van phai tai su dung:

- `score_candidate(...)`
- `hard_skill_gate`
- `evidence detection`
- `open-set matching`
- `multilingual embedding`

Khong train model moi, khong goi GPT trong core.

### 3.2 Tach module candidate-side reranker rieng

Can tao mot lop rieng:

```text
src/candidate_job_reranker.py
```

de:

- nhan `candidate_profile`
- nhan `retrieved_jobs`
- score chi tiet tung job
- map employer-side score sang candidate-side fit label
- sort final top_k

### 3.3 Giu employer-side screening on dinh

Phase 22 chi dong vao:

- candidate-side recommendation flow
- candidate-side API output

Khong duoc lam lech:

- `/screening`
- recruiter review card
- employer ranking behavior

### 3.4 Explainable-first

Moi final ranked job phai co:

- `fit_score`
- `fit_label`
- `fit_summary`
- `why_fit`
- `what_to_improve`
- `hard_skill_gate`

Ung vien va giang vien deu co the doc duoc logic.

## 4. Kien truc de xuat

### 4.1 Luong xu ly tong the

```text
Candidate CV
  -> candidate query profile
  -> Phase 21 retrieval top-N jobs
  -> Phase 22 reranker
      -> score tung job bang core scorer
      -> map fit label
      -> build candidate-facing explanation
  -> final top_k jobs
```

### 4.2 Module moi de xuat

Them:

```text
src/candidate_job_reranker.py
tests/test_candidate_job_reranker.py
```

Co the cap nhat:

```text
src/job_recommendation_pipeline.py
src/review_card_generator.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
README.md
docs/dev-learning-log.md
```

### 4.3 Trach nhiem module reranker

Module `candidate_job_reranker.py` nen lam:

1. nhan candidate payload/profile;
2. nhan retrieved jobs;
3. chay screening core tren tung job;
4. lay:
   - `base_score`
   - `final_score`
   - `recommendation`
   - `scores`
   - `hard_skill_gate`
5. map sang:
   - `fit_score`
   - `fit_label`
   - `fit_rationale`
6. sort final jobs theo candidate-side ordering.

## 5. Candidate-side fit model de xuat

### 5.1 Giữ nguyen weighted score core

Weighted score va hard-skill gate hien tai van giu nguyen:

```text
skill_semantic
evidence
experience
seniority
domain
nice_to_have
hard_skill_gate
```

Ly do:

- da test on dinh o employer-side;
- de bao ve do an;
- giu consistency giua hai chieu candidate/employer.

### 5.2 Them candidate-side fit label

Khong nen tra employer label truc tiep cho ung vien.

De xuat map:

```text
Strong Review           -> Strong Fit
Review                  -> Good Fit
Maybe Review            -> Potential Fit
Low Priority            -> Stretch
Not Enough Evidence     -> Low Fit
```

Hoac dung rule ro hon theo `final_score`:

```text
85-100 -> Strong Fit
70-84  -> Good Fit
55-69  -> Potential Fit
40-54  -> Stretch
0-39   -> Low Fit
```

Huong nay giu minh bach hon va khong phu thuoc wording employer-side.

### 5.3 Them candidate-side fit summary

Vi du:

```text
This role is a Good Fit because your core backend stack aligns well,
but you should make AWS evidence more explicit.
```

Neu hard-skill gate bi apply:

```text
This role is currently a Stretch because must-have technical evidence is incomplete.
```

## 6. Final ordering strategy

### 6.1 Retrieval score khong dong vai tro chinh trong final rank

Phase 22 can chot ro:

```text
retrieval_score = shortlist score
fit_score       = final rerank score
```

Final ordering de xuat:

```text
1. fit_score desc
2. evidence desc
3. hard-skill gate passed truoc
4. retrieval_score desc
5. title asc
```

### 6.2 Ly do cua tie-break nay

- `fit_score` moi la person-job fit chi tiet
- `evidence` uu tien CV co bang chung thuc te hon
- `hard_skill_gate` tranh "ao tuong fit"
- `retrieval_score` chi la tie-break

## 7. Candidate-side output de xuat

Moi job trong `top_jobs` nen duoc bo sung/chuẩn hoa:

```json
{
  "job_id": 10,
  "job_title": "Backend Java Developer",
  "retrieval_score": 0.84,
  "fit_score": 86,
  "fit_label": "Strong Fit",
  "fit_summary": "Your backend stack aligns strongly with this role.",
  "hard_skill_gate": {
    "passed": true,
    "applied": false
  },
  "matched_must_have_skills": [],
  "missing_must_have_skills": [],
  "why_fit": [],
  "what_to_improve": [],
  "review_card": {}
}
```

### 7.1 Giu lai review_card hay khong?

Phase 22 de xuat:

- van giu `review_card` trong JSON de debug/noi bo;
- nhung web ung vien khong nhat thiet phai render full recruiter review card;
- UI candidate-side co the doc:
  - `fit_label`
  - `fit_summary`
  - `why_fit`
  - `what_to_improve`

## 8. Pham vi thuc hien cua Phase 22

### 8.1 Trong scope

- tach candidate-side reranking thanh module rieng;
- map candidate-side fit labels;
- them fit summary ngan gon;
- lam ro ordering retrieval vs reranking;
- update output contract candidate-side;
- tests cho fit labels, ordering, hard-skill gate behavior;
- full regression.

### 8.2 Ngoai scope

- chua sua employer-side labels;
- chua them preference-aware ranking;
- chua them click/apply feedback loop;
- chua them GPT rewrite CV;
- chua co UI web.

## 9. Test plan

Them/cap nhat:

```text
tests/test_candidate_job_reranker.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
tests/test_scorer.py
```

### 9.1 Cases can co

1. Candidate-side reranker map `86 -> Strong Fit`.
2. Candidate-side reranker map `72 -> Good Fit`.
3. Candidate-side reranker map `58 -> Potential Fit`.
4. Candidate-side reranker map `45 -> Stretch`.
5. Candidate-side reranker map `25 -> Low Fit`.
6. Job bi hard-skill gate cap thi fit label ha xuong dung muc.
7. Retrieval score khong vuot len tren fit score trong final ordering.
8. Job co fit score bang nhau thi evidence cao hon xep tren.
9. `/screening` van giu label employer-side cu.
10. `/recommend-jobs` tra them `fit_label` va `fit_summary`.

### 9.2 Benchmark thu cong de xuat

Sau khi code:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

- `top_jobs[0].fit_label`
- `top_jobs[0].fit_summary`
- `top_jobs[0].retrieval_score`
- `top_jobs[0].fit_score`
- `top_jobs[0].hard_skill_gate`

## 10. Acceptance criteria

Phase 22 hoan thanh khi:

- candidate-side reranking duoc tach thanh module rieng;
- output co `fit_label` va `fit_summary`;
- retrieval score chi dong vai tro shortlist/tie-break;
- hard-skill gate van duoc ton trong trong candidate-side fit label;
- `/screening` khong bi anh huong;
- full `pytest` pass.

## 11. Rui ro va giam thieu

### 11.1 Fit label gay nham voi employer label

Risk:

```text
Web candidate va employer hien label giong nhau, de gay nham.
```

Giam thieu:

- candidate-side dung `fit_label`
- employer-side van dung `recommendation`

### 11.2 Candidate-side output qua "de thuong"

Risk:

```text
Label candidate-side qua lac quan, lam ung vien hieu nham.
```

Giam thieu:

- hard-skill gate phai co tac dong that
- `Stretch` va `Low Fit` phai duoc giu ro
- `what_to_improve` phai thang than

### 11.3 Retrieval va reranking bi tron

Risk:

```text
Khong ro job len cao do retrieval hay do fit score.
```

Giam thieu:

- giu rieng `retrieval_score`
- giu rieng `fit_score`
- giu `fit_summary`

## 12. Ghi chu cho bao cao

Co the trinh bay:

```text
Sau khi bo sung retrieval layer, he thong tiep tuc tach rieng candidate-side
reranking o Phase 22. Cac JD da retrieve duoc cham chi tiet bang chinh AI
core person-job fit da xay dung cho employer-side, bao gom skill matching,
evidence detection, weighted scoring va hard-skill gate. Tuy nhien, ket qua
duoc dien giai lai theo goc nhin ung vien thong qua cac nhan nhu Strong Fit,
Good Fit, Potential Fit, Stretch va Low Fit. Cach thiet ke nay giu tinh
nhat quan cua score core, nhung giup giao dien ung vien de hieu va dung ngu
cảnh hon.
```

Mot cau ngan khi bao ve:

```text
Phase 22 khong doi bo nao scoring, ma tach rieng lop candidate-side reranking
va dien giai ket qua theo ngon ngu fit thay vi ngon ngu review cua recruiter.
```

