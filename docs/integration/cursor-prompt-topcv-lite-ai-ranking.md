# Cursor Prompt - Integrate AI Candidate Ranking into TOPCV Lite

Copy prompt duoi day vao Cursor trong project PHP `C:\xampp\htdocs\topcv_lite`.

```text
Ban dang lam trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

Muc tieu:

Tich hop chuc nang "AI goi y xep hang ung vien" vao trang employer xem danh sach ung vien theo tung tin tuyen dung.

Ngu canh UI hien co:

1. Trang /employer/candidate_screening.php
   - Hien danh sach tin tuyen dung.
   - Moi dong co nut "Xem ung vien".

2. Trang /employer/job_candidates.php?job_id=...
   - Hien danh sach ung vien cua mot job.
   - Hien placeholder "AI goi y xep hang ung vien - sap ra mat".
   - Can bien placeholder nay thanh chuc nang that.

AI Python hien tai CHUA co HTTP API.
AI Python hien tai da co CLI chay duoc:

C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\python.exe C:\SEMANTIC_SKILLS_RESUME\main.py --jd <jd_txt_path> --cv-dir <cv_txt_dir> --output-json <result_json_path>

Hay tich hop theo huong PHP goi Python CLI truoc.

Khong copy AI project vao topcv_lite.
Dung absolute path toi AI project.

Can lam:

1. Doc cau truc project PHP hien tai.
   - Kiem tra config DB.
   - Kiem tra cac bang lien quan job, applications, candidates, CV.
   - Kiem tra file employer/job_candidates.php.
   - Kiem tra file employer/candidate_screening.php neu can.

2. Tao config AI screening.
   - Co the tao file config/ai_screening.php hoac them vao config hien co.
   - Khai bao:
     AI_PYTHON_PATH = C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\python.exe
     AI_MAIN_PATH = C:\SEMANTIC_SKILLS_RESUME\main.py
     AI_RUNTIME_DIR = C:\topcv_ai_runtime

3. Tao helper/service PHP cho AI.
   Goi y file:
   includes/ai_screening.php
   hoac includes/services/ai_screening_service.php

   Helper can co cac ham:
   - build_job_text($job): string
   - build_candidate_cv_text($candidate, $application, $cvData): string
   - prepare_ai_runtime_files($job, $applications): array
   - run_ai_screening_cli($jdPath, $cvDir, $outputJson): array
   - parse_application_id_from_source_file($sourceFile): ?int
   - save_ai_screening_results($jobId, $aiResult): void

4. Runtime file convention.
   Tao folder moi moi lan chay:

   C:\topcv_ai_runtime\job-{job_id}\run-{timestamp}\
   |-- jd.txt
   |-- cvs\
   |   |-- application-{application_id}__candidate-{candidate_id}.txt
   |-- ranking_results.json

   Bat buoc dat ten file CV theo format:
   application-{application_id}__candidate-{candidate_id}.txt

   Ly do:
   AI result tra ve source_file, PHP se parse source_file de map ket qua ve application_id.

5. Build JD text.
   Format:

   {job_title}

   Requirements:
   - {requirement_1}
   - {requirement_2}
   - {experience_requirement}

   Nice to have:
   - {nice_to_have_1}

   Responsibilities:
   - {responsibility_1}

   Neu DB khong tach field requirements/nice_to_have/responsibilities, hay dung field mo ta job hien co va tach line tot nhat co the.
   Khong duoc hard-code job demo.

6. Build CV text.
   Format:

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

   Neu web co CV online structured trong DB, lay data structured.
   Neu chi co CV file upload/PDF/DOCX ma da co extracted text trong DB, dung extracted text.
   Neu chua co extracted text, hien thong bao ung vien thieu CV text va bo qua ung vien do hoac dua text toi thieu gom ten/email.

7. Tao endpoint/action chay AI.
   Goi y:
   employer/run_ai_screening.php?job_id=...

   Yeu cau:
   - Chi employer dang dang nhap moi duoc goi.
   - Validate employer so huu job_id hoac co quyen voi job.
   - Validate job ton tai.
   - Validate co applications/candidates.
   - Goi AI CLI.
   - Doc output JSON.
   - Luu ket qua vao DB.
   - Redirect ve employer/job_candidates.php?job_id=... voi flash message thanh cong/that bai.

8. Goi Python CLI an toan.
   Dung exec/proc_open va quote path.
   Vi du:

   function quote_path($path) {
       return '"' . str_replace('"', '\"', $path) . '"';
   }

   $cmd = quote_path($pythonPath)
       . ' ' . quote_path($mainPath)
       . ' --jd ' . quote_path($jdPath)
       . ' --cv-dir ' . quote_path($cvDir)
       . ' --output-json ' . quote_path($outputJson);

   exec($cmd . ' 2>&1', $outputLines, $exitCode);

   if ($exitCode !== 0) {
       log loi va hien message than thien.
   }

9. Database luu ket qua.
   Hay inspect schema truoc.

   Neu co the sua bang application hien co, them cac cot:
   - ai_rank INT NULL
   - ai_score INT NULL
   - ai_recommendation VARCHAR(50) NULL
   - ai_review_json LONGTEXT NULL
   - ai_screened_at DATETIME NULL

   Neu khong chac, tao bang moi:

   ai_screening_results:
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

   Hay tao SQL migration/notes trong docs neu project co quy trinh migration.

10. Cap nhat UI employer/job_candidates.php.
   - Thay placeholder "AI goi y xep hang ung vien - sap ra mat" bang panel co nut:
     "Chay AI goi y xep hang"
   - Sau khi co ket qua, hien:
     AI Rank
     AI Score
     Recommendation
   - Nen sap xep optional theo ai_rank neu co ket qua.
   - Them nut "Xem AI review" cho tung ung vien.

11. Review card UI.
   Hien modal hoac page chi tiet gom:
   - Summary
   - Score breakdown
   - Strengths
   - Concerns
   - Evidence highlights
   - Suggested interview questions

   Data lay tu ai_review_json.

12. Error handling.
   Can xu ly:
   - Python path sai.
   - AI project chua co .venv.
   - CV text rong.
   - JD text rong.
   - AI command fail.
   - ranking_results.json khong ton tai.
   - JSON parse fail.

13. Security.
   - Khong cho ung vien/employer nhap truc tiep shell command.
   - Tat ca path phai do backend tao.
   - Quote path khi goi shell.
   - Runtime folder khong nen public.
   - Validate job ownership.

14. Acceptance criteria.
   Sau khi lam xong:
   - Vao /employer/job_candidates.php?job_id=10 thay nut chay AI.
   - Bam nut thi PHP tao jd.txt va folder cvs.
   - PHP goi duoc Python CLI.
   - Co file ranking_results.json.
   - Ket qua duoc luu DB.
   - Table ung vien hien AI rank/score/recommendation.
   - Xem duoc AI review card.
   - Neu AI loi, UI hien message than thien va log chi tiet.

Luu y:
Dung AI CLI truoc, chua lam HTTP API.
Khong sua code AI Python trong task nay.
Neu can thay doi AI Python de nhan payload JSON truc tiep, hay dung lai va bao cho toi de lam phase API rieng.
```
