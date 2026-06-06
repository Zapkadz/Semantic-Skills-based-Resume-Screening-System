# Phase 05 - Rule-based Skill Matching

## 1. Muc tieu phase

Phase 05 tao module so khop ky nang rule-based dau tien cho he thong. Sau Phase 04, CV va JD da co skill duoc chuan hoa theo taxonomy. Phase nay se so sanh danh sach skill cua JD voi danh sach skill cua ung vien va tao match result co cau truc.

Muc tieu:

- Tao `src/semantic_matcher.py` cho MVP rule-based matching.
- Match must-have skills va nice-to-have skills o muc skill list.
- Ho tro cac match type dau tien:
  - `exact_match`
  - `related_match`
  - `transferable_match`
  - `no_match`
- Tra ve score rieng cho tung skill match theo dinh huong tai lieu goc.
- Them tests cho matcher.

Phase nay chua lam evidence detection va chua tinh final score.

## 2. Van de phase nay giai quyet

Sau Phase 04, he thong biet skill chuan cua CV va JD, vi du:

```python
JD: ["Java", "Spring Boot", "REST API", "SQL", "Docker"]
CV: ["Java", "Spring Boot", "REST API", "MySQL", "Docker"]
```

Nhung he thong van chua biet skill nao khop, skill nao thieu, va skill nao lien quan. Phase 05 giai quyet viec tao ket qua so khop:

```text
SQL in JD
  -> MySQL in CV
  -> related_match
```

## 3. Vi sao phase nay quan trong voi do an

Day la buoc dau tien bien skills-based hiring thanh logic so khop thuc te. He thong khong chi kiem tra text giong nhau, ma bat dau dung taxonomy de nhan dien skill lien quan va transferable.

Trong bao cao, phase nay co the duoc mo ta la rule-based semantic skill matching baseline. No tao nen tang de sau nay them embedding semantic matching.

## 4. Pham vi thuc hien

Trong Phase 05 se lam:

- Tao `src/semantic_matcher.py`.
- Implement `match_skills(job_skills, candidate_skills, taxonomy) -> list[dict]`.
- Implement helper tim exact match.
- Implement helper tim related match dua tren `related` trong taxonomy.
- Implement helper tim transferable match dua tren `transferable` trong taxonomy.
- Implement `get_missing_skills(matches)`.
- Them tests cho:
  - exact match
  - related match
  - transferable match
  - no match
  - parser + normalizer + matcher integration
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong evidence detection.
- Khong final scoring/ranking.
- Khong recommendation label.
- Khong review card.
- Khong Streamlit UI.
- Khong embedding model.
- Khong cosine similarity.
- Khong tu dong reject/pass ung vien.
- Khong thay doi scoring weights.
- Khong sua parser/normalizer neu khong co loi lien quan truc tiep.

## 6. Module lien quan

Module chinh:

- `src/semantic_matcher.py`

Module dung lam input:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`

Tests:

- `tests/test_semantic_matcher.py`

## 7. File du kien tao moi

- `src/semantic_matcher.py`
- `tests/test_semantic_matcher.py`
- `docs/phases/phase-05-rule-based-matching.md`
- `docs/refactoring/phase-05-refactoring-plan.md` sau khi code xong

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `data/taxonomy/skills.json`, tru khi test cho thay thieu related/transferable can thiet cho demo.
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_normalizer.py`
- `app.py`

## 9. Flow xu ly sau phase nay

Sau Phase 05, flow co the la:

```text
CV text
  -> load_text_file()
  -> parse_resume()
  -> normalize_skills(profile["raw_skills"])
  -> candidate_skills

JD text
  -> load_text_file()
  -> parse_jd()
  -> normalize_skills(criteria["must_have_skills"])
  -> job_skills

job_skills + candidate_skills + taxonomy
  -> match_skills()
  -> match results
```

Vi du output:

```python
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
    }
]
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc matching rule-based la gi va vi sao matching khac scoring.

Can nam:

- Job skill la skill JD yeu cau.
- Candidate skill la skill ung vien co.
- Exact match la gi.
- Related match la gi.
- Transferable match la gi.
- No match la gi.
- Match score o phase nay chi la diem tung skill, chua phai final score.

### 10.2 Cac khai niem ky thuat can hieu

- Match result: dict mo ta mot required skill khop voi candidate skill nao.
- Match type: loai khop nhu exact, related, transferable, no match.
- Related skills: ky nang lien quan truc tiep trong taxonomy.
- Transferable skills: ky nang co the chuyen doi ve mat nang luc.
- Missing skills: JD skill khong co match phu hop.
- Deterministic matching: cung input thi ket qua nhu nhau, de test va giai thich.

### 10.3 Cac logic nho can nam

Thu tu uu tien match:

1. Exact match.
2. Related match.
3. Transferable match.
4. No match.

Score de xuat:

```text
exact_match        = 1.00
related_match      = 0.75
transferable_match = 0.55
no_match           = 0.00
```

Alias match da duoc xu ly o Phase 04 bang normalization. Vi vay Phase 05 lam viec tren canonical skill.

### 10.4 Vi du input/output

Input:

```python
job_skills = ["Java", "Spring Boot", "REST API", "SQL"]
candidate_skills = ["Java", "Spring Boot", "REST API", "MySQL"]
```

Output:

```python
[
    {"required_skill": "Java", "candidate_skill": "Java", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "Spring Boot", "candidate_skill": "Spring Boot", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "REST API", "candidate_skill": "REST API", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "SQL", "candidate_skill": "MySQL", "match_type": "related_match", "score": 0.75}
]
```

### 10.5 Noi dung co the dua vao bao cao

Rule-based Skill Matching la buoc so khop ky nang giua JD va CV dua tren taxonomy. He thong uu tien exact match, sau do xet cac ky nang related va transferable. Cach tiep can nay giup he thong bot phu thuoc vao keyword trung khop tuyet doi va tao baseline de mo rong sang semantic embedding o phase sau.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/05-rule-based-matching`.
2. Tao `src/semantic_matcher.py`.
3. Dinh nghia match score constants.
4. Implement `match_skills`.
5. Implement exact match.
6. Implement related match.
7. Implement transferable match.
8. Implement no match fallback.
9. Implement helper missing skills neu can.
10. Them `tests/test_semantic_matcher.py`.
11. Chay `pytest`.
12. Test thu cong voi demo JD/CV.
13. Cap nhat README.
14. Cap nhat `docs/dev-learning-log.md`.
15. Tao `docs/refactoring/phase-05-refactoring-plan.md`.
16. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong voi demo JD/CV:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

## 13. Tieu chi hoan thanh phase

Phase 05 hoan thanh khi:

- Co `src/semantic_matcher.py`.
- Match duoc exact, related, transferable va no match.
- Output match result co key on dinh.
- Co tests tu dong.
- `pytest` pass.
- Demo JD/CV tao match result hop ly.
- Learning log duoc cap nhat.
- Refactoring plan Phase 05 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Related/transferable trong taxonomy con nho nen ket qua match co the chua phong phu.
- Neu match qua rong, co the lam ung vien duoc danh gia cao hon thuc te.
- Neu match qua hep, co the bo sot transferable candidate.
- Neu them scoring final trong phase nay se vuot scope.
- Neu dung embedding ngay se lam MVP nang va kho test.

## 15. Ghi chu cho bao cao

Phase Rule-based Skill Matching tao baseline de so khop ky nang JD va CV bang taxonomy. He thong uu tien exact match, sau do xet related va transferable skills. Ket qua cua phase nay la danh sach match co giai thich loai match va diem tung skill, nhung chua phai final ranking. Dieu nay giup recruiter va nguoi phat trien hieu ro vi sao mot ky nang duoc xem la phu hop truoc khi dua vao evidence detection va scoring.
