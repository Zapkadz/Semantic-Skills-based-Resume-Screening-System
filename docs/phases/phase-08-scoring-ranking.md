# Phase 08 - Scoring and Ranking

## 1. Muc tieu phase

Phase 08 tao module Scoring and Ranking de tinh diem ung vien dua tren cac tin hieu da co tu cac phase truoc:

- Skill matching.
- Evidence detection.
- Experience fit.
- Seniority fit.
- Domain fit.
- Nice-to-have skills.

Muc tieu la tao candidate result co `final_score`, score components va recommendation label. Phase nay van chua tao review card chi tiet.

## 2. Van de phase nay giai quyet

Sau Phase 07, he thong da biet:

```text
Skill nao match?
Match type la gi?
Match score bao nhieu?
Skill do co evidence level may?
Evidence text la gi?
```

Nhung he thong van chua co diem tong hop va ranking ung vien. Phase 08 giai quyet bai toan:

```text
job criteria + resume profile + enriched matches
  -> score_candidate()
  -> final score + recommendation
```

Va khi co nhieu CV:

```text
candidate results
  -> rank_candidates()
  -> ordered ranking list
```

## 3. Vi sao phase nay quan trong voi do an

Scoring and Ranking bien cac tin hieu rieng le thanh ket qua recruiter co the xem nhanh. Diem quan trong la scoring phai rule-based va explainable, khong de AI/LLM tu cham diem tuy y.

Trong bao cao, phase nay the hien ro cach he thong ket hop semantic skill match voi evidence-based screening.

## 4. Pham vi thuc hien

Trong Phase 08 se lam:

- Tao `src/scorer.py`.
- Co the tao `src/experience_analyzer.py`, `src/seniority_detector.py`, `src/domain_analyzer.py` neu can tach logic nho.
- Implement `score_candidate(job_criteria, resume_profile, matches, nice_to_have_matches=None) -> dict`.
- Implement `rank_candidates(candidate_results) -> list[dict]`.
- Tinh score components:
  - skill_semantic
  - evidence
  - experience
  - seniority
  - domain
  - nice_to_have
- Tinh final score theo weight trong tai lieu goc.
- Tao recommendation label:
  - `Strong Review`
  - `Review`
  - `Maybe Review`
  - `Low Priority`
  - `Not Enough Evidence`
- Them tests cho scoring.
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong tao review card chi tiet.
- Khong generate interview questions.
- Khong Streamlit UI.
- Khong PDF/DOCX support.
- Khong dung LLM de cham diem.
- Khong auto reject/pass ung vien.
- Khong thay doi match/evidence logic neu khong co bug.
- Khong fine-tune hay train model.

## 6. Module lien quan

Module chinh:

- `src/scorer.py`

Module co the tao neu can:

- `src/experience_analyzer.py`
- `src/seniority_detector.py`
- `src/domain_analyzer.py`

Module input tu phase truoc:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `src/semantic_matcher.py`
- `src/evidence_detector.py`

Tests:

- `tests/test_scorer.py`
- Co the them tests cho analyzer neu tach file.

## 7. File du kien tao moi

- `src/scorer.py`
- `tests/test_scorer.py`
- `docs/phases/phase-08-scoring-ranking.md`
- `docs/refactoring/phase-08-refactoring-plan.md` sau khi code xong

Co the tao them neu can:

- `src/experience_analyzer.py`
- `src/seniority_detector.py`
- `src/domain_analyzer.py`
- `tests/test_experience_analyzer.py`
- `tests/test_seniority_detector.py`
- `tests/test_domain_analyzer.py`

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/semantic_matcher.py`
- `src/evidence_detector.py`
- Parser modules.
- Taxonomy JSON, tru khi scoring tests can demo data ro hon.
- `app.py`.

## 9. Flow xu ly sau phase nay

Flow sau Phase 08:

```text
JD text + CV text
  -> document loader
  -> parser
  -> skill normalization
  -> skill matching
  -> evidence detection
  -> scoring
  -> ranking result
```

Vi du output:

```python
{
    "candidate_name": "Nguyen Van A",
    "final_score": 86,
    "recommendation": "Strong Review",
    "scores": {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.75,
        "seniority": 0.85,
        "domain": 1.0,
        "nice_to_have": 0.33
    },
    "matched_skills": [...],
    "missing_skills": [],
    "seniority": "Junior"
}
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc:

- Scoring khac matching nhu the nao.
- Score component la gi.
- Weight la gi.
- Evidence level map sang score nhu the nao.
- Recommendation label nen la label ho tro recruiter, khong phai pass/fail.
- Ranking la sap xep ung vien theo final score, khong phai tu dong quyet dinh tuyen dung.

### 10.2 Cac khai niem ky thuat can hieu

- Skill semantic score: trung binh match score cua must-have skills.
- Evidence score: trung binh evidence score cua matched must-have skills.
- Experience score: muc phu hop nam kinh nghiem.
- Seniority score: muc phu hop level ung vien voi JD.
- Domain score: muc overlap domain.
- Nice-to-have score: ty le nice-to-have matched.
- Weighted final score: tong co trong so cua cac score components.

### 10.3 Cac logic nho can nam

Cong thuc dinh huong:

```text
Final Score =
  40% Semantic Skill Match
+ 20% Evidence Strength
+ 15% Experience Fit
+ 10% Seniority Fit
+ 10% Domain Fit
+ 5% Nice-to-have Bonus
```

Evidence level map:

```text
Level 0 -> 0.0
Level 1 -> 0.4
Level 2 -> 0.7
Level 3 -> 1.0
```

Recommendation label de xuat:

```text
>= 85: Strong Review
70-84: Review
55-69: Maybe Review
40-54: Low Priority
< 40: Not Enough Evidence
```

### 10.4 Vi du input/output

Input:

```python
matches = [
    {"required_skill": "Java", "score": 1.0, "evidence_level": 3},
    {"required_skill": "SQL", "score": 0.75, "evidence_level": 3}
]
```

Output component:

```python
skill_semantic = (1.0 + 0.75) / 2
evidence = (1.0 + 1.0) / 2
```

### 10.5 Noi dung co the dua vao bao cao

Scoring and Ranking ket hop cac tin hieu da trich xuat tu CV/JD thanh diem tong hop co giai thich. He thong dung cong thuc rule-based co trong so ro rang, giup ket qua minh bach va co the kiem thu. Recommendation label chi ho tro recruiter uu tien review, khong thay the quyet dinh tuyen dung.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/08-scoring-ranking`.
2. Tao `src/scorer.py`.
3. Dinh nghia score weights va thresholds.
4. Implement evidence level to score mapping.
5. Implement skill semantic score.
6. Implement evidence score.
7. Implement experience score baseline.
8. Implement seniority score baseline.
9. Implement domain score baseline.
10. Implement nice-to-have score.
11. Implement final score va recommendation.
12. Implement ranking helper.
13. Them `tests/test_scorer.py`.
14. Chay `pytest`.
15. Test thu cong voi demo JD/CV.
16. Cap nhat README.
17. Cap nhat `docs/dev-learning-log.md`.
18. Tao `docs/refactoring/phase-08-refactoring-plan.md`.
19. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong voi demo JD/CV:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(normalize_skills(criteria['nice_to_have_skills'], taxonomy), candidate, taxonomy); print(score_candidate(criteria, profile, matches, nice))"
```

## 13. Tieu chi hoan thanh phase

Phase 08 hoan thanh khi:

- Co `src/scorer.py`.
- Tinh duoc score components.
- Tinh duoc final score 0-100.
- Tao duoc recommendation label khong tuyet doi.
- Rank duoc nhieu candidate result.
- Co tests tu dong.
- `pytest` pass.
- Demo strong CV co score/recommendation hop ly.
- Learning log duoc cap nhat.
- Refactoring plan Phase 08 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Weight scoring co the lam ranking demo khong nhu ky vong neu chua can chinh.
- Experience/seniority/domain detection baseline co the don gian.
- Neu scoring gan nhan pass/fail se sai tinh chat ho tro recruiter.
- Neu scorer tu thay doi match/evidence logic se vuot scope.
- Neu thieu tests cho threshold label, output co the lech.

## 15. Ghi chu cho bao cao

Phase Scoring and Ranking tao buoc tong hop cac tin hieu cua he thong thanh diem ung vien. Diem duoc tinh bang cong thuc rule-based co trong so, ket hop skill match, evidence, experience, seniority, domain va nice-to-have. Ket qua chi la recommendation de recruiter uu tien review, khong phai quyet dinh tuyen dung tu dong.
