# Phase 21 - Job Retrieval Index for Active JDs

## 1. Muc tieu phase

Phase 20 da cho phep candidate-side flow chay theo kieu:

```text
1 CV -> score tat ca JDs trong request -> sort -> top_k
```

Huong nay dung va an toan cho V1, nhung se som gap gioi han khi:

- so luong JD active tang len;
- web khong muon gui nguyen tat ca JD vao moi request;
- candidate-side recommendation can phan hoi nhanh hon;
- can tach ro retrieval va reranking theo dung pipeline recommender thuc te.

Muc tieu cua Phase 21 la them mot tang:

```text
job catalog loading + retrieval indexing
```

de chuyen candidate-side flow thanh:

```text
1 CV
  -> build candidate query profile
  -> retrieve top-N JD kha nang
  -> Phase 22 rerank bang AI core
  -> top_k jobs
```

Noi ngan gon:

```text
Phase 20 = recommendation API foundation
Phase 21 = retrieval/index layer truoc khi reranking
```

## 2. Van de can giai quyet

Neu tiep tuc score moi CV voi toan bo JD active theo cach Phase 20:

- request se ngay cang nang;
- web phai gui qua nhieu text sang Python API;
- thoi gian xu ly tang theo so JD;
- kho mo rong len danh sach job lon;
- khong tach bach duoc retrieval score va rerank score.

Phase 21 giai quyet bai toan:

```text
Lam sao lay ra mot tap JD "co kha nang phu hop"
truoc khi dung scorer core de cham chi tiet.
```

Day la kien truc dung huong voi hầu het he thong recommender va search thuc te:

```text
retrieve first
rerank later
```

## 3. Nguyen tac thiet ke

### 3.1 Khong bo score core da co

Phase 21 khong thay scorer employer/candidate-side.

Phase nay chi them lop truoc scorer:

```text
CV -> job retrieval
```

Con:

```text
CV -> job reranking
```

se de Phase 22 chot chat che hon.

### 3.2 Retrieval va reranking phai tach ro

Khong nen de retrieval score va fit score bi tron nhau.

Can co 2 muc score:

- `retrieval_score`
- `fit_score`

Y nghia:

- `retrieval_score`: giup lay nhanh cac JD kha nang
- `fit_score`: diem AI sau khi so khop chi tiet

### 3.3 Local-first, khong can vector DB o Phase 21

Phase 21 khong can nhay thang vao:

- Elasticsearch
- FAISS
- Qdrant
- Milvus
- pgvector

V1 hop ly hon la:

- in-memory index
- JSON/payload-based catalog
- sparse retrieval + optional dense retrieval local

Ly do:

- de test;
- de bao ve;
- khong them qua nhieu infra som;
- phu hop scope do an.

### 3.4 Khong anh huong employer-side screening

Employer flow:

```text
POST /screening
```

van nhu cu.

Candidate flow se mo rong theo huong:

```text
POST /recommend-jobs
  -> neu co jobs trong request: dung request list
  -> neu khong co jobs trong request: dung active job catalog/index
```

Nhung Phase 21 co the chot an toan hon:

- them module retrieval rieng;
- chua can bat buoc doi contract web ngay;
- cho phep candidate flow dung catalog tai Python side.

## 4. Bai toan nghiep vu

Can ho tro tinh huong thuc te:

```text
Ung vien tai CV
-> he thong tu lay danh sach JD active
-> tra ve top 10 job phu hop
```

Khong bat web phai gui tat ca JD text trong moi request nua.

Can co kha nang:

1. nap job catalog active;
2. tien xu ly thanh searchable job documents;
3. retrieve top-N nhanh;
4. giao top-N do cho Phase 22 rerank.

## 5. Kien truc de xuat

### 5.1 Luong xu ly tong the

```text
Active JD source
  -> job catalog loader
  -> parsed/normalized job cards
  -> retrieval index

Candidate CV
  -> candidate profile
  -> candidate query profile
  -> retrieve top-N jobs
  -> pass top-N to reranker
```

### 5.2 Module moi de xuat

Them:

```text
src/job_catalog_loader.py
src/job_indexer.py
src/job_retriever.py
tests/test_job_catalog_loader.py
tests/test_job_indexer.py
tests/test_job_retriever.py
```

Co the them sample data/doc:

```text
docs/integration/sample-job-catalog.json
```

### 5.3 Trach nhiem tung module

#### `src/job_catalog_loader.py`

Nhiem vu:

- nhan danh sach job payloads;
- validate;
- parse JD;
- classify requirement groups;
- normalize must-have / nice-to-have / domain;
- build `job_card` on dinh.

Ham de xuat:

```python
def build_job_catalog(
    jobs: list[dict[str, Any]],
    taxonomy_path: str = DEFAULT_TAXONOMY_PATH,
) -> list[dict[str, Any]]:
    ...
```

#### `src/job_indexer.py`

Nhiem vu:

- build retrievable text tu `job_card`;
- tao sparse text fields;
- tao dense text fields;
- luu metadata can cho retrieval.

Ham de xuat:

```python
def build_job_index_documents(job_catalog: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ...
```

#### `src/job_retriever.py`

Nhiem vu:

- nhan candidate query profile;
- tinh sparse retrieval score;
- optional dense retrieval score;
- merge score;
- tra ve top-N jobs candidate.

Ham de xuat:

```python
def retrieve_candidate_jobs(
    candidate_profile: dict[str, Any],
    indexed_jobs: list[dict[str, Any]],
    top_n: int = 50,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
) -> list[dict[str, Any]]:
    ...
```

## 6. Job card va index document

### 6.1 Job card

Moi JD active sau khi parse nen co structure nhu:

```json
{
  "job_id": 10,
  "job_title": "Backend Java Developer",
  "raw_text": "...",
  "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
  "nice_to_have_skills": ["AWS", "Kafka"],
  "open_set_requirements": [],
  "minimum_experience_years": 1,
  "seniority": "Junior",
  "domain": ["Backend", "Web Application"],
  "requirement_groups": {}
}
```

### 6.2 Index document

Job retrieval khong nen dung nguyen output screening raw.

Can build mot searchable representation:

```json
{
  "job_id": 10,
  "job_title": "Backend Java Developer",
  "sparse_text": "Backend Java Developer Java Spring Boot REST API SQL Docker Backend Web Application",
  "dense_text": "Backend Java Developer. Must-have skills: Java, Spring Boot, REST API, SQL, Docker. Domain: Backend, Web Application. Experience: 1 year.",
  "metadata": {
    "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
    "domain": ["Backend", "Web Application"],
    "seniority": "Junior",
    "minimum_experience_years": 1
  }
}
```

## 7. Candidate query profile

Can build candidate query profile rieng cho retrieval, khong dung nguyen review card hay final score.

De xuat:

```json
{
  "candidate_name": "Nguyen Van A",
  "headline": "Backend Developer",
  "skills": ["Java", "Spring Boot", "REST API", "MySQL", "Docker"],
  "domains": ["Backend", "Web Application"],
  "experience_years": 1.2,
  "summary_text": "...",
  "dense_query_text": "Backend Developer with Java, Spring Boot, REST API, MySQL, Docker experience."
}
```

Module retrieval se dung:

- `skills`
- `domains`
- `headline`
- `summary_text`
- `dense_query_text`

## 8. Retrieval strategy de xuat

### 8.1 Sparse retrieval truoc

Phase 21 nen uu tien mot sparse retrieval giai thich duoc:

- job title overlap
- canonical skill overlap
- domain overlap
- seniority compatibility nhe

Co the tao score don gian:

```text
retrieval_score =
  0.45 * must_have_skill_overlap
  0.20 * title_overlap
  0.20 * domain_overlap
  0.10 * nice_to_have_overlap
  0.05 * experience_compatibility
```

Huong nay du:

- nhanh;
- de debug;
- de viet test;
- khong can model.

### 8.2 Dense retrieval optional

Neu `embedding_matcher` co san, co the them:

```text
candidate dense_query_text
vs
job dense_text
```

roi tron vao sparse score.

De xuat:

```text
hybrid_retrieval_score =
  0.70 * sparse_score
  0.30 * dense_score
```

Neu embedding tat:

```text
hybrid_retrieval_score = sparse_score
```

### 8.3 Chua can ANN

Vi phase nay du kien so job chua qua lon trong do an, co the:

- sort in-memory;
- lay top 30 hoac top 50.

ANN/vector DB la huong future, khong can dua vao core Phase 21.

## 9. Input/Output contract de xuat

### 9.1 Input catalog

Phase 21 co the ho tro 2 cach:

#### Cach A - request-time jobs

Van giu nhu Phase 20:

```json
{
  "candidate": {},
  "jobs": [...]
}
```

#### Cach B - active catalog payload

Them schema de Python ben trong xu ly catalog active:

```json
{
  "candidate": {},
  "catalog": {
    "jobs": [...],
    "catalog_id": "active-jobs-2026-06-17"
  }
}
```

Trong Phase 21, de an toan va nhanh, co the chi can ho tro:

```text
jobs list -> build catalog/index inside request
```

roi tach han sang file/module rieng.

### 9.2 Output retrieval layer

Phase 21 can co output giua duong de debug:

```json
{
  "retrieved_jobs": [
    {
      "job_id": 10,
      "job_title": "Backend Java Developer",
      "retrieval_score": 0.84,
      "retrieval_reasons": [
        "Strong must-have skill overlap",
        "Backend domain overlap"
      ]
    }
  ]
}
```

Output nay cuc ky huu ich cho:

- debug web;
- so sanh retrieval va fit score;
- bao cao do an.

## 10. Pham vi thuc hien cua Phase 21

### 10.1 Trong scope

- them job catalog loader;
- them job index document builder;
- them sparse retrieval score;
- optional dense retrieval neu embedding available;
- tra ve top-N retrieved jobs;
- tich hop retrieval layer vao candidate recommendation pipeline;
- them debug metadata `retrieval_score` / `retrieval_reasons`;
- full tests.

### 10.2 Ngoai scope

- chua can retrieval tu DB truc tiep;
- chua can cache persistent index giua nhieu request;
- chua can vector DB;
- chua can preference-aware ranking;
- chua can feedback learning;
- chua can candidate-facing CV rewrite.

## 11. Cach tich hop voi Phase 20

Phase 20 hien tai:

```text
candidate -> score all jobs -> top_k
```

Sau Phase 21:

```text
candidate -> retrieve top_n jobs -> score retrieved jobs -> top_k
```

Thong so de xuat:

```text
top_n_retrieval = 30 hoac 50
top_k_output = 10
```

Neu tong job it:

```text
retrieve = all
```

Nen Phase 21 van khong lam vo behavior cu.

## 12. Test plan

Can them:

```text
tests/test_job_catalog_loader.py
tests/test_job_indexer.py
tests/test_job_retriever.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
```

### 12.1 Cases can co

1. Job catalog loader build duoc `job_card` tu list jobs.
2. Job index document co `sparse_text` va `dense_text`.
3. Candidate backend retrieve backend job cao hon security job.
4. Candidate CV AI/Computer Vision retrieve AI/CV jobs cao hon frontend jobs.
5. Retrieval van chay khi embedding tat.
6. Retrieval score tang khi skill overlap tang.
7. Retrieval reasons giai thich duoc tai sao job duoc lay.
8. Candidate recommendation pipeline chi rerank top-N sau retrieval.
9. `/screening` van khong bi anh huong.
10. `/recommend-jobs` van tra top_k nhu cu.

### 12.2 Benchmark thu cong de xuat

Sau khi code, benchmark candidate-side:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect them:

- `retrieval_stats`
- `retrieval_score`
- `retrieval_reasons`

## 13. Acceptance criteria

Phase 21 hoan thanh khi:

- candidate flow co retrieval layer rieng truoc reranking;
- job catalog/index duoc build on dinh;
- retrieval lay duoc top-N jobs hop ly cho CV;
- output co `retrieval_score` va `retrieval_reasons`;
- candidate recommendation pipeline van tra top_k jobs;
- screening cu khong bi anh huong;
- full `pytest` pass.

## 14. Rui ro va giam thieu

### 14.1 Retrieval bo sot job tot

Risk:

```text
Job phu hop bi rot truoc khi vao reranking.
```

Giam thieu:

- lay `top_n` kha rong;
- giu hybrid sparse + dense;
- test voi bo CV/JD benchmark.

### 14.2 Retrieval qua uu tien keyword overlap

Risk:

```text
Job co mot vai keyword trung nhung khong thuc su hop van len cao.
```

Giam thieu:

- domain overlap;
- title overlap;
- dense score optional;
- Phase 22 rerank lai bang fit score chi tiet.

### 14.3 Candidate flow bi phuc tap qua som

Risk:

```text
Them index/cache/vector DB qua nhanh lam kho bao ve.
```

Giam thieu:

- Phase 21 chi lam in-memory retrieval index;
- giu architecture don gian nhung dung huong.

## 15. Ghi chu cho bao cao

Co the trinh bay:

```text
De mo rong candidate-side recommendation theo huong thuc te, he thong duoc
bo sung mot tang job retrieval truoc khi reranking. Thay vi cham diem tren
toan bo tap JD active, he thong dau tien xay dung job catalog va retrieval
index, sau do lay ra mot tap JD kha nang phu hop dua tren overlap ve ky nang,
chuc danh, domain va thong tin tom tat. Tap nay moi duoc dua vao AI core de
rerank chi tiet. Kien truc retrieve -> rerank giup giam tai tinh toan, de mo
rong hon va phu hop voi cach cac he thong recommender/search thuc te van hanh.
```

Mot cau ngan khi bao ve:

```text
Phase 21 tach retrieval khoi reranking: retrieval tim nhanh cac JD kha nang,
con AI core o phase sau se cham fit chi tiet tren tap JD da duoc loc.
```

