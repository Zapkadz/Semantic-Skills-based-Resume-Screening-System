# Refactoring Plan - Phase 03

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 03 da them Resume Parser va JD Parser. Hai parser dang chay dung theo test va tao output co cau truc cho demo data.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring vi Phase 03 chua co scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

`src/resume_parser.py` va `src/jd_parser.py` co mot so helper giong nhau:

- `_split_sections`
- `_parse_section_heading`
- `_parse_simple_list`
- `_strip_bullet`

Duplication nay hien tai con nho va giup moi parser doc lap, de hoc va de giai thich.

### 3.2 Oversized files

Khong co file qua lon.

- `src/resume_parser.py` chua logic resume-specific.
- `src/jd_parser.py` chua logic JD-specific.
- Tests duoc tach thanh `tests/test_resume_parser.py` va `tests/test_jd_parser.py`.

### 3.3 Naming

Ten function va key output ro rang:

- `parse_resume`
- `parse_jd`
- `candidate_name`
- `raw_skills`
- `work_experience`
- `must_have_skills`
- `nice_to_have_skills`
- `minimum_experience_years`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Resume demo data.
- Work experience parsing.
- Project parsing.
- Minimal resume khong co section.
- Inline summary heading.
- JD demo data.
- Responsibilities parsing.
- Missing JD sections.
- Seniority from title.
- Inline requirements heading.

Co the them test cho nhieu CV/JD format hon trong phase sau khi co them demo data.

### 3.5 API compatibility

Public API hien tai:

```python
parse_resume(text: str) -> dict
parse_jd(text: str) -> dict
```

Moi refactor sau nay can giu nguyen API nay de cac phase sau goi duoc parser ma khong doi code.

## 4. De xuat refactor

### De xuat 1 - Chua tach common parser utils ngay

- File lien quan: `src/resume_parser.py`, `src/jd_parser.py`
- Van de: co helper section/bullet bi lap nhe.
- Cach refactor: co the tach sang `src/parser_utils.py`.
- Rui ro: tach qua som lam nguoi hoc phai doc them file khi logic con don gian.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua refactor trong Phase 03. Nen giu parser doc lap de de hoc va de bao ve.

### De xuat 2 - Can nhac dataclass/TypedDict cho output trong phase sau

- File lien quan: parser modules va cac module sau.
- Van de: output hien tai la dict, linh hoat nhung chua co schema type chat.
- Cach refactor: khi scorer/matcher bat dau phu thuoc vao output, co the tao TypedDict cho CandidateProfile va JobCriteria.
- Rui ro: them type schema som co the lam phase hien tai dai hon can thiet.
- Cach test sau refactor: chay `pytest` va test manual parser.
- Co thay doi behavior khong? Khong.

Ket luan: de sau khi parser output on dinh hon.

### De xuat 3 - Khong wire parser vao CLI trong Phase 03

- File lien quan: `main.py`
- Van de: CLI hien van placeholder.
- Cach refactor: co the them command parser demo vao CLI.
- Rui ro: Phase 03 dang tap trung parser module, wire CLI co the lam scope lon hon.
- Cach test sau refactor: chay `python main.py`.
- Co thay doi behavior khong? Co the co neu CLI output doi.

Ket luan: khong lam trong Phase 03.

## 5. Pham vi refactor

Phase 03 khong thuc hien refactor code them.

Khong refactor:

- Khong tach common helpers sang file moi.
- Khong doi output dict.
- Khong doi exception/behavior.
- Khong wire parser vao CLI/UI.
- Khong them parser cho PDF/DOCX.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; print(parse_resume(load_text_file('data/cvs/cv_strong.txt')))"
python -c "from src.document_loader import load_text_file; from src.jd_parser import parse_jd; print(parse_jd(load_text_file('data/jobs/jd_backend_java.txt')))"
```

Ket qua mong doi:

- Tat ca tests pass.
- Resume parser van tra ve candidate `Nguyen Van A`.
- JD parser van tra ve job title `Backend Java Developer`.

## 7. Ghi chu cho bao cao

Sau Phase 03, du an co buoc review refactor de dam bao parser khong bi phinh to va van giu mot trach nhiem ro rang: chuyen raw text thanh structured data. Hien tai chua refactor them vi code con nho, co test va de doc. Day la quyet dinh co kiem soat de tranh over-engineering trong MVP.
