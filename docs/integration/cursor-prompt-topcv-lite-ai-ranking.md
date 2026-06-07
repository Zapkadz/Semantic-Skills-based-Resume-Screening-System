# Cursor Prompt - Integrate AI Candidate Ranking into TOPCV Lite

Copy prompt duoi day vao Cursor trong project PHP `C:\xampp\htdocs\topcv_lite`.

```text
Ban dang lam trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

AI Python hien tai DA CO HTTP API service bang FastAPI.

Chay API server bang lenh:

cd C:\SEMANTIC_SKILLS_RESUME
C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\uvicorn.exe api:app --host 127.0.0.1 --port 8000

Health check:

GET http://127.0.0.1:8000/health

Screening endpoint:

POST http://127.0.0.1:8000/screening
Content-Type: application/json

Muc tieu:

Tich hop chuc nang "AI goi y xep hang ung vien" vao trang employer xem danh sach ung vien theo tung tin tuyen dung.

Ngu canh UI hien co:

1. /employer/candidate_screening.php
   - Hien danh sach tin tuyen dung.
   - Moi dong co nut "Xem ung vien".

2. /employer/job_candidates.php?job_id=...
   - Hien danh sach ung vien cua mot job.
   - Hien placeholder "AI goi y xep hang ung vien - sap ra mat".
   - Can bien placeholder nay thanh chuc nang that.

Khong copy AI project vao topcv_lite.
Khong goi truc tiep module Python.
Hay goi HTTP API noi bo tai http://127.0.0.1:8000/screening.

Can lam:

1. Doc cau truc project PHP hien tai.
   - Kiem tra config DB.
   - Kiem tra session/login employer.
   - Kiem tra cac bang lien quan jobs, applications, candidates, CV.
   - Kiem tra employer/job_candidates.php.
   - Kiem tra employer/candidate_screening.php neu can.

2. Tao config AI screening.
   Co the tao config/ai_screening.php hoac them vao config hien co.

   Can co:
   AI_SCREENING_API_URL = http://127.0.0.1:8000/screening
   AI_SCREENING_HEALTH_URL = http://127.0.0.1:8000/health
   AI_SCREENING_TIMEOUT_SECONDS = 60

3. Tao helper/service PHP cho AI.
   Goi y file:
   includes/ai_screening.php
   hoac includes/services/ai_screening_service.php

   Helper can co cac ham:
   - build_ai_job_payload($job): array
   - build_ai_candidate_payload($candidate, $application, $cvData): array
   - build_ai_screening_payload($job, $applications): array
   - call_ai_screening_api(array $payload): array
   - save_ai_screening_results($jobId, array $aiResult): void

4. Build job payload.
   Payload gui sang AI can co:

   [
     'job' => [
       'job_id' => $jobId,
       'job_title' => 'Backend Java Developer',
       'requirements' => [...],
       'nice_to_have' => [...],
       'responsibilities' => [...]
     ],
     'candidates' => [...]
   ]

   Neu DB khong tach field requirements/nice_to_have/responsibilities, hay dung field mo ta job hien co va tach line tot nhat co the.
   Khong hard-code job demo.

5. Build candidate payload.
   Moi candidate gui sang AI nen co:

   [
     'application_id' => $applicationId,
     'candidate_id' => $candidateId,
     'candidate_name' => $candidateName,
     'email' => $email,
     'phone' => $phone,
     'applied_at' => $appliedAt,
     'cv_text' => $cvText
   ]

   Quan trong:
   - Bat buoc can cv_text hoac du lieu structured du de build CV.
   - Neu CV online structured trong DB, build cv_text tu DB.
   - Neu CV file upload da co extracted text, dung extracted text.
   - Neu chua co extracted text, danh dau ung vien thieu CV text va hien message than thien.

6. Format cv_text khuyen nghi:

   {candidate_name}
   {headline_or_position}

   Summary:
   {summary}

   Skills:
   - {skill_1}
   - {skill_2}

   Work Experience:
   {title} - {company}
   {start_date} - {end_date}
   - {description}

   Projects:
   {project_name}
   - {description}

   Education:
   {education}

7. Tao endpoint/action chay AI.
   Goi y:
   employer/run_ai_screening.php?job_id=...

   Yeu cau:
   - Chi employer dang dang nhap moi duoc goi.
   - Validate employer so huu job_id hoac co quyen voi job.
   - Validate job ton tai.
   - Validate co applications/candidates.
   - Build payload.
   - POST payload toi AI API.
   - Nhan ranking JSON.
   - Luu ket qua vao DB.
   - Redirect ve employer/job_candidates.php?job_id=... voi flash message thanh cong/that bai.

8. Goi API bang cURL.
   Vi du:

   $ch = curl_init(AI_SCREENING_API_URL);
   curl_setopt($ch, CURLOPT_POST, true);
   curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
   curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($payload, JSON_UNESCAPED_UNICODE));
   curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
   curl_setopt($ch, CURLOPT_TIMEOUT, AI_SCREENING_TIMEOUT_SECONDS);

   $response = curl_exec($ch);
   $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
   $curlError = curl_error($ch);
   curl_close($ch);

   if ($response === false || $httpCode >= 400) {
       // log loi ky thuat va hien message than thien
   }

   $aiResult = json_decode($response, true);

9. Database luu ket qua.
   Hay inspect schema truoc.

   Neu co the sua bang application hien co, them:
   - ai_rank INT NULL
   - ai_score INT NULL
   - ai_recommendation VARCHAR(50) NULL
   - ai_review_json LONGTEXT NULL
   - ai_screened_at DATETIME NULL

   Neu khong chac, tao bang moi ai_screening_results:
   - id
   - job_id
   - application_id
   - candidate_id
   - ai_rank
   - final_score
   - recommendation
   - scores_json
   - review_card_json
   - raw_result_json
   - created_at
   - updated_at

   Khuyen nghi: dung bang rieng de it anh huong schema hien tai.

10. Cap nhat UI employer/job_candidates.php.
   - Thay placeholder "AI goi y xep hang ung vien - sap ra mat" bang panel co nut:
     "Chay AI goi y xep hang"
   - Sau khi co ket qua, hien:
     AI Rank
     AI Score
     Recommendation
   - Nen cho sap xep theo ai_rank neu co ket qua.
   - Them nut "Xem AI review" cho tung ung vien.

11. Review card UI.
   Hien modal hoac page chi tiet gom:
   - Summary
   - Score breakdown
   - Strengths
   - Concerns
   - Evidence highlights
   - Suggested interview questions

   Data lay tu ai_review_json hoac review_card_json.

12. Error handling.
   Can xu ly:
   - API server chua chay.
   - API health check fail.
   - Job khong ton tai.
   - Employer khong co quyen voi job.
   - Job thieu requirement/JD text.
   - Khong co ung vien.
   - Ung vien khong co CV text.
   - API tra HTTP 400/422/500.
   - JSON parse fail.

13. Security.
   - Khong cho user nhap URL API tuy y.
   - Payload phai do backend tao tu DB.
   - Validate job ownership.
   - Khong expose raw error technical ra UI.
   - Log loi ky thuat vao file log.

14. Acceptance criteria.
   Sau khi lam xong:
   - Vao /employer/job_candidates.php?job_id=10 thay nut chay AI.
   - Bam nut thi PHP POST duoc JSON toi AI API.
   - AI response co candidates ranked.
   - Ket qua duoc luu DB theo application_id.
   - Table ung vien hien AI rank/score/recommendation.
   - Xem duoc AI review card.
   - Neu API chua chay, UI hien message than thien.

Luu y:
API Python phai duoc chay rieng bang uvicorn truoc khi test tu web.
Khong sua code AI Python trong task web nay.
Neu can thay doi schema API, dung lai va bao toi de cap nhat AI project truoc.
```
