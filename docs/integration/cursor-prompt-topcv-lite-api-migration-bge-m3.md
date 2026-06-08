# Cursor Prompt - Migrate TOPCV Lite AI Screening from CLI to API

Copy prompt duoi day vao Cursor trong project PHP:

```text
Ban dang lam trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

Hien tai web co the dang goi AI bang Python CLI. Task nay la CHUYEN LUONG CHINH SANG GOI FASTAPI, de web khong can tao file JD/CV tam va khong can chay `python main.py` moi lan.

Khong copy AI project vao topcv_lite.
Khong sua code AI Python trong task nay.
Khong goi truc tiep module Python.
Khong chay `exec`, `shell_exec`, `proc_open`, `passthru`, `popen` trong luong API moi.

## 1. AI API can duoc chay rieng truoc khi test web

Truoc khi test tu PHP, mo PowerShell rieng va chay:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1

$env:HF_HUB_OFFLINE='1'
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_THRESHOLD='0.72'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'

uvicorn api:app --host 127.0.0.1 --port 8000
```

Health check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

Screening endpoint:

```text
POST http://127.0.0.1:8000/screening
Content-Type: application/json
```

## 2. Viec dau tien: inspect CLI integration hien tai

Search toan project de tim doan dang goi CLI:

```text
SEMANTIC_SKILLS_RESUME
python.exe
main.py
--jd
--cv-dir
--output-json
ranking_results.json
exec(
shell_exec(
proc_open(
passthru(
popen(
ai_screening
run_ai
```

Neu dung PowerShell trong `C:\xampp\htdocs\topcv_lite`:

```powershell
Get-ChildItem -Recurse -Include *.php |
  Select-String -Pattern 'SEMANTIC_SKILLS_RESUME','python.exe','main.py','--jd','--cv-dir','--output-json','ranking_results.json','exec\(','shell_exec\(','proc_open\(','passthru\(','popen\(','ai_screening','run_ai'
```

Can xac dinh:

- File/action nao dang chay AI ranking.
- Web dang build JD text o dau.
- Web dang build CV text o dau.
- Web dang luu ket qua AI vao DB o dau.
- UI nao hien rank/score/recommendation.

Trong migration nay, co the TAI SU DUNG logic build JD/CV text hien co, nhung thay vi ghi file va goi CLI, hay dua text vao JSON payload va POST toi API.

## 3. Config API de xuat

Tao file config rieng neu chua co, vi du:

```text
config/ai_screening.php
```

Noi dung goi y:

```php
<?php

return [
    'api_url' => 'http://127.0.0.1:8000/screening',
    'health_url' => 'http://127.0.0.1:8000/health',
    'timeout_seconds' => 180,
    'connect_timeout_seconds' => 5,
];
```

Khong cho user nhap/sua API URL tu request.

## 4. Payload API bat buoc

PHP can POST JSON dang:

```json
{
  "job": {
    "job_id": 10,
    "job_title": "Backend Java Developer",
    "requirements": [
      "Java",
      "Spring Boot",
      "REST API",
      "SQL"
    ],
    "nice_to_have": [
      "AWS",
      "Kafka"
    ],
    "responsibilities": [
      "Build RESTful APIs."
    ],
    "description": "Optional raw job description"
  },
  "candidates": [
    {
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "email": "candidate@example.com",
      "phone": "0900000000",
      "headline": "Backend Developer",
      "summary": "Optional summary",
      "skills": ["Java", "Spring Boot"],
      "work_experience": [],
      "projects": [],
      "education": [],
      "cv_text": "Full CV text here",
      "applied_at": "2026-06-08 10:30:00"
    }
  ]
}
```

Field quan trong nhat:

- `job.job_id`
- `job.job_title`
- `job.requirements` hoac `job.description`
- `candidates[].application_id`
- `candidates[].candidate_id`
- `candidates[].candidate_name`
- `candidates[].cv_text`

Neu khong co `cv_text`, API co the build tu structured fields nhu `summary`, `skills`, `work_experience`, `projects`, `education`. Tuy nhien, MVP nen uu tien gui `cv_text` day du.

## 5. Build job payload tu DB

Tao/sua helper:

```php
function build_ai_job_payload(array $job): array
{
    return [
        'job_id' => $job['id'] ?? null,
        'job_title' => $job['title'] ?? $job['job_title'] ?? '',
        'requirements' => split_ai_lines($job['requirements'] ?? ''),
        'nice_to_have' => split_ai_lines($job['nice_to_have'] ?? ''),
        'responsibilities' => split_ai_lines($job['responsibilities'] ?? ''),
        'minimum_experience_years' => isset($job['minimum_experience_years'])
            ? (int) $job['minimum_experience_years']
            : null,
        'description' => $job['description'] ?? $job['job_description'] ?? '',
    ];
}
```

Neu DB khong tach field `requirements`, `nice_to_have`, `responsibilities`, dung field description hien co:

```php
'requirements' => [],
'description' => $job['description'] ?? '',
```

Khong hard-code job demo.

## 6. Build candidate payload tu DB

Tao/sua helper:

```php
function build_ai_candidate_payload(array $application, array $candidate, string $cvText): array
{
    return [
        'application_id' => $application['id'] ?? null,
        'candidate_id' => $candidate['id'] ?? null,
        'candidate_name' => trim(($candidate['full_name'] ?? '') ?: ($candidate['name'] ?? '')),
        'email' => $candidate['email'] ?? '',
        'phone' => $candidate['phone'] ?? '',
        'headline' => $candidate['headline'] ?? '',
        'summary' => $candidate['summary'] ?? '',
        'skills' => split_ai_lines($candidate['skills'] ?? ''),
        'work_experience' => [],
        'projects' => [],
        'education' => split_ai_lines($candidate['education'] ?? ''),
        'cv_text' => $cvText,
        'applied_at' => $application['created_at'] ?? $application['applied_at'] ?? '',
    ];
}
```

Neu web hien co da build file CV `.txt` cho CLI, co the tam thoi tai su dung ham build text do:

```php
$cvText = build_cv_text_for_ai($application, $candidate, $cvData);
```

Nhung trong luong API moi, khong can ghi file `.txt` nua.

Neu candidate khong co CV text:

- Khong gui candidate do len API.
- Log ly do.
- Hien message than thien neu tat ca candidates deu thieu CV text.

## 7. Helper split line

Neu DB luu multiline text, tao helper:

```php
function split_ai_lines(?string $value): array
{
    if ($value === null) {
        return [];
    }

    $lines = preg_split('/\r\n|\r|\n|;/', $value);
    $items = [];

    foreach ($lines as $line) {
        $line = trim($line);
        $line = preg_replace('/^\s*[-*•]\s*/u', '', $line);
        if ($line !== '') {
            $items[] = $line;
        }
    }

    return $items;
}
```

## 8. Call API bang cURL

Tao helper/service, vi du:

```text
includes/ai_screening_api.php
```

Code mau:

```php
<?php

function call_ai_screening_api(array $payload): array
{
    $config = require __DIR__ . '/../config/ai_screening.php';

    $json = json_encode($payload, JSON_UNESCAPED_UNICODE);
    if ($json === false) {
        throw new RuntimeException('Cannot encode AI payload: ' . json_last_error_msg());
    }

    $ch = curl_init($config['api_url']);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $config['connect_timeout_seconds']);
    curl_setopt($ch, CURLOPT_TIMEOUT, $config['timeout_seconds']);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curlError = curl_error($ch);
    curl_close($ch);

    if ($response === false) {
        throw new RuntimeException('AI API cURL failed: ' . $curlError);
    }

    if ($httpCode < 200 || $httpCode >= 300) {
        throw new RuntimeException("AI API HTTP {$httpCode}: {$response}");
    }

    $result = json_decode($response, true);
    if (!is_array($result)) {
        throw new RuntimeException('AI API returned invalid JSON: ' . json_last_error_msg());
    }

    return $result;
}
```

## 9. Optional health check

Truoc khi POST `/screening`, co the goi `/health` de hien loi than thien neu API chua bat:

```php
function check_ai_api_health(): bool
{
    $config = require __DIR__ . '/../config/ai_screening.php';

    $ch = curl_init($config['health_url']);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return $response !== false && $httpCode >= 200 && $httpCode < 300;
}
```

Neu health fail, UI hien:

```text
Khong the ket noi AI service. Vui long bat Python API va thu lai.
```

## 10. Endpoint/action chay AI trong web

Neu hien co co file CLI action, co the sua file do sang API.

Goi y file:

```text
employer/run_ai_screening.php
```

Flow bat buoc:

1. Kiem tra employer da dang nhap.
2. Validate `job_id`.
3. Validate employer co quyen voi job.
4. Query job.
5. Query applications/candidates cua job.
6. Build `$payload`.
7. Neu `$payload['candidates']` rong, hien message khong co CV text hop le.
8. Call `call_ai_screening_api($payload)`.
9. Luu ket qua vao DB.
10. Redirect ve `employer/job_candidates.php?job_id=...` voi flash success/fail.

## 11. Response API va mapping ket qua

API response co dang:

```json
{
  "job": {
    "job_id": 10,
    "title": "Backend Java Developer",
    "must_have_skills": [],
    "nice_to_have_skills": []
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

Khong can parse `source_file` nua neu API response co `application_id`.

Luu theo `application_id`:

```php
foreach ($result['candidates'] as $candidateResult) {
    $applicationId = $candidateResult['application_id'] ?? null;
    if (!$applicationId) {
        continue;
    }

    // update DB by application_id
}
```

## 12. DB luu ket qua

Neu bang applications co the them cot:

```sql
ALTER TABLE applications
ADD COLUMN ai_rank INT NULL,
ADD COLUMN ai_score INT NULL,
ADD COLUMN ai_recommendation VARCHAR(50) NULL,
ADD COLUMN ai_review_json LONGTEXT NULL,
ADD COLUMN ai_result_json LONGTEXT NULL,
ADD COLUMN ai_screened_at DATETIME NULL;
```

Neu khong muon sua bang hien co, tao bang rieng:

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
    matched_skills_json LONGTEXT NULL,
    missing_skills_json LONGTEXT NULL,
    review_card_json LONGTEXT NULL,
    raw_candidate_json LONGTEXT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    UNIQUE KEY uniq_job_application (job_id, application_id)
);
```

Khuyen nghi: neu project dang gan deadline, sua cot trong `applications` se nhanh hon. Neu muon sach schema, dung bang rieng.

Khi luu JSON, dung:

```php
json_encode($value, JSON_UNESCAPED_UNICODE)
```

## 13. UI can cap nhat

Trong:

```text
employer/job_candidates.php?job_id=...
```

Can co:

- Nut `Chay AI goi y xep hang`.
- Cot `AI Rank`.
- Cot `AI Score`.
- Cot `Recommendation`.
- Nut `Xem AI review`.
- Flash message success/fail.

Neu da co ket qua AI, co the sort theo `ai_rank`.

Review modal/page hien:

- Summary.
- Score breakdown.
- Strengths.
- Concerns.
- Evidence highlights.
- Suggested interview questions.

Data lay tu `ai_review_json` hoac `review_card_json`.

## 14. Error handling bat buoc

Xu ly:

- API server chua chay.
- cURL timeout.
- HTTP 400/422/500.
- Payload khong co candidate hop le.
- Candidate thieu CV text.
- JSON encode/decode fail.
- DB save fail.
- Employer khong co quyen voi job.

UI khong expose stack trace. Hien message than thien:

```text
Khong the chay AI screening luc nay. Vui long kiem tra AI service hoac thu lai sau.
```

Log ky thuat nen co:

- job_id.
- employer_id.
- payload candidate count.
- HTTP code.
- response body khi loi.
- exception message.

## 15. Test API doc lap truoc khi test web

Tu PowerShell:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
$body = Get-Content C:\SEMANTIC_SKILLS_RESUME\docs\integration\sample-screening-request.json -Raw
$result = Invoke-RestMethod http://127.0.0.1:8000/screening -Method Post -ContentType "application/json" -Body $body
$result.candidates | Select-Object rank,candidate_name,final_score,recommendation,application_id,candidate_id
```

Neu test doc lap fail, sua/chay Python API truoc, chua test web.

## 16. Test tu web

1. Dam bao API dang chay tai `http://127.0.0.1:8000`.
2. Vao `http://localhost/topcv_lite/employer/job_candidates.php?job_id=...`.
3. Bam `Chay AI goi y xep hang`.
4. Kiem tra web khong tao/chay command CLI trong luong moi.
5. Kiem tra network/log PHP co POST `/screening`.
6. Kiem tra DB da luu ket qua theo `application_id`.
7. Kiem tra UI hien rank/score/recommendation.
8. Tat API thu va bam lai de dam bao UI hien loi than thien.

## 17. Migration strategy

Lam theo cach it rui ro:

1. Giu helper CLI cu trong file rieng neu can rollback.
2. Tao helper API moi.
3. Doi action `run_ai_screening` sang goi helper API.
4. Khong xoa runtime folder/CLI code ngay neu chua chac.
5. Sau khi API pass, co the them config `AI_SCREENING_DRIVER=api|cli` neu muon fallback.

Mac dinh nen la:

```text
AI_SCREENING_DRIVER=api
```

## 18. Acceptance criteria

Hoan thanh khi:

- Web khong goi `python main.py` trong luong AI ranking moi.
- Web POST JSON toi `http://127.0.0.1:8000/screening`.
- Payload co job + candidates + `cv_text`.
- API response duoc luu DB theo `application_id`.
- UI hien AI rank/score/recommendation.
- Xem duoc review card.
- API offline/down thi UI bao loi than thien.
- CLI code cu khong anh huong luong moi.

Sau task nay, bao lai:

- File nao da sua.
- Endpoint/action nao dang chay AI.
- DB schema da them cot hay tao bang rieng.
- Payload mau web gui len API.
- Ket qua test API doc lap va test tu web.
```

