# Phase 17 - Taxonomy-independent Open-set Screening Core

## 1. Muc tieu phase

Phase 17 giai quyet van de lon vua phat hien:

```text
Neu JD thuoc nganh/chuc vu chua co trong taxonomy,
he thong khong duoc cham diem thap chi vi taxonomy chua bao phu.
```

Muc tieu cua phase nay la bien taxonomy thanh mot tang ho tro giai thich/chuan hoa, khong phai dieu kien bat buoc de matching.

Huong moi:

```text
JD
  -> known taxonomy skills
  -> open-set requirements/capabilities

CV
  -> known taxonomy skills
  -> evidence/capabilities from summary, skills, work, projects, certifications

Matching
  -> rule-based taxonomy match cho known skills
  -> multilingual embedding + evidence match cho open-set requirements
  -> scoring dung ca hai nhom
  -> output noi ro known-taxonomy vs semantic-open-set
```

Noi ngan gon:

```text
Taxonomy-known skills explain strongly.
Open-set requirements keep the system useful for new domains.
```

## 2. Ly do can Phase 17

Case JD_2 / CV_3 cho thay:

- JD title bi trong.
- JD domain bi gan sai `Mobile AI` do keyword `edge` match nham trong tu `knowledge`.
- CV_3/David Chen rat phu hop voi JD IT Security & Governance, nhung diem thap vi taxonomy chua co nhom IT Security/GRC.
- Extract taxonomy skills tu JD_2 va CV_3 tra ve rong.

Neu minh chi them `Qualys`, `Vulnerability Management`, `Access Management`, `PAM`, `ISO 27001` vao taxonomy thi diem case nay se tang, nhung do la cach va tung de.

Phase 17 khac cach do:

- Khong them skill cu the chi de fix JD_2.
- Khong lam demo theo bo de.
- Them kha nang extract va match requirement ngoai taxonomy.

## 3. Nguyen tac thiet ke

### 3.1 Khong phu thuoc cung vao taxonomy

Taxonomy van duoc dung cho:

- exact/alias matching.
- related/transferable matching.
- evidence search aliases.
- review card giai thich ro rang.
- suggestion queue/Admin review.

Nhung neu requirement chua co taxonomy:

- Khong bo qua.
- Khong chi dua vao Admin approve.
- Dung open-set semantic matching de tim evidence trong CV.

### 3.2 Khong goi GPT trong core

Phase 17 van local-first:

- Rule parser.
- Heuristic requirement extraction.
- Local multilingual embedding neu bat.

Khong phu thuoc GPT de tranh:

- cost.
- privacy.
- internet dependency.
- kho bao ve do an.

### 3.3 Khong de semantic match lap lo thanh exact skill

Ket qua open-set phai co marker:

```json
{
  "taxonomy_status": "unknown",
  "match_type": "semantic_only_match"
}
```

De recruiter/Admin biet day la match bang ngu nghia, khong phai skill da chuan hoa.

### 3.4 Neu embedding tat, phai bao confidence ro

Neu JD co nhieu open-set requirements ma embedding khong bat:

- Khong nen im lang cho diem thap nhu ung vien kem.
- Output phai co `screening_confidence` hoac warning.

Vi du:

```json
{
  "screening_confidence": {
    "level": "low",
    "reason": "Open-set requirements detected but embedding matcher is disabled."
  }
}
```

## 4. Pham vi thuc hien

Trong Phase 17 se lam:

- Them requirement/capability extractor doc lap taxonomy.
- Tach long requirement line thanh cac requirement units ngan gon.
- Cai thien open-set matching de cover cac requirement units nay.
- Tich hop open-set matches vao scoring pipeline ro rang hon.
- Them screening confidence metadata.
- Sua domain matching de tranh substring false positive.
- Cai thien job title fallback khi JD khong co title ro.
- Them tests voi fake embedding, khong download BGE-M3 that.
- Cap nhat README/dev log/refactoring docs.

Ngoai scope Phase 17:

- Khong them full IT Security taxonomy chi de tang diem JD_2.
- Khong import ESCO/O*NET.
- Khong goi GPT.
- Khong lam UI web.
- Khong thay doi DB PHP.
- Khong commit data test local neu khong duoc yeu cau.

## 5. Kien truc de xuat

### 5.1 Module moi: requirement/capability extraction

Co the tao:

```text
src/requirement_extractor.py
```

Trach nhiem:

- Nhan raw JD text + parsed JD sections.
- Tao danh sach requirement units ngoai taxonomy.
- Loc bo heading/soft line qua chung.
- Tach cac cum trong long requirement.

Ham de xuat:

```python
def extract_requirement_units(
    job_criteria: dict,
    jd_text: str,
    taxonomy: dict,
) -> list[dict]:
    ...
```

Output:

```json
[
  {
    "text": "Qualys",
    "source": "requirements",
    "taxonomy_status": "unknown",
    "extraction_method": "pattern_split"
  },
  {
    "text": "vulnerability management",
    "source": "requirements",
    "taxonomy_status": "unknown",
    "extraction_method": "noun_phrase_heuristic"
  }
]
```

### 5.2 Requirement line decomposition

Can xu ly cac mau nhu:

```text
Proficiency in Linux, Nutanix administration, Commvault, and Qualys
Knowledge of vulnerability management tools and access control principles
Understanding of Personal Data Protection regulations
Relevant certifications: Security+, CEH, ISO 27001
Experience in IT Security Operations, Governance, Compliance
```

Thanh:

```text
Linux
Nutanix administration
Commvault
Qualys
vulnerability management
access control
Personal Data Protection
Security+
CEH
ISO 27001
IT Security Operations
Governance
Compliance
```

Day khong phai taxonomy hard-code theo nganh, ma la generic pattern extraction.

### 5.3 Filtering de tranh requirement rac

Bo qua cac dong:

```text
Qualifications & Experience
Skills
Strong analytical, detail-oriented mindset
Ability to collaborate across teams
Excellent communication skills
```

Voi soft skill, co the de rieng future phase. Phase 17 tap trung technical/domain capabilities truoc.

### 5.4 Open-set matching

Hien tai `find_semantic_requirement_evidence` da co nen Phase 17 nen mo rong thay vi viet lai tu dau.

Can dam bao:

- Unknown requirement units duoc dua vao open-set matcher.
- Matcher so sanh voi evidence candidates tu:
  - CV skills.
  - summary.
  - headline.
  - work experience bullets.
  - projects.
  - certifications.
- Moi unknown requirement co ket qua:
  - `semantic_only_match` neu tim thay evidence.
  - `no_semantic_evidence` neu khong thay.

### 5.5 Scoring

Scorer hien da tinh tren `matches`, va pipeline da ghep:

```python
scored_matches = [*enriched_matches, *open_set_matches]
```

Nhung Phase 17 can dam bao:

- Open-set requirements duoc tao du chuan.
- Open-set match co evidence level.
- Khong de empty matches lam diem tro nen vo nghia.
- Neu embedding disabled va open-set requirements nhieu, output co warning.

### 5.6 Screening confidence

Them output:

```json
{
  "job": {
    "screening_confidence": {
      "level": "high",
      "known_requirement_count": 4,
      "open_set_requirement_count": 8,
      "embedding_enabled": true,
      "warnings": []
    }
  }
}
```

Rules de xuat:

```text
high:
  known requirements > 0, hoac open-set requirements > 0 va embedding available

medium:
  taxonomy coverage thap nhung embedding available

low:
  open-set requirements > 0 nhung embedding disabled/unavailable
```

### 5.7 Domain matching fix

Hien bug:

```text
"edge" match nham trong "knowledge"
```

Can dung word/phrase boundary helper:

```python
contains_phrase(text, "edge")
```

Thay vi:

```python
"edge" in text
```

Dong thoi them domain detection tong quat cho:

```text
IT Security / Governance / Compliance
```

Day khong phai them skill taxonomy, chi la domain category de scoring domain khong sai.

### 5.8 Job title fallback

Neu JD khong co intro title ro, nhu:

```text
Mô tả Công việc
1. IT Security Operations
...
Yêu Cầu Công Việc
```

Co the suy luan title tu:

- web/API payload title neu co.
- first numbered heading trong responsibilities.
- domain labels gan nhat.

Voi CLI raw text, fallback co the la:

```text
IT Security Operations
```

Nhung voi web API, title nen lay tu payload/web DB, vi anh web dang co title:

```text
IT Security & IT Governance Officer
```

## 6. Output sau Phase 17

Job output nen co them:

```json
{
  "must_have_skills": ["known taxonomy skills"],
  "open_set_requirements": [
    "Qualys",
    "vulnerability management",
    "access control",
    "Personal Data Protection"
  ],
  "taxonomy_coverage": {
    "known_count": 0,
    "unknown_count": 8,
    "coverage_ratio": 0.0
  },
  "screening_confidence": {
    "level": "medium",
    "embedding_enabled": true,
    "warnings": []
  }
}
```

Candidate output da co:

```json
{
  "open_set_requirement_matches": []
}
```

Sau Phase 17 field nay phai co gia tri that khi JD co open-set requirements.

## 7. Test plan

Them/cap nhat tests:

```text
tests/test_requirement_extractor.py
tests/test_open_set_matcher.py
tests/test_screening_pipeline.py
tests/test_payload_pipeline.py
tests/test_jd_parser.py
tests/test_scorer.py
```

Cases quan trong:

1. Extract capability units tu long requirement line.
2. Extract certifications tu `Security+, CEH, ISO 27001`.
3. Khong giu heading `Qualifications & Experience`, `Skills`.
4. Khong giu soft lines qua chung.
5. Open-set matcher match `vulnerability management` voi CV evidence `Managed enterprise vulnerability management using Qualys`.
6. Open-set matcher match `Personal Data Protection` voi CV evidence tu project/summary.
7. Pipeline co open_set_requirement_matches khi taxonomy khong co skill do.
8. Scoring tang khi open-set evidence match tot.
9. Domain detector khong match `edge` trong `knowledge`.
10. Domain detector nhan `IT Security/GRC` cho security/governance/compliance JD/CV.
11. Screening confidence low khi open-set co nhung embedding disabled.
12. Screening confidence medium/high khi embedding available.

Dung fake embedding model trong tests, khong download BGE-M3.

Full regression:

```powershell
pytest
```

Manual benchmark sau khi code:

```powershell
python main.py --jd data/jobs/JD_2.txt --cv-dir outputs/test_cv1_cv3 --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only --output-json outputs/jd2_cv1_cv3_phase17_result.json --show-review-cards
```

API/web benchmark:

```powershell
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_THRESHOLD='0.72'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'
uvicorn api:app --host 127.0.0.1 --port 8000
```

Sau do tren web bam lai:

```text
Chạy AI gợi ý xếp hạng
```

Luu y: phai restart uvicorn sau khi code Phase 17.

## 8. Acceptance criteria

Phase 17 hoan thanh khi:

- He thong extract duoc open-set requirement units tu JD ngoai taxonomy.
- Pipeline khong bo qua requirement ngoai taxonomy.
- Khi embedding enabled, CV co evidence gan nghia duoc semantic-only match.
- Output noi ro taxonomy-known vs open-set semantic matches.
- Score khong con phu thuoc hoan toan vao taxonomy coverage.
- Neu embedding disabled, output co confidence warning.
- Domain matching khong con false positive `edge` trong `knowledge`.
- JD/CV nganh moi khong bi diem thap chi vi taxonomy thieu.
- Full `pytest` pass.
- Khong them taxonomy cu the chi de fix JD_2.

## 9. Rui ro va giam thieu

### 9.1 Open-set extractor tao qua nhieu requirement

Risk:

```text
Long JD bi tach ra qua nhieu phrase va lam score nhiu.
```

Giam thieu:

- Gioi han phrase length.
- Loc heading/soft skill.
- Dedupe.
- Gioi han max requirements neu can.

### 9.2 Embedding match sai

Risk:

```text
Semantic similarity cao nhung khong dung skill.
```

Giam thieu:

- Threshold ro rang.
- Evidence text bat buoc.
- Mark `semantic_only_match`.
- Review card neu semantic-only thi ghi recruiter can verify.

### 9.3 Diem tang qua manh khi semantic-only

Risk:

```text
Unknown semantic match duoc cham nhu exact skill.
```

Giam thieu:

- Open-set match score thap hon exact match.
- Giu `OPEN_SET_MATCH_SCORE = 0.65` hoac dieu chinh co can nhac.

### 9.4 Phase qua rong

Risk:

```text
Dung toi parser, matcher, scorer, pipeline cung luc.
```

Giam thieu:

- Them module extractor rieng.
- Reuse open-set matcher hien co.
- Tests nho, synthetic, khong download model that.

## 10. Ghi chu cho bao cao

Co the trinh bay:

```text
De tranh phu thuoc hoan toan vao skill taxonomy, he thong bo sung co che
open-set requirement matching. Cac yeu cau trong JD duoc tach thanh cac
capability units, bao gom ca nhung yeu cau chua co trong taxonomy. Voi cac
yeu cau da co taxonomy, he thong dung rule-based matching de dam bao giai
thich ro rang. Voi cac yeu cau chua co taxonomy, he thong dung multilingual
embedding de tim bang chung gan nghia trong CV va danh dau ket qua la
semantic-only. Cach nay giup he thong van hoat dong voi nganh nghe moi,
trong khi taxonomy suggestion queue tiep tuc giup Admin mo rong taxonomy
ve lau dai.
```

Mot cau tom gon khi bao ve:

```text
Taxonomy la lop chuan hoa va giai thich, con open-set semantic matching giup
he thong khong bi that bai khi gap skill/nganh nghe moi.
```

## 11. Sau khi code Phase 17

Da trien khai:

- Them `src/requirement_extractor.py`.
- Them `tests/test_requirement_extractor.py`.
- Them `docs/refactoring/phase-17-refactoring-plan.md`.
- Cap nhat CLI pipeline va API payload pipeline de dung open-set requirement extraction.
- Cap nhat `open_set_matcher` de:
  - dong bo threshold voi embedding matcher.
  - uu tien exact phrase evidence.
  - uu tien evidence source manh hon khi similarity gan nhau.
- Cap nhat `evidence_detector` de dung certifications lam evidence candidates.
- Cap nhat `jd_parser`:
  - title fallback.
  - `yeear` typo tolerance.
  - word-boundary domain matching.
  - IT Security/GRC domain.
- Cap nhat `scorer`:
  - word-boundary candidate domain matching.
  - IT Security/GRC domain.

Output moi trong job:

```json
{
  "open_set_requirements": [],
  "screening_confidence": {}
}
```

Manual benchmark voi JD_2 va CV_1/CV_3:

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

Lenh benchmark:

```powershell
python main.py --jd data\jobs\JD_2.txt --cv-dir outputs\test_cv1_cv3 --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only --output-json outputs\jd2_cv1_cv3_phase17_bge.json
```

Full regression:

```text
143 passed
```

Ghi chu quan trong:

- Neu API server dang chay, phai restart `uvicorn` sau khi update code.
- Web can bat embedding env vars de thay cai thien open-set matching.
- Neu embedding khong bat, output co `screening_confidence.level = low` khi JD co open-set requirements.
