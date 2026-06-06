# Phase 09 - Explainable Review Card

## 1. Muc tieu phase

Phase 09 tao module Explainable Review Card de bien ket qua scoring thanh thong tin de doc cho recruiter.

Sau Phase 08, he thong da co:

- `final_score`
- `recommendation`
- score components
- matched skills
- missing skills
- nice-to-have matches
- evidence text
- seniority
- experience years
- domain

Muc tieu Phase 09 la tao review card co cau truc, giai thich vi sao ung vien duoc khuyen nghi review hoac can can nhac them.

## 2. Van de phase nay giai quyet

Scoring result hien tai la dict ky thuat. Recruiter co the can mot ban tom tat nhu:

```text
Candidate: Nguyen Van A
Score: 87/100 - Strong Review

Strengths:
- Strong must-have skill coverage.
- Clear work evidence for Java, Spring Boot, REST API, SQL/MySQL, and Docker.

Concerns:
- Missing AWS.
- Missing Kafka.

Suggested Interview Questions:
1. Explain the REST API modules you built with Spring Boot.
2. How did you design the MySQL schema?
```

Phase 09 giai quyet viec chuyen output scoring thanh review card co:

- Summary.
- Score breakdown.
- Skill evidence highlights.
- Missing skill concerns.
- Nice-to-have notes.
- Suggested interview questions.

## 3. Vi sao phase nay quan trong voi do an

Du an khong chi cham diem CV. Muc tieu la explainable screening: recruiter can hieu vi sao he thong xep hang ung vien.

Review card giup:

- Giai thich final score.
- Giam tinh trang diem so bi xem nhu "black box".
- Cho thay evidence trong CV.
- Ho tro phong van bang cau hoi dua tren skill/evidence/missing skill.
- Chung minh he thong chi ho tro recruiter, khong auto reject/pass ung vien.

## 4. Pham vi thuc hien

Trong Phase 09 se lam:

- Tao `src/review_card_generator.py`.
- Implement `generate_review_card(candidate_result, job_criteria=None) -> dict`.
- Implement `format_review_card_markdown(review_card) -> str`.
- Tao rule-based strengths tu score components va matched skills.
- Tao rule-based concerns tu missing skills, low evidence, low component score, missing nice-to-have.
- Tao evidence highlights tu matched skills co evidence text.
- Tao suggested interview questions dua tren evidence va missing/nice-to-have skills.
- Them tests cho review card.
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong thay doi cong thuc scoring Phase 08.
- Khong thay doi matcher/evidence detector.
- Khong tao Streamlit UI.
- Khong implement full CLI pipeline.
- Khong save report ra file output.
- Khong dung LLM de viet explanation.
- Khong generate email, PDF, DOCX, hoac HTML report.
- Khong tao interview plan phuc tap.
- Khong auto reject/pass ung vien.

## 6. Module lien quan

Module chinh:

- `src/review_card_generator.py`

Module input tu phase truoc:

- `src/scorer.py`
- `src/evidence_detector.py`
- `src/semantic_matcher.py`
- `src/jd_parser.py`
- `src/resume_parser.py`

Tests:

- `tests/test_review_card_generator.py`

## 7. File du kien tao moi

- `src/review_card_generator.py`
- `tests/test_review_card_generator.py`
- `docs/phases/phase-09-explainable-review-card.md`
- `docs/refactoring/phase-09-refactoring-plan.md` sau khi code xong

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/scorer.py`
- `src/evidence_detector.py`
- `src/semantic_matcher.py`
- Parser modules.
- Taxonomy JSON.
- `app.py`.
- `main.py`.

## 9. Output review card de xuat

`generate_review_card` nen tra ve dict co cau truc:

```python
{
    "candidate_name": "Nguyen Van A",
    "final_score": 87,
    "recommendation": "Strong Review",
    "summary": "Strong fit for Backend Java Developer...",
    "score_breakdown": {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.5,
        "seniority": 1.0,
        "domain": 1.0,
        "nice_to_have": 0.3333
    },
    "matched_skills": [...],
    "missing_skills": [],
    "nice_to_have_matches": [...],
    "evidence_highlights": [...],
    "strengths": [...],
    "concerns": [...],
    "suggested_interview_questions": [...]
}
```

Markdown output nen la display format tu dict:

```text
# Nguyen Van A

Score: 87/100
Recommendation: Strong Review

## Score Breakdown
- Skill semantic: 0.95
- Evidence: 1.00

## Strengths
- Strong must-have skill coverage.

## Concerns
- Missing AWS.

## Evidence Highlights
- Java: Built REST APIs using Java and Spring Boot.

## Suggested Interview Questions
1. Explain how you used Java in: Built REST APIs using Java and Spring Boot.
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc:

- Explanation khac scoring nhu the nao.
- Vi sao review card nen dung scoring result thay vi tinh lai score.
- Cach viet rule-based explanation de minh bach.
- Cach tach structured output va display output.
- Cach sinh interview questions tu evidence/missing skills ma khong dung LLM.

### 10.2 Cac khai niem ky thuat can hieu

- Explainable output: dau ra co ly do ro rang.
- Evidence highlight: doan CV dung lam bang chung.
- Strength: diem manh dua tren score/match/evidence.
- Concern: diem can xem them dua tren missing skill hoac score component thap.
- Interview question: cau hoi goi y dua tren bang chung hoac skill thieu.
- Structured review card: dict/JSON de UI va CLI dung lai.
- Markdown formatting: cach hien thi review card de doc bang text.

### 10.3 Nguyen tac explanation

Review card phai:

- Dua tren du lieu da co, khong tu suy dien qua muc.
- Giu recommendation la goi y review, khong phai pass/fail.
- Hien missing skills ro rang.
- Hien evidence text khi co.
- Neu evidence yeu, phai noi ro day la concern.
- Neu nice-to-have missing, chi xem la concern nhe.

## 11. Rule logic du kien

### 11.1 Summary

Summary dua tren `final_score`, `recommendation`, `candidate_name`, va job title neu co.

Vi du:

```text
Nguyen Van A is a Strong Review candidate for Backend Java Developer with strong skill match and evidence coverage.
```

### 11.2 Strengths

Rule de tao strengths:

- `scores.skill_semantic >= 0.85`: strong must-have skill coverage.
- `scores.evidence >= 0.85`: strong evidence in work/project descriptions.
- `scores.domain >= 0.85`: good domain alignment.
- `scores.seniority >= 0.85`: seniority looks aligned.
- Match co `evidence_level >= 3`: add skill evidence strength.

### 11.3 Concerns

Rule de tao concerns:

- Co missing must-have skills.
- `scores.evidence < 0.5`: weak evidence.
- `scores.experience < 0.5`: experience may be below requirement.
- `scores.domain < 0.5`: domain alignment may be weak.
- Nice-to-have no match: mention as optional gap.

### 11.4 Evidence highlights

Evidence highlight lay tu `matched_skills` co:

- `candidate_skill` hoac `required_skill`
- `evidence_level >= 2`
- `evidence_text` khong rong

Neu qua nhieu highlights, co the gioi han 5 highlight dau tien trong MVP.

### 11.5 Suggested interview questions

Question templates:

```text
Explain how you used {skill} in: {evidence_text}
Can you walk through the implementation details behind {skill}?
How would you handle {missing_skill} in this role?
Do you have production experience with {nice_to_have_skill}?
```

MVP nen gioi han 3-5 cau hoi de review card gon.

## 12. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/09-explainable-review-card`.
2. Tao `src/review_card_generator.py`.
3. Dinh nghia public API `generate_review_card`.
4. Dinh nghia public API `format_review_card_markdown`.
5. Implement summary generation.
6. Implement score breakdown formatting.
7. Implement evidence highlights.
8. Implement strengths generation.
9. Implement concerns generation.
10. Implement interview question generation.
11. Them `tests/test_review_card_generator.py`.
12. Test voi candidate result fixture.
13. Test end-to-end demo JD/CV tu Phase 08 scoring result.
14. Chay `pytest`.
15. Chay manual review card command.
16. Cap nhat README.
17. Cap nhat `docs/dev-learning-log.md`.
18. Tao `docs/refactoring/phase-09-refactoring-plan.md`.
19. Dung lai cho ban test va xac nhan.

## 13. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong voi demo JD/CV:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; from src.review_card_generator import generate_review_card, format_review_card_markdown; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); nice_skills=normalize_skills(criteria['nice_to_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(nice_skills, candidate, taxonomy); result=score_candidate(criteria, profile, matches, nice); card=generate_review_card(result, criteria); print(format_review_card_markdown(card))"
```

## 14. Tieu chi hoan thanh phase

Phase 09 hoan thanh khi:

- Co `src/review_card_generator.py`.
- `generate_review_card` tra ve dict co cau truc on dinh.
- `format_review_card_markdown` tao review card dang text de doc.
- Review card co summary, score breakdown, strengths, concerns, evidence highlights, interview questions.
- Demo strong CV co review card hop ly.
- Co tests tu dong.
- `pytest` pass.
- README duoc cap nhat.
- Learning log duoc cap nhat.
- Refactoring plan Phase 09 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 15. Rui ro

- Explanation co the qua dai neu hien tat ca evidence.
- Concern co the nghe nhu auto reject neu viet qua manh.
- Interview question co the lap lai neu nhieu skill chung evidence text.
- Neu review card tinh lai score, co the lech voi scorer.
- Neu format Markdown tron voi logic generation, sau nay UI kho dung lai.

## 16. Ghi chu cho bao cao

Explainable Review Card la buoc bien ket qua scoring thanh dau ra co kha nang giai thich. Thay vi chi hien diem tong, he thong hien cac ly do chinh nhu skill match, bang chung kinh nghiem, skill thieu, nice-to-have gap va cau hoi phong van goi y. Cach tiep can nay giup he thong minh bach va phu hop voi vai tro ho tro recruiter.
