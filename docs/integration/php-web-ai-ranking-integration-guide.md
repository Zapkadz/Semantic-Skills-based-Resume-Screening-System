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

Khong can copy AI project vao trong `topcv_lite`. PHP co the goi Python bang absolute path.

## 2. Trang thai tich hop hien tai

Hien tai AI project da co:

- CLI pipeline chay duoc.
- Input dang JD `.txt`.
- Input dang folder CV `.txt`.
- Output ranking summary.
- Output JSON neu truyen `--output-json`.
- Output Markdown review cards neu truyen `--output-dir`.

Lenh da chay duoc:

```bash
C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\python.exe C:\SEMANTIC_SKILLS_RESUME\main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

## 3. Da co API cho web goi chua?

Chua co HTTP API service.

Nghia la hien tai web PHP **chua the goi kieu REST API** nhu:

```text
POST http://localhost:8000/screening
```

Hien tai web co the tich hop bang cach:

```text
PHP
  -> tao file JD .txt va cac file CV .txt tam
  -> goi Python CLI
  -> doc file JSON output
  -> luu ket qua vao database
  -> hien thi len UI
```

Neu muon goi API that, can lam them mot phase backend Python:

```text
FastAPI / Flask service
  -> POST /screening
  -> nhan JSON payload tu PHP
  -> tra ve ranking JSON
```

## 4. Huong tich hop khuyen nghi cho MVP

Nen lam theo 2 buoc:

### Buoc 1 - Tich hop nhanh bang CLI

Dung PHP goi Python CLI de co chuc nang AI ranking chay duoc trong web.

Uu diem:

- Nhanh.
- Khong can viet API ngay.
- Dung duoc code AI hien tai.
- Phu hop demo.

Nhuoc diem:

- PHP phai quan ly file tam.
- Can xu ly duong dan Windows can than.
- Khong dep bang HTTP API service.

### Buoc 2 - Nang cap thanh API service

Sau khi CLI integration on, tao FastAPI service de web goi bang JSON.

Uu diem:

- Sach hon.
- De maintain.
- De deploy rieng.
- Web khong can tao file tam qua nhieu.

## 5. Flow tich hop bang CLI

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
4. Build JD text.
5. Build CV text cho tung ung vien.
6. Ghi JD text vao file tam jd.txt.
7. Ghi moi CV text vao 1 file .txt trong folder cvs/.
8. Goi Python CLI voi --jd, --cv-dir, --output-json.
9. Doc JSON output.
10. Map ket qua AI ve application_id.
11. Luu ket qua AI vao database.
12. Redirect/render lai trang danh sach ung vien voi AI rank/score.
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

## 10. Goi Python CLI tu PHP

Vi du PHP pseudo-code:

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

Luu y:

- Luon quote path vi Windows path co dau `\`.
- Nen redirect stderr `2>&1` de debug loi Python.
- Nen set timeout neu dung process runner rieng.
- Nen log command output khi loi.

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
- Tao helper build JD text.
- Tao helper build CV text.
- Tao helper goi Python CLI.
- Tao runtime folder cho tung job/run.
- Tao endpoint/action `run_ai_screening.php`.
- Them nut tren `job_candidates.php`.
- Luu ket qua AI vao DB.
- Hien AI rank/score/recommendation tren table.
- Tao modal/page hien review card.
- Them error handling va permission check.

## 15. Khi nao can lam API service?

Nen lam API service khi:

- Muon web goi AI bang HTTP JSON thay vi CLI.
- Muon deploy AI rieng.
- Muon nhieu web/client goi chung AI.
- Muon giam file tam.
- Muon queue/background job sau nay.

API de xuat:

```text
POST /screening
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

Hien tai da du de web PHP tich hop theo cach **goi Python CLI**.

Chua du de web goi theo cach **HTTP API**, vi AI project chua co FastAPI/Flask server.

Huong nen lam ngay:

```text
PHP web
  -> build JD/CV text
  -> write temp .txt files
  -> call Python CLI
  -> read ranking_results.json
  -> save DB
  -> show AI ranking
```

Huong nang cap sau:

```text
PHP web
  -> POST JSON to Python FastAPI
  -> receive ranking JSON
```
