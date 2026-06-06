# Phase 04 - Skill Taxonomy and Normalization

## 1. Muc tieu phase

Phase 04 tao nen tang cho viec chuan hoa ky nang trong he thong. Sau Phase 03, parser da trich duoc `raw_skills` tu CV va `must_have_skills` / `nice_to_have_skills` tu JD, nhung cac skill nay van la text tho.

Muc tieu cua phase nay:

- Tao skill taxonomy dang JSON.
- Tao module load taxonomy.
- Tao alias map de tim ten skill chuan.
- Tao skill normalizer de chuan hoa skill tu CV/JD.
- Them tests cho taxonomy va normalizer.

Phase nay chua so khop skill CV voi JD va chua cham diem.

## 2. Van de phase nay giai quyet

CV va JD co the viet cung mot ky nang bang nhieu cach khac nhau:

```text
ReactJS, React.js, React
K8s, Kubernetes
Postgres, PostgreSQL
JS, JavaScript
SpringBoot, Spring Boot
```

Neu he thong so sanh text tho, cac bien the nay co the bi xem la khac nhau. Phase 04 giai quyet bang cach dua skill ve ten chuan trong taxonomy.

## 3. Vi sao phase nay quan trong voi do an

Skills-based hiring can danh gia ung vien theo nang luc that, khong nen phu thuoc qua nhieu vao cach viet tu khoa. Taxonomy va normalization giup he thong:

- Giam sai sot do alias.
- Tao nen tang cho matching o Phase 05.
- Giup scoring sau nay dua tren skill chuan thay vi text lung tung.
- De giai thich hon vi sao mot skill duoc match.

Trong bao cao, phase nay co the duoc mo ta la buoc chuan hoa tri thuc ky nang truoc khi so khop CV-JD.

## 4. Pham vi thuc hien

Trong Phase 04 se lam:

- Tao `data/taxonomy/skills.json`.
- Tao `src/skill_taxonomy.py`.
- Tao `src/skill_normalizer.py`.
- Implement `load_taxonomy(path: str) -> dict`.
- Implement `build_alias_map(taxonomy: dict) -> dict`.
- Implement `normalize_skill(skill: str, taxonomy: dict) -> str`.
- Implement `normalize_skills(skills: list[str], taxonomy: dict) -> list[str]`.
- Them tests:
  - `tests/test_skill_taxonomy.py`
  - `tests/test_skill_normalizer.py`
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong extract skill tu raw text ngoai parser output.
- Khong match skill CV voi JD.
- Khong related/transferable matching.
- Khong evidence detection.
- Khong scoring/ranking.
- Khong review card.
- Khong embedding semantic matching.
- Khong UI.
- Khong sua parser neu parser dang pass.

## 6. Module lien quan

Module chinh:

- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`

Du lieu chinh:

- `data/taxonomy/skills.json`

Module input tu phase truoc:

- `src/resume_parser.py`
- `src/jd_parser.py`

Tests:

- `tests/test_skill_taxonomy.py`
- `tests/test_skill_normalizer.py`

## 7. File du kien tao moi

- `data/taxonomy/skills.json`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `tests/test_skill_taxonomy.py`
- `tests/test_skill_normalizer.py`
- `docs/phases/phase-04-skill-taxonomy.md`
- `docs/refactoring/phase-04-refactoring-plan.md` sau khi code xong

## 8. File du kien chinh sua

- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `app.py`
- `PROJECT_SEMANTIC_SKILLS_RESUME_SCREENING.md`

## 9. Flow xu ly sau phase nay

Sau Phase 04, flow co the la:

```text
CV raw text
  -> load_text_file()
  -> parse_resume()
  -> raw_skills
  -> normalize_skills()
  -> normalized candidate skills

JD raw text
  -> load_text_file()
  -> parse_jd()
  -> must_have_skills / nice_to_have_skills
  -> normalize_skills()
  -> normalized job skills
```

Vi du:

```python
normalize_skill("SpringBoot", taxonomy) == "Spring Boot"
normalize_skill("Postgres", taxonomy) == "PostgreSQL"
normalize_skill("JS", taxonomy) == "JavaScript"
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc skill taxonomy va skill normalization la gi.

Can nam:

- Taxonomy la tap tri thuc ky nang co cau truc.
- Alias la cac cach viet khac nhau cua cung mot skill.
- Normalization la dua text tho ve ten chuan.
- Vi sao phai normalize truoc khi matching.
- Vi sao taxonomy nen nam trong JSON de de sua.

### 10.2 Cac khai niem ky thuat can hieu

- Skill taxonomy: danh sach skill chuan kem metadata.
- Canonical skill: ten skill chuan, vi du `PostgreSQL`.
- Alias: ten goi khac, vi du `Postgres`.
- Category: nhom skill, vi du Programming Language, Database.
- Related skills: ky nang lien quan truc tiep.
- Transferable skills: ky nang co the chuyen doi ve mat nang luc.
- Alias map: dict tra cuu nhanh alias -> canonical skill.

### 10.3 Cac logic nho can nam

- `load_taxonomy` doc JSON thanh dict.
- `build_alias_map` tao mapping lowercase/case-insensitive tu canonical skill va aliases ve canonical skill.
- `normalize_skill` xu ly trim whitespace va case-insensitive lookup.
- `normalize_skills` chuan hoa list skill va loai duplicate nhung giu thu tu.
- Skill khong co trong taxonomy co the duoc giu nguyen de khong mat thong tin.

### 10.4 Vi du input/output

Input taxonomy:

```json
{
  "React": {
    "aliases": ["ReactJS", "React.js"],
    "category": "Frontend Framework",
    "related": ["JavaScript"],
    "transferable": ["Vue.js", "Angular"]
  }
}
```

Input skill:

```text
ReactJS
```

Output:

```text
React
```

Input list:

```python
["JS", "ReactJS", "Postgres", "React.js"]
```

Output:

```python
["JavaScript", "React", "PostgreSQL"]
```

### 10.5 Noi dung co the dua vao bao cao

Skill Taxonomy giup he thong chuan hoa cac ky nang duoc viet theo nhieu cach khac nhau trong CV va JD. Buoc nay lam giam phu thuoc vao keyword exact match va tao nen tang cho semantic/rule-based matching o cac phase sau.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/04-skill-taxonomy`.
2. Tao `data/taxonomy/skills.json` voi nhom skill MVP.
3. Tao `src/skill_taxonomy.py`.
4. Implement `load_taxonomy`.
5. Implement `build_alias_map`.
6. Tao `src/skill_normalizer.py`.
7. Implement `normalize_skill`.
8. Implement `normalize_skills`.
9. Them tests cho taxonomy loader va alias map.
10. Them tests cho normalizer.
11. Chay `pytest`.
12. Test thu cong voi parser output tu CV/JD demo.
13. Cap nhat README.
14. Cap nhat `docs/dev-learning-log.md`.
15. Tao `docs/refactoring/phase-04-refactoring-plan.md`.
16. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong skill normalizer:

```bash
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); print(normalize_skills(['JS', 'SpringBoot', 'Postgres'], taxonomy))"
```

Test voi parser output:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); print(normalize_skills(profile['raw_skills'], taxonomy))"
```

## 13. Tieu chi hoan thanh phase

Phase 04 hoan thanh khi:

- Co `data/taxonomy/skills.json`.
- Co `src/skill_taxonomy.py`.
- Co `src/skill_normalizer.py`.
- Normalize duoc alias pho bien.
- Duplicate sau normalization duoc loai bo nhung van giu thu tu.
- Skill unknown khong bi mat.
- Co tests tu dong.
- `pytest` pass.
- Learning log duoc cap nhat.
- Refactoring plan Phase 04 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- Taxonomy qua nho se bo sot skill.
- Taxonomy qua lon trong MVP se ton cong quan ly.
- Alias map neu khong case-insensitive se bo sot bien the viet hoa.
- Normalize qua manh co the bien skill unknown thanh sai ten.
- Neu phase nay lam matching luon se vuot scope.

## 15. Ghi chu cho bao cao

Phase Skill Taxonomy and Normalization tao lop tri thuc ky nang cho he thong. Taxonomy luu ten skill chuan, alias, category, related skills va transferable skills. Normalizer su dung taxonomy de dua cac skill tu CV va JD ve dang thong nhat, giup cac phase sau so khop chinh xac hon va giam sai sot do khac biet cach viet.
