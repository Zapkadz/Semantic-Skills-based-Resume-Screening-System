# Semantic Skills-based Resume Screening System

## 1. Tên dự án

**Semantic Skills-based Resume Screening System**

Tên tiếng Việt đề xuất:

**Hệ thống sàng lọc CV theo kỹ năng sử dụng tìm kiếm ngữ nghĩa và đánh giá bằng chứng kinh nghiệm**

---

## 2. Mục tiêu tổng quan

Dự án xây dựng một hệ thống hỗ trợ nhà tuyển dụng sàng lọc CV theo hướng **skills-based hiring**. Hệ thống không chỉ so sánh CV và JD theo từ khóa hoặc độ giống văn bản đơn thuần, mà phân tích CV thành hồ sơ năng lực của ứng viên, phân tích JD thành bộ tiêu chí tuyển dụng, sau đó đánh giá mức độ phù hợp dựa trên:

- Kỹ năng bắt buộc của công việc.
- Kỹ năng bổ sung có lợi.
- Kỹ năng liên quan hoặc có thể chuyển đổi.
- Bằng chứng ứng viên đã sử dụng kỹ năng trong dự án hoặc kinh nghiệm làm việc.
- Mức kinh nghiệm và seniority.
- Mức độ phù hợp domain.
- Giải thích lý do hệ thống đề xuất ứng viên.

Dự án không tập trung vào việc train một mô hình AI mới từ đầu. Thay vào đó, hệ thống sử dụng các kỹ thuật AI/NLP có sẵn, skill taxonomy, semantic embedding, rule-based scoring và explanation generation để tạo thành một hệ thống sàng lọc CV thông minh, có thể giải thích.

---

## 3. Bản chất của dự án

Đây là một hệ thống **AI-powered recruitment screening application**, không phải một mô hình AI tự train từ đầu.

Hệ thống sử dụng:

- NLP để xử lý CV và JD.
- Skill taxonomy để chuẩn hóa kỹ năng.
- Semantic similarity để hiểu mức độ liên quan giữa kỹ năng/mô tả kinh nghiệm và yêu cầu công việc.
- Rule-based matching để xử lý exact match, alias match, related match và transferable match.
- Evidence-based scoring để giảm tình trạng CV nhồi keyword nhưng thiếu bằng chứng thực tế.
- Explainable output để nhà tuyển dụng hiểu vì sao ứng viên được xếp hạng cao hoặc thấp.

Nói ngắn gọn:

```text
CV/JD text
→ Information extraction
→ Skill normalization
→ Semantic skill matching
→ Evidence detection
→ Scoring
→ Ranking
→ Recruiter review card
```

---

## 4. Vấn đề cần giải quyết

Các hệ thống lọc CV truyền thống thường dựa vào keyword matching hoặc text similarity đơn giản. Cách này có một số hạn chế:

1. Ứng viên phù hợp có thể bị bỏ sót nếu không dùng đúng từ khóa trong JD.
2. CV nhồi keyword có thể được đánh giá cao dù thiếu kinh nghiệm thực tế.
3. Hệ thống khó hiểu kỹ năng liên quan hoặc kỹ năng có thể chuyển đổi.
4. Kết quả chỉ là một điểm số, thiếu giải thích cho recruiter.
5. Không phân biệt được kỹ năng chỉ được liệt kê với kỹ năng đã được sử dụng trong dự án thật.

Ví dụ:

JD yêu cầu:

```text
Backend API development
```

CV ghi:

```text
Built RESTful services using Spring Boot and MySQL.
```

Keyword matching có thể không đánh giá chính xác nếu câu chữ không trùng. Hệ thống cần hiểu rằng:

```text
RESTful services + Spring Boot ≈ Backend API development
```

---

## 5. Hướng tiếp cận của dự án

Dự án đi theo hướng:

```text
Semantic + Skills-based + Evidence-based + Explainable Screening
```

Trong đó:

- **Semantic**: hiểu ngữ nghĩa, không chỉ trùng từ khóa.
- **Skills-based**: đánh giá dựa trên kỹ năng và yêu cầu công việc.
- **Evidence-based**: kiểm tra bằng chứng kỹ năng trong project/experience.
- **Explainable**: tạo review card có giải thích rõ ràng.

---

## 6. Phạm vi MVP

Phiên bản MVP nên tập trung vào nhóm ngành IT, ưu tiên role:

- Backend Developer.
- Java Developer.
- Frontend Developer.
- Fullstack Developer.
- Tester/QA.
- Data Analyst.

MVP ban đầu nên tập trung trước vào một job mẫu:

```text
Backend Java Developer
```

Input MVP:

- 1 JD dạng TXT.
- N CV dạng TXT.

Output MVP:

- Danh sách ứng viên được xếp hạng.
- Final score.
- Recommendation label.
- Matched skills.
- Missing skills.
- Evidence cho từng skill.
- Seniority detection.
- Explanation.
- Suggested interview questions.

---

## 7. Kiến trúc tổng quan

```text
                 ┌──────────────────┐
                 │       CV         │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Resume Parser    │
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Candidate Profile│
                 └────────┬─────────┘
                          ↓
                 ┌──────────────────┐
                 │ Candidate Skills │
                 └────────┬─────────┘
                          ↓
┌──────────────┐   ┌──────────────────┐
│      JD      │ → │ JD Parser        │
└──────────────┘   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Job Criteria     │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Skill Normalizer │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Semantic Matcher │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Evidence Detector│
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Scorer           │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Ranking          │
                   └────────┬─────────┘
                            ↓
                   ┌──────────────────┐
                   │ Review Card      │
                   └──────────────────┘
```

---

## 8. Các module chính

### 8.1 Document Loader

File đề xuất:

```text
src/document_loader.py
```

Nhiệm vụ:

- Đọc nội dung CV/JD từ file.
- MVP ưu tiên hỗ trợ `.txt`.
- Bản nâng cấp hỗ trợ `.pdf`, `.docx`.

Input:

```text
data/cvs/cv_strong.txt
data/jobs/jd_backend_java.txt
```

Output:

```python
str
```

Ví dụ output:

```text
Nguyen Van A
Backend Developer
Built REST APIs using Java Spring Boot and MySQL...
```

---

### 8.2 Resume Parser

File đề xuất:

```text
src/resume_parser.py
```

Nhiệm vụ:

- Phân tích CV text thành candidate profile có cấu trúc.
- Nhận diện các section phổ biến:
  - Personal Information.
  - Summary.
  - Skills.
  - Work Experience.
  - Projects.
  - Education.
  - Certifications.

Output dạng JSON/dict:

```json
{
  "candidate_name": "Nguyen Van A",
  "email": "vana@example.com",
  "phone": "0123456789",
  "summary": "Backend developer with experience in Java Spring Boot.",
  "raw_skills": [
    "Java",
    "Spring Boot",
    "REST API",
    "MySQL",
    "Docker"
  ],
  "work_experience": [
    {
      "title": "Backend Developer Intern",
      "company": "ABC Tech",
      "duration": "06/2024 - 12/2024",
      "description": [
        "Built REST APIs using Java Spring Boot",
        "Designed MySQL database schema",
        "Used Docker Compose for local deployment"
      ]
    }
  ],
  "projects": [
    {
      "name": "E-commerce API",
      "description": [
        "Developed authentication and order modules",
        "Implemented JWT login",
        "Created RESTful APIs with Spring Boot"
      ],
      "technologies": [
        "Java",
        "Spring Boot",
        "MySQL",
        "Docker"
      ]
    }
  ],
  "education": [
    "Bachelor of Software Engineering"
  ],
  "certifications": []
}
```

MVP có thể dùng rule-based parser thay vì LLM.

---

### 8.3 JD Parser

File đề xuất:

```text
src/jd_parser.py
```

Nhiệm vụ:

- Phân tích JD thành bộ tiêu chí tuyển dụng.
- Tách must-have skills, nice-to-have skills, responsibilities, seniority, domain và minimum experience.

Output dạng JSON/dict:

```json
{
  "job_title": "Backend Java Developer",
  "must_have_skills": [
    "Java",
    "Spring Boot",
    "REST API",
    "SQL"
  ],
  "nice_to_have_skills": [
    "Docker",
    "Kubernetes",
    "AWS",
    "Kafka"
  ],
  "responsibilities": [
    "Develop backend services",
    "Build REST APIs",
    "Work with relational databases"
  ],
  "minimum_experience_years": 1,
  "seniority": "Junior/Middle",
  "domain": [
    "Backend",
    "Web Application"
  ]
}
```

JD parser cần nhận diện các cụm như:

```text
Requirements
Must have
Required skills
Nice to have
Responsibilities
Qualifications
Preferred
```

---

### 8.4 Skill Taxonomy

File đề xuất:

```text
data/taxonomy/skills.json
src/skill_taxonomy.py
```

Nhiệm vụ:

- Lưu danh sách kỹ năng chuẩn.
- Lưu alias của kỹ năng.
- Lưu category.
- Lưu related skills.
- Lưu transferable skills.

Ví dụ:

```json
{
  "Java": {
    "aliases": ["Core Java", "Java SE"],
    "category": "Programming Language",
    "related": ["Spring Boot", "Hibernate", "Maven"],
    "transferable": ["C#", "Kotlin"]
  },
  "Spring Boot": {
    "aliases": ["SpringBoot", "Spring Framework"],
    "category": "Backend Framework",
    "related": ["Java", "REST API", "Microservices"],
    "transferable": ["ASP.NET Core", "Express.js", "Django"]
  },
  "React": {
    "aliases": ["ReactJS", "React.js"],
    "category": "Frontend Framework",
    "related": ["JavaScript", "TypeScript", "Redux"],
    "transferable": ["Vue.js", "Angular"]
  },
  "PostgreSQL": {
    "aliases": ["Postgres", "PostgreSQL DB"],
    "category": "Database",
    "related": ["SQL", "Relational Database"],
    "transferable": ["MySQL", "SQL Server"]
  },
  "Kubernetes": {
    "aliases": ["K8s"],
    "category": "DevOps",
    "related": ["Docker", "Containerization", "Cloud"],
    "transferable": []
  }
}
```

Nhóm skill nên có trong MVP:

- Programming Language.
- Backend Framework.
- Frontend Framework.
- Database.
- DevOps.
- Cloud.
- Testing.
- Data.
- Soft Skills.

---

### 8.5 Skill Normalizer

File đề xuất:

```text
src/skill_normalizer.py
```

Nhiệm vụ:

- Chuẩn hóa kỹ năng về tên chuẩn.
- Xử lý alias.
- Xử lý viết tắt.

Ví dụ:

```text
ReactJS → React
React.js → React
K8s → Kubernetes
Postgres → PostgreSQL
JS → JavaScript
Node → Node.js
SpringBoot → Spring Boot
```

Function đề xuất:

```python
def normalize_skill(skill: str, taxonomy: dict) -> str:
    pass


def normalize_skills(skills: list[str], taxonomy: dict) -> list[str]:
    pass
```

---

### 8.6 Skill Extractor

File đề xuất:

```text
src/skill_extractor.py
```

Nhiệm vụ:

- Tìm các kỹ năng xuất hiện trong CV/JD text.
- Dựa vào taxonomy và aliases.
- Trích xuất skill từ raw text, project, experience và skill section.

Input:

```text
Built REST APIs using Java Spring Boot and MySQL. Containerized app with Docker.
```

Output:

```json
[
  "REST API",
  "Java",
  "Spring Boot",
  "MySQL",
  "Docker"
]
```

MVP có thể dùng matching theo keyword/alias trong taxonomy.

---

### 8.7 Semantic Matcher

File đề xuất:

```text
src/semantic_matcher.py
```

Nhiệm vụ:

- So khớp kỹ năng JD với kỹ năng CV.
- Hỗ trợ nhiều loại match:
  - exact_match.
  - alias_match.
  - related_match.
  - transferable_match.
  - semantic_match.
  - no_match.

Các loại match:

```text
exact_match:
JD skill và CV skill giống nhau.

alias_match:
JD skill và CV skill là alias của nhau.
Ví dụ ReactJS ↔ React.

related_match:
CV skill có liên quan trực tiếp đến JD skill.
Ví dụ MySQL ↔ SQL.

transferable_match:
CV skill không giống nhưng có thể chuyển đổi về mặt năng lực.
Ví dụ ASP.NET Core backend ↔ Spring Boot backend.

semantic_match:
Mô tả kinh nghiệm trong CV gần nghĩa với yêu cầu JD.
Ví dụ "Built RESTful services" ↔ "Backend API development".

no_match:
Không tìm thấy tín hiệu phù hợp.
```

Điểm mặc định:

```text
exact_match        = 1.00
alias_match        = 0.95
semantic_match     = 0.85
related_match      = 0.75
transferable_match = 0.55
no_match           = 0.00
```

Output ví dụ:

```json
[
  {
    "required_skill": "Java",
    "candidate_skill": "Java",
    "match_type": "exact_match",
    "score": 1.0
  },
  {
    "required_skill": "SQL",
    "candidate_skill": "MySQL",
    "match_type": "related_match",
    "score": 0.75
  },
  {
    "required_skill": "Spring Boot",
    "candidate_skill": "ASP.NET Core",
    "match_type": "transferable_match",
    "score": 0.55
  }
]
```

MVP implementation order:

1. Exact match.
2. Alias match.
3. Related match.
4. Transferable match.
5. Semantic embedding matching.

Embedding model đề xuất cho bản nâng cấp:

```text
sentence-transformers/all-MiniLM-L6-v2
BAAI/bge-small-en-v1.5
intfloat/e5-small-v2
```

---

### 8.8 Evidence Detector

File đề xuất:

```text
src/evidence_detector.py
```

Nhiệm vụ:

- Kiểm tra mỗi skill có bằng chứng thực tế trong CV hay không.
- Phân biệt skill chỉ nằm trong skill list với skill có trong project/experience.
- Trích xuất câu bằng chứng cho từng skill.

Evidence level:

```text
0 = Không tìm thấy skill.
1 = Skill chỉ xuất hiện trong skill list.
2 = Skill xuất hiện trong project hoặc work experience.
3 = Skill xuất hiện cùng hành động cụ thể, ngữ cảnh rõ hoặc kết quả cụ thể.
```

Ví dụ:

```text
Level 1:
Skills: Docker

Level 2:
Used Docker in project.

Level 3:
Containerized Spring Boot services using Docker Compose for deployment.
```

Action verbs tiếng Anh:

```text
built
developed
implemented
designed
deployed
optimized
integrated
configured
maintained
tested
automated
containerized
created
improved
refactored
monitored
```

Action verbs tiếng Việt:

```text
xây dựng
phát triển
triển khai
thiết kế
tối ưu
tích hợp
cấu hình
kiểm thử
tự động hóa
bảo trì
cải thiện
```

Output ví dụ:

```json
{
  "skill": "Docker",
  "found": true,
  "evidence_level": 3,
  "evidence_text": "Containerized Spring Boot service using Docker Compose",
  "confidence": 0.91
}
```

---

### 8.9 Experience Analyzer

File đề xuất:

```text
src/experience_analyzer.py
```

Nhiệm vụ:

- Ước tính số năm kinh nghiệm từ CV.
- Nhận diện khoảng thời gian trong work experience.
- Nhận diện các cụm như:
  - 1 year of experience.
  - 2+ years.
  - 06/2024 - 12/2024.
  - 2023 - 2025.

Output:

```json
{
  "estimated_years": 1.5,
  "experience_evidence": [
    "Backend Developer Intern, 06/2024 - 12/2024",
    "Java Backend Developer, 01/2025 - Present"
  ]
}
```

Experience score logic:

```text
candidate_years >= required_years:
score = 1.0

candidate_years >= 0.75 * required_years:
score = 0.75

candidate_years >= 0.5 * required_years:
score = 0.5

otherwise:
score = 0.25
```

---

### 8.10 Seniority Detector

File đề xuất:

```text
src/seniority_detector.py
```

Nhiệm vụ:

- Phân loại seniority của ứng viên.
- So sánh với seniority yêu cầu của JD.

Các cấp độ:

```text
Intern
Fresher
Junior
Middle
Senior
Lead
```

Tín hiệu nhận diện:

```text
Intern/Fresher:
- internship
- academic project
- coursework
- basic CRUD
- learned

Junior:
- developed features
- fixed bugs
- built APIs
- worked under guidance

Middle:
- owned modules
- optimized performance
- handled production issues
- integrated third-party services

Senior:
- designed architecture
- led technical decisions
- mentored developers
- scaled systems
- distributed systems

Lead:
- led team
- managed delivery
- architecture ownership
- cross-team coordination
```

Output:

```json
{
  "detected_seniority": "Junior/Middle",
  "seniority_score": 0.75,
  "seniority_evidence": [
    "Built REST APIs",
    "Designed database schema",
    "Deployed service using Docker"
  ]
}
```

---

### 8.11 Domain Analyzer

File đề xuất:

```text
src/domain_analyzer.py
```

Nhiệm vụ:

- Nhận diện domain trong CV và JD.
- So sánh domain fit.

Ví dụ domain:

```text
Backend
Frontend
Fullstack
E-commerce
Fintech
Education
Healthcare
Data Analytics
DevOps
Testing
Mobile
```

Output:

```json
{
  "candidate_domains": ["Backend", "E-commerce"],
  "job_domains": ["Backend", "Web Application"],
  "domain_score": 0.85
}
```

---

### 8.12 Scorer

File đề xuất:

```text
src/scorer.py
```

Nhiệm vụ:

- Tính điểm tổng cho từng ứng viên.
- Kết hợp các điểm thành phần:
  - Semantic Skill Match.
  - Evidence Strength.
  - Experience Fit.
  - Seniority Fit.
  - Domain Fit.
  - Nice-to-have Bonus.

Công thức đề xuất:

```text
Final Score =
  0.40 × Score_skill_semantic
+ 0.20 × Score_evidence
+ 0.15 × Score_experience
+ 0.10 × Score_seniority
+ 0.10 × Score_domain
+ 0.05 × Score_nice_to_have
```

Tất cả score thành phần nằm trong khoảng 0 đến 1. Final score nhân 100.

Recommendation label:

```text
85 - 100: Strong Review
70 - 84: Review
55 - 69: Maybe Review
40 - 54: Low Priority
0 - 39: Not Enough Evidence
```

Không nên dùng label như `Reject`, `Fail`, `Pass`, vì hệ thống chỉ hỗ trợ recruiter, không thay thế quyết định cuối cùng của con người.

---

### 8.13 Review Card Generator

File đề xuất:

```text
src/review_card_generator.py
```

Nhiệm vụ:

- Sinh báo cáo đánh giá ứng viên dễ hiểu cho recruiter.
- Review card nên có:
  - Candidate name.
  - Target role.
  - Final score.
  - Recommendation label.
  - Matched must-have skills.
  - Matched nice-to-have skills.
  - Missing/weak skills.
  - Evidence.
  - Seniority.
  - Strengths.
  - Concerns.
  - Suggested interview questions.

Output mẫu:

```text
Candidate: Nguyen Van A
Target Role: Backend Java Developer

Recommendation: Strong Review
Final Score: 86/100

Matched Must-have Skills:
✓ Java — exact match — strong evidence
  Evidence: Built REST APIs using Java Spring Boot.

✓ Spring Boot — exact match — strong evidence
  Evidence: Developed authentication and order modules using Spring Boot.

✓ REST API — semantic match — strong evidence
  Evidence: Created RESTful APIs for product and order management.

✓ SQL — related match — medium evidence
  Evidence: Designed MySQL database schema.

Nice-to-have Skills:
✓ Docker — exact match — strong evidence
△ AWS — missing
△ Kafka — missing

Seniority:
Junior to Middle

Strengths:
- Strong backend development experience with Java Spring Boot.
- Clear evidence of REST API and database work.
- Has Docker deployment experience.

Concerns:
- No clear evidence of cloud deployment.
- No Kafka or distributed messaging experience.
- Production scale is not clearly shown.

Suggested Interview Questions:
1. Explain the authentication flow in your Spring Boot project.
2. How did you design your database schema?
3. Have you deployed your backend service to cloud or only locally?
```

---

## 9. Cấu trúc thư mục đề xuất

```text
semantic-resume-screening/
│
├── app.py
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── cvs/
│   │   ├── cv_strong.txt
│   │   ├── cv_medium.txt
│   │   ├── cv_keyword_stuffing.txt
│   │   ├── cv_transferable.txt
│   │   └── cv_weak.txt
│   │
│   ├── jobs/
│   │   └── jd_backend_java.txt
│   │
│   └── taxonomy/
│       └── skills.json
│
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── resume_parser.py
│   ├── jd_parser.py
│   ├── skill_taxonomy.py
│   ├── skill_extractor.py
│   ├── skill_normalizer.py
│   ├── semantic_matcher.py
│   ├── evidence_detector.py
│   ├── experience_analyzer.py
│   ├── seniority_detector.py
│   ├── domain_analyzer.py
│   ├── scorer.py
│   ├── review_card_generator.py
│   └── utils.py
│
├── outputs/
│   ├── candidate_profiles/
│   ├── job_criteria/
│   ├── reports/
│   └── ranking_results.json
│
└── tests/
    ├── test_skill_normalizer.py
    ├── test_semantic_matcher.py
    ├── test_evidence_detector.py
    └── test_scorer.py
```

---

## 10. Luồng xử lý chính

### CLI flow

Command đề xuất:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Các bước xử lý:

```text
1. Load JD text.
2. Parse JD thành job criteria.
3. Load tất cả CV trong thư mục.
4. Parse từng CV thành candidate profile.
5. Extract skills từ JD và CV.
6. Normalize skills bằng taxonomy.
7. Match JD skills với candidate skills.
8. Detect evidence cho từng matched skill.
9. Analyze experience và seniority.
10. Tính final score.
11. Rank candidates.
12. Generate review card cho từng candidate.
13. Save output vào outputs/.
```

Output CLI mẫu:

```text
Rank 1: Nguyen Van A — 86/100 — Strong Review
Rank 2: Tran Thi B — 72/100 — Review
Rank 3: Le Van C — 58/100 — Maybe Review
Rank 4: Pham Van D — 41/100 — Low Priority
Rank 5: Hoang Van E — 28/100 — Not Enough Evidence
```

---

## 11. Streamlit UI đề xuất

File:

```text
app.py
```

UI cần có:

1. Upload JD.
2. Upload nhiều CV.
3. Button `Analyze Candidates`.
4. Bảng ranking:
   - Rank.
   - Candidate name.
   - Final score.
   - Recommendation.
   - Skill match score.
   - Evidence score.
   - Seniority.
5. Khi click vào candidate:
   - Hiển thị review card.
   - Matched skills.
   - Missing skills.
   - Evidence text.
   - Suggested interview questions.

---

## 12. Dữ liệu demo nên chuẩn bị

JD mẫu:

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

CV demo:

### CV 1: Strong fit

Đặc điểm:

```text
Java, Spring Boot, REST API, MySQL, Docker.
Có project backend rõ ràng.
Có evidence mạnh.
```

Expected:

```text
Strong Review, score >= 85
```

### CV 2: Medium fit

Đặc điểm:

```text
Java, SQL, REST API.
Thiếu Spring Boot hoặc Docker yếu.
```

Expected:

```text
Review, score khoảng 70-84
```

### CV 3: Keyword stuffing

Đặc điểm:

```text
Skills list có Java, Spring Boot, Docker, Kafka, AWS.
Nhưng project/experience không chứng minh được.
```

Expected:

```text
Maybe Review hoặc Low Priority.
Lý do: nhiều keyword nhưng evidence yếu.
```

### CV 4: Transferable skills

Đặc điểm:

```text
C#, ASP.NET Core, REST API, SQL Server, Docker.
Không có Java/Spring Boot nhưng có backend transferable skill.
```

Expected:

```text
Maybe Review.
Lý do: backend skill tốt nhưng thiếu core Java/Spring Boot.
```

### CV 5: Weak fit

Đặc điểm:

```text
HTML, CSS, Photoshop, content marketing.
```

Expected:

```text
Not Enough Evidence.
```

---

## 13. Output JSON tổng hợp đề xuất

File:

```text
outputs/ranking_results.json
```

Schema:

```json
{
  "job": {
    "title": "Backend Java Developer",
    "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL"],
    "nice_to_have_skills": ["Docker", "AWS", "Kafka", "Kubernetes"]
  },
  "candidates": [
    {
      "rank": 1,
      "candidate_name": "Nguyen Van A",
      "final_score": 86,
      "recommendation": "Strong Review",
      "scores": {
        "skill_semantic": 0.91,
        "evidence": 0.95,
        "experience": 0.80,
        "seniority": 0.85,
        "domain": 0.90,
        "nice_to_have": 0.60
      },
      "matched_skills": [
        {
          "required_skill": "Java",
          "candidate_skill": "Java",
          "match_type": "exact_match",
          "match_score": 1.0,
          "evidence_level": 3,
          "evidence_text": "Built REST APIs using Java Spring Boot."
        }
      ],
      "missing_skills": ["Kafka", "AWS"],
      "seniority": "Junior/Middle",
      "strengths": [
        "Strong Java Spring Boot backend experience.",
        "Clear REST API and database project evidence."
      ],
      "concerns": [
        "No clear evidence of cloud deployment.",
        "No Kafka or distributed messaging experience."
      ],
      "interview_questions": [
        "Explain how you designed authentication in your Spring Boot project.",
        "How did you design your database schema?",
        "Have you deployed this backend service to cloud or only locally?"
      ]
    }
  ]
}
```

---

## 14. Quy tắc scoring chi tiết

### 14.1 Skill semantic score

Chỉ tính trên must-have skills.

Ví dụ JD có:

```text
Java, Spring Boot, REST API, SQL
```

Candidate match:

```text
Java = 1.0
Spring Boot = 1.0
REST API = 0.85
SQL = 0.75
```

Skill semantic score:

```text
(1.0 + 1.0 + 0.85 + 0.75) / 4 = 0.90
```

### 14.2 Evidence score

Map evidence level sang score:

```text
Level 0 → 0.0
Level 1 → 0.4
Level 2 → 0.7
Level 3 → 1.0
```

Evidence score là trung bình evidence score của các must-have skill đã match.

### 14.3 Experience score

```text
candidate_years >= required_years:
score = 1.0

candidate_years >= 0.75 * required_years:
score = 0.75

candidate_years >= 0.5 * required_years:
score = 0.5

otherwise:
score = 0.25
```

### 14.4 Seniority score

Mapping:

```text
JD Junior, Candidate Junior → 1.0
JD Junior/Middle, Candidate Junior → 0.85
JD Junior/Middle, Candidate Middle → 1.0
JD Middle, Candidate Junior → 0.65
JD Senior, Candidate Junior → 0.25
Candidate much higher than JD → 0.7 to 0.85 depending on context
```

### 14.5 Domain score

```text
Exact domain overlap → 1.0
Related domain → 0.75
Generic IT/software domain → 0.5
No domain evidence → 0.25
Wrong domain → 0.0
```

### 14.6 Nice-to-have score

```text
matched nice-to-have skills / total nice-to-have skills
```

Nếu JD không có nice-to-have skills, mặc định score = 0.5 hoặc bỏ trọng số này và redistribute weight.

---

## 15. Quy tắc phát triển code cho Cursor

Khi triển khai, Cursor cần ưu tiên:

1. Viết code rõ ràng, dễ đọc, tách module.
2. Mỗi module nên có function nhỏ, dễ test.
3. Không hard-code toàn bộ logic trong `main.py`.
4. Các tham số scoring nên để trong config hoặc constant.
5. Taxonomy nên nằm trong file JSON để dễ chỉnh sửa.
6. Output nên là dict/JSON chuẩn để UI hoặc CLI đều dùng được.
7. Không để AI/LLM tự quyết định toàn bộ kết quả. Scoring phải dựa trên rule rõ ràng.
8. Nếu dùng embedding model, cần fallback khi model không tải được.
9. MVP phải chạy được với file TXT trước, sau đó mới mở rộng PDF/DOCX.
10. Tất cả kết quả quan trọng cần có explanation.

---

## 16. Thứ tự triển khai đề xuất cho Cursor

### Step 1: Tạo skeleton project

Tạo cấu trúc thư mục:

```text
data/
src/
outputs/
tests/
```

Tạo file:

```text
main.py
app.py
requirements.txt
README.md
```

### Step 2: Tạo data demo

Tạo:

```text
data/jobs/jd_backend_java.txt
data/cvs/cv_strong.txt
data/cvs/cv_medium.txt
data/cvs/cv_keyword_stuffing.txt
data/cvs/cv_transferable.txt
data/cvs/cv_weak.txt
data/taxonomy/skills.json
```

### Step 3: Implement document_loader.py

Function:

```python
def load_text_file(path: str) -> str:
    pass
```

### Step 4: Implement skill_taxonomy.py

Function:

```python
def load_taxonomy(path: str) -> dict:
    pass


def build_alias_map(taxonomy: dict) -> dict:
    pass
```

### Step 5: Implement skill_extractor.py

Function:

```python
def extract_skills(text: str, taxonomy: dict) -> list[str]:
    pass
```

### Step 6: Implement skill_normalizer.py

Function:

```python
def normalize_skill(skill: str, taxonomy: dict) -> str:
    pass


def normalize_skills(skills: list[str], taxonomy: dict) -> list[str]:
    pass
```

### Step 7: Implement jd_parser.py

Function:

```python
def parse_jd(text: str, taxonomy: dict) -> dict:
    pass
```

### Step 8: Implement resume_parser.py

Function:

```python
def parse_resume(text: str, taxonomy: dict) -> dict:
    pass
```

### Step 9: Implement semantic_matcher.py

Function:

```python
def match_skills(job_skills: list[str], candidate_skills: list[str], taxonomy: dict) -> list[dict]:
    pass
```

### Step 10: Implement evidence_detector.py

Function:

```python
def detect_evidence(skill: str, resume_profile: dict) -> dict:
    pass


def detect_all_evidence(matches: list[dict], resume_profile: dict) -> list[dict]:
    pass
```

### Step 11: Implement experience_analyzer.py

Function:

```python
def estimate_experience_years(resume_profile: dict) -> dict:
    pass
```

### Step 12: Implement seniority_detector.py

Function:

```python
def detect_seniority(resume_profile: dict) -> dict:
    pass
```

### Step 13: Implement scorer.py

Function:

```python
def score_candidate(job_criteria: dict, resume_profile: dict, matches: list[dict]) -> dict:
    pass
```

### Step 14: Implement review_card_generator.py

Function:

```python
def generate_review_card(candidate_result: dict) -> str:
    pass
```

### Step 15: Implement main.py

CLI command:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

### Step 16: Implement app.py

Streamlit UI:

```bash
streamlit run app.py
```

---

## 17. Requirements đề xuất

File:

```text
requirements.txt
```

Nội dung MVP:

```text
streamlit
pandas
numpy
scikit-learn
python-docx
pymupdf
sentence-transformers
```

Nếu MVP chỉ chạy TXT và rule-based thì có thể bắt đầu với:

```text
streamlit
pandas
numpy
```

Sau đó thêm dần:

```text
sentence-transformers
scikit-learn
pymupdf
python-docx
```

---

## 18. Những điểm không nên làm trong MVP

Không nên làm ngay:

- Train model từ đầu.
- Fine-tune model khi chưa có dataset có label.
- Xử lý tất cả ngành nghề.
- Làm graph database phức tạp.
- Dùng LLM để quyết định điểm số cuối cùng.
- Tự động reject ứng viên tuyệt đối.
- Phụ thuộc hoàn toàn vào PDF parser ngay từ đầu.

Nên ưu tiên:

- TXT input trước.
- Taxonomy nhỏ nhưng rõ.
- Rule-based matching chạy ổn.
- Evidence detection rõ ràng.
- Review card dễ hiểu.
- Sau đó mới thêm embedding.

---

## 19. Tiêu chí đánh giá hệ thống

Để báo cáo/demo, hệ thống nên chứng minh được:

1. CV phù hợp có điểm cao.
2. CV không phù hợp có điểm thấp.
3. CV nhồi keyword không được điểm quá cao nếu thiếu evidence.
4. CV có transferable skills được nhận diện ở mức vừa phải.
5. Hệ thống giải thích được vì sao ứng viên được xếp hạng như vậy.
6. Hệ thống chỉ hỗ trợ recruiter, không thay thế hoàn toàn quyết định tuyển dụng.

---

## 20. Câu mô tả đề tài dùng trong báo cáo

Có thể dùng đoạn sau:

```text
Đề tài xây dựng hệ thống sàng lọc CV theo kỹ năng sử dụng tìm kiếm ngữ nghĩa và đánh giá bằng chứng kinh nghiệm. Thay vì chỉ so khớp CV và mô tả công việc dựa trên từ khóa hoặc độ tương đồng văn bản, hệ thống phân tích CV thành hồ sơ năng lực của ứng viên, trích xuất và chuẩn hóa kỹ năng theo taxonomy, phát hiện các kỹ năng liên quan hoặc có thể chuyển đổi, đánh giá mức độ bằng chứng của từng kỹ năng trong dự án hoặc kinh nghiệm làm việc, sau đó xếp hạng ứng viên và sinh thẻ đánh giá có giải thích cho nhà tuyển dụng.
```

---

## 21. Câu trả lời khi được hỏi có train AI không

```text
Dự án không train mô hình AI từ đầu. Thay vào đó, hệ thống sử dụng các kỹ thuật NLP và mô hình ngôn ngữ đã được huấn luyện sẵn để biểu diễn ngữ nghĩa của kỹ năng và mô tả kinh nghiệm, kết hợp với skill taxonomy và scoring rule để đánh giá mức độ phù hợp giữa CV và yêu cầu tuyển dụng. Cách tiếp cận này phù hợp với điều kiện dữ liệu hạn chế của đồ án và vẫn phản ánh được cách các hệ thống tuyển dụng hiện đại ứng dụng AI trong thực tế.
```

---

## 22. Định hướng nâng cấp sau MVP

Sau khi MVP chạy tốt, có thể nâng cấp:

### 22.1 PDF/DOCX support

- PDF: PyMuPDF.
- DOCX: python-docx.

### 22.2 Embedding semantic search

- sentence-transformers.
- FAISS hoặc ChromaDB nếu cần index nhiều CV.

### 22.3 LLM explanation

- Dùng LLM để viết review card tự nhiên hơn.
- Không dùng LLM để tự chấm điểm nếu không có rule kiểm soát.

### 22.4 Recruiter feedback loop

Cho recruiter đánh dấu:

```text
Good recommendation
Bad recommendation
Need review
```

Sau đó lưu feedback để điều chỉnh weight/scoring.

### 22.5 Audit log

Lưu lại:

- Input JD.
- Input CV.
- Skills extracted.
- Match result.
- Score components.
- Final recommendation.

Audit log giúp hệ thống minh bạch hơn.

---

## 23. Kết luận định hướng

Dự án cần được triển khai theo hướng:

```text
Không chỉ tính CV giống JD bao nhiêu phần trăm.
Mà đánh giá ứng viên có kỹ năng gì, kỹ năng đó có bằng chứng không, có liên quan đến yêu cầu công việc không, mức kinh nghiệm có phù hợp không, và vì sao recruiter nên hoặc không nên xem tiếp ứng viên đó.
```

Tên kỹ thuật nên dùng:

```text
Semantic Skills-based Resume Screening System
```

Tên tiếng Việt nên dùng:

```text
Hệ thống sàng lọc CV theo kỹ năng sử dụng tìm kiếm ngữ nghĩa và đánh giá bằng chứng kinh nghiệm
```
