# Refactoring Plan - Phase 02

## 1. Muc tieu refactor

Muc tieu chi la cai thien chat luong code, khong thay doi hanh vi he thong.

Phase 02 da them Document Loader de doc file `.txt`. Module hien tai nho, co test, va chua can refactor lon.

## 2. Nguyen tac bat buoc

- Khong thay doi behavior hien tai.
- Giu API compatibility.
- Khong thay doi input/output da thong nhat.
- Khong doi cong thuc scoring vi Phase 02 chua co scoring.
- Khong doi flow nghiep vu.
- Chi refactor sau khi da co test hoac huong dan test ro rang.

## 3. Cac van de code can xem xet

### 3.1 Duplication

Validation duoc tach thanh `_validate_text_file_path` va `_validate_directory_path`, nen function chinh khong bi lap logic nhieu.

Chua co duplication can xu ly ngay.

### 3.2 Oversized files

`src/document_loader.py` con nho va chi lam mot viec: doc text documents.

`tests/test_document_loader.py` co 8 test case, moi test mot hanh vi ro rang. File test chua qua lon.

### 3.3 Naming

Ten function ro rang:

- `load_text_file`
- `load_text_files_from_directory`

Ten helper ro rang:

- `_validate_text_file_path`
- `_validate_directory_path`

Ten constant ro rang:

- `SUPPORTED_TEXT_EXTENSIONS`
- `DEFAULT_ENCODING`

Chua can doi naming.

### 3.4 Missing tests

Da co test cho:

- Doc file `.txt` thanh cong.
- Strip whitespace ngoai cung.
- File khong ton tai.
- Path la directory.
- Extension khong duoc ho tro.
- Doc thu muc va bo qua file khong phai `.txt`.
- Thu muc khong ton tai.
- Path thu muc thuc ra la file.

Co the them test file rong trong tuong lai neu business rule can tu choi empty text. Hien tai loader cho phep empty text vi parser/scorer phase sau moi quyet dinh cach xu ly.

### 3.5 API compatibility

Public API hien tai:

```python
load_text_file(path: str | Path, encoding: str = "utf-8") -> str
load_text_files_from_directory(directory: str | Path, encoding: str = "utf-8") -> list[dict]
```

Moi refactor sau nay can giu nguyen API nay tru khi co phase plan rieng.

## 4. De xuat refactor

### De xuat 1 - Chua refactor code ngay

- File lien quan: `src/document_loader.py`
- Van de: code hien tai nho, ro, co test.
- Cach refactor: khong refactor ngay.
- Rui ro: refactor qua som co the lam tang abstraction khong can thiet.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: nen giu nguyen code Phase 02.

### De xuat 2 - Can nhac TypedDict trong phase sau

- File lien quan: `src/document_loader.py`
- Van de: output cua `load_text_files_from_directory` dang la `list[dict[str, Any]]`.
- Cach refactor: khi project co nhieu module dung document dict, co the tao `TypedDict` hoac dataclass cho document.
- Rui ro: lam code dai hon khi hien tai moi co mot module dung output nay.
- Cach test sau refactor: chay `pytest`.
- Co thay doi behavior khong? Khong.

Ket luan: chua lam trong Phase 02, chi ghi nhan cho phase sau khi co parser.

## 5. Pham vi refactor

Phase 02 khong thuc hien refactor code them.

Khong refactor:

- Khong doi ten function.
- Khong doi exception type.
- Khong doi output format cua `load_text_files_from_directory`.
- Khong them PDF/DOCX support.
- Khong wire loader vao CLI neu chua co yeu cau rieng.

## 6. Ke hoach test sau refactor

Neu co refactor sau nay, can chay:

```bash
pytest
python -c "from src.document_loader import load_text_file; print(load_text_file('data/jobs/jd_backend_java.txt'))"
python -c "from src.document_loader import load_text_files_from_directory; print(len(load_text_files_from_directory('data/cvs')))"
```

Ket qua mong doi:

- Tat ca tests pass.
- JD demo duoc in ra console.
- Thu muc CV demo co it nhat 1 document.

## 7. Ghi chu cho bao cao

Sau khi hoan thanh Document Loader, du an co buoc review refactor de dam bao module van giu mot trach nhiem duy nhat: doc text tu file. Viec chua refactor them trong phase nay la hop ly vi code dang nho, co test va ro rang. Cach lam nay giup tranh over-engineering nhung van giu quy trinh phat trien chuyen nghiep.
