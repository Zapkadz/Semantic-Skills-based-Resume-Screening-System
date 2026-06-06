# Phase 02 - Document Loader and Text Input

## 1. Muc tieu phase

Phase 02 tao module dau tien trong flow xu ly: Document Loader. Module nay co nhiem vu doc noi dung tu file text `.txt` de cac phase sau co du lieu dau vao cho JD Parser va Resume Parser.

Muc tieu cu the:

- Tao `src/document_loader.py`.
- Ho tro doc file `.txt` bang encoding UTF-8.
- Bao loi ro rang khi file khong ton tai, khong phai file, hoac extension chua duoc ho tro.
- Tao du lieu demo toi thieu cho JD va CV dang `.txt`.
- Them test tu dong cho document loader.
- Cap nhat learning log sau khi code.

## 2. Van de phase nay giai quyet

He thong sang loc CV can co text dau vao truoc khi co the parse, trich xuat ky nang hay cham diem. Hien tai project moi co cau truc nen tang, chua co cach doc noi dung JD/CV tu file.

Phase nay giai quyet bai toan:

```text
File .txt tren may
  -> Document Loader
  -> Raw text string
```

Raw text nay se la input cho cac phase sau.

## 3. Vi sao phase nay quan trong voi do an

Document Loader la diem vao cua pipeline. Neu doc file sai, cac module sau se nhan du lieu sai hoac rong, dan den parser, skill extractor va scorer deu sai theo.

Trong bao cao, co the giai thich day la buoc chuyen doi du lieu tu dang tai lieu thanh text thuan de he thong NLP/rule-based co the xu ly.

## 4. Pham vi thuc hien

Trong Phase 02 se lam:

- Implement function `load_text_file(path: str) -> str`.
- Implement function `load_text_files_from_directory(directory: str) -> list[dict]` neu can cho demo nhieu CV.
- Tao demo file:
  - `data/jobs/jd_backend_java.txt`
  - `data/cvs/cv_strong.txt`
- Them tests:
  - `tests/test_document_loader.py`
- Cap nhat README neu can them cach test loader.
- Cap nhat `docs/dev-learning-log.md`.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong parse JD thanh job criteria.
- Khong parse CV thanh candidate profile.
- Khong trich xuat skill.
- Khong chuan hoa skill.
- Khong match CV voi JD.
- Khong cham diem.
- Khong tao review card.
- Khong ho tro PDF/DOCX.
- Khong them embedding model.
- Khong sua cong thuc scoring.
- Khong xay UI upload file.

## 6. Module lien quan

Module chinh:

- `src/document_loader.py`

Module dung de test hoac demo:

- `main.py` co the chua can tich hop loader trong phase nay, tru khi pham vi duoc xac nhan ro.
- `tests/test_document_loader.py`

Du lieu lien quan:

- `data/jobs/jd_backend_java.txt`
- `data/cvs/cv_strong.txt`

## 7. File du kien tao moi

- `src/document_loader.py`
- `tests/test_document_loader.py`
- `data/jobs/jd_backend_java.txt`
- `data/cvs/cv_strong.txt`
- `docs/phases/phase-02-document-loader.md`
- `docs/refactoring/phase-02-refactoring-plan.md` sau khi code xong

## 8. File du kien chinh sua

- `docs/dev-learning-log.md`
- `README.md` neu can bo sung cach chay test cho Phase 02

Tam thoi khong chinh sua:

- `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md`
- `app.py`
- Scoring, matching, parser modules vi chua ton tai trong phase nay

## 9. Flow xu ly sau phase nay

Sau Phase 02, he thong se co kha nang doc text:

```text
data/jobs/jd_backend_java.txt
  -> load_text_file()
  -> JD raw text

data/cvs/cv_strong.txt
  -> load_text_file()
  -> CV raw text
```

Day moi la buoc lay raw text, chua hieu noi dung text.

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc Document Loader la gi va vi sao no la buoc dau tien cua pipeline NLP.

Can nam:

- File path la gi.
- Encoding UTF-8 la gi.
- Vi sao can validate file truoc khi doc.
- Vi sao output nen la `str`.
- Vi sao loader khong nen parse noi dung.
- Khac nhau giua doc mot file va doc ca thu muc CV.

### 10.2 Cac khai niem ky thuat can hieu

- Raw text: noi dung text nguyen ban doc tu file.
- Encoding: cach may tinh giai ma ky tu trong file. UTF-8 phu hop voi tieng Anh va tieng Viet.
- File extension: phan duoi cua ten file, vi du `.txt`.
- Exception: cach bao loi co kiem soat khi input khong hop le.
- Unit test: test mot function nho doc lap.

### 10.3 Cac logic nho can nam

- Input cua `load_text_file` la duong dan file.
- Output cua `load_text_file` la chuoi text.
- Neu file khong ton tai, function can bao loi ro rang.
- Neu path la thu muc, function khong nen doc.
- Neu file khong phai `.txt`, MVP nen tu choi de giu pham vi gon.
- Loader khong xoa, khong sua, khong danh gia noi dung CV/JD.

### 10.4 Vi du input/output

Input:

```text
data/jobs/jd_backend_java.txt
```

Noi dung file:

```text
Backend Java Developer

Requirements:
- Java
- Spring Boot
- REST API
```

Output:

```python
"Backend Java Developer\n\nRequirements:\n- Java\n- Spring Boot\n- REST API"
```

### 10.5 Noi dung co the dua vao bao cao

Document Loader la module dau vao cua he thong, co nhiem vu doc noi dung CV va JD tu file text thanh chuoi ky tu. Viec tach rieng module nay giup pipeline xu ly ro rang hon: moi thanh phan chi dam nhan mot nhiem vu. Trong MVP, he thong uu tien `.txt` de dam bao baseline on dinh truoc khi mo rong sang PDF/DOCX.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/02-document-loader`.
2. Tao `src/document_loader.py`.
3. Viet `load_text_file(path: str) -> str`.
4. Viet validation cho path, file extension va empty file neu can.
5. Tao demo JD/CV `.txt`.
6. Tao `tests/test_document_loader.py`.
7. Chay `pytest`.
8. Chay test thu cong bang Python.
9. Cap nhat `docs/dev-learning-log.md`.
10. Tao `docs/refactoring/phase-02-refactoring-plan.md`.
11. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong:

```bash
python -c "from src.document_loader import load_text_file; print(load_text_file('data/jobs/jd_backend_java.txt'))"
```

Neu dung virtual environment:

```bash
.\.venv\Scripts\Activate.ps1
pytest
```

## 13. Tieu chi hoan thanh phase

Phase 02 hoan thanh khi:

- `src/document_loader.py` ton tai.
- `load_text_file` doc duoc file `.txt`.
- Loi input duoc bao ro rang.
- Co demo JD/CV `.txt`.
- Co test tu dong cho truong hop thanh cong va that bai.
- `pytest` pass.
- Learning log duoc cap nhat.
- Refactoring plan Phase 02 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Xu ly qua nhieu format som se lam phase phinh to.
- Neu loader vua doc file vua parse noi dung, module se bi sai trach nhiem.
- File tieng Viet co the loi ky tu neu encoding khong ro.
- Test chi voi happy path se bo sot loi file khong ton tai hoac extension sai.

## 15. Ghi chu cho bao cao

Phase Document Loader tap trung vao viec chuan hoa dau vao cua pipeline bang cach doc CV va JD tu file text. Day la buoc nen tang de cac module NLP/rule-based sau co the xu ly noi dung mot cach nhat quan. MVP chi ho tro `.txt` truoc de giam rui ro ky thuat, sau khi flow chay on dinh moi mo rong sang PDF va DOCX.
