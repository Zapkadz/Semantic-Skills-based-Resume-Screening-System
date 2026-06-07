# PHP Web Integration Guide - AI Candidate Ranking

## 1. Boi canh hien tai

Du an web PHP hien tai nam o:

```text
C:\xampp\htdocs\topcv_lite
```

Du an AI Python hien tai nam rieng o:

```text
C:\SEMANTIC_SKILLS_RESUME
```

Day la cach dat thu muc phu hop:

```text
C:\
|-- xampp\
|   `-- htdocs\
|       `-- topcv_lite\        # Web PHP
|
`-- SEMANTIC_SKILLS_RESUME\    # AI Python project
```

Khong can copy AI project vao trong `topcv_lite`. PHP co the goi AI bang HTTP API noi bo hoac bang Python CLI fallback.

## 2. Trang thai tich hop hien tai

Hien tai AI project da co:

- CLI pipeline chay duoc.
- FastAPI HTTP API service.
- Input dang JD `.txt`.
- Input dang folder CV `.txt`.
- Input dang JSON payload gom job va candidates.
- Output ranking summary.
- Output JSON neu truyen `--output-json`.
- Output Markdown review cards neu truyen `--output-dir`.
- Output JSON truc tiep tu `POST /screening`.

CLI van chay duoc:

```bash
C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\python.exe C:\SEMANTIC_SKILLS_RESUME\main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

API service chay bang:

```bash
cd C:\SEMANTIC_SKILLS_RESUME
C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\uvicorn.exe api:app --host 127.0.0.1 --port 8000
```

## 3. Da co API cho web goi chua?

Da co FastAPI HTTP API service.

Web PHP co the goi:

```text
POST http://127.0.0.1:8000/screening
```

Health check:

```text
GET http://127.0.0.1:8000/health
```

Flow API khuyen nghi:

```text
PHP
  -> build JSON payload tu job va candidates
  -> POST /screening
  -> nhan ranking JSON
  -> luu ket qua vao database
  -> hien thi len UI
```

## 4. Huong tich hop khuyen nghi cho MVP

Nen lam theo thu tu:

### Buoc 1 - Tich hop bang API

Dung PHP `curl` de goi:

```text
POST http://127.0.0.1:8000/screening
```

Uu diem:

- Sach hon CLI.
- Khong can tao JD/CV file tam.
- Web gui structured JSON truc tiep.
- De debug bang Postman/cURL.
- De nang cap deployment sau nay.

### Buoc 2 - Giu CLI lam fallback

Neu chua muon chay API server, van co the dung PHP goi Python CLI.

CLI fallback phu hop khi:

- Demo nhanh.
- Chua setup `uvicorn`.
- Muon debug pipeline bang file `.txt`.

## 5. Flow tich hop bang API

Khi employer vao:

```text
/employer/job_candidates.php?job_id=10
```

Va bam nut:

```text
AI goi y xep hang ung vien
```

Web nen chay flow:

```text
1. Validate employer co quyen voi job_id.
2. Query thong tin job.
3. Query danh sach applications/candidates cua job.
4. Build job payload.
5. Build candidate payloads.
6. POST JSON toi http://127.0.0.1:8000/screening.
7. Nhan ranking JSON.
8. Map ket qua AI ve application_id.
9. Luu ket qua AI vao database.
10. Redirect/render lai trang danh sach ung vien voi AI rank/score.
```

## 6. Thu muc runtime de xuat

Nen de file tam ngoai web public neu co the:

```text
C:\topcv_ai_runtime\
`-- job-10\
    `-- run-20260607-153000\
        |-- jd.txt
        |-- cvs\
        |   |-- application-123__candidate-456.txt
        |   `-- application-124__candidate-457.txt
        `-- ranking_results.json
```

Neu bat buoc de trong `topcv_lite`, nen tao:

```text
C:\xampp\htdocs\topcv_lite\storage\ai_screening\
```

Va them `.htaccess` chan truy cap truc tiep:

```apache
Deny from all
```

## 7. Quy tac dat ten file CV

Vì AI CLI hien tai doc cac file `.txt` trong folder va tra ve `source_file`, web nen dat ten file CV co chua ID de map nguoc:

```text
application-{application_id}__candidate-{candidate_id}.txt
```

Vi du:

```text
application-123__candidate-456.txt
```

Sau khi AI tra ve:

```json
{
  "source_file": "application-123__candidate-456.txt",
  "candidate_name": "Nguyen Van A",
  "final_score": 87
}
```

PHP co the parse `application_id = 123` de luu ket qua dung application.

## 8. Build JD text tu database

Tu `job_id`, web can lay thong tin job va build text:

```text
{job_title}

Requirements:
- {requirement_1}
- {requirement_2}
- {experience_requirement}

Nice to have:
- {nice_to_have_1}
- {nice_to_have_2}

Responsibilities:
- {responsibility_1}
- {responsibility_2}
```

Neu database dang luu JD trong mot field mo ta lon, co the build toi thieu:

```text
{job_title}

Requirements:
- {job_description_or_requirements_lines}
```

Nhung de AI cham tot hon, nen tach duoc:

- requirements
- nice_to_have
- responsibilities
- experience

## 9. Build CV text tu database/file upload

Moi ung vien can co `cv_text`.

Format khuyen nghi:

```text
{candidate_name}
{headline}

Summary:
{summary}

Skills:
- {skill_1}
- {skill_2}

Work Experience:
{job_title} - {company}
{start_month_year} - {end_month_year}
- {description_1}
- {description_2}

Projects:
{project_name}
- {project_description_1}
- {project_description_2}

Education:
{education}
```

Neu web co CV online structured trong DB, hay build text tu DB.

Neu web chi co PDF/DOCX upload:

```text
PDF/DOCX
  -> extract text
  -> clean text
  -> luu cv_text
  -> dua vao AI
```

Neu file la anh:

```text
Image
  -> OCR
  -> text
  -> AI
```

MVP nen uu tien CV online/structured hoac text da extract.

## 10. Goi Python API tu PHP

Vi du PHP pseudo-code:

```php
<?php

$payload = [
    'job' => [
        'job_id' => 10,
        'job_title' => 'Backend Java Developer',
        'requirements' => ['Java', 'Spring Boot', 'REST API', 'SQL'],
        'nice_to_have' => ['AWS', 'Kafka'],
        'responsibilities' => ['Build RESTful APIs.'],
    ],
    'candidates' => [
        [
            'application_id' => 123,
            'candidate_id' => 456,
            'candidate_name' => 'Nguyen Van A',
            'email' => 'candidate@example.com',
            'cv_text' => $cvText,
        ],
    ],
];

$ch = curl_init('http://127.0.0.1:8000/screening');
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload, JSON_UNESCAPED_UNICODE));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlError = curl_error($ch);
curl_close($ch);

if ($response === false || $httpCode >= 400) {
    throw new RuntimeException("AI API failed: HTTP {$httpCode} {$curlError} {$response}");
}

$result = json_decode($response, true);
```

Luu y:

- Can chay API server truoc bang `uvicorn api:app --host 127.0.0.1 --port 8000`.
- Nen set timeout cho cURL neu production.
- Nen log HTTP status va response body khi loi.
- `application_id` trong response dung de map ket qua ve application DB.

## 10.1 CLI fallback neu chua dung API

Neu chua chay API server, van co the goi CLI:

```php
<?php

function quote_path(string $path): string {
    return '"' . str_replace('"', '\"', $path) . '"';
}

$python = 'C:\\SEMANTIC_SKILLS_RESUME\\.venv\\Scripts\\python.exe';
$main = 'C:\\SEMANTIC_SKILLS_RESUME\\main.py';
$jdPath = 'C:\\topcv_ai_runtime\\job-10\\run-20260607-153000\\jd.txt';
$cvDir = 'C:\\topcv_ai_runtime\\job-10\\run-20260607-153000\\cvs';
$outputJson = 'C:\\topcv_ai_runtime\\job-10\\run-20260607-153000\\ranking_results.json';

$cmd = quote_path($python)
    . ' ' . quote_path($main)
    . ' --jd ' . quote_path($jdPath)
    . ' --cv-dir ' . quote_path($cvDir)
    . ' --output-json ' . quote_path($outputJson);

exec($cmd . ' 2>&1', $outputLines, $exitCode);

if ($exitCode !== 0) {
    throw new RuntimeException("AI screening failed: " . implode("\n", $outputLines));
}

$result = json_decode(file_get_contents($outputJson), true);
```

## 11. Database luu ket qua AI

Neu DB hien co bang applications, co the them cot:

```sql
ALTER TABLE applications
ADD COLUMN ai_rank INT NULL,
ADD COLUMN ai_score INT NULL,
ADD COLUMN ai_recommendation VARCHAR(50) NULL,
ADD COLUMN ai_review_json LONGTEXT NULL,
ADD COLUMN ai_screened_at DATETIME NULL;
```

Neu khong muon sua bang cu, tao bang rieng:

```sql
CREATE TABLE ai_screening_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    application_id INT NOT NULL,
    candidate_id INT NULL,
    ai_rank INT NULL,
    final_score INT NULL,
    recommendation VARCHAR(50) NULL,
    scores_json LONGTEXT NULL,
    review_card_json LONGTEXT NULL,
    raw_result_json LONGTEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL
);
```

Khuyen nghi: dung bang rieng `ai_screening_results` de it anh huong schema hien tai.

## 12. UI can them vao job_candidates.php

Tren trang:

```text
/employer/job_candidates.php?job_id=10
```

Can them:

- Nut `AI goi y xep hang ung vien`.
- Cot `AI Rank`.
- Cot `AI Score`.
- Cot `AI Recommendation`.
- Button `Xem AI review`.

Vi du table:

```text
Ung vien | Ho so | Ngay nop | Trang thai | AI Rank | AI Score | AI Recommendation | Hanh dong
```

Khi bam `Xem AI review`, hien modal hoac trang chi tiet:

- Summary
- Score breakdown
- Strengths
- Concerns
- Evidence highlights
- Suggested interview questions

## 13. Error handling can co

Web can xu ly cac truong hop:

- Job khong ton tai.
- Employer khong co quyen voi job.
- Job thieu requirement/JD text.
- Khong co ung vien.
- Ung vien khong co CV text.
- API server chua chay.
- API tra HTTP 400/422.
- cURL fail.
- Python path sai.
- `.venv` chua cai dependency.
- AI command fail.
- JSON output khong ton tai.
- JSON parse fail.

UI nen hien loi de doc:

```text
Khong the chay AI screening. Vui long kiem tra CV/JD hoac thu lai sau.
```

Va log loi ky thuat vao file log.

## 14. Checklist de Cursor lam tren web

- Tao config duong dan AI.
- Tao helper build job payload.
- Tao helper build candidate payload.
- Tao helper goi Python API bang cURL.
- Tao endpoint/action `run_ai_screening.php`.
- Them nut tren `job_candidates.php`.
- Luu ket qua AI vao DB.
- Hien AI rank/score/recommendation tren table.
- Tao modal/page hien review card.
- Them error handling va permission check.

## 15. API request/response tom tat

Endpoint:

```text
POST http://127.0.0.1:8000/screening
Content-Type: application/json

{
  "job": {...},
  "candidates": [...]
}
```

Response:

```json
{
  "job": {...},
  "candidates": [...]
}
```

## 16. Ket luan

Hien tai da du de web PHP tich hop theo cach **HTTP API**.

Huong nen lam ngay:

```text
PHP web
  -> build job/candidate JSON
  -> POST to Python FastAPI
  -> receive ranking JSON
  -> save DB
  -> show AI ranking
```

CLI van co the giu lam fallback:

```text
PHP web
  -> build JD/CV text files
  -> call Python CLI
  -> read ranking_results.json
```
