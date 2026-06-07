# Web Integration Input Contract - JD and CV

## 1. Muc dich tai lieu

Tai lieu nay mo ta dang input ma module AI Resume Screening hien tai can nhan tu web TOPCV Lite.

Ngu canh web hien tai:

- Trang `candidate_screening.php`: nha tuyen dung chon tung tin tuyen dung/JD de xem ung vien.
- Trang `job_candidates.php?job_id=...`: hien danh sach ung vien cua mot JD.
- Sau nay tren trang danh sach ung vien, web se goi AI de xep hang ung vien theo JD do.

Muc tieu tich hop:

```text
job_id
  -> lay thong tin JD
  -> lay danh sach CV ung vien da nop vao JD do
  -> chuyen JD va CV ve text theo format chuan
  -> dua vao AI screening pipeline
  -> nhan ranking + review card
  -> hien thi tren web
```

## 2. Ket luan ngan gon

Hien tai module AI dang ho tro input MVP o dang **plain text UTF-8**.

```text
JD input: 1 file .txt hoac 1 chuoi text co cau truc JD
CV input: nhieu file .txt hoac nhieu chuoi text co cau truc CV
```

Chua ho tro truc tiep:

- Anh chup CV.
- PDF upload chua extract text.
- DOCX upload chua extract text.
- HTML CV online chua convert ve plain text.

Neu web dang co PDF/DOCX/CV online, buoc tich hop can lam la:

```text
PDF/DOCX/HTML CV
  -> extract/convert thanh plain text
  -> dua text vao AI pipeline
```

## 3. Format JD hien tai

JD nen la plain text co cau truc nhu sau:

```text
Backend Java Developer

Requirements:
- Java
- Spring Boot
- REST API
- SQL
- Basic Docker
- 1+ year backend experience

Nice to have:
- AWS
- Kafka
- Kubernetes

Responsibilities:
- Develop backend services.
- Build RESTful APIs.
- Work with relational databases.
- Collaborate with frontend developers.
```

### 3.1 Truong bat buoc cho JD

Toi thieu nen co:

```text
job_title
requirements / must_have_skills
```

Trong text:

- Dong dau tien la job title.
- Section `Requirements:` la cac yeu cau bat buoc.

### 3.2 Truong khuyen nghi cho JD

Nen co them:

```text
nice_to_have_skills
responsibilities
minimum_experience_years
seniority
domain
```

Trong text:

- `Nice to have:` dung cho ky nang cong diem them.
- `Responsibilities:` giup mo ta domain/cong viec.
- So nam kinh nghiem co the viet trong Requirements, vi du `1+ year backend experience`.

### 3.3 Mapping tu database web sang JD text

Neu web co bang `jobs` hoac `job_posts`, co the map:

```text
job.title              -> dong dau tien
job.requirements       -> Requirements
job.nice_to_have       -> Nice to have
job.responsibilities   -> Responsibilities
job.experience_years   -> Requirements, dang "X+ year experience"
```

Neu web chua tach field, co the lay noi dung mo ta tin tuyen dung va build text theo template tren.

## 4. Format CV hien tai

CV nen la plain text co cau truc nhu sau:

```text
Nguyen Van A
Backend Developer

Summary:
Backend developer with experience building Java Spring Boot services and REST APIs.

Skills:
- Java
- Spring Boot
- REST API
- MySQL
- Docker

Work Experience:
Backend Developer Intern - ABC Tech
06/2024 - 12/2024
- Built REST APIs using Java and Spring Boot.
- Designed MySQL database schemas for product and order modules.
- Used Docker Compose for local development and testing.

Projects:
E-commerce API
- Developed authentication and order management modules.
- Implemented JWT login for backend services.
- Created RESTful APIs with Spring Boot and MySQL.

Education:
Bachelor of Software Engineering
```

### 4.1 Truong bat buoc cho CV

Toi thieu nen co:

```text
candidate_name
skills
```

Trong text:

- Dong dau tien la ten ung vien.
- Dong thu hai la headline/vi tri mong muon neu co.
- Section `Skills:` la danh sach ky nang ung vien.

### 4.2 Truong rat nen co cho CV

Nen co them:

```text
summary
work_experience
projects
education
certifications
```

Quan trong nhat cho AI ranking la:

- `Skills:` de match voi JD.
- `Work Experience:` va `Projects:` de tim evidence.

Neu CV chi co danh sach skill ma khong co project/experience, AI co the cho diem evidence thap.

### 4.3 Mapping tu database web sang CV text

Neu web co ho so/CV online, co the map:

```text
candidate.full_name       -> dong dau tien
candidate.title/headline  -> dong thu hai
candidate.summary         -> Summary
candidate.skills          -> Skills
candidate.experiences     -> Work Experience
candidate.projects        -> Projects
candidate.education       -> Education
candidate.certifications  -> Certifications
```

Neu web chi co file CV upload:

```text
cv_file
  -> extract text
  -> clean text
  -> dua vao AI
```

## 5. Dang input khuyen nghi cho web integration

Voi web hien tai, khuyen nghi backend tao payload noi bo dang JSON nhu sau truoc khi goi AI.

### 5.1 Job payload

```json
{
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
}
```

Sau do convert thanh JD text theo template:

```text
{job_title}

Requirements:
- {requirement 1}
- {requirement 2}

Nice to have:
- {nice_to_have 1}

Responsibilities:
- {responsibility 1}
```

### 5.2 Candidate/CV payload

```json
{
  "application_id": 123,
  "candidate_id": 456,
  "candidate_name": "Nguyen Van A",
  "email": "candidate@example.com",
  "phone": "0900000000",
  "applied_at": "2026-06-06 22:28:00",
  "cv_text": "Nguyen Van A\nBackend Developer\n\nSummary:\n...",
  "cv_file_path": "uploads/cv/nguyen-van-a.pdf"
}
```

Trong MVP, field quan trong nhat la:

```text
candidate_name
cv_text
```

Neu `cv_text` chua co, backend can tao `cv_text` tu CV online hoac file upload.

### 5.3 Screening request payload

```json
{
  "job": {
    "job_id": 10,
    "job_title": "Backend Java Developer",
    "requirements": [],
    "nice_to_have": [],
    "responsibilities": []
  },
  "candidates": [
    {
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "cv_text": "..."
    }
  ]
}
```

Hien tai project Python da co CLI path-based. Khi tich hop web that, co 2 cach:

1. Web ghi JD/CV text ra file tam `.txt`, sau do goi CLI hoac Python service.
2. Mo rong pipeline de nhan string payload truc tiep thay vi file path.

Khuyen nghi dai han: cach 2, vi sach hon cho web/API.

## 6. Mapping theo man hinh web cua ban

### 6.1 Trang sang loc ung vien theo JD

Man hinh 1 hien danh sach tin tuyen dung:

```text
Vi tri tuyen dung
Han nop
Tong UV
Cho duyet
Trang thai
Hanh dong: Xem ung vien
```

Khi bam `Xem ung vien`, web da co:

```text
job_id
```

AI can dung `job_id` de lay:

```text
job_title
job_requirements
job_nice_to_have
job_responsibilities
```

### 6.2 Trang danh sach ung vien cua mot JD

Man hinh 2 hien:

```text
Ung vien - Test
Han nop
So ho so
Danh sach ung vien
CV online
Ngay nop
Trang thai
Xu ly
```

Tai day AI can lay danh sach application theo `job_id`:

```text
application_id
candidate_id
candidate_name
email
phone
cv_online_id hoac cv_file_path
applied_at
status
```

Sau do voi moi ung vien:

```text
CV online/file
  -> cv_text
  -> AI screening
```

Ket qua AI nen gan nguoc lai theo:

```text
application_id
candidate_id
```

De web hien dung hang ung vien.

## 7. Output AI de web hien thi

Sau khi AI chay, web nen nhan output dang:

```json
{
  "job": {
    "title": "Backend Java Developer"
  },
  "candidates": [
    {
      "rank": 1,
      "candidate_name": "Nguyen Van A",
      "final_score": 87,
      "recommendation": "Strong Review",
      "scores": {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.5,
        "seniority": 1.0,
        "domain": 1.0,
        "nice_to_have": 0.3333
      },
      "matched_skills": [],
      "missing_skills": [],
      "review_card": {
        "summary": "...",
        "strengths": [],
        "concerns": [],
        "evidence_highlights": [],
        "suggested_interview_questions": []
      }
    }
  ]
}
```

Tren UI co the hien:

- Cot AI Rank.
- Cot AI Score.
- Recommendation label.
- Button xem review card.
- Skill match/evidence khi bam chi tiet.

## 8. Luu y quan trong ve upload CV

Neu ung vien upload file:

```text
PDF/DOCX/Image
```

AI khong nen nhan file goc ngay trong MVP. Backend nen xu ly:

```text
file upload
  -> extract plain text
  -> validate text khong rong
  -> luu cv_text
  -> dua cv_text vao AI
```

Anh chup CV la truong hop kho hon vi can OCR:

```text
image
  -> OCR
  -> plain text
  -> AI
```

MVP nen uu tien:

1. CV online da co du lieu structured trong DB.
2. TXT/plain text.
3. PDF/DOCX sau khi co text extraction.
4. Image/OCR de sau.

## 9. Checklist cho web truoc khi tich hop AI

Web nen chuan bi:

- Lay duoc `job_id` khi bam `Xem ung vien`.
- Lay duoc thong tin JD theo `job_id`.
- Lay duoc danh sach application/candidate theo `job_id`.
- Moi candidate co `candidate_name`.
- Moi candidate co `cv_text` hoac co cach convert CV sang text.
- Luu duoc ket qua AI theo `application_id`.
- UI co cho hien `rank`, `final_score`, `recommendation`.
- UI co modal/page xem `review_card`.

## 10. Vi du flow tich hop de xuat

```text
Employer opens /employer/job_candidates.php?job_id=10

Backend:
1. Query job by job_id.
2. Query applications by job_id.
3. Build JD text.
4. Build CV text for each application.
5. Call AI screening service.
6. Receive ranked candidates.
7. Save ai_score, ai_rank, ai_review_card by application_id.
8. Render ranking on page.
```

## 11. Trang thai hien tai cua Python project

Hien tai project Python da chay duoc voi file text:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Input hien tai:

```text
data/jobs/jd_backend_java.txt
data/cvs/*.txt
```

Output hien tai:

```text
Ranking terminal
Optional JSON: outputs/ranking_results.json
Optional Markdown review cards: outputs/reports/
```

Buoc tich hop web sau nay nen mo rong tu file-based pipeline sang payload/API-based pipeline de web khong can thao tac file tam qua nhieu.
