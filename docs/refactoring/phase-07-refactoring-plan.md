# Refactoring Plan - Phase 07

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 07 da them Evidence Detection. Code hien tai co test va phan biet duoc evidence level 0/1/2/3.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring final vi Phase 07 chua co final scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Khong co duplication dang ke. Evidence detector co cac helper rieng:

- `_collect_evidence_candidates`
- `_find_best_evidence`
- `_contains_skill`
- `_calculate_evidence_level`

Moi helper co trach nhiem nho va de test gian tiep.

### 3.2 Oversized files

`src/evidence_detector.py` con vua phai. File test `tests/test_evidence_detector.py` co nhieu case nhung moi case ro rang.

Chua can tach file.

### 3.3 Naming

Ten function va field ro rang:

- `detect_evidence`
- `detect_all_evidence`
- `evidence_level`
- `evidence_text`
- `evidence_source`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Level 3 work experience action bullet.
- Level 3 project action bullet.
- Level 2 project/work context khong co action verb.
- Level 1 skill list.
- Level 1 summary.
- Level 0 missing skill.
- Related match SQL -> MySQL dung candidate skill de tim evidence.
- Demo pipeline integration.

Co the them keyword-stuffing CV demo trong phase scoring neu can demo ranking ro hon.

### 3.5 API compatibility

Public API hien tai:

```python
detect_evidence(skill, resume_profile) -> dict
detect_all_evidence(matches, resume_profile) -> list[dict]
```

Moi refactor sau nay can giu output fields:

```python
evidence_level
evidence_text
evidence_source
```

## 4. De xuat refactor

### De xuat 1 - Chua tach action verbs sang config rieng

- File lien quan: `src/evidence_detector.py`
- Van de: `ACTION_VERBS` dang hard-code trong module.
- Cach refactor: co the chuyen sang config JSON hoac constants rieng khi danh sach lon hon.
- Rui ro: tach som lam tang so file trong khi MVP con nho.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua refactor trong Phase 07.

### De xuat 2 - Chua them fuzzy/embedding evidence search

- File lien quan: `src/evidence_detector.py`
- Van de: evidence search hien la rule-based phrase search.
- Cach refactor: co the them semantic evidence search o phase sau neu can.
- Rui ro: them som lam evidence kho giai thich va cham hon.
- Cach test sau refactor: can tests semantic/fallback rieng.
- Co thay doi behavior khong? Co the co.

Ket luan: khong lam trong Phase 07.

### De xuat 3 - Khong tinh evidence score trung binh trong detector

- File lien quan: `src/evidence_detector.py`
- Van de: co the muon tinh average evidence score ngay.
- Cach refactor: khong lam; scoring thuoc Phase 08.
- Rui ro: tron trach nhiem detector voi scorer.
- Cach test sau refactor: chay tests scoring trong Phase 08.
- Co thay doi behavior khong? Co.

Ket luan: de Phase 08.

## 5. Pham vi refactor

Phase 07 khong thuc hien refactor code them.

Khong refactor:

- Khong tach action verbs.
- Khong them fuzzy/semantic evidence search.
- Khong tinh final/evidence score aggregate.
- Khong wire vao CLI/UI.
- Khong them review card.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); matches=match_skills(required, candidate, taxonomy); print(detect_all_evidence(matches, profile))"
```

Ket qua mong doi:

- Tat ca tests pass.
- Strong CV co evidence level 3 cho must-have matches.
- SQL -> MySQL van tim dung evidence MySQL.

## 7. Ghi chu cho bao cao

Sau Phase 07, du an co buoc review refactor de dam bao Evidence Detector chi lam dung mot viec: tim va gan muc do bang chung cho tung matched skill. Hien tai chua refactor them vi code con nho, co test va de giai thich. Scoring/ranking se duoc tach sang Phase 08 de giu module ro trach nhiem.
