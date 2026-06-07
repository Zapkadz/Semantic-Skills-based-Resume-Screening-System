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

## [2026-06-06] Phase 03 - Resume Parser and JD Parser

### 1. Boi canh

Du an dang o Phase 03 - Resume Parser and JD Parser. Phase 02 da doc duoc file `.txt` thanh raw text. Phase 03 tiep tuc chuyen raw text thanh dict co cau truc.

Muc tieu la tao output on dinh de cac phase sau co the trich xuat skill, chuan hoa skill, so khop va cham diem.

### 2. Van de / chuc nang

Da tao hai parser rule-based:

- `src/resume_parser.py`
- `src/jd_parser.py`

Resume Parser tao candidate profile dict. JD Parser tao job criteria dict.

### 3. Vi sao can lam

Raw text la chuoi tu do, kho xu ly truc tiep. He thong can biet dau la skill, dau la experience, dau la project, dau la requirement, dau la nice-to-have.

Parser giup bien text thanh du lieu co cau truc. Khi du lieu co cau truc, cac module sau co the xu ly tung truong rieng thay vi doan ca chuoi text dai.

### 4. Nguyen nhan / logic nen tang

Logic nen tang cua parser la section detection:

- Tim heading nhu `Summary:`, `Skills:`, `Work Experience:`, `Projects:`.
- Tim heading JD nhu `Requirements:`, `Nice to have:`, `Responsibilities:`.
- Gom cac dong ben duoi heading vao section tuong ung.
- Tach bullet thanh list item.
- Giu output dang dict co key on dinh.

Parser khong match skill, khong tinh evidence, khong cham diem.

### 5. Cach xu ly

Resume Parser:

- Lay `candidate_name` tu dong dau tien.
- Lay `headline` tu dong gioi thieu thu hai neu co.
- Parse `summary`, `raw_skills`, `work_experience`, `projects`, `education`, `certifications`.
- Work experience MVP tach title/company bang pattern `Title - Company`.
- Project MVP tach project name va description bullet.

JD Parser:

- Lay `job_title` tu dong dau tien.
- Parse `must_have_skills` tu section Requirements.
- Parse `nice_to_have_skills` tu section Nice to have.
- Parse `responsibilities`.
- Tach `minimum_experience_years` tu pattern nhu `1+ year`.
- Suy luan `seniority` don gian tu title hoac so nam kinh nghiem.
- Suy luan `domain` don gian tu keyword nhu backend, API, web, testing.

### 6. File da thay doi

- `src/resume_parser.py`
- `src/jd_parser.py`
- `tests/test_resume_parser.py`
- `tests/test_jd_parser.py`
- `README.md`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input resume:

```text
Raw text tu data/cvs/cv_strong.txt
```

Output resume:

```python
{
    "candidate_name": "Nguyen Van A",
    "headline": "Backend Developer",
    "raw_skills": ["Java", "Spring Boot", "REST API", "MySQL", "Docker"],
    "work_experience": [...],
    "projects": [...]
}
```

Input JD:

```text
Raw text tu data/jobs/jd_backend_java.txt
```

Output JD:

```python
{
    "job_title": "Backend Java Developer",
    "must_have_skills": ["Java", "Spring Boot", "REST API", "SQL", "Basic Docker"],
    "nice_to_have_skills": ["AWS", "Kafka", "Kubernetes"],
    "minimum_experience_years": 1,
    "seniority": "Junior",
    "domain": ["Backend", "Web Application"]
}
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong Resume Parser:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; print(parse_resume(load_text_file('data/cvs/cv_strong.txt')))"
```

Test thu cong JD Parser:

```bash
python -c "from src.document_loader import load_text_file; from src.jd_parser import parse_jd; print(parse_jd(load_text_file('data/jobs/jd_backend_java.txt')))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Resume Parser tra ve candidate profile co `candidate_name`, `raw_skills`, `work_experience`, `projects`.
- JD Parser tra ve job criteria co `job_title`, `must_have_skills`, `nice_to_have_skills`, `responsibilities`.
- Parser khong cham diem va khong dua ra recommendation.

### 10. Loi thuong gap

- Format CV/JD khac heading demo co the parse chua tot.
- Nhieu work experience phuc tap co the can rule rieng o phase sau.
- Suy luan seniority/domain trong Phase 03 chi la baseline don gian, khong phai scoring cuoi cung.

### 11. Ghi chu cho bao cao

Resume Parser va JD Parser la buoc information extraction trong pipeline. Module nay chuyen noi dung CV/JD tu raw text thanh du lieu co cau truc, giup cac module sau lam viec tren truong thong tin ro rang. Cach tiep can rule-based trong MVP giup ket qua deterministic, de test va de giai thich, phu hop voi muc tieu xay dung baseline truoc khi them AI/embedding nang cao.

## [2026-06-06] Phase 04 - Skill Taxonomy and Normalization

### 1. Boi canh

Du an dang o Phase 04 - Skill Taxonomy and Normalization. Phase 03 da parse CV/JD thanh dict co cau truc, trong do co cac field nhu `raw_skills`, `must_have_skills` va `nice_to_have_skills`.

Muc tieu Phase 04 la chuan hoa cac skill text nay ve ten chuan truoc khi so khop o Phase 05.

### 2. Van de / chuc nang

Da tao:

- `data/taxonomy/skills.json`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `tests/test_skill_taxonomy.py`
- `tests/test_skill_normalizer.py`

Taxonomy luu canonical skill, aliases, category, related skills va transferable skills. Normalizer dung alias map de dua skill tho ve ten chuan.

### 3. Vi sao can lam

CV va JD co the viet cung mot skill bang nhieu cach:

```text
SpringBoot -> Spring Boot
Postgres -> PostgreSQL
JS -> JavaScript
Basic Docker -> Docker
K8s -> Kubernetes
```

Neu khong chuan hoa, he thong co the xem cac cach viet nay la skill khac nhau va bo sot ung vien phu hop.

### 4. Nguyen nhan / logic nen tang

Logic nen tang:

- `load_taxonomy` doc file JSON va validate cau truc toi thieu.
- `build_alias_map` tao mapping case-insensitive tu alias ve canonical skill.
- `normalize_skill` chuan hoa mot skill.
- `normalize_skills` chuan hoa list skill, loai duplicate sau normalization va giu thu tu dau tien.
- Skill khong co trong taxonomy duoc giu nguyen de khong mat thong tin.

### 5. Cach xu ly

Taxonomy duoc luu o JSON de de sua va mo rong. Moi skill co cau truc:

```json
{
  "aliases": [],
  "category": "...",
  "related": [],
  "transferable": []
}
```

Alias map duoc tao tu ca canonical skill va aliases. Vi du:

```python
"springboot" -> "Spring Boot"
"postgres" -> "PostgreSQL"
"js" -> "JavaScript"
```

### 6. File da thay doi

- `data/taxonomy/skills.json`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `tests/test_skill_taxonomy.py`
- `tests/test_skill_normalizer.py`
- `README.md`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input:

```python
["JS", "ReactJS", "Postgres", "React.js"]
```

Output:

```python
["JavaScript", "React", "PostgreSQL"]
```

Input tu parser:

```python
["Java", "Spring Boot", "REST API", "MySQL", "Docker"]
```

Output:

```python
["Java", "Spring Boot", "REST API", "MySQL", "Docker"]
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong:

```bash
python -c "from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); print(normalize_skills(['JS', 'SpringBoot', 'Postgres'], taxonomy))"
```

Test voi parser output:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); print(normalize_skills(profile['raw_skills'], taxonomy))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Alias duoc map ve canonical skill.
- Duplicate sau normalization duoc loai bo.
- Unknown skill duoc giu nguyen.
- Parser output co the normalize duoc ma khong can sua parser.

### 10. Loi thuong gap

- Them alias trung nhau cho hai skill khac nhau lam alias ambiguous.
- Quen viet alias vao taxonomy nen skill khong duoc chuan hoa.
- Normalize qua manh va lam mat skill unknown.
- Lam matching trong Phase 04 se vuot scope.

### 11. Ghi chu cho bao cao

Skill Taxonomy va Normalization giup he thong dua cac ky nang duoc viet theo nhieu cach khac nhau ve ten chuan. Day la nen tang quan trong cua skills-based hiring vi he thong khong chi so sanh keyword tho, ma lam viec tren mot bo ky nang da duoc chuan hoa. Buoc nay giup Phase 05 co the so khop skill CV/JD chinh xac hon.

## [2026-06-06] Phase 05 - Rule-based Skill Matching

### 1. Boi canh

Du an dang o Phase 05 - Rule-based Skill Matching. Phase 04 da co taxonomy va normalizer de dua skill tu CV/JD ve canonical skill. Phase 05 bat dau so khop danh sach skill cua JD voi danh sach skill cua ung vien.

Muc tieu la tao match result co cau truc, chua phai final score/ranking.

### 2. Van de / chuc nang

Da tao:

- `src/semantic_matcher.py`
- `tests/test_semantic_matcher.py`

Matcher ho tro:

- `exact_match`
- `related_match`
- `transferable_match`
- `no_match`

### 3. Vi sao can lam

Skills-based screening can biet JD skill nao duoc ung vien dap ung, ky nang nao lien quan, ky nang nao transferable va ky nang nao dang thieu.

Neu chi so sanh exact text, `SQL` va `MySQL` co the bi xem la khong lien quan. Matcher dung taxonomy de nhan dien cac quan he nay.

### 4. Nguyen nhan / logic nen tang

Thu tu uu tien match:

1. Exact match.
2. Related match.
3. Transferable match.
4. No match.

Score tung match:

```text
exact_match        = 1.00
related_match      = 0.75
transferable_match = 0.55
no_match           = 0.00
```

Alias da duoc xu ly o Phase 04 bang normalization. Matcher van co canonicalization nhe de tranh loi neu input con alias.

### 5. Cach xu ly

`match_skills(job_skills, candidate_skills, taxonomy)` xu ly tung required skill cua JD:

- Tim exact match trong candidate skills.
- Neu khong co, tim related match dua tren field `related` trong taxonomy.
- Neu khong co, tim transferable match dua tren field `transferable`.
- Neu van khong co, tra ve `no_match`.

`get_missing_skills(matches)` tra ve cac required skill co `match_type == "no_match"`.

### 6. File da thay doi

- `src/semantic_matcher.py`
- `tests/test_semantic_matcher.py`
- `README.md`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input:

```python
job_skills = ["Java", "Spring Boot", "REST API", "SQL"]
candidate_skills = ["Java", "Spring Boot", "REST API", "MySQL"]
```

Output:

```python
[
    {"required_skill": "Java", "candidate_skill": "Java", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "Spring Boot", "candidate_skill": "Spring Boot", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "REST API", "candidate_skill": "REST API", "match_type": "exact_match", "score": 1.0},
    {"required_skill": "SQL", "candidate_skill": "MySQL", "match_type": "related_match", "score": 0.75}
]
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Demo CV/JD co exact match cho Java, Spring Boot, REST API, Docker.
- Demo CV/JD co related match cho SQL voi MySQL.
- No match tra `candidate_skill = None`.
- Phase nay chua tao recommendation label.

### 10. Loi thuong gap

- Hieu nham match score la final score. Thuc te day chi la diem tung skill match.
- Taxonomy thieu related/transferable thi matcher se tra no_match.
- Them evidence/scoring vao matcher se lam module sai trach nhiem.

### 11. Ghi chu cho bao cao

Rule-based Skill Matching la baseline so khop ky nang giua JD va CV. He thong uu tien exact match, sau do dung taxonomy de xet related va transferable skills. Ket qua la danh sach match co loai match va diem tung skill, giup cac phase sau tiep tuc evidence detection va scoring mot cach minh bach.

## [2026-06-06] Phase 06 - Semantic Matching with Embeddings

### 1. Boi canh

Du an dang o Phase 06 - Semantic Matching with Embeddings. Phase 05 da co rule-based matcher dua tren exact, related va transferable skills. Phase 06 them semantic embedding matcher nhu mot fallback khi rule-based matcher tra `no_match`.

Muc tieu la them kha nang gan nghia ma khong lam mat tinh minh bach cua baseline rule-based.

### 2. Van de / chuc nang

Da tao:

- `src/embedding_matcher.py`
- `tests/test_embedding_matcher.py`

Da cap nhat:

- `src/semantic_matcher.py`
- `tests/test_semantic_matcher.py`
- `requirements.txt`

Matcher hien co them `semantic_match` voi score `0.85` khi embedding similarity dat threshold.

### 3. Vi sao can lam

Taxonomy khong the bao phu moi cach dien dat. Vi du:

```text
Backend API development
Built RESTful services
```

Hai cum nay co the gan nghia du khong trung keyword hoan toan. Embedding giup do muc do gan nghia giua hai chuoi text.

### 4. Nguyen nhan / logic nen tang

Logic Phase 06:

- Rule-based match van uu tien truoc.
- Semantic match chi chay khi exact/related/transferable deu khong match.
- Embedding model duoc load lazy.
- Neu dependency/model unavailable, he thong khong crash.
- Tests dung fake embedding model de khong phu thuoc download model.

### 5. Cach xu ly

`SemanticEmbeddingMatcher` co cac thanh phan:

- `load_model()`: load pretrained model neu co.
- `is_available()`: kiem tra model da load chua.
- `similarity(text_a, text_b)`: tinh cosine similarity hoac tra `None` neu fallback.
- `best_match(required_skill, candidate_skills)`: tim candidate co similarity cao nhat tren threshold.

`match_skills` nhan optional `embedding_matcher`. Neu khong truyen tham so nay, behavior Phase 05 giu nguyen.

### 6. File da thay doi

- `requirements.txt`
- `src/embedding_matcher.py`
- `src/semantic_matcher.py`
- `tests/test_embedding_matcher.py`
- `tests/test_semantic_matcher.py`
- `README.md`
- `docs/dev-learning-log.md`

### 7. Input / Output can nho

Input:

```python
required_skill = "Backend API development"
candidate_skills = ["React", "REST API"]
```

Output semantic match neu similarity du nguong:

```python
{
    "required_skill": "Backend API development",
    "candidate_skill": "REST API",
    "match_type": "semantic_match",
    "score": 0.85,
    "similarity": 0.9939
}
```

Output fallback khi model unavailable:

```python
{
    "required_skill": "Backend API development",
    "candidate_skill": None,
    "match_type": "no_match",
    "score": 0.0
}
```

### 8. Cach test

Chay:

```bash
pytest
```

Test fallback:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(auto_load=False); print(matcher.is_available())"
```

Test demo matcher rule-based van hoat dong:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); print(match_skills(required, candidate, taxonomy))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Rule-based matcher van cho ket qua nhu Phase 05 neu khong truyen embedding matcher.
- Embedding matcher khong crash khi model unavailable.
- Semantic match chi xuat hien khi co embedding matcher va similarity du threshold.

### 10. Loi thuong gap

- Hieu nham semantic match la final score. Thuc te day chi la match-level signal.
- Model download co the fail neu khong co internet.
- Threshold qua thap co the match sai.
- Threshold qua cao co the bo sot match gan nghia.
- Dung embedding thay rule-based baseline se lam he thong kem minh bach.

### 11. Ghi chu cho bao cao

Semantic Matching with Embeddings giup he thong nhan dien cac ky nang hoac mo ta gan nghia, bo sung cho rule-based matching. Du an khong train model tu dau ma dung pretrained embedding model khi kha dung. De dam bao tinh on dinh, module co fallback neu model khong load duoc va rule-based matching van la baseline chinh.

## [2026-06-06] Phase 07 - Evidence Detection

### 1. Boi canh

Du an dang o Phase 07 - Evidence Detection. Phase 05/06 da tao match result cho tung skill JD voi skill ung vien. Tuy nhien, match result moi cho biet skill co lien quan hay khong, chua cho biet ung vien co bang chung da dung skill do trong CV hay chua.

Muc tieu Phase 07 la them evidence level va evidence text cho tung match.

### 2. Van de / chuc nang

Da tao:

- `src/evidence_detector.py`
- `tests/test_evidence_detector.py`

Evidence detector ho tro:

- Level 0: khong co bang chung.
- Level 1: skill chi xuat hien trong summary/headline/skill list.
- Level 2: skill xuat hien trong project/work context nhung action chua ro.
- Level 3: skill xuat hien trong project/work bullet co action verb.

### 3. Vi sao can lam

Neu CV chi liet ke skill trong muc Skills, he thong chua nen xem do la bang chung manh. Evidence Detection giup phan biet:

```text
Skills: Kafka
```

voi:

```text
Built REST APIs using Java and Spring Boot.
Designed MySQL database schemas.
```

Buoc nay giup giam tinh trang CV nhoi keyword.

### 4. Nguyen nhan / logic nen tang

Logic evidence:

- Thu thap evidence candidates tu work experience, projects, summary, headline va raw skills.
- Tim skill trong tung cau/dong theo case-insensitive search.
- Neu evidence nam trong work/project va co action verb thi level 3.
- Neu evidence nam trong work/project nhung khong co action verb thi level 2.
- Neu evidence chi nam trong summary/headline/skills thi level 1.
- Neu khong thay thi level 0.

Voi related match nhu `SQL -> MySQL`, detector uu tien tim `candidate_skill` la `MySQL` trong CV.

### 5. Cach xu ly

`detect_evidence(skill, resume_profile)` tra ve evidence cho mot skill.

`detect_all_evidence(matches, resume_profile)` enrich match result bang:

```python
{
    "evidence_level": 3,
    "evidence_text": "Built REST APIs using Java and Spring Boot.",
    "evidence_source": "work_experience"
}
```

Evidence detector khong thay doi `match_type` hay `score` cua matcher.

### 6. File da thay doi

- `src/evidence_detector.py`
- `tests/test_evidence_detector.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-07-evidence-detection.md`

### 7. Input / Output can nho

Input:

```python
{
    "required_skill": "SQL",
    "candidate_skill": "MySQL",
    "match_type": "related_match",
    "score": 0.75
}
```

Output:

```python
{
    "required_skill": "SQL",
    "candidate_skill": "MySQL",
    "match_type": "related_match",
    "score": 0.75,
    "evidence_level": 3,
    "evidence_text": "Designed MySQL database schemas for product and order modules.",
    "evidence_source": "work_experience"
}
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); matches=match_skills(required, candidate, taxonomy); print(detect_all_evidence(matches, profile))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Demo strong CV co evidence level 3 cho Java, Spring Boot, REST API, SQL/MySQL va Docker.
- Keyword-only profile chi duoc level 1.
- Skill khong xuat hien co level 0.

### 10. Loi thuong gap

- Hieu nham evidence level la final score. Thuc te final score se lam o Phase 08.
- Evidence detector co the bo sot neu CV dung cach viet qua khac.
- Action verbs con la danh sach rule-based nho trong MVP.
- Neu evidence detector tu tinh ranking thi vuot scope.

### 11. Ghi chu cho bao cao

Evidence Detection giup he thong phan biet giua ky nang chi duoc liet ke va ky nang co bang chung su dung trong kinh nghiem/du an. Day la thanh phan quan trong de giam keyword stuffing va tao nen tang cho evidence-based scoring trong Phase 08.

## [2026-06-06] Phase 08 - Scoring and Ranking

### 1. Boi canh

Du an dang o Phase 08 - Scoring and Ranking. Phase 07 da enrich match result bang `evidence_level`, `evidence_text` va `evidence_source`. Tuy nhien, he thong van chua co diem tong hop de sap xep ung vien.

Muc tieu Phase 08 la bien cac tin hieu rieng le thanh score components, final score va recommendation label.

### 2. Van de / chuc nang

Da tao:

- `src/scorer.py`
- `tests/test_scorer.py`

Scorer ho tro:

- Tinh skill semantic score tu match score.
- Tinh evidence score tu evidence level.
- Tinh experience fit.
- Tinh seniority fit.
- Tinh domain fit.
- Tinh nice-to-have coverage.
- Tinh final score 0-100.
- Gan recommendation label.
- Rank nhieu candidate result.

### 3. Vi sao can lam

Recruiter can xem nhanh ung vien nao nen duoc uu tien review. Match result va evidence result la du lieu chi tiet, nhung chua tao thu tu uu tien.

Scoring giup tong hop cac tin hieu:

```text
matched skills + evidence + experience + seniority + domain + nice-to-have
  -> final score
  -> recommendation label
```

Ket qua van chi la recommendation ho tro review, khong phai quyet dinh tuyen dung tu dong.

### 4. Nguyen nhan / logic nen tang

Cong thuc Phase 08:

```text
Final Score =
  40% skill_semantic
+ 20% evidence
+ 15% experience
+ 10% seniority
+ 10% domain
+  5% nice_to_have
```

Evidence level map sang score:

```text
Level 0 -> 0.0
Level 1 -> 0.4
Level 2 -> 0.7
Level 3 -> 1.0
```

Recommendation label:

```text
>= 85: Strong Review
>= 70: Review
>= 55: Maybe Review
>= 40: Low Priority
<  40: Not Enough Evidence
```

### 5. Cach xu ly

`score_candidate(job_criteria, resume_profile, matches, nice_to_have_matches)` tra ve dict co:

- `candidate_name`
- `final_score`
- `recommendation`
- `scores`
- `matched_skills`
- `missing_skills`
- `nice_to_have_matches`
- `seniority`
- `experience_years`
- `domain`

Experience duoc estimate tu duration trong work experience theo pattern `MM/YYYY - MM/YYYY`.

Seniority duoc suy luan tu text va so nam kinh nghiem:

- >= 5 nam: Senior
- >= 2 nam: Middle
- >= 0.5 nam hoac co developer/engineer: Junior
- intern/fresher text: Intern/Fresher neu khong bi rule tren match truoc

Domain duoc suy luan tu keyword trong profile. Rule `Testing` duoc giu tuong doi chat de tranh gan domain testing chi vi co cum "local development and testing".

`rank_candidates(candidate_results)` sap xep theo:

1. `final_score` giam dan.
2. `scores.evidence` giam dan.
3. `candidate_name` tang dan.

### 6. File da thay doi

- `src/scorer.py`
- `tests/test_scorer.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-08-scoring-ranking.md`

### 7. Input / Output can nho

Input:

```python
matches = [
    {"required_skill": "Java", "score": 1.0, "evidence_level": 3},
    {"required_skill": "SQL", "score": 0.75, "evidence_level": 3}
]
```

Output component:

```python
skill_semantic = 0.875
evidence = 1.0
```

Demo JD/CV output chinh:

```python
{
    "candidate_name": "Nguyen Van A",
    "final_score": 87,
    "recommendation": "Strong Review",
    "scores": {
        "skill_semantic": 0.95,
        "evidence": 1.0,
        "experience": 0.5,
        "seniority": 1.0,
        "domain": 1.0,
        "nice_to_have": 0.3333
    }
}
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong scoring:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); nice_skills=normalize_skills(criteria['nice_to_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(nice_skills, candidate, taxonomy); print(score_candidate(criteria, profile, matches, nice))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Demo CV/JD co final score 87.
- Demo CV/JD co recommendation `Strong Review`.
- Score components duoc tra ve rieng de giai thich.
- Missing skills duoc lay tu match co `match_type == "no_match"`.
- Ranking gan `rank` bat dau tu 1.

### 10. Loi thuong gap

- Hieu nham final score la pass/fail tu dong. Thuc te day chi la uu tien review.
- Weight scoring co the can dieu chinh khi co tap CV/JD lon hon.
- Experience parser hien moi ho tro duration dang `MM/YYYY - MM/YYYY`.
- Domain/seniority van la baseline rule-based, chua phai suy luan phuc tap.
- Neu nice-to-have khong co input, scorer dung diem trung tinh `0.5`.

### 11. Ghi chu cho bao cao

Scoring and Ranking la buoc tong hop cua pipeline MVP. He thong ket hop skill match, evidence strength, experience, seniority, domain va nice-to-have bang cong thuc co trong so ro rang. Cach tiep can rule-based giup ket qua deterministic, test duoc va giai thich duoc cho recruiter.

## [2026-06-06] Phase 09 - Explainable Review Card

### 1. Boi canh

Du an dang o Phase 09 - Explainable Review Card. Phase 08 da tao `candidate_result` co final score, recommendation, score components, matched skills, missing skills va evidence.

Tuy nhien, output Phase 08 van la dict ky thuat. Recruiter can mot ban tom tat de doc nhanh va hieu ly do he thong goi y review.

### 2. Van de / chuc nang

Da tao:

- `src/review_card_generator.py`
- `tests/test_review_card_generator.py`

Review card generator ho tro:

- Tao structured review card tu `candidate_result`.
- Tao summary.
- Giu score breakdown.
- Tao evidence highlights.
- Tao strengths.
- Tao concerns.
- Tao suggested interview questions.
- Format review card sang Markdown.

### 3. Vi sao can lam

Neu he thong chi tra ve diem so, recruiter kho biet vi sao ung vien duoc xep hang cao hoac thap. Explainable Review Card giup minh bach hoa:

```text
Final score
  -> score breakdown
  -> matched skills
  -> evidence snippets
  -> missing skills
  -> strengths / concerns
  -> interview questions
```

Day la buoc quan trong de chung minh he thong khong phai black-box scoring.

### 4. Nguyen nhan / logic nen tang

Nguyen tac Phase 09:

- Review card khong tinh lai score.
- Review card chi doc output tu scorer.
- Strengths dua tren score components cao va evidence highlights.
- Concerns dua tren missing skills, score components thap va nice-to-have gaps.
- Interview questions duoc tao bang template rule-based.
- Structured dict la output chinh, Markdown chi la format hien thi.

### 5. Cach xu ly

`generate_review_card(candidate_result, job_criteria=None)` tra ve dict co:

- `candidate_name`
- `job_title`
- `final_score`
- `recommendation`
- `summary`
- `score_breakdown`
- `seniority`
- `experience_years`
- `domain`
- `matched_skills`
- `missing_skills`
- `nice_to_have_matches`
- `evidence_highlights`
- `strengths`
- `concerns`
- `suggested_interview_questions`

`format_review_card_markdown(review_card)` chuyen dict tren thanh Markdown de doc trong terminal hoac sau nay hien thi o UI.

Evidence highlights chi lay match co:

- `match_type != "no_match"`
- `evidence_level >= 2`
- `evidence_text` khong rong

Question generation gioi han 5 cau hoi va co dedupe theo evidence text de tranh lap lai khi Java, Spring Boot va REST API cung chung mot evidence sentence.

### 6. File da thay doi

- `src/review_card_generator.py`
- `tests/test_review_card_generator.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-09-explainable-review-card.md`

### 7. Input / Output can nho

Input:

```python
candidate_result = {
    "candidate_name": "Nguyen Van A",
    "final_score": 87,
    "recommendation": "Strong Review",
    "scores": {...},
    "matched_skills": [...],
    "missing_skills": [],
    "nice_to_have_matches": [...]
}
```

Output chinh:

```python
{
    "candidate_name": "Nguyen Van A",
    "final_score": 87,
    "recommendation": "Strong Review",
    "summary": "Nguyen Van A is a Strong Review candidate...",
    "strengths": [...],
    "concerns": [...],
    "evidence_highlights": [...],
    "suggested_interview_questions": [...]
}
```

Markdown output co cac section:

```text
Summary
Score Breakdown
Strengths
Concerns
Evidence Highlights
Missing Skills
Suggested Interview Questions
```

### 8. Cach test

Chay:

```bash
pytest
```

Test thu cong review card:

```bash
python -c "from src.document_loader import load_text_file; from src.resume_parser import parse_resume; from src.jd_parser import parse_jd; from src.skill_taxonomy import load_taxonomy; from src.skill_normalizer import normalize_skills; from src.semantic_matcher import match_skills; from src.evidence_detector import detect_all_evidence; from src.scorer import score_candidate; from src.review_card_generator import generate_review_card, format_review_card_markdown; taxonomy=load_taxonomy('data/taxonomy/skills.json'); profile=parse_resume(load_text_file('data/cvs/cv_strong.txt')); criteria=parse_jd(load_text_file('data/jobs/jd_backend_java.txt')); candidate=normalize_skills(profile['raw_skills'], taxonomy); required=normalize_skills(criteria['must_have_skills'], taxonomy); nice_skills=normalize_skills(criteria['nice_to_have_skills'], taxonomy); matches=detect_all_evidence(match_skills(required, candidate, taxonomy), profile); nice=match_skills(nice_skills, candidate, taxonomy); result=score_candidate(criteria, profile, matches, nice); card=generate_review_card(result, criteria); print(format_review_card_markdown(card))"
```

### 9. Ket qua mong doi

- `pytest` pass.
- Demo CV/JD tao review card Markdown doc duoc.
- Review card co score 87 va recommendation `Strong Review`.
- Evidence highlights gom cac skill co evidence manh.
- Concerns hien optional nice-to-have gaps nhu AWS va Kafka.
- Suggested questions dua tren evidence va skill gap.

### 10. Loi thuong gap

- Review card tinh lai score va lam lech voi scorer.
- Explanation viet qua manh nhu pass/fail thay vi goi y review.
- Cau hoi phong van bi lap lai vi nhieu skill chung evidence text.
- Hien qua nhieu evidence lam review card dai.
- Bo structured dict va chi tao Markdown se lam UI sau nay kho dung lai.

### 11. Ghi chu cho bao cao

Explainable Review Card bien ket qua scoring thanh dau ra co kha nang giai thich. He thong hien thi diem tong, score breakdown, strengths, concerns, evidence snippets va cau hoi phong van goi y. Cach lam nay giup recruiter hieu ly do xep hang va giu vai tro cua he thong la cong cu ho tro ra quyet dinh, khong phai tu dong tuyen dung hay loai ung vien.

## [2026-06-07] Phase 10 - CLI Pipeline and Output

### 1. Boi canh

Du an dang o Phase 10 - CLI Pipeline and Output. Phase 09 da co review card generator, nhung nguoi dung van phai chay cac lenh `python -c` dai de test tung buoc.

Muc tieu Phase 10 la ket noi cac module da co thanh mot CLI pipeline chay dau-cuoi.

### 2. Van de / chuc nang

Da tao:

- `src/screening_pipeline.py`
- `tests/test_screening_pipeline.py`
- `tests/test_main.py`

Da cap nhat:

- `main.py`

Pipeline ho tro:

- Load JD `.txt`.
- Load nhieu CV `.txt` trong folder.
- Parse JD/CV.
- Normalize skill.
- Match must-have skills.
- Match nice-to-have skills.
- Detect evidence.
- Score candidate.
- Rank candidates.
- Generate review card.
- Print ranking summary.
- Save JSON result.
- Save Markdown review cards.

### 3. Vi sao can lam

Truoc Phase 10, cac module da dung rieng nhung chua thanh ung dung co the demo bang mot lenh ngan.

CLI pipeline giup nguoi dung chay:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Va nhan ranking summary ngay trong terminal.

### 4. Nguyen nhan / logic nen tang

Logic duoc tach thanh hai lop:

- `src/screening_pipeline.py`: orchestration/business flow.
- `main.py`: CLI adapter.

Cach tach nay giup:

- Pipeline test duoc truc tiep.
- Streamlit UI sau nay co the goi lai pipeline.
- `main.py` khong bi phinh to.
- Save file va print terminal khong tron vao logic scoring/matching.

### 5. Cach xu ly

`run_screening_pipeline(jd_path, cv_dir, taxonomy_path)` tra ve:

```python
{
    "job": {
        "title": "Backend Java Developer",
        "must_have_skills": [...],
        "nice_to_have_skills": [...],
        "minimum_experience_years": 1,
        "seniority": "Junior",
        "domain": [...]
    },
    "candidates": [
        {
            "rank": 1,
            "candidate_name": "Nguyen Van A",
            "final_score": 87,
            "recommendation": "Strong Review",
            "review_card": {...}
        }
    ]
}
```

`main.py` nhan cac tham so:

- `--jd`
- `--cv-dir`
- `--taxonomy`
- `--output-json`
- `--output-dir`
- `--show-review-cards`

Output runtime nhu JSON va Markdown reports nam trong `outputs/`, da duoc `.gitignore`, nen khong commit ket qua sinh ra.

### 6. File da thay doi

- `main.py`
- `src/screening_pipeline.py`
- `tests/test_screening_pipeline.py`
- `tests/test_main.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-10-cli-pipeline-output.md`

### 7. Input / Output can nho

Input CLI:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Output terminal:

```text
Semantic Skills-based Resume Screening System
Phase 10 - CLI Pipeline and Output

Job: Backend Java Developer
Candidates analyzed: 1

Ranking:
1. Nguyen Van A - 87/100 - Strong Review
```

Save JSON:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

Save Markdown review card:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-dir outputs/reports
```

### 8. Cach test

Chay:

```bash
pytest
```

Test CLI mac dinh:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Test in review card:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --show-review-cards
```

Test save output:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json --output-dir outputs/reports
```

### 9. Ket qua mong doi

- `pytest` pass.
- CLI in duoc job title.
- CLI in duoc so ung vien da analyze.
- Demo CV co rank 1.
- Demo CV co score 87 va recommendation `Strong Review`.
- JSON output duoc tao neu truyen `--output-json`.
- Markdown review card duoc tao neu truyen `--output-dir`.

### 10. Loi thuong gap

- Chay `python main.py` khong co `--jd` va `--cv-dir` se bi argparse bao thieu tham so.
- Dung sai duong dan JD/CV/taxonomy se co validation error tu loader.
- Thu muc CV khong co file `.txt` thi ranking rong.
- Runtime output trong `outputs/` khong hien trong git vi da ignore.
- Khong nen viet lai scoring/review logic trong `main.py`.

### 11. Ghi chu cho bao cao

CLI Pipeline and Output la buoc tich hop cac thanh phan cua he thong thanh mot flow co the chay thuc te. Tu mot JD va thu muc CV, he thong tu dong parse, normalize, match, detect evidence, score, rank va generate review card. Viec tach pipeline khoi CLI giup he thong de test va san sang mo rong sang giao dien Streamlit.
