# Phase 27 - Typed Requirement Schema and Section-aware JD Parsing

## 1. Muc tieu phase

Sau Phase 26, he thong da co core logic benchmark va failure taxonomy de khoa lai
cac benh logic quan trong.

Nhung benchmark chi cho ta biet:

```text
he thong dang sai o dau
```

Con Phase 27 la phase bat dau sua goc re dau tien:

```text
JD parser va requirement typing
```

Muc tieu cua Phase 27 la:

```text
Khong parse JD thanh mot danh sach requirement chung chung nua,
ma tach requirement thanh dung loai nghiep vu.
```

Noi ngan gon:

```text
Phase 26 = dong bang benh logic
Phase 27 = sua tan goc requirement typing va section parsing
```

## 2. Van de can giai quyet

### 2.1 Soft skill dang di nham vao hard-skill scoring

Day la mot benh logic lon da lo ra rat ro:

- enthusiastic
- eager to learn
- good communication
- ability to work in team

co the bi dua vao requirement matching flow nhu mot hard skill hoac open-set
technical requirement.

Dieu nay lam:

- score sai nghia;
- open-set bi nhieu;
- taxonomy suggestion queue ban;
- review card giai thich khong dung logic tuyen dung.

### 2.2 Requirement experience / education / language dang bi tron voi skill

Trong thuc te, JD co nhieu loai requirement:

- hard skill
- tool/platform
- years of experience
- degree / major
- certifications
- foreign language
- soft skill
- responsibility context

Neu parser khong tach ro, he thong de:

- xem `3+ years experience` la skill;
- xem `Bachelor's degree` la skill;
- xem `English communication` la skill ky thuat;
- xem `responsibilities` la `must-have`.

### 2.3 Parser chua tan dung section structure cua JD

Nhieu JD thuc te co section:

- Job description
- Requirements
- Responsibilities
- Qualifications
- Nice to have
- Benefits

Nhung neu parser xem toan bo noi dung gan nhu cung muc uu tien, he thong rat de:

- missing requirement that nam o section requirements;
- keo nham responsibility line vao hard skill list;
- bo sot technical terms nam trong qualification section.

### 2.4 Job title va section context chua duoc dung de giai nghia requirement

Vi du:

```text
Good at writing
```

neu di mot minh rat mo ho.

Nhung:

```text
Good at writing technical documentation
```

trong mot IT Security role lai la context khac.

Phase 27 chua giai triet de bang role-family layer, nhung can it nhat:

- hieu section nao dang chua requirement chinh;
- hieu line nao la soft requirement;
- hieu line nao la non-technical qualifier.

## 3. Vi sao Phase 27 la buoc tiep theo dung nhat

Sau Phase 26, benh logic da duoc benchmark hoa.
Trong cac benh da khoa lai, benh xuat hien trung tam nhat la:

```text
REQUIREMENT_TYPE_ERROR
```

Neu khong sua benh nay truoc, cac phase sau nhu:

- open-set filtering
- role-family inference
- scoring gate

se van phai xu ly tren input requirement da sai loai.

Noi cach khac:

```text
typed input dung truoc
scoring, open-set, suggestion moi dung sau
```

## 4. Nguyen tac thiet ke

### 4.1 Typed requirement schema phai ro, nhung khong qua nang

Schema moi nen du ro de he thong xu ly dung, nhung khong nen rat phuc tap ngay tu
phase nay.

De xuat nhom requirement chinh:

- `TECH_SKILL`
- `TOOL_PLATFORM`
- `EXPERIENCE_REQUIREMENT`
- `EDUCATION_REQUIREMENT`
- `CERTIFICATION_REQUIREMENT`
- `LANGUAGE_REQUIREMENT`
- `SOFT_SKILL`
- `RESPONSIBILITY_CONTEXT`
- `DOMAIN_CONTEXT`
- `UNKNOWN_REQUIREMENT`

### 4.2 Section-aware truoc, role-aware sau

Phase 27 uu tien:

- section-aware parsing
- rule-based requirement typing

Chu chua dua role-family inference vao day.
Role-family se den o phase sau.

### 4.3 Backward-compatible voi pipeline hien tai

Phase 27 khong nen pha tung lop toan bo flow screening/recommendation.

Can thiet ke sao cho:

- parser output moi duoc bo sung field typed schema;
- module cu van co the dung requirement group summary;
- API contract khong bi vo ngay lap tuc.

### 4.4 Khong dua soft skill vao hard-skill scoring nua

Nguyen tac quan trong nhat cua phase nay:

```text
Soft skill, education, language, experience
khong duoc tro thanh must-have technical skill chi vi parser chua tach ro.
```

## 5. Kien truc de xuat

### 5.1 Luong xu ly moi cho JD

```text
Raw JD text
  -> section parser
  -> typed requirement extractor
  -> requirement groups
  -> scoring requirement builder
```

### 5.2 Tinh than cua output moi

Thay vi chi co:

```json
{
  "must_have_skills": [],
  "nice_to_have_skills": []
}
```

can co them:

```json
{
  "typed_requirements": [
    {
      "text": "Java",
      "type": "TECH_SKILL",
      "section": "requirements",
      "priority": "must_have"
    }
  ]
}
```

### 5.3 Requirement groups van giu de dung cho scorer hien tai

Vi scorer hien tai dang dua tren `requirement_groups`, Phase 27 nen giu va lam manh
nhom nay thay vi xoa bo.

Vi du:

```json
{
  "requirement_groups": {
    "must_have_technical": [],
    "nice_to_have_technical": [],
    "soft_skills": [],
    "education": [],
    "experience": [],
    "certifications": [],
    "language": [],
    "domain_context": [],
    "responsibilities": [],
    "ignored": []
  }
}
```

## 6. Module du kien can tao / cap nhat

Them:

```text
src/jd_section_parser.py
tests/test_jd_section_parser.py
```

Cap nhat manh:

```text
src/jd_parser.py
src/jd_requirement_classifier.py
src/requirement_extractor.py
src/payload_pipeline.py
src/screening_pipeline.py
src/job_catalog_loader.py
tests/test_jd_parser.py
tests/test_jd_requirement_classifier.py
tests/test_requirement_extractor.py
tests/test_payload_pipeline.py
tests/test_screening_pipeline.py
tests/test_job_catalog_loader.py
tests/test_core_logic_benchmark.py
```

Neu can, co the them helper nho:

```text
src/requirement_types.py
```

de gom constant/type code cho on dinh.

## 7. Trach nhiem cua tung phan

### 7.1 `src/jd_section_parser.py`

Module nay nen:

- tach section theo heading;
- support heading English va Vietnamese;
- normalize section keys;
- khong quyet dinh scoring;
- chi tra ve section map on dinh.

Vi du:

```json
{
  "title": "...",
  "description": [],
  "requirements": [],
  "responsibilities": [],
  "nice_to_have": [],
  "benefits": []
}
```

### 7.2 `src/jd_parser.py`

Cap nhat de:

- dung section parser moi;
- dua title/description/requirements/responsibilities vao cau truc ro hon;
- giu backward-compatible output cho cac field cu can thiet.

### 7.3 `src/jd_requirement_classifier.py`

Day la trai tim cua phase nay.

Can cap nhat de:

- phan loai requirement theo type;
- xac dinh `must_have` vs `nice_to_have`;
- tach `SOFT_SKILL`, `LANGUAGE_REQUIREMENT`, `EXPERIENCE_REQUIREMENT`, ...
- build lai `requirement_groups`.

### 7.4 `src/requirement_extractor.py`

Can cap nhat de:

- khong xem soft/non-technical line la open-set technical requirement;
- bo sung metadata de benchmark va diagnostics doc duoc.

## 8. Typed schema de xuat

### 8.1 Requirement object

De xuat format:

```json
{
  "text": "Good communication skills",
  "type": "SOFT_SKILL",
  "section": "requirements",
  "priority": "must_have",
  "source_line": "Good communication skills",
  "normalized_text": "good communication skills"
}
```

### 8.2 Meaning cua tung type

#### `TECH_SKILL`

Ky nang ky thuat cot loi:

- Java
- Spring Boot
- SQL
- Face recognition

#### `TOOL_PLATFORM`

Cong cu / framework / platform:

- Docker
- Kubernetes
- AWS
- VMware
- SAP

#### `EXPERIENCE_REQUIREMENT`

Yeu cau ve so nam kinh nghiem:

- 2+ years experience
- at least 3 years

#### `EDUCATION_REQUIREMENT`

Bang cap / nganh hoc:

- Bachelor's in CS
- Tot nghiep Dai hoc CNTT

#### `CERTIFICATION_REQUIREMENT`

Chung chi:

- CEH
- Security+
- AWS Certified

#### `LANGUAGE_REQUIREMENT`

Ngoai ngu:

- English communication
- written English

#### `SOFT_SKILL`

Ky nang mem / thai do:

- teamwork
- communication
- eager to learn

#### `RESPONSIBILITY_CONTEXT`

Dong mo ta trach nhiem cong viec, chua chac la requirement phai match truc tiep.

#### `DOMAIN_CONTEXT`

Dong cho biet bai toan / nganh / boi canh domain:

- banking
- eKYC
- fintech

#### `UNKNOWN_REQUIREMENT`

Requirement chua phan loai duoc ro o phase nay.

## 9. Rule typing de xuat

### 9.1 Uu tien section requirements / qualifications

Neu line nam trong:

- Requirements
- Qualifications
- Yeu cau

thi duoc xet la requirement chinh.

### 9.2 Responsibilities chi la signal bo tro

Neu line nam trong responsibilities:

- khong dua thang vao must-have technical skill
- co the duoc dung lam bo tro domain/context
- phase sau moi co logic promotion co kiem soat

### 9.3 Soft skill detection uu tien truoc open-set technical

Neu line match pattern:

- communication
- teamwork
- eager to learn
- detail oriented

thi uu tien xep vao `SOFT_SKILL`, khong dua vao open-set technical.

### 9.4 Experience va education phai duoc nhan dien som

Vi du:

- `3+ years experience`
- `Bachelor's degree`

phai duoc cat ra khoi technical pool ngay tu dau.

### 9.5 Language requirement can tach rieng

Vi du:

- spoken English
- writing English

khong nen de tro thanh "unknown technical requirement".

## 10. Anh huong mong doi len he thong

Sau Phase 27, minh ky vong:

- soft skill contamination giam ro;
- open-set technical pool sach hon;
- taxonomy suggestion queue it nhieu hon;
- benchmark `REQUIREMENT_TYPE_ERROR` giam;
- review card va diagnostics doc hop ly hon.

## 11. Pham vi thuc hien cua Phase 27

### 11.1 Trong scope

- section-aware JD parsing;
- typed requirement schema;
- requirement classifier moi/duoc nang cap;
- group mapping moi;
- update benchmark va regression tests;
- giu backward compatibility cho flow screening/recommendation.

### 11.2 Ngoai scope

- chua lam role-family inference;
- chua redesign scoring formula;
- chua lam confidence gate moi;
- chua lam open-set governance moi cho admin queue;
- chua lam multilingual embedding moi.

## 12. Test plan

Them:

```text
tests/test_jd_section_parser.py
```

Cap nhat:

```text
tests/test_jd_parser.py
tests/test_jd_requirement_classifier.py
tests/test_requirement_extractor.py
tests/test_payload_pipeline.py
tests/test_screening_pipeline.py
tests/test_job_catalog_loader.py
tests/test_core_logic_benchmark.py
tests/test_api.py
```

### 12.1 Cac case bat buoc phai pass

1. Soft skill khong vao `must_have_technical`.
2. Education requirement khong vao `missing_skills`.
3. Language requirement khong vao open-set technical sai nghia.
4. Requirement line technical van duoc parse dung.
5. Responsibilities khong len thanh hard skill mot cach may moc.
6. Benchmark Phase 26 van pass.

### 12.2 Regression quan trong

Can chay lai benchmark:

- `screening_backend_strong`
- `screening_backend_evidence_without_skills_section`
- `screening_backend_hard_skill_deficit`
- `screening_cross_lingual_cv`
- `recommendation_placeholder_jobs_excluded`

## 13. Acceptance criteria

Phase 27 duoc xem la hoan thanh khi:

1. JD parser tach duoc section on dinh;
2. he thong co typed requirement schema ro rang;
3. soft skill / education / language / experience khong con di nham vao hard-skill scoring path;
4. benchmark Phase 26 van pass;
5. full `pytest` pass;
6. output API van backward-compatible o muc can thiet.

## 14. Dau ra mong muon sau phase nay

Sau Phase 27, khi gap 1 line trong JD, he thong khong chi biet:

```text
day la requirement
```

ma biet ro hon:

```text
day la SOFT_SKILL
day la EXPERIENCE_REQUIREMENT
day la EDUCATION_REQUIREMENT
day la TOOL_PLATFORM
```

Day la nen tang rat quan trong de:

- Phase 28 loc open-set technical sach hon;
- Phase 29 them role-family dung hon;
- Phase 31 siet scoring dung nghia hon.

## 15. Huong sau Phase 27

Sau khi typed requirement schema da on, buoc tiep theo hop ly la:

```text
Phase 28 - Open-set Technical Requirement Filtering
```

Muc tieu cua phase do la:

- chi giu unknown requirement technical that su;
- loai bot soft/general requirement ra khoi open-set technical flow;
- lam sach input cho taxonomy suggestion va semantic fallback.
