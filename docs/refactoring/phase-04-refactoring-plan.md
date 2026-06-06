# Refactoring Plan - Phase 04

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 04 da them Skill Taxonomy va Skill Normalization. Code hien tai co test, output on dinh va chua can refactor lon.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring vi Phase 04 chua co scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Code taxonomy va normalizer dang tach trach nhiem ro:

- `skill_taxonomy.py` doc JSON, validate va build alias map.
- `skill_normalizer.py` normalize skill dua tren alias map.

Chua co duplication dang ke.

### 3.2 Oversized files

`skills.json` co nhieu entry hon cac file code, nhung day la du lieu taxonomy nen chap nhan duoc.

`skill_taxonomy.py` va `skill_normalizer.py` con nho, chua qua lon.

### 3.3 Naming

Ten function ro rang:

- `load_taxonomy`
- `build_alias_map`
- `make_lookup_key`
- `normalize_skill`
- `normalize_skills`

Ten constant ro rang:

- `REQUIRED_SKILL_FIELDS`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Load taxonomy JSON.
- Build alias map.
- Missing taxonomy file.
- Unsupported taxonomy extension.
- Invalid JSON.
- Missing required field.
- Ambiguous alias.
- Normalize alias.
- Normalize case-insensitive.
- Unknown skill duoc giu nguyen.
- Duplicate sau normalization.
- Parser output integration.

Co the them test taxonomy lon hon sau khi Phase 05 can related/transferable matching.

### 3.5 API compatibility

Public API hien tai:

```python
load_taxonomy(path) -> dict
build_alias_map(taxonomy) -> dict
normalize_skill(skill, taxonomy) -> str
normalize_skills(skills, taxonomy) -> list[str]
```

Moi refactor sau nay can giu API nay de cac phase tiep theo dung on dinh.

## 4. De xuat refactor

### De xuat 1 - Chua cache alias map ngay

- File lien quan: `src/skill_normalizer.py`
- Van de: `normalize_skill` va `normalize_skills` build alias map tu taxonomy.
- Cach refactor: co the cache alias map neu taxonomy lon hoac goi lien tuc nhieu lan.
- Rui ro: cache som co the lam kho hieu khi taxonomy thay doi trong test.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua refactor trong Phase 04. Performance hien tai du cho MVP.

### De xuat 2 - Can nhac schema type cho taxonomy trong phase sau

- File lien quan: `src/skill_taxonomy.py`
- Van de: taxonomy metadata hien dang la dict/list linh hoat.
- Cach refactor: tao TypedDict cho skill metadata khi code phu thuoc nhieu hon vao `related` va `transferable`.
- Rui ro: them type schema som lam code dai hon khi Phase 04 moi chi can load/normalize.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: de sang phase matching neu can.

### De xuat 3 - Khong them matching logic vao normalizer

- File lien quan: `src/skill_normalizer.py`
- Van de: co the muon dung `related` va `transferable` ngay.
- Cach refactor: khong lam trong Phase 04, de Phase 05 xu ly matching.
- Rui ro: neu them vao Phase 04 se lam module sai trach nhiem va vuot scope.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Co the co neu output thay doi.

Ket luan: khong lam.

## 5. Pham vi refactor

Phase 04 khong thuc hien refactor code them.

Khong refactor:

- Khong cache alias map.
- Khong tao TypedDict cho taxonomy.
- Khong doi output format.
- Khong them matching.
- Khong them scoring.
- Khong wire vao CLI/UI.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); print(normalize_skills(['JS', 'SpringBoot', 'Postgres'], taxonomy))"
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); print(normalize_skills(profile['raw_skills'], taxonomy))"
```

Ket qua mong doi:

- Tat ca tests pass.
- Alias list duoc chuan hoa thanh `['JavaScript', 'Spring Boot', 'PostgreSQL']`.
- CV demo skills duoc chuan hoa va giu dung thu tu.

## 7. Ghi chu cho bao cao

Sau Phase 04, du an co buoc review refactor de dam bao taxonomy va normalizer van tach trach nhiem ro rang. Hien tai chua refactor them vi code dang nho, co test va de giai thich. Quyet dinh nay giup MVP tranh over-engineering trong khi van giu nen tang de mo rong sang related/transferable matching o Phase 05.
