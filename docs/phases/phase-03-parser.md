# Phase 03 - Resume Parser and JD Parser

## 1. Muc tieu phase

Phase 03 tao hai parser rule-based dau tien cho he thong:

- `src/resume_parser.py`
- `src/jd_parser.py`

Muc tieu la chuyen raw text da doc tu Document Loader thanh du lieu co cau truc de cac phase sau co the trich xuat skill, normalize skill, match va cham diem.

Phase nay chua cham diem va chua so khop CV voi JD.

## 2. Van de phase nay giai quyet

Sau Phase 02, he thong da doc duoc file `.txt` thanh raw text. Tuy nhien raw text van la mot chuoi dai, cac module sau chua biet dau la section Skills, Work Experience, Projects, Requirements hay Nice to have.

Phase 03 giai quyet bai toan:

```text
Raw resume text
  -> Resume Parser
  -> Candidate profile dict

Raw JD text
  -> JD Parser
  -> Job criteria dict
```

## 3. Vi sao phase nay quan trong voi do an

Parser la buoc bien text tu do thanh thong tin co cau truc. Neu parser khong tach duoc section, he thong se kho biet ung vien co skill gi, kinh nghiem nam o dau, JD yeu cau gi, va skill nao la must-have hay nice-to-have.

Trong bao cao, phase nay co the duoc giai thich la buoc information extraction co kiem soat bang rule-based logic, phu hop voi MVP khi chua dung LLM.

## 4. Pham vi thuc hien

Trong Phase 03 se lam:

- Tao `src/resume_parser.py`.
- Tao `src/jd_parser.py`.
- Parse resume text thanh candidate profile dict.
- Parse JD text thanh job criteria dict.
- Nhan dien mot so section pho bien trong demo data.
- Them test tu dong cho parser.
- Co the bo sung them CV demo neu can test parser.
- Cap nhat `docs/dev-learning-log.md`.
- Tao `docs/refactoring/phase-03-refactoring-plan.md` sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong tao skill taxonomy JSON day du.
- Khong normalize skill alias.
- Khong match skill CV/JD.
- Khong evidence scoring.
- Khong final scoring/ranking.
- Khong review card.
- Khong Streamlit UI upload file.
- Khong PDF/DOCX parsing.
- Khong embedding semantic matching.
- Khong dung LLM de parse.

## 6. Module lien quan

Module chinh:

- `src/resume_parser.py`
- `src/jd_parser.py`

Module da co va duoc dung lam input:

- `src/document_loader.py`

Tests:

- `tests/test_resume_parser.py`
- `tests/test_jd_parser.py`

Demo data:

- `data/cvs/cv_strong.txt`
- `data/jobs/jd_backend_java.txt`

## 7. File du kien tao moi

- `src/resume_parser.py`
- `src/jd_parser.py`
- `tests/test_resume_parser.py`
- `tests/test_jd_parser.py`
- `docs/phases/phase-03-parser.md`
- `docs/refactoring/phase-03-refactoring-plan.md` sau khi code xong

Co the tao them neu can:

- `data/cvs/cv_minimal.txt`

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/document_loader.py` tru khi test phat hien loi lien quan input text.
- `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md`
- `app.py`
- Scoring/matching modules vi chua thuoc phase nay.

## 9. Flow xu ly sau phase nay

Sau Phase 03, flow co the la:

```text
data/jobs/jd_backend_java.txt
  -> load_text_file()
  -> parse_jd()
  -> job criteria dict

data/cvs/cv_strong.txt
  -> load_text_file()
  -> parse_resume()
  -> candidate profile dict
```

Vi du output JD:

```python
{
    "job_title": "Backend Java Developer",
    "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Basic Docker"],
    "nice_to_have_skills": ["AWS", "Kafka", "Kubernetes"],
    "responsibilities": [
        "Develop backend services.",
        "Build RESTful APIs.",
        "Work with relational databases.",
        "Collaborate with frontend developers."
    ],
    "minimum_experience_years": 1,
    "seniority": "Junior",
    "domain": ["Backend", "Web Application"]
}
```

Vi du output resume:

```python
{
    "candidate_name": "Nguyen Van A",
    "summary": "Backend developer with experience building Java Spring Boot services and REST APIs.",
    "raw_skills": ["Java", "Spring Boot", "REST API", "MySQL", "Docker"],
    "work_experience": [
        {
            "title": "Backend Developer Intern",
            "company": "ABC Tech",
            "duration": "06/2024 - 12/2024",
            "description": [
                "Built REST APIs using Java and Spring Boot.",
                "Designed MySQL database schemas for product and order modules.",
                "Used Docker Compose for local development and testing."
            ]
        }
    ],
    "projects": [
        {
            "name": "E-commerce API",
            "description": [
                "Developed authentication and order management modules.",
                "Implemented JWT login for backend services.",
                "Created RESTful APIs with Spring Boot and MySQL."
            ]
        }
    ],
    "education": ["Bachelor of Software Engineering"],
    "certifications": []
}
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc parser rule-based la gi va vi sao parser nen tach khoi loader.

Can nam:

- Raw text khac structured data nhu the nao.
- Section detection la gi.
- Vi sao parser chi trich cau truc, khong cham diem.
- Cach parse list bullet trong text.
- Cach test parser bang input nho va output dict mong doi.

### 10.2 Cac khai niem ky thuat can hieu

- Parser: module doc text va trich thong tin co cau truc.
- Section: cac vung noi dung nhu Skills, Work Experience, Projects.
- Rule-based parsing: dung quy tac va heading de tach thong tin.
- Candidate profile: dict mo ta ung vien sau khi parse CV.
- Job criteria: dict mo ta yeu cau tuyen dung sau khi parse JD.
- Deterministic output: cung input thi parser cho cung output, de test va giai thich.

### 10.3 Cac logic nho can nam

Resume Parser:

- Lay candidate name tu dong dau tien co noi dung.
- Nhan dien section `Summary`, `Skills`, `Work Experience`, `Projects`, `Education`, `Certifications`.
- Tach bullet trong Skills thanh list.
- Tach Work Experience thanh title/company/duration/description o muc MVP.
- Tach Projects thanh name va description.

JD Parser:

- Lay job title tu dong dau tien co noi dung.
- Nhan dien `Requirements`, `Nice to have`, `Responsibilities`.
- Tach bullet thanh list.
- Tim minimum experience years tu pattern nhu `1+ year`.
- Suy luan seniority don gian tu title hoac minimum years.
- Suy luan domain don gian tu keyword nhu backend, API, web.

### 10.4 Vi du input/output

Input resume:

```text
Nguyen Van A
Backend Developer

Skills:
- Java
- Spring Boot
```

Output:

```python
{
    "candidate_name": "Nguyen Van A",
    "raw_skills": ["Java", "Spring Boot"]
}
```

Input JD:

```text
Backend Java Developer

Requirements:
- Java
- Spring Boot
- 1+ year backend experience
```

Output:

```python
{
    "job_title": "Backend Java Developer",
    "must_have_skills": ["Java", "Spring Boot"],
    "minimum_experience_years": 1
}
```

### 10.5 Noi dung co the dua vao bao cao

Parser giup he thong chuyen raw text tu CV va JD thanh du lieu co cau truc. Day la buoc quan trong de cac module sau co the xu ly theo tung truong thong tin nhu ky nang, kinh nghiem, du an va yeu cau cong viec. Trong MVP, parser duoc thiet ke rule-based de ket qua on dinh, de test va de giai thich.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/03-parser`.
2. Tao `src/resume_parser.py`.
3. Implement `parse_resume(text: str) -> dict`.
4. Tao `src/jd_parser.py`.
5. Implement `parse_jd(text: str) -> dict`.
6. Them helper nho neu can cho section extraction va bullet parsing.
7. Them `tests/test_resume_parser.py`.
8. Them `tests/test_jd_parser.py`.
9. Chay `pytest`.
10. Test thu cong bang demo JD/CV da co.
11. Cap nhat README neu can.
12. Cap nhat `docs/dev-learning-log.md`.
13. Tao `docs/refactoring/phase-03-refactoring-plan.md`.
14. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong resume:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; print(parse_resume(load_text_file('data/cvs/cv_strong.txt')))"
```

Test thu cong JD:

```bash
python -c "from src.document_loader import load_text_file; from src.jd_parser import parse_jd; print(parse_jd(load_text_file('data/jobs/jd_backend_java.txt')))"
```

## 13. Tieu chi hoan thanh phase

Phase 03 hoan thanh khi:

- `src/resume_parser.py` ton tai va parse duoc CV demo.
- `src/jd_parser.py` ton tai va parse duoc JD demo.
- Output la dict co cau truc on dinh.
- Co test tu dong cho resume parser va JD parser.
- `pytest` pass.
- Learning log duoc cap nhat.
- Refactoring plan Phase 03 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Rule-based parser co the phu thuoc vao format heading.
- CV ngoai format demo co the parse chua tot.
- Tach title/company/duration co the sai neu text khong theo pattern.
- Suy luan seniority/domain trong phase nay chi nen don gian, tranh bien thanh scoring.
- Neu parser lam qua nhieu viec, se lan sang phase Skill Extraction.

## 15. Ghi chu cho bao cao

Phase Resume Parser and JD Parser tap trung vao information extraction. He thong khong danh gia ung vien o buoc nay, ma chi chuyen CV va JD thanh cau truc du lieu ro rang. Cach tiep can rule-based trong MVP giup ket qua co the kiem thu va giai thich, dong thoi tao nen tang cho cac phase sau nhu skill taxonomy, matching, evidence detection va scoring.
