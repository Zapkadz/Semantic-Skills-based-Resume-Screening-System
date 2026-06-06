# Refactoring Plan - Phase 05

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 05 da them Rule-based Skill Matching. Code hien tai co test va output on dinh cho exact, related, transferable va no match.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring final vi Phase 05 chua co final scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Matcher co mot so helper rieng cho canonicalization va relationship lookup. Hien tai duplication khong dang ke.

`_canonicalize_skills` co logic gan giong `normalize_skills`, nhung trong matcher no dung de bao ve khi input van con alias. Chua can tach chung vi normalizer va matcher co trach nhiem khac nhau.

### 3.2 Oversized files

`src/semantic_matcher.py` con nho va chi lam matching. Tests duoc tach rieng trong `tests/test_semantic_matcher.py`.

Chua co file qua lon.

### 3.3 Naming

Ten function va constant ro rang:

- `MATCH_SCORES`
- `MATCH_PRIORITY`
- `match_skills`
- `get_missing_skills`
- `_skills_are_connected`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Exact match.
- Alias canonicalization thanh exact match.
- Related match.
- Transferable match.
- No match.
- Exact priority cao hon related.
- Missing skills.
- Duplicate sau canonicalization.
- Non-string input.
- Demo pipeline integration.

Co the them tests cho nice-to-have matching o phase scoring/ranking neu can.

### 3.5 API compatibility

Public API hien tai:

```python
match_skills(job_skills, candidate_skills, taxonomy) -> list[dict]
get_missing_skills(matches) -> list[str]
```

Moi refactor sau nay can giu output match result:

```python
{
    "required_skill": "...",
    "candidate_skill": "...",
    "match_type": "...",
    "score": 0.0
}
```

## 4. De xuat refactor

### De xuat 1 - Chua tao dataclass cho match result

- File lien quan: `src/semantic_matcher.py`
- Van de: match result dang la dict.
- Cach refactor: co the tao dataclass hoac TypedDict khi scorer va review card bat dau phu thuoc nhieu vao schema.
- Rui ro: them schema som co the lam code dai hon khi output dict dang de dung cho JSON.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua refactor trong Phase 05.

### De xuat 2 - Chua tach canonicalization helper dung chung

- File lien quan: `src/skill_normalizer.py`, `src/semantic_matcher.py`
- Van de: matcher co canonicalization nhe gan giong normalizer.
- Cach refactor: co the tach helper chung neu nhieu module cung can.
- Rui ro: tach som lam nguoi hoc phai nhay qua nhieu file.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: de sau khi scorer/evidence module xuat hien.

### De xuat 3 - Khong them embedding vao matcher luc nay

- File lien quan: `src/semantic_matcher.py`
- Van de: ten module la semantic matcher, nhung Phase 05 moi la rule-based.
- Cach refactor: embedding semantic similarity se la phase rieng.
- Rui ro: them model som lam MVP nang, kho cai dat, kho test va vuot scope.
- Cach test sau refactor: can tests rieng cho embedding fallback.
- Co thay doi behavior khong? Co.

Ket luan: khong lam trong Phase 05.

## 5. Pham vi refactor

Phase 05 khong thuc hien refactor code them.

Khong refactor:

- Khong tao dataclass/TypedDict.
- Khong tach common canonicalization.
- Khong them embedding.
- Khong them final scoring.
- Khong wire vao CLI/UI.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

Ket qua mong doi:

- Tat ca tests pass.
- Demo JD/CV van co exact matches cho Java, Spring Boot, REST API, Docker.
- Demo JD/CV van co related match cho SQL voi MySQL.

## 7. Ghi chu cho bao cao

Sau Phase 05, du an co buoc review refactor de dam bao matcher van giu trach nhiem ro rang: tao match result cho tung required skill. Hien tai chua refactor them vi code nho, co test va de giai thich. Viec tri hoan embedding/scoring giup MVP giu baseline rule-based minh bach truoc khi mo rong.
