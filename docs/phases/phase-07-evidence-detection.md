# Phase 07 - Evidence Detection

## 1. Muc tieu phase

Phase 07 tao module Evidence Detection de kiem tra cac skill da match co bang chung trong CV hay khong.

Sau Phase 05/06, he thong da biet JD skill nao match voi candidate skill nao. Tuy nhien, match skill chua du de danh gia ung vien. Can biet skill do chi nam trong danh sach Skills hay co duoc ung vien su dung trong Work Experience/Projects.

Muc tieu:

- Tao `src/evidence_detector.py`.
- Gan evidence level cho tung matched skill.
- Tra ve evidence text neu tim thay.
- Phan biet keyword-only evidence voi project/work evidence.
- Them tests cho evidence detector.

Phase nay chua tinh final score/ranking.

## 2. Van de phase nay giai quyet

Mot CV co the ghi:

```text
Skills:
- Java
- Spring Boot
- Docker
- Kafka
```

Nhung neu Work Experience/Projects khong co dong nao cho thay ung vien da dung cac skill do, he thong khong nen danh gia bang chung qua cao.

Phase 07 giai quyet bai toan:

```text
matched skill
  -> search resume profile evidence
  -> evidence level + evidence text
```

## 3. Vi sao phase nay quan trong voi do an

Evidence Detection la diem khac biet quan trong cua du an so voi keyword matching thong thuong. No giup he thong:

- Giam tinh trang CV nhoi keyword.
- Uu tien skill co bang chung trong project/experience.
- Tao du lieu cho scoring evidence o Phase 08.
- Giai thich duoc vi sao ung vien duoc danh gia tot hoac yeu.

Trong bao cao, day la buoc evidence-based screening.

## 4. Pham vi thuc hien

Trong Phase 07 se lam:

- Tao `src/evidence_detector.py`.
- Implement `detect_evidence(skill, resume_profile) -> dict`.
- Implement `detect_all_evidence(matches, resume_profile) -> list[dict]`.
- Evidence level MVP:
  - Level 0: Khong co bang chung.
  - Level 1: Chi xuat hien trong summary/headline hoac skill list.
  - Level 2: Xuat hien trong work experience/project context.
  - Level 3: Xuat hien trong action-based bullet co dong tu hanh dong.
- Them evidence text dau tien phu hop.
- Them tests cho evidence detector.
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong final scoring.
- Khong ranking.
- Khong recommendation label.
- Khong review card.
- Khong interview questions.
- Khong LLM explanation.
- Khong thay match score.
- Khong sua semantic matcher neu khong co loi.
- Khong PDF/DOCX support.

## 6. Module lien quan

Module chinh:

- `src/evidence_detector.py`

Module input tu phase truoc:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `src/semantic_matcher.py`

Tests:

- `tests/test_evidence_detector.py`

## 7. File du kien tao moi

- `src/evidence_detector.py`
- `tests/test_evidence_detector.py`
- `docs/phases/phase-07-evidence-detection.md`
- `docs/refactoring/phase-07-refactoring-plan.md` sau khi code xong

Co the tao them demo CV neu can test keyword stuffing:

- `data/cvs/cv_keyword_stuffing.txt`

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/semantic_matcher.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_normalizer.py`
- `app.py`

## 9. Flow xu ly sau phase nay

Sau Phase 07, flow co the la:

```text
CV text
  -> parse_resume()
  -> resume_profile

JD text + CV text
  -> match_skills()
  -> matches

matches + resume_profile
  -> detect_all_evidence()
  -> matches enriched with evidence
```

Vi du output:

```python
{
    "required_skill": "Java",
    "candidate_skill": "Java",
    "match_type": "exact_match",
    "score": 1.0,
    "evidence_level": 3,
    "evidence_text": "Built REST APIs using Java and Spring Boot.",
    "evidence_source": "work_experience"
}
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc:

- Evidence la gi trong bai toan CV screening.
- Vi sao keyword trong Skills section chua du.
- Cach tim bang chung trong structured resume profile.
- Evidence level dung de lam gi.
- Vi sao evidence detection khac scoring.

### 10.2 Cac khai niem ky thuat can hieu

- Evidence text: cau/dong trong CV chung minh skill.
- Evidence source: noi tim thay bang chung, vi du skill list, summary, work experience, project.
- Evidence level: muc do manh/yew cua bang chung.
- Action-based evidence: cau co hanh dong nhu built, developed, designed, implemented.
- Keyword stuffing: CV liet ke nhieu keyword nhung thieu bang chung dung skill.

### 10.3 Cac logic nho can nam

Thu tu uu tien evidence:

1. Action-based project/work bullet -> Level 3.
2. Project/work bullet co skill nhung action chua ro -> Level 2.
3. Summary/headline/skill list -> Level 1.
4. Khong tim thay -> Level 0.

Candidate skill va required skill deu co the duoc dung de tim evidence.

Vi du match:

```python
required_skill = "SQL"
candidate_skill = "MySQL"
```

Evidence detector nen tim duoc MySQL trong CV:

```text
Designed MySQL database schemas for product and order modules.
```

### 10.4 Vi du input/output

Input:

```python
skill = "Spring Boot"
resume_profile = {
    "raw_skills": ["Java", "Spring Boot"],
    "work_experience": [
        {
            "description": ["Built REST APIs using Java and Spring Boot."]
        }
    ]
}
```

Output:

```python
{
    "skill": "Spring Boot",
    "evidence_level": 3,
    "evidence_text": "Built REST APIs using Java and Spring Boot.",
    "evidence_source": "work_experience"
}
```

### 10.5 Noi dung co the dua vao bao cao

Evidence Detection giup he thong phan biet giua ky nang chi duoc liet ke va ky nang co bang chung su dung trong du an/kinh nghiem. Buoc nay lam giam rui ro CV nhoi keyword va tao nen tang cho evidence score trong phase scoring.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/07-evidence-detection`.
2. Tao `src/evidence_detector.py`.
3. Implement helper thu thap evidence candidates tu resume profile.
4. Implement skill keyword matching case-insensitive.
5. Implement action-based level 3 detection.
6. Implement `detect_evidence`.
7. Implement `detect_all_evidence`.
8. Them `tests/test_evidence_detector.py`.
9. Co the them CV keyword stuffing demo neu can.
10. Chay `pytest`.
11. Test thu cong voi demo CV/JD.
12. Cap nhat README.
13. Cap nhat `docs/dev-learning-log.md`.
14. Tao `docs/refactoring/phase-07-refactoring-plan.md`.
15. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong voi demo CV/JD:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); matches=match_skills(required, candidate, taxonomy); print(detect_all_evidence(matches, profile))"
```

## 13. Tieu chi hoan thanh phase

Phase 07 hoan thanh khi:

- Co `src/evidence_detector.py`.
- Detect duoc evidence level 0/1/2/3.
- Match result duoc enrich voi `evidence_level`, `evidence_text`, `evidence_source`.
- Demo strong CV co evidence manh cho Java/Spring Boot/REST API/MySQL/Docker.
- Co tests tu dong.
- `pytest` pass.
- Learning log duoc cap nhat.
- Refactoring plan Phase 07 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Rule evidence co the phu thuoc vao tu khoa action verbs.
- Evidence detector co the bo sot cau dung skill nhung viet khac cach.
- Related match nhu SQL -> MySQL can tim candidate skill trong evidence.
- Neu evidence detection lam scoring luon se vuot scope.
- CV format phuc tap hon demo co the can rule bo sung sau.

## 15. Ghi chu cho bao cao

Phase Evidence Detection giup he thong danh gia muc do bang chung cua tung skill matched. Thay vi chi dua vao viec skill xuat hien trong danh sach Skills, he thong tim skill trong work experience va project, dac biet la cac cau co hanh dong cu the. Dieu nay giup giam tinh trang keyword stuffing va tao nen tang cho evidence-based scoring o phase tiep theo.
