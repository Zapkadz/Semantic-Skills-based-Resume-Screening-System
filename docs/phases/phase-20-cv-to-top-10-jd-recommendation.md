# Phase 20 - CV to Top 10 JD Recommendation Foundation

## 1. Muc tieu phase

Phase 20 mo rong he thong tu bai toan:

```text
1 JD -> xep hang nhieu CV
```

sang bai toan nguoc lai:

```text
1 CV -> tim Top 10 JD phu hop nhat
```

Muc tieu cua phase nay khong phai viet mot "AI khac" tu dau, ma la:

- tai su dung toi da AI screening core hien co;
- tach rieng employer flow va candidate flow de tranh anh huong chuc nang cu;
- tao nen tang kien truc ro rang de co the them retrieval, reranking, giai thich va goi y cai thien CV trong cac phase sau.

Noi ngan gon:

```text
Employer flow:
  JD -> rank candidates

Candidate flow:
  CV -> rank jobs
```

## 2. Cau hoi thiet ke quan trong nhat

Can tra loi ro ngay tu dau:

```text
Tinh nang CV -> Top 10 JD co duong den rieng hay sua truc tiep screening cu?
```

Cau tra loi de xuat:

```text
Khong sua truc tiep screening cu.
Tao candidate-side pipeline va API endpoint rieng.
Chi tai su dung cac module core dung chung.
```

Dieu nay giup:

- khong pha `POST /screening` hien tai;
- web employer khong bi anh huong;
- co the phat trien candidate recommendation doc lap;
- de regression test vi moi flow co contract rieng.

Kien truc an toan:

```text
Shared core
  - document loader
  - resume parser
  - jd parser
  - taxonomy + normalization
  - requirement extractor
  - JD requirement classifier
  - embedding matcher
  - evidence detector
  - scorer
  - review/explanation helpers

Employer flow
  - screening_pipeline.py
  - POST /screening

Candidate flow
  - job_recommendation_pipeline.py
  - POST /recommend-jobs
```

## 3. Bai toan nghiep vu can giai quyet

Voi vai tro ung vien, he thong can:

1. Nhan CV cua ung vien.
2. So sanh CV do voi tap JD dang active.
3. Tra ve Top 10 JD phu hop nhat.
4. Giai thich vi sao tung JD phu hop.
5. Noi ro ung vien dang thieu gi de "an diem" hon voi JD do.

Output nghiep vu ky vong:

```text
Top 10 cong viec phu hop
  + diem match
  + ly do phu hop
  + ky nang da match
  + ky nang con thieu
  + goi y nen bo sung gi trong CV
```

Day khong phai bai toan collaborative filtering co lich su click/ung tuyen lon.
Trong giai doan do an va du lieu hien tai, day la bai toan:

```text
content-based candidate-job recommendation
+ explainable reranking
+ multilingual skill/evidence matching
```

## 4. Co so hoc thuat va ly do chon huong di

Phase 20 nen di theo huong:

```text
retrieve -> filter -> rerank -> explain
```

thay vi nhay thang vao black-box recommendation.

### 4.1 Vi sao nen bat dau bang content-based

Voi do an nay, he thong chua co:

- lich su click/ung tuyen day du;
- user-item interaction matrix lon;
- feedback du lieu thuc te de hoc collaborative filtering.

Vi vay, V1 hop ly nhat la:

```text
Lay CV lam trung tam
-> trich xuat skill/evidence/profile
-> tim cac JD co noi dung phu hop
-> rerank bang person-job fit score
```

Huong nay phu hop voi:

- cold-start cho ung vien moi;
- de giai thich khi bao ve;
- co the tai su dung core screening hien co.

### 4.2 Nguon nen hoc hoi

#### PJFNN

Paper PJFNN mo ta bai toan person-job fit la matching giua requirement cua job va kinh nghiem/skill cua candidate.

Nguon:

- https://ar5iv.labs.arxiv.org/html/1810.04040

Y tuong co the hoc:

```text
Khong chi match keyword.
Can match requirement cua job voi evidence trong ho so candidate.
```

#### APJFNN

APJFNN mo rong person-job fit bang cach modeling requirement va ung vien o muc cau/segment.

Nguon:

- https://arxiv.org/abs/1812.08947

Y tuong co the hoc:

```text
Moi JD khong nen chi la 1 vector tho.
Nen co requirement groups va evidence groups.
```

#### Your Career Path Matters in Person-Job Fit

Paper AAAI 2024 nhan manh qua trinh nghe nghiep/career path cung quan trong trong person-job fit.

Nguon:

- https://ojs.aaai.org/index.php/AAAI/article/view/28685/29329

Y tuong co the hoc:

```text
Ngoai skill hien tai, candidate recommendation co the can nhac do gan ve
seniority/domain/career direction.
```

#### Explainable Person-Job Recommender Review

Tong quan 2025 cho thay bai toan person-job recommendation can:

- explainability;
- fairness;
- trust;
- minh bach ly do goi y.

Nguon:

- https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1660548/full

Y tuong ap dung:

```text
Top 10 JD khong chi co score.
Phai co "why this job" va "what to improve".
```

#### Job Recommender System Review

Tong quan 2025 cho thay content-based va hybrid la huong hop ly khi du lieu han che hoac cold-start manh.

Nguon:

- https://link.springer.com/article/10.1186/s40537-025-01173-y

#### Skill Scanner 2023

Paper Skill Scanner mo ta huong trich xuat skill, vector hoa, clustering va so khop skill giua job seeker, employer va education.

Nguon:

- https://online-journals.org/index.php/i-jac/article/view/34779

Y tuong ap dung:

```text
CV -> skill profile
JD -> skill profile
match -> gap -> suggestion
```

## 5. Nguyen tac thiet ke

### 5.1 Khong tao AI moi neu core hien tai da dung duoc

Khong can viet mot engine khac hoan toan cho candidate-side.

Nen tai su dung:

- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `src/embedding_matcher.py`
- `src/evidence_detector.py`
- `src/requirement_extractor.py`
- `src/jd_requirement_classifier.py`
- `src/scorer.py`
- `src/review_card_generator.py`

Phan moi chu yeu nam o:

- retrieval job candidates;
- candidate-to-job orchestration;
- explanation theo huong "goi y cong viec";
- top-k output contract.

### 5.2 Tach rieng orchestration, dung chung core

Can tach ro:

```text
Core logic dung chung
  parse, normalize, match, evidence, scoring

Use-case logic rieng
  employer screening
  candidate job recommendation
```

Neu sau nay sua taxonomy, multilingual embedding, evidence detector, scorer:

- ca hai flow deu huong theo core moi;
- nhung API contract va pipeline van tach rieng;
- regression test se bat loi som.

### 5.3 Explainable-first

Top 10 JD phai giai thich duoc bang ngon ngu nghiep vu:

- cong viec nay hop vi skill nao;
- cong viec nay chua hop o diem nao;
- neu muon ung tuyen, nen bo sung skill/tu khoa/du an nao trong CV.

### 5.4 Local-first, GPT la optional tang nang cao

Core recommendation nen van chay local-first:

- rule-based;
- taxonomy-based;
- multilingual embedding local;
- hard-skill gate.

GPT neu co chi nen la tang VIP/optional sau nay, khong phai dependency bat buoc cua Phase 20.

## 6. Kien truc tong the de xuat

### 6.1 Kien truc muc cao

```text
Candidate CV
  -> parse candidate profile
  -> normalize skills/evidence
  -> candidate query profile

Job catalog
  -> parse all JDs
  -> classify requirements
  -> normalize/index jobs

Retrieval
  -> sparse retrieval
  -> dense multilingual retrieval
  -> union top-N jobs

Reranking
  -> reuse screening core
  -> job-as-target, candidate-as-subject
  -> weighted score + hard-skill gate

Explanation
  -> why fit
  -> missing must-have
  -> optional strengths
  -> what to improve

Output
  -> top 10 jobs
```

### 6.2 Shared core vs new modules

#### Shared core modules

Dung lai:

```text
src/document_loader.py
src/resume_parser.py
src/jd_parser.py
src/skill_taxonomy.py
src/skill_normalizer.py
src/semantic_matcher.py
src/embedding_matcher.py
src/evidence_detector.py
src/requirement_extractor.py
src/jd_requirement_classifier.py
src/scorer.py
src/review_card_generator.py
```

#### New modules de xuat

Can tao moi:

```text
src/job_catalog_loader.py
src/job_retriever.py
src/job_recommendation_pipeline.py
src/candidate_job_reranker.py
src/job_recommendation_explainer.py
tests/test_job_catalog_loader.py
tests/test_job_retriever.py
tests/test_job_recommendation_pipeline.py
tests/test_candidate_job_reranker.py
tests/test_job_recommendation_explainer.py
```

Co the them CLI/API:

```text
recommend_jobs.py
POST /recommend-jobs
```

### 6.3 Ranh gioi an toan de khong anh huong screening cu

Khong sua contract cu:

```text
POST /screening
main.py screening flow
screening_pipeline.py employer use-case
```

Them contract moi:

```text
POST /recommend-jobs
recommend_jobs.py
job_recommendation_pipeline.py
```

Neu can dung lai `scorer.py`, chi nen them wrapper hoac adapter, khong fork score logic thanh 2 ban neu chua can.

## 7. Luong xu ly end-to-end

### 7.1 Buoc 1 - Parse CV thanh candidate profile

Input:

```text
CV text
```

Output:

```json
{
  "candidate_name": "Daniel Kim",
  "headline": "Senior AI Computer Vision Engineer",
  "raw_skills": [],
  "work_experience": [],
  "projects": [],
  "certifications": [],
  "education": []
}
```

Sau do normalize va mo rong evidence candidates tu:

- headline;
- summary;
- skills section;
- work bullets;
- projects;
- certifications.

### 7.2 Buoc 2 - Load va parse job catalog

Moi JD can duoc chuyen thanh `job card` co cau truc:

```json
{
  "job_id": "JD_102",
  "job_title": "Senior AI Computer Vision Engineer",
  "must_have_skills": [],
  "nice_to_have_skills": [],
  "requirement_groups": {},
  "minimum_experience_years": 3,
  "seniority": "Senior",
  "domain": ["Computer Vision", "AI", "Biometrics"]
}
```

### 7.3 Buoc 3 - Retrieval de loc danh sach JD kha nang

Khong nen rerank toan bo hang ngan JD ngay tu dau.

Can retrieval 2 tang:

#### Sparse retrieval

So khop nhanh dua tren:

- title overlap;
- canonical skills overlap;
- domain overlap;
- must-have phrase overlap.

Co the bat dau bang:

```text
keyword overlap / TF-IDF / BM25-like scoring
```

#### Dense multilingual retrieval

Dung embedding local de so khop:

- CV summary + skills + evidence summary
voi
- JD condensed text + requirement summary

Model de xuat:

- `BAAI/bge-m3`
- hoac `intfloat/multilingual-e5-large`

#### Hybrid retrieval

De xuat V1:

```text
Top 50 sparse
U Top 50 dense
-> dedupe
-> top 50-80 candidates for reranking
```

V1 khong can ANN phuc tap.

### 7.4 Buoc 4 - Hard filtering

Neu web co metadata, co the filter them:

- location;
- remote/on-site/hybrid;
- seniority mismatch qua xa;
- salary range;
- employment type.

Phase 20 foundation co the cho cac filter nay la optional.

### 7.5 Buoc 5 - Reranking bang AI core hien co

Day la phan quan trong nhat.

Moi JD candidate se duoc dua vao scoring flow da co:

```text
JD requirements
vs
candidate evidence from CV
```

Tai day ta co the tai su dung:

- rule-based + taxonomy matching;
- open-set matching;
- multilingual embedding;
- evidence detection;
- weighted score;
- hard-skill gate.

Noi cach khac:

```text
Employer flow:
  1 JD -> score many CVs

Candidate flow:
  1 CV -> score many JDs
```

nhung score engine co the la mot.

### 7.6 Buoc 6 - Explain va goi y cai thien CV

Moi JD trong Top 10 can co:

- `why_fit`
- `matched_must_have_skills`
- `missing_must_have_skills`
- `optional_strengths`
- `what_to_improve`

Vi du:

```text
Why fit:
- Strong alignment in Python, Computer Vision, Face Recognition.
- Experience evidence found in liveness detection and anti-spoofing projects.

What to improve:
- Add explicit ONNX deployment evidence.
- Mention mobile/edge optimization metrics if available.
- Surface quantization or pruning work in the CV.
```

## 8. Scoring va ranking strategy de xuat

### 8.1 Khong nen chi dung retrieval score de xep Top 10 cuoi

Retrieval score chi dung de lay ung vien JD kha nang.

Top 10 cuoi nen dua tren:

```text
rerank fit score = AI screening score tai su dung
```

### 8.2 Thanh phan score V1

Co the dung lai logic hien tai:

```text
skill_semantic
evidence
experience
seniority
domain
nice_to_have
hard_skill_gate
```

Khac biet la output duoc dien giai theo huong:

```text
Cong viec nay hop voi CV cua ban den muc nao
```

thay vi:

```text
Ung vien nay hop voi JD den muc nao
```

### 8.3 Tai sao dung cung score core la hop ly

Neu he thong employer-side dang do:

```text
person-job fit
```

thi candidate-side recommendation cung la cung mot bai toan, chi dao chieu query.

Dieu nay giup:

- tinh nhat quan giua hai phia candidate/employer;
- de bao ve do an;
- de maintenance;
- de doi chieu khi test.

### 8.4 Hard-skill gate van can giu

Neu candidate co domain tot nhung thieu qua nhieu must-have hard skills thi:

- job do khong nen len qua cao trong Top 10;
- can bi cap score hoac ha recommendation;
- explanation phai noi ro "career stretch" hay "missing core skills".

## 9. Output contract de xuat

### 9.1 API moi

De xuat endpoint:

```text
POST /recommend-jobs
```

### 9.2 Request schema V1

Phase 20 foundation nen uu tien kieu request de web co the goi duoc ngay:

```json
{
  "candidate": {
    "candidate_id": "cand-001",
    "resume_text": "..."
  },
  "jobs": [
    {
      "job_id": "job-10",
      "title": "Backend Java Developer",
      "job_description_text": "..."
    }
  ],
  "options": {
    "top_k": 10,
    "enable_embedding": true,
    "taxonomy_path": "data/taxonomy/skills.json"
  }
}
```

Ly do chon schema nay:

- web PHP co the doc CV va JD tu DB roi gui len Python API;
- chua can Python doc truc tiep DB web;
- khong buoc phase nay phai co job index phuc tap ngay.

### 9.3 Response schema V1

```json
{
  "candidate": {
    "candidate_id": "cand-001",
    "candidate_name": "Daniel Kim"
  },
  "top_jobs": [
    {
      "job_id": "job-10",
      "job_title": "Backend Java Developer",
      "fit_score": 84,
      "base_score": 86,
      "recommendation": "Review",
      "hard_skill_gate": {
        "passed": true,
        "applied": false
      },
      "matched_must_have_skills": [],
      "missing_must_have_skills": [],
      "optional_strengths": [],
      "why_fit": [],
      "what_to_improve": [],
      "review_card": {}
    }
  ],
  "retrieval_stats": {
    "jobs_received": 100,
    "jobs_retrieved": 50,
    "jobs_reranked": 10
  }
}
```

### 9.4 Output UI nghiep vu

UI candidate-side co the hien:

- Top 10 jobs;
- score badge;
- tag "Strong Fit / Review / Stretch";
- matched skills;
- missing skills;
- goi y "nen bo sung gi vao CV".

## 10. Pham vi thuc hien cua Phase 20

Phase 20 foundation chi nen lam nhung phan can thiet nhat de co mot V1 ben vung:

### 10.1 Trong scope

- them candidate-side pipeline rieng;
- them API endpoint `POST /recommend-jobs`;
- nhan `candidate.resume_text` + danh sach `jobs`;
- parse CV va parse tat ca JDs trong request;
- retrieval co ban de loc top-N jobs;
- rerank bang scorer core hien co;
- tra ve Top 10 jobs;
- tra ve matched/missing skills + explanation co ban;
- them tests rieng cho recommendation flow;
- dam bao khong pha `POST /screening`.

### 10.2 Ngoai scope cua Phase 20

- chua can ket noi truc tiep DB MySQL cua web;
- chua can user history/personalization;
- chua can collaborative filtering;
- chua can feedback loop click/apply;
- chua can GPT rewrite CV;
- chua can online ANN/vector DB;
- chua can scheduler dong bo tat ca JD tu web vao Python runtime.

## 11. Lo trinh cac phase tiep theo cho feature nay

### Phase 20 - Candidate Job Recommendation Foundation

Muc tieu:

- endpoint moi;
- request/response contract moi;
- scoring reused;
- top 10 jobs tu danh sach jobs web gui vao.

### Phase 21 - Job Catalog Retrieval and Indexing

Muc tieu:

- xay `job catalog loader`;
- tien xu ly JD thanh condensed searchable documents;
- hybrid retrieval sparse + dense;
- toi uu top-N truoc reranking.

### Phase 22 - Candidate-to-Job Reranking and Recommendation Labels

Muc tieu:

- adapter tai su dung scorer core cho candidate-side;
- tao nhan `Strong Fit`, `Good Fit`, `Stretch`, `Low Fit`;
- hard-skill gate theo huong candidate recommendation.

### Phase 23 - Skill-gap Explanation and CV Improvement Suggestions

Muc tieu:

- giai thich `why this job`;
- giai thich `what is missing`;
- sinh goi y "bo sung evidence nao vao CV";
- uu tien evidence tu experience/project/certification.

### Phase 24 - Preference-aware Ranking

Muc tieu:

- dua them location, work mode, salary, seniority, domain preference vao ranking;
- tach `fit_score` va `preference_fit_score`.

### Phase 25 - Feedback Loop and Behavioral Personalization

Muc tieu:

- luu click/save/apply history;
- hoc them tu hanh vi user;
- mo duong cho hybrid recommender trong tuong lai.

## 12. Test plan

Can them/cap nhat tests:

```text
tests/test_job_catalog_loader.py
tests/test_job_retriever.py
tests/test_candidate_job_reranker.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
```

### 12.1 Cases can co

1. Recommendation flow khong lam thay doi ket qua `POST /screening`.
2. CV input rong hoac JD list rong duoc bao loi ro rang.
3. Candidate-side pipeline parse CV dung.
4. Job list duoc parse va classify requirement groups dung.
5. Retrieval dua job lien quan vao top-N.
6. Reranking dua job phu hop hon len tren.
7. Job thieu hard skills bi cap score/recommendation.
8. Output tra ve dung `top_k = 10`.
9. Explanation co `why_fit` va `what_to_improve`.
10. API response backward-compatible voi employer flow.
11. Embedding tat van chay, nhung retrieval/explanation giam muc semantic.
12. Multilingual JD/CV van cho ket qua hop ly khi embedding bat.

### 12.2 Benchmark thu cong de xuat

CLI/fixture benchmark:

```powershell
pytest
```

API benchmark:

```powershell
uvicorn api:app --host 127.0.0.1 --port 8000
```

Sau do goi:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

## 13. Acceptance criteria cua Phase 20

Phase 20 duoc xem la hoan thanh khi:

- co endpoint rieng `POST /recommend-jobs`;
- employer screening flow cu van chay binh thuong;
- he thong nhan 1 CV + nhieu JD va tra ve top 10;
- top 10 jobs da duoc rerank boi AI core, khong chi la keyword sort;
- output co `fit_score`, `matched_must_have_skills`, `missing_must_have_skills`, `why_fit`, `what_to_improve`;
- hard-skill gate van duoc ap dung cho job recommendation;
- code va tests tach rieng giua employer flow va candidate flow;
- full `pytest` pass.

## 14. Rui ro va giam thieu

### 14.1 Dung chung scorer nhung output nghiep vu khac nhau

Risk:

```text
Score logic dung, nhung wording candidate-side nghe giong employer-side.
```

Giam thieu:

- them explainer rieng cho candidate recommendation;
- tach label UI rieng: `Strong Fit`, `Good Fit`, `Stretch`.

### 14.2 Retrieval bo sot JD tot

Risk:

```text
Job dung bi rot o retrieval nen khong vao duoc top 10.
```

Giam thieu:

- hybrid retrieval sparse + dense;
- union top-N thay vi chi dung 1 kenh;
- test voi CV/JD da biet phu hop.

### 14.3 Candidate recommendation lam anh huong screening cu

Risk:

```text
Sua API/pipeline chung gay vo employer flow.
```

Giam thieu:

- route rieng;
- pipeline rieng;
- regression tests cho ca 2 flow.

### 14.4 Explanation qua chung chung

Risk:

```text
Tra top 10 nhung goi y khong thuc dung.
```

Giam thieu:

- uu tien missing must-have skills;
- uu tien evidence gap tu project/work/certification;
- khong sinh goi y vuot qua du lieu CV/JD.

## 15. Ghi chu cho bao cao

Co the trinh bay:

```text
Sau khi xay dung chuc nang sang loc CV cho nha tuyen dung, he thong duoc mo
rong sang bai toan nguoc la goi y cong viec phu hop cho ung vien. Thay vi
xay dung mot AI hoan toan moi, de tai tai su dung lai loi person-job fit
engine da co, bao gom parser, taxonomy, multilingual embedding, evidence
detection va scoring. He thong duoc thiet ke theo kien truc retrieve ->
filter -> rerank -> explain: dau tien lay ra mot tap JD kha nang tu job
catalog, sau do dung AI core de rerank va tra ve Top 10 JD phu hop nhat
kem giai thich skill match, skill gap va goi y cai thien CV. Cach tiep can
nay phu hop voi content-based recommendation trong boi canh cold-start,
dong thoi dam bao tinh minh bach va kha nang bao ve hoc thuat.
```

Mot cau ngan khi bao ve:

```text
Candidate-side job recommendation trong de tai khong phai mot he thong tach
biet, ma la bai toan person-job fit duoc dao chieu query: tu 1 CV, he thong
tim ra va giai thich 10 JD phu hop nhat bang cung mot AI core da dung cho
sang loc employer-side.
```

