# Dev Learning Log

## [2026-06-06] Phase 01 - Project Foundation

### 1. Boi canh

Du an dang o Phase 01 - Project Foundation. Muc tieu la tao nen mong repository truoc khi viet cac module xu ly CV/JD.

Tai thoi diem bat dau phase, project moi co tai lieu goc `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md` va phase plan `docs/phases/phase-01-project-foundation.md`.

### 2. Van de / chuc nang

Da tao cau truc project ban dau:

- Source code folder.
- Data folder cho CV, JD va taxonomy.
- Output folder cho ket qua ranking/report.
- Tests folder.
- Documentation folder.
- Minimal CLI entry point.
- Minimal Streamlit entry point.

### 3. Vi sao can lam

He thong sang loc CV co nhieu buoc xu ly rieng nhu document loading, parsing, skill extraction, skill normalization, matching, evidence detection va scoring. Neu khong tao cau truc tu dau, code de bi tron lan va kho giai thich khi bao ve do an.

Phase Foundation giup cac phase sau co vi tri ro rang de them module ma khong phai refactor lon.

### 4. Nguyen nhan / logic nen tang

Project duoc chia theo trach nhiem:

- `src/`: logic xu ly chinh.
- `data/`: du lieu dau vao va taxonomy.
- `tests/`: test tu dong.
- `outputs/`: ket qua sinh ra.
- `docs/`: phase plan, learning log va refactoring plan.
- `main.py`: entry point CLI.
- `app.py`: entry point Streamlit.

Logic nen tang nay lien quan truc tiep den skills-based hiring vi moi thanh phan trong flow screening can duoc tach rieng de co the test va giai thich.

### 5. Cach xu ly

Da tao cac thu muc va file nen tang. `main.py` chi in thong tin phase hien tai va thong bao foundation da san sang. `app.py` chi hien thi placeholder neu Streamlit da duoc cai.

Chua implement bat ky logic nghiep vu nao trong Phase 01.

### 6. File da thay doi

- `.gitignore`
- `README.md`
- `requirements.txt`
- `main.py`
- `app.py`
- `src/__init__.py`
- `data/cvs/.gitkeep`
- `data/jobs/.gitkeep`
- `data/taxonomy/.gitkeep`
- `outputs/.gitkeep`
- `outputs/reports/.gitkeep`
- `tests/.gitkeep`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input:

```text
Tai lieu goc cua du an
Phase plan da duoc xac nhan
Workspace hien tai
```

Output:

```text
Cau truc project nen tang
Minimal CLI entry point
Minimal Streamlit entry point
Learning log cho Phase 01
```

### 8. Cach test

Chay cac lenh:

```bash
git status --short --branch
python main.py --help
python main.py
python app.py
```

Neu chua cai Streamlit, `python app.py` se thong bao can chay `pip install -r requirements.txt`.

### 9. Ket qua mong doi

- Branch van la `phase/01-project-foundation`.
- `python main.py --help` hien thi CLI help.
- `python main.py` in ten du an va phase hien tai.
- `python app.py` khong crash khi Streamlit chua duoc cai, ma hien huong dan cai dependency.

### 10. Loi thuong gap

- Chua cai Python hoac `python` khong co trong PATH.
- Chua cai Streamlit nen khong chay duoc `streamlit run app.py`.
- Hieu nham Phase 01 la da co chuc nang screening. Phase nay chi tao nen tang.

### 11. Ghi chu cho bao cao

Giai doan Project Foundation giup du an co cau truc ro rang theo huong module hoa. Cach to chuc nay giup he thong de mo rong tu MVP rule-based sang cac chuc nang nang cao nhu semantic embedding, PDF/DOCX support va giao dien Streamlit. Moi module trong he thong se co input/output ro rang, giup qua trinh test va giai thich khi bao ve do an thuan loi hon.

## [2026-06-06] Phase 02 - Document Loader and Text Input

### 1. Boi canh

Du an dang o Phase 02 - Document Loader and Text Input. Phase 01 da tao cau truc project, con Phase 02 bat dau module dau tien trong pipeline xu ly CV/JD.

Muc tieu cua phase nay la doc noi dung `.txt` thanh raw text de cac phase sau parse va phan tich.

### 2. Van de / chuc nang

Da tao `src/document_loader.py` voi hai function chinh:

- `load_text_file(path)`
- `load_text_files_from_directory(directory)`

Dong thoi them du lieu demo:

- `data/jobs/jd_backend_java.txt`
- `data/cvs/cv_strong.txt`

Va them test:

- `tests/test_document_loader.py`

### 3. Vi sao can lam

Moi he thong NLP can co dau vao dang text truoc khi xu ly. CV va JD ban dau nam tren file, nen Document Loader la buoc chuyen file thanh chuoi text.

Neu loader doc sai file hoac chap nhan nham format, cac module parser, extractor va scorer se nhan du lieu sai.

### 4. Nguyen nhan / logic nen tang

Document Loader chi lam mot viec: doc text.

Logic chinh:

- Kiem tra file co ton tai khong.
- Kiem tra path co phai file khong.
- Chi chap nhan extension `.txt`.
- Doc bang UTF-8.
- Tra ve raw text dang `str`.
- Khi doc thu muc, chi lay cac file `.txt` va sap xep theo ten file.

Loader khong parse section, khong tim skill, khong danh gia ung vien.

### 5. Cach xu ly

Da tach validation thanh helper rieng:

- `_validate_text_file_path`
- `_validate_directory_path`

Dieu nay giup function chinh ngan gon va de test. Cac loi input duoc bao bang exception ro rang nhu `FileNotFoundError`, `IsADirectoryError`, `NotADirectoryError` va `ValueError`.

### 6. File da thay doi

- `src/document_loader.py`
- `tests/test_document_loader.py`
- `data/jobs/jd_backend_java.txt`
- `data/cvs/cv_strong.txt`
- `README.md`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input:

```text
data/jobs/jd_backend_java.txt
data/cvs/cv_strong.txt
```

Output:

```python
"Backend Java Developer\n\nRequirements:\n- Java\n..."
```

Khi doc thu muc CV, output la list dict:

```python
[
    {
        "path": "data/cvs/cv_strong.txt",
        "filename": "cv_strong.txt",
        "text": "Nguyen Van A\nBackend Developer\n..."
    }
]
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong:

```bash
python -c "from src.document_loader import load_text_file; print(load_text_file('data/jobs/jd_backend_java.txt'))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Loader doc duoc JD/CV `.txt`.
- Loader bao loi khi file khong ton tai.
- Loader tu choi extension khac `.txt`.
- Loader khong xu ly noi dung ngoai viec doc text.

### 10. Loi thuong gap

- Quen activate `.venv` nen chay nham Python global.
- Dung sai duong dan file.
- Thu doc PDF/DOCX trong Phase 02, trong khi phase nay chi ho tro `.txt`.
- Chay `pytest` bi `ModuleNotFoundError: No module named 'src'` neu pytest khong tu them project root vao import path. Du an xu ly bang `pytest.ini` voi `pythonpath = .`.

### 11. Ghi chu cho bao cao

Document Loader la module dau vao cua pipeline sang loc CV. Module nay chuyen noi dung JD va CV tu file `.txt` thanh raw text de cac module sau co the parse, trich xuat ky nang va cham diem. Viec gioi han MVP o `.txt` giup he thong co baseline on dinh truoc khi mo rong sang PDF va DOCX.

### 12. Ghi chu ve cau hinh test

Da them `pytest.ini` o root project:

```ini
[pytest]
testpaths = tests
pythonpath = .
```

Cau hinh nay giup pytest tim dung thu muc test va import duoc package `src` khi chay lenh `pytest` truc tiep trong terminal. Day la cach giu test on dinh giua cac moi truong chay khac nhau.
