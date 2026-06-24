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

## [2026-06-07] Phase 11 - Python API Service for Web Integration

### 1. Boi canh

Du an dang o Phase 11 - Python API Service. Phase 10 da co CLI pipeline chay duoc, nhung web PHP muon tich hop sach hon thi nen goi AI bang HTTP JSON thay vi shell command va file tam.

Muc tieu phase nay la them FastAPI service ma khong pha CLI hien tai.

### 2. Van de / chuc nang

Da tao:

- `api.py`
- `src/api_models.py`
- `src/payload_pipeline.py`
- `tests/test_api.py`
- `tests/test_payload_pipeline.py`
- `docs/integration/sample-screening-request.json`

Da cap nhat:

- `requirements.txt`
- `README.md`

API ho tro:

- `GET /health`
- `POST /screening`

### 3. Vi sao can lam

Web PHP TOPCV Lite co the goi AI bang CLI, nhung API service phu hop hon cho tich hop dai han:

```text
PHP web
  -> POST JSON /screening
  -> Python API
  -> payload pipeline
  -> scorer/review card
  -> ranking JSON
```

Cach nay giup web khong phai tao qua nhieu file tam va de debug bang Postman/cURL.

### 4. Nguyen nhan / logic nen tang

Phase 11 tach thanh cac lop:

- `api.py`: HTTP adapter.
- `src/api_models.py`: Pydantic request models.
- `src/payload_pipeline.py`: chuyen JSON payload thanh screening result.
- Cac module cu: parser, matcher, evidence, scorer, review card.

CLI van dung:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

API dung:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

### 5. Cach xu ly

`build_jd_text_from_payload(job)` chuyen job JSON thanh JD text parser-friendly.

`build_cv_document_from_payload(candidate)` chuyen candidate JSON thanh document dict giong loader output.

`run_screening_payload(payload)` xu ly:

1. Build JD text.
2. Parse JD.
3. Build CV document tu tung candidate.
4. Parse resume.
5. Normalize skills.
6. Match skills.
7. Detect evidence.
8. Score candidate.
9. Rank candidates.
10. Generate review cards.

Response giu lai:

- `application_id`
- `candidate_id`
- `email`
- `phone`
- `applied_at`
- `cv_file_path`
- `source_file`

De PHP co the map ket qua ve application trong database.

### 6. File da thay doi

- `api.py`
- `requirements.txt`
- `src/api_models.py`
- `src/payload_pipeline.py`
- `tests/test_api.py`
- `tests/test_payload_pipeline.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-11-python-api-service.md`
- `docs/integration/sample-screening-request.json`

### 7. Input / Output can nho

Input API:

```json
{
  "job": {
    "job_id": 10,
    "job_title": "Backend Java Developer",
    "requirements": ["Java", "Spring Boot"],
    "nice_to_have": ["AWS"]
  },
  "candidates": [
    {
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "cv_text": "Nguyen Van A\nBackend Developer\n..."
    }
  ]
}
```

Output API:

```json
{
  "job": {
    "job_id": 10,
    "title": "Backend Java Developer"
  },
  "candidates": [
    {
      "rank": 1,
      "application_id": 123,
      "candidate_id": 456,
      "candidate_name": "Nguyen Van A",
      "final_score": 87,
      "recommendation": "Strong Review",
      "review_card": {}
    }
  ]
}
```

### 8. Cach test

Chay:

```bash
pytest
```

Chay API:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Screening request:

```bash
curl -X POST http://127.0.0.1:8000/screening -H "Content-Type: application/json" -d @docs/integration/sample-screening-request.json
```

CLI regression:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

### 9. Ket qua mong doi

- `pytest` pass.
- `/health` tra `status = ok`.
- `/screening` tra candidate `Nguyen Van A`.
- Demo payload tra final score 87.
- Demo payload tra recommendation `Strong Review`.
- Response co `application_id` va `candidate_id`.
- CLI Phase 10 van chay binh thuong.

### 10. Loi thuong gap

- Quen cai `fastapi` trong `.venv`.
- Quen chay `uvicorn` truoc khi PHP goi API.
- Candidate payload khong co `cv_text` hoac structured CV data se bi HTTP 400.
- Payload job khong co `job_title`, `raw_text`, hoac `description` se bi HTTP 400.
- Response khong co `application_id` thi PHP kho luu dung application.

### 11. Ghi chu cho bao cao

Python API Service la lop tich hop giua AI screening engine va web application. Service nhan JD/CV theo JSON, dung lai pipeline san co de xep hang ung vien va tra ve review card co giai thich. Thiet ke nay giu CLI on dinh dong thoi mo duong cho web PHP goi AI theo HTTP API chuyen nghiep hon.

## [2026-06-07] Phase 12 - Vietnamese-English Parser, Taxonomy, and Evidence Foundation

### 1. Boi canh

Sau Phase 11, API da goi duoc tu web PHP. Khi test `JD_1.txt` voi 3 CV tieng Viet `CV_30.txt`, `CV_70.txt`, `CV_85.txt`, ca 3 ung vien deu ve 35/100.

Nguyen nhan chinh khong phai do thieu GPT hay multilingual embedding, ma do cac tang nen chua doc duoc input:

- JD co heading `Requirements` khong dau hai cham.
- CV tieng Viet co heading nhu `KY NANG`, `KINH NGHIEM LAM VIEC`, `DU AN`.
- Taxonomy chua co AI, Computer Vision, eKYC.
- Evidence detector chua nhan dong tu tieng Viet.
- Mot so file text local bi mojibake do UTF-8 bi doc/saved sai encoding.

### 2. Van de / chuc nang

Da tao:

- `src/text_normalization.py`
- `src/section_parser.py`
- `src/skill_extractor.py`
- `tests/test_skill_extractor.py`

Da cap nhat:

- `src/jd_parser.py`
- `src/resume_parser.py`
- `src/evidence_detector.py`
- `src/scorer.py`
- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `src/skill_taxonomy.py`
- `data/taxonomy/skills.json`
- Tests parser, taxonomy, normalizer, evidence, payload, CLI/pipeline.
- `README.md`
- `docs/phases/phase-12-vietnamese-english-multilingual-support.md`

### 3. Vi sao can lam

Neu nhay thang vao multilingual embedding, model co the hieu ngu nghia Viet-Anh nhung pipeline van co the nhan input rong hoac sai.

Phase 12 sua cac tang dau vao truoc:

```text
Raw JD/CV
  -> repair encoding neu can
  -> bilingual section parser
  -> taxonomy aliases Viet-Anh
  -> full-text skill extraction fallback
  -> Vietnamese evidence detection
  -> scoring/ranking hien tai
```

### 4. Nguyen nhan / logic nen tang

`src/text_normalization.py` gom cac helper:

- repair mojibake UTF-8/Windows-1252 pho bien.
- strip Vietnamese accents.
- normalize lookup/search text.
- strip bullet/list marker.

`src/section_parser.py` tach section dua tren aliases da normalize, ho tro:

- heading co dau hai cham: `Requirements:`
- heading khong dau hai cham: `Requirements`
- heading Viet co dau/khong dau: `Kỹ năng`, `Ky nang`

`src/skill_extractor.py` scan raw text bang taxonomy:

- canonical skill.
- aliases tieng Anh.
- aliases tieng Viet co dau.
- aliases tieng Viet khong dau.

### 5. Cach xu ly

JD/CV parser van giu schema output cu.

CLI/API pipeline duoc bo sung:

1. Parse JD/CV nhu truoc.
2. Normalize skill tu section neu parser lay duoc.
3. Extract them taxonomy skills tu raw text.
4. Merge va dedupe skills.
5. Match/evidence/score nhu cu.

Evidence detector co them optional `taxonomy`, de khi required skill la `Face Recognition`, he thong van tim duoc cau co alias `nhan dien khuon mat`.

### 6. File da thay doi

- `README.md`
- `data/taxonomy/skills.json`
- `docs/dev-learning-log.md`
- `docs/phases/phase-12-vietnamese-english-multilingual-support.md`
- `src/evidence_detector.py`
- `src/jd_parser.py`
- `src/payload_pipeline.py`
- `src/resume_parser.py`
- `src/scorer.py`
- `src/screening_pipeline.py`
- `src/section_parser.py`
- `src/skill_extractor.py`
- `src/skill_taxonomy.py`
- `src/text_normalization.py`
- `tests/test_evidence_detector.py`
- `tests/test_jd_parser.py`
- `tests/test_main.py`
- `tests/test_payload_pipeline.py`
- `tests/test_resume_parser.py`
- `tests/test_screening_pipeline.py`
- `tests/test_skill_extractor.py`
- `tests/test_skill_normalizer.py`
- `tests/test_skill_taxonomy.py`

### 7. Input / Output can nho

Input web/API khong doi. Web van gui:

```json
{
  "job": {
    "raw_text": "Computer Vision Engineer\n\nRequirements\n..."
  },
  "candidates": [
    {
      "candidate_name": "Le Van A",
      "cv_text": "Le Van A\nAI Engineer\n\nKy nang\nPython..."
    }
  ]
}
```

Output API khong doi, nhung skill/evidence/ranking tot hon:

- `must_have_skills` co canonical English skill.
- `matched_skills` co evidence tieng Viet neu tim duoc.
- `review_card` giai thich bang evidence text.

### 8. Cach test

Chay full test:

```bash
pytest
```

Test CLI:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Test API sample:

```bash
uvicorn api:app --host 127.0.0.1 --port 8000
curl -X POST http://127.0.0.1:8000/screening -H "Content-Type: application/json" -d @docs/integration/sample-screening-request.json
```

Benchmark local voi `JD_1/CV_30/CV_70/CV_85`:

```text
CV_85: 89/100 - Strong Review
CV_70: 66/100 - Maybe Review
CV_30: 26/100 - Not Enough Evidence
```

### 9. Ket qua mong doi

- Parser doc duoc heading Anh/Viet.
- Taxonomy map duoc aliases Viet-Anh ve canonical English skill.
- Evidence detector nhan cau tieng Viet co action verb.
- CV dung domain AI/CV/eKYC duoc xep tren CV frontend.
- API/CLI khong doi schema/command.

### 10. Loi thuong gap

- File CV/JD export sai encoding co the hien mojibake. Phase 12 co repair mot so case pho bien, nhung khong thay the buoc extract text dung encoding.
- Taxonomy fallback uu tien precision, nen skill qua chung co the khong duoc bat neu chua co alias ro.
- Required skill tu JD dang la cau dai se duoc convert sang taxonomy skill neu co alias; neu taxonomy chua co skill do thi co the bi bo qua.
- Day chua phai multilingual embedding, nen cac cau Viet-Anh dong nghia nhung khong co alias van co the chua match.

### 11. Ghi chu cho bao cao

Phase 12 la buoc lam sach va chuan hoa dau vao cho bai toan song ngu. He thong van explainable vi skill duoc dua ve taxonomy canonical va evidence lay tu cau that trong CV. Day la nen tang de Phase 13 them local multilingual embedding ma khong lam mat kha nang giai thich.

## [2026-06-08] Phase 13 - Local Multilingual Embedding

### 1. Boi canh

Phase 12 da lam tot bilingual parser, taxonomy, full-text skill extraction va evidence tieng Viet. Tuy nhien, neu JD/CV dung cach dien dat khac nhau va taxonomy chua co alias, rule-based matcher van co the bo sot.

Muc tieu Phase 13 la them local multilingual embedding nhu mot semantic fallback, nhung khong thay the rule-based/taxonomy/evidence backbone.

### 2. Van de / chuc nang

Da cap nhat:

- `src/embedding_matcher.py`
- `src/semantic_matcher.py` thong qua optional `embedding_matcher` da co.
- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `main.py`
- `api.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-13-local-multilingual-embedding.md`
- Tests lien quan embedding, semantic matcher, payload pipeline, CLI.

Them ho tro:

- Default recommended local multilingual model: `BAAI/bge-m3`.
- Alternative E5 model formatting: `intfloat/multilingual-e5-large-instruct`.
- Query instruction cho E5 instruct.
- In-memory embedding cache trong mot matcher instance.
- `--enable-embedding`, `--embedding-model`, `--embedding-threshold`, `--embedding-local-only` cho CLI.
- API env vars:
  - `SEMANTIC_EMBEDDING_ENABLED`
  - `SEMANTIC_EMBEDDING_MODEL`
  - `SEMANTIC_EMBEDDING_THRESHOLD`
  - `SEMANTIC_EMBEDDING_LOCAL_ONLY`

### 3. Vi sao can lam

Embedding giup so sanh ngu nghia khi keyword/taxonomy chua du.

Vi du:

```text
JD: identity verification
CV: digital identity verification
```

Neu taxonomy chua co quan he truc tiep, embedding co the sinh `semantic_match` neu cosine similarity vuot threshold.

### 4. Nguyen nhan / logic nen tang

`SemanticEmbeddingMatcher` van lazy-load model:

- Neu model co san: encode text va tinh cosine similarity.
- Neu model khong co: tra `None`, pipeline fallback ve rule-based.

Rule priority van giu:

```text
exact_match
related_match
transferable_match
semantic_match
no_match
```

Nghia la embedding khong duoc chen len tren exact/related/transferable match.

### 5. Cach xu ly

CLI mac dinh khong auto load model de tranh tai model nang khi nguoi dung chi chay test:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Neu muon bat local multilingual embedding:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

API mac dinh cung khong bat embedding. Muon bat:

```powershell
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_THRESHOLD='0.72'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'
uvicorn api:app --host 127.0.0.1 --port 8000
```

### 6. File da thay doi

- `api.py`
- `main.py`
- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-13-local-multilingual-embedding.md`
- `src/embedding_matcher.py`
- `src/payload_pipeline.py`
- `src/screening_pipeline.py`
- `tests/test_embedding_matcher.py`
- `tests/test_main.py`
- `tests/test_payload_pipeline.py`
- `tests/test_semantic_matcher.py`

### 7. Input / Output can nho

Neu semantic match duoc kich hoat, match output co dang:

```json
{
  "required_skill": "identity verification",
  "candidate_skill": "digital identity verification",
  "match_type": "semantic_match",
  "score": 0.85,
  "similarity": 0.9991
}
```

API response schema khong doi. Web van doc `matched_skills`, `final_score`, `recommendation`, `review_card` nhu truoc.

### 8. Cach test

Chay:

```bash
pytest
```

Test fallback khong can model:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_loader=lambda name: (_ for _ in ()).throw(RuntimeError('model unavailable'))); print(matcher.similarity('face recognition', 'nhan dien khuon mat')); print(matcher.unavailable_reason)"
```

Test real model neu da tai duoc:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_name='BAAI/bge-m3', local_files_only=True); print(round(matcher.similarity('face recognition', 'nhận diện khuôn mặt') or 0, 4)); print(matcher.unavailable_reason)"
```

### 9. Ket qua mong doi

- Tests khong download model that.
- CLI/API van chay khi embedding disabled.
- CLI/API khong crash khi model unavailable.
- Khi co fake model, semantic match duoc tao dung threshold.
- Rule-based exact/related/transferable van uu tien hon semantic.

### 10. Loi thuong gap

- Lan dau dung `BAAI/bge-m3` co the tai model lau.
- May CPU co the chay cham voi model lon.
- Neu offline hoac model chua cached, `unavailable_reason` co gia tri va pipeline fallback ve rule-based.
- Neu model da cached, dung `--embedding-local-only` tren CLI hoac `SEMANTIC_EMBEDDING_LOCAL_ONLY=1` tren API de demo on dinh hon.
- E5 instruct can query instruction; helper da format query side cho model co `e5` trong ten.

### 11. Ghi chu cho bao cao

Phase 13 them pretrained local multilingual embedding vao he thong. He thong bieu dien requirement va candidate skill/evidence thanh vector, sau do dung cosine similarity de tim semantic match. Cach nay giup xu ly JD/CV khac ngon ngu hoac khac cach dien dat, nhung van giu tinh minh bach nho taxonomy, evidence text, match type va similarity score.

---

## Phase 14 - Open-set Requirement Matching

### 1. Muc tieu

Phase 14 xu ly requirement/skill trong JD chua nam trong taxonomy.

Thiet ke chinh:

```text
Known taxonomy requirement
  -> rule-based + evidence

Unknown requirement
  -> report trong taxonomy_coverage
  -> neu embedding bat thi tim semantic evidence trong CV
  -> gan nhan semantic_only_match / unknown taxonomy
```

### 2. Van de giai quyet

Taxonomy khong the bao phu moi nganh nghe ngay tu dau. Neu JD co skill la nhu:

```text
carbon footprint analysis
drone mission planning
robot navigation with SLAM
```

He thong cu co the bo qua hoac ep vao skill list sai. Phase 14 giu nguyen requirement goc va danh dau ro no nam ngoai taxonomy.

### 3. Cach xu ly

Them module:

```text
src/open_set_matcher.py
```

Module nay lam:

- Tach known/unknown requirements.
- Tinh `taxonomy_coverage`.
- Lay evidence candidates tu CV.
- Dung `SemanticEmbeddingMatcher.similarity_matrix` de so sanh unknown requirement voi evidence text.
- Tao `semantic_only_match` khi similarity dat threshold.
- Tao `no_semantic_evidence` khi embedding co san nhung khong tim duoc evidence du threshold.

### 4. Output moi

Job output co:

```json
{
  "taxonomy_coverage": {
    "known_count": 2,
    "unknown_count": 1,
    "coverage_ratio": 0.6667,
    "known_requirements": ["Python", "SQL"],
    "unknown_requirements": ["carbon footprint analysis"]
  }
}
```

Candidate match co the co:

```json
{
  "required_skill": "carbon footprint analysis",
  "candidate_skill": null,
  "match_type": "semantic_only_match",
  "taxonomy_status": "unknown",
  "score": 0.65,
  "similarity": 0.8421,
  "evidence_level": 3,
  "evidence_text": "Built carbon emission reports for ESG audits.",
  "evidence_source": "projects"
}
```

### 5. Diem can nho

- Unknown requirement khong duoc them vao taxonomy tu dong.
- `semantic_only_match` khong duoc xem nhu exact taxonomy match.
- Score cua semantic-only bi gioi han o `0.65`.
- Neu embedding disabled hoac unavailable, unknown requirements van nam trong coverage nhung khong crash pipeline.
- Review card them concern de recruiter biet co requirement duoc danh gia ngoai taxonomy.

### 6. File da thay doi

- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-14-open-set-requirement-matching.md`
- `docs/refactoring/phase-14-refactoring-plan.md`
- `main.py`
- `src/evidence_detector.py`
- `src/open_set_matcher.py`
- `src/payload_pipeline.py`
- `src/review_card_generator.py`
- `src/scorer.py`
- `src/screening_pipeline.py`
- `tests/test_open_set_matcher.py`
- `tests/test_payload_pipeline.py`
- `tests/test_review_card_generator.py`
- `tests/test_screening_pipeline.py`

### 7. Cach test

Chay:

```bash
pytest
```

Test nhom open-set:

```bash
pytest tests/test_open_set_matcher.py tests/test_payload_pipeline.py tests/test_review_card_generator.py
```

Manual CLI voi embedding local:

```powershell
$env:HF_HUB_OFFLINE='1'
python main.py --jd data/jobs/JD_1.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

### 8. Ghi chu cho bao cao

Co the trinh bay:

```text
Taxonomy khong the bao phu toan bo nganh nghe ngay tu dau, nen he thong duoc thiet ke theo huong open-set. Voi skill da co trong taxonomy, he thong dung rule-based matching va evidence de danh gia chinh xac, giai thich duoc. Voi requirement chua co trong taxonomy, he thong giu nguyen text goc va dung multilingual embedding de tim bang chung gan nghia trong CV. Ket qua nay duoc danh dau la semantic-only/unknown-taxonomy de tranh nham voi skill da chuan hoa.
```

Phase 15 se lam human-in-the-loop taxonomy suggestion cho Admin duyet skill moi.

---

## Phase 15 - Human-in-the-loop Taxonomy Suggestion Queue

### 1. Muc tieu

Phase 15 tao queue de xuat taxonomy tu cac unknown requirements da duoc Phase 14 phat hien.

Thiet ke:

```text
AI proposes
Admin approves
```

Python project chi tao suggestion JSON. He thong khong tu dong sua `data/taxonomy/skills.json`.

### 2. Van de giai quyet

Taxonomy khong the bao phu moi nganh ngay tu dau. Sau Phase 14, he thong da biet requirement nao nam ngoai taxonomy. Phase 15 bien cac requirement la lap lai thanh pending suggestions de Admin co the xem xet.

### 3. Cach xu ly

Them:

- `src/taxonomy_suggestion.py`
- `taxonomy_suggest.py`
- `tests/test_taxonomy_suggestion.py`
- `docs/refactoring/phase-15-refactoring-plan.md`

Module suggestion lam:

- Collect unknown requirement observations tu `job.taxonomy_coverage`.
- Merge evidence tu `candidate.open_set_requirement_matches`.
- Group exact phrase va optional embedding-similar phrase.
- Build pending suggestion co canonical name, aliases, frequency, confidence, nearest skills, examples.
- Save/load versioned JSON queue.

### 4. CLI moi

Lenh:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Demo nho co the dung:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json --min-frequency 1
```

### 5. Output moi

```json
{
  "version": 1,
  "suggestions": [
    {
      "suggestion_id": "tax-sug-carbon-footprint-analysis",
      "suggested_canonical_name": "Carbon Footprint Analysis",
      "suggested_category": "Pending Classification",
      "suggested_aliases": ["carbon footprint analysis"],
      "frequency": 2,
      "confidence": 0.7,
      "nearest_existing_skills": [],
      "example_contexts": ["carbon footprint analysis"],
      "example_evidence": [],
      "status": "pending_review"
    }
  ]
}
```

### 6. File da thay doi

- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-15-taxonomy-suggestion-queue.md`
- `docs/refactoring/phase-15-refactoring-plan.md`
- `main.py`
- `taxonomy_suggest.py`
- `src/taxonomy_suggestion.py`
- `tests/test_taxonomy_suggestion.py`

### 7. Cach test

Chay:

```bash
pytest
```

Test rieng:

```bash
pytest tests/test_taxonomy_suggestion.py
```

### 8. Ghi chu cho bao cao

Co the noi:

```text
He thong khong tu dong mo rong taxonomy. Khi gap requirement la nhieu lan, AI chi tao de xuat gom canonical name, aliases, tan suat va vi du evidence. Admin phai duyet truoc khi skill moi duoc them vao taxonomy, giup dam bao chat luong va tranh sai lech.
```

---

## Phase 16 - Admin Taxonomy Review and Merged Runtime Taxonomy

### 1. Muc tieu

Phase 16 them tang merge/validate taxonomy de cac skill da duoc Admin duyet co the duoc dua vao AI screening ma khong sua taxonomy goc.

Thiet ke:

```text
Base taxonomy
  + Admin-approved custom overlay
  = one merged runtime taxonomy
```

### 2. Van de giai quyet

Phase 15 da tao duoc pending suggestions, nhung web/Admin can mot cach an toan de dua cac decision da duyet quay lai vao he thong. Neu sua truc tiep `data/taxonomy/skills.json` thi kho audit va de loi khi update source code.

Phase 16 giai quyet bang cach tao file runtime rieng:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

AI CLI/API chi can doc file merged nay.

### 3. Cach xu ly

Them:

- `src/taxonomy_merge.py`
- `taxonomy_merge.py`
- `tests/test_taxonomy_merge.py`
- `docs/integration/sample-custom-taxonomy-overlay.json`
- `docs/refactoring/phase-16-refactoring-plan.md`

Module merge lam:

- Validate custom overlay JSON.
- Add custom skills.
- Add aliases vao existing base/custom skill.
- Dedupe aliases.
- Reject ambiguous aliases.
- Atomic write merged taxonomy.

### 4. CLI moi

Lenh:

```powershell
python taxonomy_merge.py --base data/taxonomy/skills.json --custom docs/integration/sample-custom-taxonomy-overlay.json --output outputs/skills_merged.json
```

### 5. Cach AI dung taxonomy merged

CLI:

```powershell
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --taxonomy outputs/skills_merged.json
```

API:

```json
{
  "taxonomy_path": "C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json"
}
```

### 6. File da thay doi

- `README.md`
- `docs/dev-learning-log.md`
- `docs/phases/phase-16-admin-taxonomy-review-merged-taxonomy.md`
- `docs/refactoring/phase-16-refactoring-plan.md`
- `docs/integration/cursor-prompt-topcv-lite-admin-taxonomy-suggestions.md`
- `docs/integration/sample-custom-taxonomy-overlay.json`
- `taxonomy_merge.py`
- `src/taxonomy_merge.py`
- `tests/test_taxonomy_merge.py`

### 7. Cach test

Chay:

```bash
pytest
```

Test rieng:

```bash
pytest tests/test_taxonomy_merge.py
```

Manual check:

```bash
python taxonomy_merge.py --base data/taxonomy/skills.json --custom docs/integration/sample-custom-taxonomy-overlay.json --output outputs/skills_merged.json
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --taxonomy outputs/skills_merged.json
```

### 8. Ghi chu cho bao cao

Co the noi:

```text
He thong khong de AI tu dong sua taxonomy. Thay vao do, cac skill moi duoc Admin duyet se duoc luu thanh custom taxonomy overlay. He thong merge overlay nay voi taxonomy goc de tao mot runtime taxonomy duy nhat cho cac lan sang loc tiep theo. Cach thiet ke nay giup dam bao kha nang giai thich, kiem soat chat luong va truy vet thay doi.
```

---

## Phase 17 - Taxonomy-independent Open-set Screening Core

### 1. Muc tieu

Phase 17 giai quyet van de he thong cham diem thap khi JD/CV thuoc nganh chua co trong taxonomy.

Nguyen tac moi:

```text
Taxonomy la lop chuan hoa/giai thich.
Open-set semantic matching la lop giup he thong xu ly skill/nganh moi.
```

### 2. Van de giai quyet

Case JD_2 IT Security/GRC cho thay:

- JD title bi trong.
- Domain bi match sai do substring `edge` trong `knowledge`.
- CV phu hop nhung diem thap vi taxonomy chua co IT Security/GRC.
- Neu chi them taxonomy cho JD_2 thi se thanh va tung case.

Phase 17 khong them taxonomy de fix rieng JD_2. Thay vao do, he thong tach requirement ngoai taxonomy va match bang embedding.

### 3. Cach xu ly

Them:

- `src/requirement_extractor.py`
- `tests/test_requirement_extractor.py`
- `docs/refactoring/phase-17-refactoring-plan.md`

Cap nhat:

- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `src/open_set_matcher.py`
- `src/evidence_detector.py`
- `src/jd_parser.py`
- `src/scorer.py`

### 4. Output moi

Job output co them:

```json
{
  "open_set_requirements": [],
  "screening_confidence": {
    "level": "high",
    "known_requirement_count": 0,
    "open_set_requirement_count": 0,
    "embedding_enabled": false,
    "warnings": []
  }
}
```

Neu embedding tat nhung JD co open-set requirements:

```json
{
  "level": "low",
  "warnings": [
    "Open-set requirements detected but embedding matcher is disabled."
  ]
}
```

### 5. Manual benchmark

Voi JD_2 va CV_1/CV_3:

Khong embedding:

```text
David Chen - 36/100 - Not Enough Evidence
Kevin Walker - 32/100 - Not Enough Evidence
```

Co BGE-M3:

```text
David Chen - 72/100 - Review
Kevin Walker - 36/100 - Not Enough Evidence
```

Dieu nay cho thay Phase 17 khong can them IT Security taxonomy rieng van co the cai thien ranking khi embedding duoc bat.

### 6. Cach test

Chay:

```bash
pytest
```

Ket qua Phase 17:

```text
143 passed
```

### 7. Ghi chu cho bao cao

Co the noi:

```text
He thong ket hop taxonomy-based matching va open-set semantic matching. Voi skill da co trong taxonomy, he thong dung rule-based matching de dam bao giai thich ro rang. Voi requirement chua co trong taxonomy, he thong khong bo qua ma tach thanh capability units va dung multilingual embedding de tim bang chung gan nghia trong CV. Ket qua nay duoc danh dau la semantic-only de recruiter biet can verify. Cach tiep can nay giup he thong van hoat dong voi nganh nghe moi ma khong can them taxonomy thu cong cho tung case.
```

---

## Phase 18 - JD Requirement Classification and Weighted Scoring Refinement

### 1. Muc tieu

Phase 18 giai quyet van de JD dai lam diem bi keo thap vi he thong tinh moi dong requirement nhu must-have skill.

Case thuc te:

```text
JD_3 Fullstack Developer
CV_3_3 phu hop hon CV_3_1, ranking dung,
nhung diem CV_3_3 chi 55/100 vi soft skill, education va nice-to-have bi tinh nhu missing must-have.
```

### 2. Cach xu ly

Them:

- `src/jd_requirement_classifier.py`
- `tests/test_jd_requirement_classifier.py`
- `docs/phases/phase-18-jd-requirement-classification-weighted-scoring.md`

Cap nhat:

- `src/jd_parser.py` nhan heading `Dieu kien bat buoc` va `Dieu kien uu tien`.
- `src/screening_pipeline.py` va `src/payload_pipeline.py` dung classifier truoc scoring.
- `src/requirement_extractor.py` strip cac tien to ky thuat tieng Viet nhu `Thanh thao`, `Co kien thuc ve`, `co so du lieu`.
- `src/review_card_generator.py` them requirement notes cho education, soft skills va domain context.

### 3. Output moi

Job output co them:

```json
{
  "requirement_groups": {
    "must_have_technical": [],
    "nice_to_have_technical": [],
    "soft_skills": [],
    "education": [],
    "experience": [],
    "certifications": [],
    "domain_context": [],
    "responsibilities": [],
    "ignored": []
  }
}
```

Candidate output co them:

```json
{
  "requirement_group_summary": {
    "must_have_matched": 0,
    "must_have_total": 0,
    "nice_to_have_matched": 0,
    "nice_to_have_total": 0
  }
}
```

Review card co them `Requirement Notes` de recruiter biet:

- Education nen review rieng.
- Soft skills nen verify khi phong van.
- Domain context nen dung de tham khao.

### 4. Manual benchmark

Voi `JD_3.txt`, `CV_3_1.txt`, `CV_3_3.txt` va BGE-M3:

Truoc Phase 18:

```text
Le Quoc Bao - 55/100 - Maybe Review
Nguyen Van Hung - 46/100 - Low Priority
```

Sau Phase 18:

```text
Le Quoc Bao - 76/100 - Review
Nguyen Van Hung - 51/100 - Low Priority
```

Ket qua nay hop ly hon:

- Ranking van giu dung.
- CV phu hop hon khong bi phat nang vi soft skills/hoc van/nice-to-have.
- Missing skills cua CV_3_3 chi con cac technical gaps nhu `OOP`, `FrontEnd va BackEnd API`.

### 5. Ghi chu cho bao cao

Co the noi:

```text
He thong khong so khop JD theo kieu keyword phang. Truoc khi scoring, moi dong JD duoc phan loai thanh ky nang chuyen mon bat buoc, ky nang uu tien, ky nang mem, hoc van, kinh nghiem, chung chi va ngu canh nganh nghe. Diem phu hop duoc tinh chu yeu tren ky nang chuyen mon bat buoc va bang chung trong CV; cac yeu cau uu tien chi dong vai tro cong diem, con ky nang mem/hoc van duoc dung de ho tro review va phong van. Cach nay giup ket qua xep hang cong bang hon va giai thich duoc hon.
```

---

## Phase 19 - Hard-skill Gate and Evidence Calibration

### 1. Muc tieu

Phase 19 xu ly van de ung vien co nhieu nam kinh nghiem/domain phu hop nhung thieu
bang chung cho hard skills bat buoc van co the vuot nguong `Review`.

Muc tieu:

- Giu weighted score hien tai de xep hang tong the.
- Them hard-skill gate sau scoring de dam bao dieu kien toi thieu.
- Khong de experience/seniority/domain che mat thieu sot hard skills.
- Review card phai noi ro khi score bi cap.

### 2. Cach xu ly

Them vao `src/scorer.py`:

- `base_score`: diem weighted score truoc gate.
- `hard_skill_gate`: metadata gom status, score cap, reasons va metrics.
- `calculate_hard_skill_gate_metrics()`.
- `evaluate_hard_skill_gate()`.
- `apply_hard_skill_gate()`.

Rule chinh:

```text
Neu base_score >= 70 va hard-skill evidence yeu:
    cap final_score toi da 69

Neu base_score >= 85 nhung confirmed coverage chua du manh:
    cap final_score toi da 84
```

Nguong Review:

```text
skill_semantic >= 0.55
evidence >= 0.50
confirmed hard-skill coverage >= 0.60
```

Confirmed match la match co `score > 0` va `evidence_level >= 2`.

### 3. Output moi

Candidate output co them:

```json
{
  "base_score": 72,
  "final_score": 69,
  "recommendation": "Maybe Review",
  "hard_skill_gate": {
    "passed": false,
    "applied": true,
    "score_cap": 69,
    "reasons": [],
    "metrics": {
      "total_must_have": 16,
      "confirmed_coverage": 0.3125
    }
  }
}
```

### 4. Review card

Neu gate duoc apply, summary va concerns se noi ro:

```text
The hard-skill gate capped the base score because must-have skill evidence is incomplete.
```

Dieu nay giup recruiter thay duoc ung vien co the du kinh nghiem, nhung van can xem
lai hard skills truoc khi shortlist.

### 5. Ghi chu cho bao cao

Co the noi:

```text
Diem cua he thong gom hai lop. Lop thu nhat la weighted score de tong hop cac tin hieu nhu skill, evidence, kinh nghiem, seniority va domain. Lop thu hai la hard-skill gate, dong vai tro dieu kien toi thieu cho cac ky nang chuyen mon bat buoc. Neu ung vien co nhieu nam kinh nghiem nhung bang chung hard skills khong du, he thong se cap diem va recommendation xuong Maybe Review. Cach nay phu hop voi nguyen tac tuyen dung dua tren person-job fit va KSAO: kinh nghiem la tin hieu ho tro, con ky nang bat buoc va bang chung thuc hien moi la dieu kien chinh de shortlist.

---

## Phase 20 - Candidate-side Job Recommendation Payload and API

### 1. Muc tieu

Phase 20 mo rong AI core hien co sang bai toan nguoc lai:

```text
1 CV -> tim Top matching JDs
```

Muc tieu cua phase nay la:

- giu nguyen employer-side screening flow;
- them candidate-side payload/API rieng;
- tai su dung screening core hien co thay vi viet mot AI moi;
- tra ve danh sach top jobs co giai thich co ban.

### 2. Cach xu ly

Them:

- `src/job_recommendation_pipeline.py`
- `docs/integration/sample-recommend-jobs-request.json`
- `tests/test_job_recommendation_pipeline.py`

Cap nhat:

- `api.py`
- `src/api_models.py`
- `src/payload_pipeline.py`
- `tests/test_api.py`
- `tests/test_payload_pipeline.py`
- `README.md`

### 3. Thiet ke thuc te

Employer flow hien tai van giu nguyen:

```text
POST /screening
1 JD -> rank many CVs
```

Candidate flow moi:

```text
POST /recommend-jobs
1 CV -> score many JDs -> sort -> top_k
```

Phase 20 chua lam retrieval index. Candidate-side flow nhan:

- `candidate`
- `jobs`
- `options.top_k`

roi chay AI core cho tung job trong request.

Huong nay duoc chon vi:

- regression risk thap;
- khong pha web employer da tich hop;
- de test, de giai thich;
- toi uu retrieval/index de Phase 21 xu ly sau.

### 4. Payload moi

Request:

```json
{
  "candidate": {
    "candidate_id": 456,
    "resume_text": "..."
  },
  "jobs": [
    {
      "job_id": 10,
      "title": "Backend Java Developer",
      "job_description_text": "..."
    }
  ],
  "options": {
    "top_k": 10
  }
}
```

Phase 20 cung bo sung alias de web goi linh hoat hon:

- `resume_text` ben canh `cv_text`
- `title` ben canh `job_title`
- `job_description_text` ben canh `raw_text`

### 5. Output moi

Response candidate-side co dang:

```json
{
  "candidate": {},
  "top_jobs": [
    {
      "rank": 1,
      "job_id": 10,
      "job_title": "Backend Java Developer",
      "fit_score": 86,
      "base_score": 86,
      "recommendation": "Strong Review",
      "matched_must_have_skills": [],
      "missing_must_have_skills": [],
      "optional_strengths": [],
      "why_fit": [],
      "what_to_improve": [],
      "review_card": {}
    }
  ],
  "retrieval_stats": {}
}
```

Y nghia:

- `fit_score`: diem sau gate.
- `base_score`: diem truoc gate.
- `why_fit`: vi sao job nay hop.
- `what_to_improve`: nen bo sung gi vao CV de tang fit.

### 6. Logics dung lai

Phase 20 khong viet lai parser/scorer. He thong tai su dung:

- parse CV/JD
- taxonomy + normalization
- rule-based va semantic matching
- evidence detection
- weighted scoring
- hard-skill gate
- review card

Noi ngan gon:

```text
Candidate-side recommendation
= screening core dao chieu query
```

### 7. Cach test

Targeted regression:

```bash
python -m pytest tests/test_payload_pipeline.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

Manual API:

```bash
curl -X POST http://127.0.0.1:8000/recommend-jobs -H "Content-Type: application/json" -d @docs/integration/sample-recommend-jobs-request.json
```

### 8. Ket qua mong doi

- `/screening` van giu nguyen contract cu.
- `/recommend-jobs` nhan 1 CV + nhieu JDs.
- Ket qua tra ve top jobs da sap xep.
- Output co matched/missing skills va goi y cai thien CV.
- Alias payload moi khong pha backward compatibility.

### 9. Ghi chu cho bao cao

Co the noi:

```text
Sau employer-side screening, he thong duoc mo rong sang candidate-side job recommendation ma khong can xay dung mot AI tach biet. He thong tai su dung person-job fit core da co, sau do dong goi thanh mot API moi nhan 1 CV va danh sach JD, cham diem tung job, xep hang va tra ve Top cong viec phu hop kem giai thich. Cach lam nay giu tinh nhat quan giua hai chieu employer-side va candidate-side, dong thoi de mo rong them retrieval index va ca nhan hoa o cac phase tiep theo.
```

---

## Phase 21 - Job Retrieval Index for Active JDs

### 1. Muc tieu

Phase 21 tach retrieval khoi reranking trong candidate-side recommendation.

Thay vi:

```text
1 CV -> score tat ca jobs trong request
```

he thong chuyen sang:

```text
1 CV
  -> build candidate query profile
  -> build job catalog/index
  -> retrieve top-N jobs
  -> rerank retrieved jobs bang AI core
```

Muc tieu la:

- giam tai tinh toan;
- chuan bi cho active JD catalog lon hon;
- tra ve retrieval debug metadata de web va bao cao de inspect.

### 2. Cach xu ly

Them:

- `src/job_catalog_loader.py`
- `src/job_indexer.py`
- `src/job_retriever.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_indexer.py`
- `tests/test_job_retriever.py`

Cap nhat:

- `src/job_recommendation_pipeline.py`
- `src/api_models.py`
- `api.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`
- `README.md`
- `docs/integration/sample-recommend-jobs-request.json`

### 3. Logic retrieval

He thong build:

- `job_card`: JD da parse va normalize
- `index_document`: searchable representation cho retrieval
- `candidate_query_profile`: skills, domain, title, summary, experience

Sparse retrieval score dua tren:

- must-have skill overlap
- title overlap
- domain overlap
- nice-to-have overlap
- experience compatibility

Neu embedding available, dense similarity duoc tron them vao retrieval score.

### 4. Output moi

Moi `top_job` trong response candidate-side co them:

```json
{
  "retrieval_rank": 1,
  "retrieval_score": 0.84,
  "retrieval_reasons": [
    "Strong must-have skill overlap.",
    "Domain overlap detected."
  ],
  "retrieval_components": {}
}
```

`retrieval_stats` co them:

- `jobs_indexed`
- `jobs_retrieved`
- `jobs_reranked`
- `retrieval_top_n`
- `retrieval_applied`

### 5. Cach test

Targeted:

```bash
python -m pytest tests/test_job_catalog_loader.py tests/test_job_indexer.py tests/test_job_retriever.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

### 6. Ket qua mong doi

- retrieval layer chay truoc reranking;
- top jobs co retrieval metadata de debug;
- `/recommend-jobs` van giu contract Phase 20 nhung thong minh hon;
- `/screening` khong bi anh huong.

### 7. Ghi chu cho bao cao

Co the noi:

```text
Candidate-side recommendation duoc mo rong theo kien truc retrieve -> rerank. O Phase 21, he thong khong cham diem tren toan bo tap JD active nua, ma dau tien xay dung job catalog va retrieval index, sau do lay ra top-N cong viec kha nang dua tren overlap ve ky nang, chuc danh, domain va kinh nghiem. Tap nay moi duoc dua vao AI core de rerank chi tiet. Cach tiep can nay phu hop voi cac he thong search/recommender thuc te va de mo rong hon trong cac phase sau.
```

---

## Phase 22 - Candidate-side Reranking with the Core Scorer

### 1. Muc tieu

Phase 22 tach candidate-side reranking thanh mot module rieng sau retrieval.

He thong van dung cung AI core person-job fit da co, nhung ket qua duoc dien
giai lai theo goc nhin ung vien thay vi recruiter.

### 2. Cach xu ly

Them:

- `src/candidate_job_reranker.py`
- `tests/test_candidate_job_reranker.py`

Cap nhat:

- `src/job_recommendation_pipeline.py`
- `api.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`
- `README.md`

### 3. Logic moi

Module reranker lam:

- score tung retrieved job bang screening core;
- lay `final_score` lam `fit_score`;
- map diem sang label candidate-side:
  - `Strong Fit`
  - `Good Fit`
  - `Potential Fit`
  - `Stretch`
  - `Low Fit`
- build `fit_summary` ngan gon;
- sort ket qua theo:
  - fit score
  - evidence
  - hard-skill gate pass
  - retrieval score

### 4. Output moi

Moi `top_job` duoc bo sung:

```json
{
  "fit_score": 86,
  "fit_label": "Strong Fit",
  "fit_summary": "This role is a Strong Fit because strong must-have skill coverage."
}
```

`recommendation` employer-side van duoc giu lai trong JSON de debug/noi bo,
nhung UI candidate-side nen uu tien `fit_label`.

### 5. Y nghia thiet ke

Phase nay giai quyet 2 viec:

1. retrieval va reranking khong con bi tron;
2. nguon goc scoring van giu nhat quan giua employer-side va candidate-side.

Noi ngan gon:

```text
Same scorer core
Different presentation layer
```

### 6. Cach test

Targeted:

```bash
python -m pytest tests/test_candidate_job_reranker.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

### 7. Ghi chu cho bao cao

Co the noi:

```text
Sau retrieval, cac JD duoc rerank bang chinh AI core person-job fit da dung cho employer-side. Tuy nhien, ket qua khong duoc tra theo nhan review cua recruiter nua, ma duoc map sang cac muc do fit de ung vien de hieu hon, gom Strong Fit, Good Fit, Potential Fit, Stretch va Low Fit. Cach thiet ke nay giu tinh nhat quan ve scoring, nhung dieu chinh lop dien giai theo dung vai tro nguoi dung.
```

---

## Phase 23 - Skill-gap Explanation and CV Improvement Suggestions

### 1. Muc tieu

Phase 23 bien candidate-side recommendation thanh co kha nang hanh dong ro hon:

```text
Job nao hop
  + thieu skill gi
  + skill nao da co nhung bang chung con yeu
  + nen sua CV theo huong nao
```

Candidate-side output khong chi dung o `fit_label` va `fit_summary`, ma bo sung mot lop giai thich co cau truc de web co the render gon hoac mo rong chi tiet.

### 2. Cach xu ly

Them:

- `src/skill_gap_explainer.py`
- `tests/test_skill_gap_explainer.py`

Cap nhat:

- `src/candidate_job_reranker.py`
- `tests/test_candidate_job_reranker.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`
- `api.py`
- `README.md`

### 3. Logic moi

Module moi `skill_gap_explainer` nhan candidate-vs-job result da duoc score va sinh ra 4 nhom gap:

- `missing_must_have`
- `weak_evidence`
- `optional_growth`
- `presentation_gaps`

Nguyen tac:

- skill bat buoc khong co match -> `missing_must_have`
- skill da match nhung `evidence_level <= 1` -> `weak_evidence`
- nice-to-have chua match -> `optional_growth`
- evidence tong the yeu / bi hard-skill gate / trinh bay mo ho -> `presentation_gaps`

Tren co so do, he thong build:

- `skill_gap_summary`
- `skill_gaps`
- `cv_improvement_suggestions`
- `next_best_actions`

### 4. Output moi

Moi `top_job` candidate-side co them:

```json
{
  "skill_gap_summary": {
    "missing_must_have_count": 1,
    "weak_evidence_count": 1,
    "optional_growth_count": 1,
    "presentation_gap_count": 2
  },
  "skill_gaps": {
    "missing_must_have": [],
    "weak_evidence": [],
    "optional_growth": [],
    "presentation_gaps": []
  },
  "cv_improvement_suggestions": [],
  "next_best_actions": []
}
```

`next_best_actions` duoc gioi han gon de UI hien o card/list, con `cv_improvement_suggestions` giu danh sach day du hon cho modal hoac trang chi tiet.

### 5. Y nghia thiet ke

Phase 23 giai quyet mot van de thuc te:

```text
Ung vien can biet can cai thien CV nhu the nao,
khong chi can biet job nao hop hon.
```

He thong cung tach ro:

- thieu nang luc that;
- co nang luc nhung bang chung con yeu;
- co the chi can viet ro hon trong CV.

Dieu nay giup output trung thuc hon, tranh viec AI khuyen "them skill ao" vao CV.

### 6. Cach test

Targeted:

```bash
python -m pytest tests/test_skill_gap_explainer.py tests/test_candidate_job_reranker.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

### 7. Ghi chu cho bao cao

Co the noi:

```text
Sau khi xep hang muc do phu hop giua CV va JD, he thong tiep tuc sinh mot lop giai thich skill-gap cho phia ung vien. Lop nay phan biet giua ky nang bat buoc con thieu, ky nang da co nhung bang chung con yeu, va cac ky nang uu tien co the bo sung them. Tu do, he thong dua ra cac goi y cai thien CV theo huong trung thuc va co the hanh dong duoc, nhu bo sung bang chung o du an/kinh nghiem, viet ro hon cong nghe da dung, va neu co kinh nghiem that thi them ky nang dang bi thieu vao CV.
```

---

## Phase 24 - JD Quality Gate and Recommendation Eligibility

### 1. Muc tieu

Phase 24 giai quyet van de du lieu web that:

```text
Mot so tin tuyen dung test / placeholder / qua ngan
van duoc candidate-side AI recommendation cham 20-35 diem.
```

Muc tieu moi:

```text
Truoc khi xep hang cong viec theo CV,
he thong phai kiem tra JD co du chat luong de AI danh gia hay khong.
```

### 2. Cach xu ly

Them:

- `src/job_quality_gate.py`
- `tests/test_job_quality_gate.py`
- `docs/refactoring/phase-24-refactoring-plan.md`

Cap nhat:

- `src/job_catalog_loader.py`
- `src/job_recommendation_pipeline.py`
- `src/candidate_job_reranker.py`
- `api.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`
- `README.md`

### 3. Logic moi

Moi job candidate-side duoc phan tich chat luong truoc retrieval:

- placeholder title nhu `Test`, `Demo`, `Test migrate`
- JD content qua ngan sau khi clean
- khong co yeu cau ky thuat co y nghia
- khong co responsibilities co y nghia
- tong signal qua ngheo

He thong sinh:

- `job_quality.quality_score`
- `job_quality.quality_label`
- `job_quality.recommendation_eligible`
- `job_quality.flags`
- `job_quality.reasons`

Neu job khong du dieu kien:

- khong dua vao `top_jobs`
- dua vao `excluded_jobs`
- them warning top-level

### 4. Output moi

Response candidate-side co them:

```json
{
  "excluded_jobs": [],
  "job_quality_stats": {
    "jobs_received": 10,
    "eligible_jobs": 7,
    "excluded_jobs": 3
  },
  "warnings": []
}
```

Moi `top_job` co them:

```json
{
  "job_quality": {
    "quality_score": 78,
    "quality_label": "eligible_with_warning",
    "recommendation_eligible": true
  }
}
```

### 5. Y nghia thiet ke

Phase 24 tach ro hai tinh huong:

1. `Low Fit`
   - JD co du du lieu
   - CV khong phu hop

2. `Insufficient JD Data`
   - JD khong du yeu cau/noi dung de AI doi sanh

Day la diem rat quan trong cho web va cho bao cao do an, vi no tranh gay hieu nham
rằng job "khong hop" trong khi thuc te la job "khong du du lieu".

### 6. Cach test

Targeted:

```bash
python -m pytest tests/test_job_quality_gate.py tests/test_job_catalog_loader.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

### 7. Ghi chu cho bao cao

Co the noi:

```text
Tren du lieu thuc te, khong phai tin tuyen dung nao cung duoc nhap day du va chat luong. Vi vay, truoc khi goi y cong viec cho ung vien, he thong bo sung mot lop JD quality gate de phat hien cac tin placeholder, qua ngan, hoac khong co du yeu cau ky thuat. Cac job khong du du lieu se khong duoc cham fit score binh thuong, ma duoc danh dau la khong du du lieu de AI danh gia. Cach thiet ke nay giup ket qua recommendation thuc te va dang tin hon.
```

---

## Phase 25 - Web Payload Quality Hardening and Runtime Diagnostics

### 1. Muc tieu

Phase 25 giai quyet van de integration thuc te:

```text
Khong phai luc nao ket qua "la" cung do AI scorer.
Rat nhieu truong hop van de nam o payload web gui sang:
- JD/CV qua ngan
- con HTML
- thieu requirement source
- profile qua sparse
```

Muc tieu moi:

```text
Bo sung diagnostics co cau truc va trace_id
de phan biet input issue, parsing issue, va matching issue.
```

### 2. Cach xu ly

Them:

- `src/payload_diagnostics.py`
- `src/runtime_diagnostics.py`
- `tests/test_payload_diagnostics.py`
- `tests/test_runtime_diagnostics.py`
- `docs/refactoring/phase-25-refactoring-plan.md`

Cap nhat:

- `src/payload_pipeline.py`
- `src/job_catalog_loader.py`
- `src/job_recommendation_pipeline.py`
- `api.py`
- `tests/test_payload_pipeline.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_api.py`
- `README.md`

### 3. Logic moi

#### 3.1 Payload diagnostics

Employer-side va candidate-side deu duoc them lop payload diagnostics:

- JD placeholder / qua ngan
- JD thieu requirements / responsibilities
- CV qua ngan
- CV qua sparse
- HTML cleaning co nguy co lam mat nhieu signal

Moi diagnostics object gom:

- `flags`
- `warnings`
- `quality_label`
- `source`
- `metrics`

#### 3.2 Runtime diagnostics

Moi request API deu co:

- `trace_id`
- `diagnostics.endpoint`
- `diagnostics.payload`
- `diagnostics.runtime`

Screening co them:

- `diagnostics.runtime.job_quality`

Recommendation co them:

- `diagnostics.runtime.top_job_ids`
- `diagnostics.runtime.excluded_job_ids`
- tong hop job payload warnings

### 4. Output moi

Ca hai endpoint deu co them:

```json
{
  "trace_id": "screening-abc123",
  "diagnostics": {
    "endpoint": "screening",
    "trace_id": "screening-abc123",
    "payload": {},
    "runtime": {}
  }
}
```

Candidate-side `excluded_jobs` cung co them:

```json
{
  "payload_diagnostics": {}
}
```

de web/admin co the debug vi sao mot job bi canh bao hoac bi loai.

### 5. Y nghia thiet ke

Phase 25 rat quan trong cho tich hop web va bao cao do an vi no cho phep tra loi:

```text
AI cham tren du lieu nao?
Payload co du manh khong?
Doan nao cua luong xu ly dang co van de?
```

No giup tach ro:

1. loi input tu web
2. gioi han parser do du lieu qua yeu
3. mismatch that giua CV va JD

Tu do, qua trinh debug nhanh hon va ket qua de bao ve hon.

### 6. Cach test

Targeted:

```bash
python -m pytest tests/test_payload_diagnostics.py tests/test_runtime_diagnostics.py tests/test_payload_pipeline.py tests/test_job_catalog_loader.py tests/test_job_recommendation_pipeline.py tests/test_api.py
```

Full regression:

```bash
pytest
```

Ket qua phase nay:

```text
188 passed
```

### 7. Ghi chu cho bao cao

Co the noi:

```text
Sau khi mo rong he thong sang API va tich hop voi web, mot van de thuc te xuat hien la ket qua AI co the bi anh huong boi chat luong payload dau vao, khong chi boi mo hinh doi sanh. Vi vay, he thong bo sung mot lop payload diagnostics va runtime diagnostics. Lop nay danh gia do day du cua CV/JD, phat hien cac truong hop qua ngan, placeholder, hoac thieu section quan trong, dong thoi sinh trace_id va metadata giai thich cho moi request. Nhờ do, he thong co the tach ro van de du lieu dau vao voi van de matching that, giup tich hop web on dinh hon va giup qua trinh kiem thu, debug, va bao ve do an ro rang hon.
```
