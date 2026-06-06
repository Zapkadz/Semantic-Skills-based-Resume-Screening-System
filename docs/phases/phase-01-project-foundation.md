# Phase 01 - Project Foundation

## 1. Muc tieu phase

Phase 01 tao nen mong ban dau cho du an Semantic Skills-based Resume Screening System. Muc tieu la chuan bi cau truc thu muc, tai lieu nen, file cau hinh toi thieu va quy tac lam viec de cac phase sau co the trien khai tung module mot cach ro rang.

Phase nay chua xu ly CV, chua parse JD, chua matching skill va chua tinh diem.

## 2. Van de phase nay giai quyet

Du an hien tai moi co tai lieu dinh huong goc `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md`, chua co cau truc project de phat trien code. Neu bat dau viet logic ngay, code se de bi don vao mot file, kho test, kho giai thich va kho mo rong.

Phase nay giai quyet van de nen tang:

- Tao cau truc thu muc de tach source code, du lieu demo, test, output va tai lieu.
- Tao cac file entry point rong hoac toi thieu de cac phase sau tiep tuc phat trien.
- Ghi lai learning plan de nguoi hoc hieu vi sao can di theo tung buoc.
- Thiet lap cach test thu cong cho nen tang du an.

## 3. Vi sao phase nay quan trong voi do an

Day la phase giup do an co hinh dang nhu mot san pham phan mem thay vi chi la mot tap script. Khi bao ve, co the giai thich rang he thong duoc thiet ke theo module:

- `data/` luu JD, CV demo va skill taxonomy.
- `src/` luu logic xu ly chinh.
- `tests/` luu test cho cac module.
- `outputs/` luu ket qua ranking va report.
- `docs/` luu tai lieu hoc, phase plan va refactoring plan.

Cau truc ro rang giup chung minh du an co kha nang mo rong tu MVP rule-based sang semantic embedding, PDF/DOCX support va Streamlit UI.

## 4. Pham vi thuc hien

Trong Phase 01, chi thuc hien cac viec nen tang:

- Tao cau truc thu muc du an theo dinh huong trong tai lieu goc.
- Tao file nen tang toi thieu nhu `README.md`, `requirements.txt`, `main.py`, `app.py`.
- Tao cac file package rong can thiet nhu `src/__init__.py`.
- Tao file `.gitignore` neu can.
- Tao `docs/dev-learning-log.md` de ghi lai kien thuc sau moi lan sua code.
- Chua implement logic nghiep vu.

## 5. Khong lam trong phase nay

Phase nay khong lam cac viec sau:

- Khong viet document loader that su.
- Khong tao parser cho CV/JD.
- Khong tao skill taxonomy chi tiet.
- Khong implement skill extraction, normalization, matching, evidence detection.
- Khong implement scoring, ranking hay review card.
- Khong them embedding model.
- Khong cai dependency nang.
- Khong tao Streamlit UI hoan chinh.

## 6. Module lien quan

Phase nay lien quan den nen tang cua toan bo project, chua lien quan den mot module nghiep vu rieng.

Nhung module se duoc chuan bi vi tri de phat trien trong cac phase sau:

- Document Loader.
- Resume Parser.
- JD Parser.
- Skill Taxonomy.
- Skill Normalizer.
- Skill Extractor.
- Semantic Matcher.
- Evidence Detector.
- Scorer.
- Review Card Generator.
- Streamlit UI.

## 7. File du kien tao moi

- `README.md`
- `requirements.txt`
- `main.py`
- `app.py`
- `.gitignore`
- `src/__init__.py`
- `data/cvs/.gitkeep`
- `data/jobs/.gitkeep`
- `data/taxonomy/.gitkeep`
- `outputs/.gitkeep`
- `outputs/reports/.gitkeep`
- `tests/.gitkeep`
- `docs/dev-learning-log.md`
- `docs/phases/phase-01-project-foundation.md`

## 8. File du kien chinh sua

Trong phase nay du kien khong chinh sua file tai lieu goc:

- Khong chinh sua `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md`.

Co the chinh sua file phase plan nay neu can bo sung pham vi sau khi ban review.

## 9. Flow xu ly sau phase nay

Sau Phase 01, project moi chi co nen tang. Flow he thong chua chay end-to-end.

Flow mong muon sau phase nay:

```text
Project structure
  -> Ready for Phase 02 Document Loader
  -> Ready for demo data
  -> Ready for tests and learning log
```

Phase tiep theo du kien la:

```text
Phase 02 - Document Loader and Text Input
```

Trong Phase 02, he thong moi bat dau doc noi dung `.txt` tu JD va CV.

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc cach mot project AI/NLP ung dung nen duoc to chuc thanh cac phan nho, de moi module co input/output ro rang va co the test doc lap.

Can nam duoc:

- Vi sao can tach `src`, `data`, `tests`, `outputs`, `docs`.
- Vi sao khong nen viet toan bo logic trong `main.py`.
- Vi sao project can README va requirements ngay tu dau.
- Vi sao moi phase can phase plan va learning log.
- Vi sao nen di tu TXT input truoc khi mo rong sang PDF/DOCX.

### 10.2 Cac khai niem ky thuat can hieu

- Project foundation: nen mong cau truc cua du an.
- Entry point: file dau vao de chay chuong trinh, vi du `main.py` cho CLI va `app.py` cho Streamlit.
- Module: file Python chiu trach nhiem cho mot nhom logic rieng.
- Test folder: noi luu test de kiem tra logic.
- Output folder: noi luu ket qua sinh ra, giup demo va audit.
- Documentation-driven development: phat trien co tai lieu di kem de nguoi hoc hieu va bao ve duoc.

### 10.3 Cac logic nho can nam

- `data/jobs/` se chua JD mau.
- `data/cvs/` se chua nhieu CV mau.
- `data/taxonomy/` se chua skill taxonomy dang JSON.
- `src/` se chua logic xu ly.
- `tests/` se chua test cho tung module.
- `outputs/` se chua ranking result va report.
- `docs/` se chua phase plan, learning log va refactoring plan.

Neu khong co cau truc nay, cac phase sau se kho quan ly vi du lieu, code, output va tai lieu bi tron lan.

### 10.4 Vi du input/output

Input cua phase:

```text
PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md
Yeu cau lam viec theo phase
Workspace hien tai
```

Output cua phase:

```text
Cau truc thu muc project
File README/requirements/entry point toi thieu
Learning log ban dau
Nen tang de bat dau Phase 02
```

### 10.5 Noi dung co the dua vao bao cao

Trong giai doan dau, du an duoc to chuc theo kien truc module de dam bao moi thanh phan cua he thong sang loc CV co trach nhiem rieng. Cach to chuc nay giup he thong de mo rong, de test va de giai thich. Cac module xu ly nhu document loader, parser, skill normalizer, matcher va scorer se duoc phat trien doc lap, sau do ket hop thanh flow sang loc CV hoan chinh.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai va dam bao dang o `phase/01-project-foundation`.
2. Tao cau truc thu muc nen tang: `src`, `data`, `tests`, `outputs`, `docs`.
3. Tao cac file nen tang toi thieu: `README.md`, `requirements.txt`, `main.py`, `app.py`, `.gitignore`.
4. Tao placeholder `.gitkeep` cho cac thu muc chua co file noi dung.
5. Tao hoac cap nhat `docs/dev-learning-log.md`.
6. Chay lenh kiem tra cau truc thu muc.
7. Huong dan test thu cong cho ban.
8. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test thu cong:

```bash
Get-ChildItem -Recurse -Depth 2
git status --short --branch
python main.py --help
```

Ket qua dung can thay:

- Thu muc `src`, `data`, `tests`, `outputs`, `docs` ton tai.
- Git dang o branch `phase/01-project-foundation`.
- `main.py` chay duoc o muc toi thieu, chua xu ly nghiep vu.
- Chua co ranking result vi phase nay chua lam logic screening.

## 13. Tieu chi hoan thanh phase

Phase 01 chi hoan thanh khi:

- Cau truc thu muc nen tang da duoc tao.
- Cac file entry point toi thieu da ton tai.
- `docs/dev-learning-log.md` da duoc cap nhat.
- Chua implement logic ngoai pham vi.
- Ban da test thu cong va xac nhan pass.
- Refactoring plan Phase 01 da duoc tao sau khi code xong.
- Ban xac nhan neu co commit.

## 14. Rui ro

- Tao qua nhieu logic ngay trong Phase 01 se lam sai pham vi.
- File entry point neu viet qua nhieu se bien Phase 01 thanh phase implement.
- Neu thieu learning log, sau nay kho tong hop bao cao.
- Neu khong tao branch rieng, thay doi cua cac phase se kho theo doi.

## 15. Ghi chu cho bao cao

Phase Project Foundation giup dinh hinh cau truc phan mem cho he thong sang loc CV theo ky nang. Viec tach rieng code, du lieu, test, output va tai lieu giup du an de bao tri, de mo rong va phu hop voi quy trinh phat trien theo tung module. Day la buoc nen tang truoc khi xay dung cac thanh phan xu ly nhu doc tai lieu, trich xuat ky nang, chuan hoa ky nang, so khop ngu nghia, phat hien bang chung va tinh diem ung vien.
