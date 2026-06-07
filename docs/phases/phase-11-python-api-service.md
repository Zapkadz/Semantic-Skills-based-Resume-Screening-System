# Phase 11 - Python API Service for Web Integration

## 1. Muc tieu phase

Phase 11 tao Python HTTP API service de web PHP TOPCV Lite co the goi AI screening bang JSON payload.

Hien tai Phase 10 da co CLI:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Phase 11 se them API ma khong pha CLI hien tai:

```text
POST http://127.0.0.1:8000/screening
```

Input la JSON gom JD va danh sach ung vien/CV text. Output la ranking JSON tu pipeline.

## 2. Van de phase nay giai quyet

Web PHP hien tai co the tich hop bang CLI, nhung CLI yeu cau:

- Tao file JD `.txt` tam.
- Tao folder CV `.txt` tam.
- Goi command line.
- Doc output JSON.

API service giup web goi gon hon:

```text
PHP
  -> POST JSON toi Python API
  -> nhan ranking JSON
  -> luu DB
  -> hien thi AI rank/score/review card
```

## 3. Vi sao phase nay quan trong voi tich hop web

Voi web PHP, HTTP API la cach tich hop sach hon CLI:

- Khong can tao qua nhieu file tam.
- PHP gui du lieu structured truc tiep.
- De debug bang Postman/cURL.
- De deploy Python AI rieng.
- De nang cap thanh background service sau nay.
- Giu code PHP khong phu thuoc nhieu vao shell command.

## 4. Nguyen tac quan trong

Phase 11 phai dam bao:

- Khong pha CLI Phase 10.
- Khong doi scoring formula.
- Khong doi matcher/evidence/review card rules.
- API dung lai core pipeline.
- API khong tu cham diem bang LLM.
- Input/Output JSON co schema ro rang.
- Tests khong can start server that neu co the dung FastAPI TestClient.

## 5. Pham vi thuc hien

Trong Phase 11 se lam:

- Them dependency `fastapi` va `uvicorn`.
- Tao API entrypoint, du kien `api.py`.
- Tao module payload pipeline, du kien `src/payload_pipeline.py`.
- Tao schema/model cho request/response neu can, du kien `src/api_models.py`.
- Implement health endpoint:
  - `GET /health`
- Implement screening endpoint:
  - `POST /screening`
- API nhan JD va danh sach CV text.
- API tra ve ranking JSON co `application_id`/`candidate_id` neu input co.
- Them tests cho payload pipeline.
- Them tests cho API endpoint.
- Cap nhat README.
- Cap nhat dev learning log.
- Tao refactoring plan sau khi code xong.

## 6. Khong lam trong phase nay

Phase nay khong lam:

- Khong sua web PHP.
- Khong tao Streamlit UI.
- Khong deploy production server.
- Khong them database.
- Khong them queue/background worker.
- Khong support PDF/DOCX extraction.
- Khong OCR image CV.
- Khong thay doi CLI behavior.
- Khong merge branch.

## 7. API de xuat

### 7.1 Health check

Request:

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "service": "semantic-skills-resume-screening",
  "phase": "Phase 11 - Python API Service"
}
```

### 7.2 Screening endpoint

Request:

```http
POST /screening
Content-Type: application/json
```

Payload:

```json
{
  "job": {
    "job_id": 10,
    "job_title": "Backend Java Developer",
    "requirements": [
      "Java",
      "Spring Boot",
      "REST API",
      "SQL",
      "Basic Docker",
      "1+ year backend experience"
    ],
    "nice_to_have": [
      "AWS",
      "Kafka",
      "Kubernetes"
    ],
    "responsibilities": [
      "Develop backend services.",
      "Build RESTful APIs.",
      "Work with relational databases."
    ]
  },
  "candidates": [
    {
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "email": "candidate@example.com",
      "cv_text": "Nguyen Van A\nBackend Developer\n\nSummary:\n..."
    }
  ]
}
```

Response:

```json
{
  "job": {
    "job_id": 10,
    "title": "Backend Java Developer",
    "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Docker"],
    "nice_to_have_skills": ["AWS", "Kafka", "Kubernetes"]
  },
  "candidates": [
    {
      "rank": 1,
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "final_score": 87,
      "recommendation": "Strong Review",
      "scores": {},
      "matched_skills": [],
      "missing_skills": [],
      "review_card": {}
    }
  ]
}
```

## 8. Module design de xuat

### 8.1 `src/payload_pipeline.py`

Module nay xu ly JSON payload thanh pipeline result.

Public functions:

```python
def build_jd_text_from_payload(job: dict) -> str:
    pass

def build_cv_document_from_payload(candidate: dict) -> dict:
    pass

def run_screening_payload(
    payload: dict,
    taxonomy_path: str = "data/taxonomy/skills.json",
) -> dict:
    pass
```

Ly do tach module:

- `screening_pipeline.py` hien xu ly file path.
- `payload_pipeline.py` xu ly JSON/string payload.
- Ca hai dung chung parser/matcher/scorer/review card.

### 8.2 `api.py`

FastAPI app:

```python
from fastapi import FastAPI

app = FastAPI(title="Semantic Skills Resume Screening API")
```

Endpoints:

- `GET /health`
- `POST /screening`

### 8.3 `src/api_models.py`

Co the dung Pydantic models de validate request:

- `JobPayload`
- `CandidatePayload`
- `ScreeningRequest`

Neu muon giu MVP nhe, co the validate bang dict trong `payload_pipeline.py` truoc, nhung FastAPI/Pydantic se chuyen nghiep hon.

## 9. Compatibility voi CLI

CLI hien tai phai tiep tuc chay:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

API chay rieng:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

Hai entrypoint rieng:

```text
main.py -> CLI
api.py  -> HTTP API
```

Khong sua logic scoring trong `main.py`.

## 10. Cach PHP web se goi API sau phase nay

PHP co the goi:

```php
$payload = [
    "job" => [...],
    "candidates" => [...]
];

$ch = curl_init("http://127.0.0.1:8000/screening");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
$result = json_decode($response, true);
```

Sau do PHP luu:

- `rank`
- `final_score`
- `recommendation`
- `scores`
- `review_card`

Theo `application_id`.

## 11. File du kien tao moi

- `api.py`
- `src/payload_pipeline.py`
- `src/api_models.py`
- `tests/test_payload_pipeline.py`
- `tests/test_api.py`
- `docs/phases/phase-11-python-api-service.md`
- `docs/refactoring/phase-11-refactoring-plan.md` sau khi code xong

## 12. File du kien chinh sua

- `requirements.txt`
- `README.md`
- `docs/dev-learning-log.md`
- Co the cap nhat `docs/integration/php-web-ai-ranking-integration-guide.md`
- Co the cap nhat `docs/integration/cursor-prompt-topcv-lite-ai-ranking.md`

Tam thoi khong chinh sua:

- `main.py`, tru khi can update docs/version nho.
- `src/screening_pipeline.py`, tru khi can reuse helper an toan.
- `src/scorer.py`
- `src/review_card_generator.py`
- Matcher/parser/evidence modules.

## 13. Learning Plan

### 13.1 Toi can hoc gi trong phase nay?

Can hoc:

- API service khac CLI nhu the nao.
- HTTP request/response.
- FastAPI endpoint.
- Pydantic validation.
- JSON payload schema.
- Cach giu core logic dung chung cho CLI va API.
- Cach test API endpoint bang TestClient.

### 13.2 Cac khai niem ky thuat can hieu

- REST API.
- Health check.
- Request model.
- Response JSON.
- Input validation.
- 422 validation error.
- API adapter.
- Payload pipeline.

### 13.3 Nguyen tac thiet ke

- API layer mong.
- Payload pipeline chua logic chuyen JSON thanh screening result.
- Scoring/matching/review logic khong duplicate.
- Response phai giu `application_id` de PHP map ve DB.
- Neu candidate thieu `cv_text`, API tra loi loi ro rang hoac bo qua theo rule da test.

## 14. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/11-python-api-service`.
2. Them `fastapi` va `uvicorn` vao requirements.
3. Tao `src/api_models.py`.
4. Tao `src/payload_pipeline.py`.
5. Implement build JD text tu job payload.
6. Implement build CV document tu candidate payload.
7. Implement `run_screening_payload`.
8. Tao `api.py`.
9. Implement `GET /health`.
10. Implement `POST /screening`.
11. Them tests payload pipeline.
12. Them tests API endpoint.
13. Chay `pytest`.
14. Test thu cong bang `uvicorn`.
15. Test thu cong bang `curl` hoac Python requests neu co.
16. Cap nhat README.
17. Cap nhat dev learning log.
18. Cap nhat integration docs neu can.
19. Tao refactoring plan Phase 11.
20. Dung lai cho ban test va xac nhan.

## 15. Cach test phase

Test tu dong:

```bash
pytest
```

Chay API service:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Screening test:

```bash
curl -X POST http://127.0.0.1:8000/screening ^
  -H "Content-Type: application/json" ^
  -d @docs/integration/sample-screening-request.json
```

Neu khong tao sample JSON file, co the test bang Python one-liner hoac TestClient.

CLI regression:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

## 16. Tieu chi hoan thanh phase

Phase 11 hoan thanh khi:

- Co FastAPI app.
- `GET /health` hoat dong.
- `POST /screening` nhan job/candidates JSON.
- Response co ranking candidates.
- Response giu `application_id` va `candidate_id`.
- Demo payload tra Nguyen Van A score 87 Strong Review.
- CLI Phase 10 van chay binh thuong.
- Co tests tu dong.
- `pytest` pass.
- README duoc cap nhat.
- Learning log duoc cap nhat.
- Refactoring plan Phase 11 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 17. Rui ro

- API duplicate logic voi CLI.
- Payload schema khong khop voi PHP web.
- Candidate khong co `cv_text`.
- Response khong co `application_id` lam PHP kho map ket qua.
- FastAPI dependency lam moi truong can cai them.
- Uvicorn server dang chay ma quen tat sau test.

## 18. Ghi chu cho bao cao

Python API Service giup he thong AI resume screening co the duoc tich hop voi web PHP nhu mot service rieng. Web gui JD va CV text theo JSON, API xu ly bang pipeline san co va tra ve ranking + review card. Cach thiet ke nay giu CLI hien tai on dinh, dong thoi tao duong tich hop sach hon cho ung dung web.
