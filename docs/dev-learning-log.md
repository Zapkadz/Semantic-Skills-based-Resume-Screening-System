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
