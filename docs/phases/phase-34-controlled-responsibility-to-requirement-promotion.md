# Phase 34 - Controlled Responsibility-to-Requirement Promotion

## 1. Muc tieu phase

Sau Phase 33, he thong da co them 2 lop du lieu moi o phia JD:

- `responsibility_signals`
- `technical_responsibility_candidates`

Noi ngan gon:

```text
Phase 33 = biet responsibilities co technical signals nao dang de y
Phase 34 = quyet dinh signal nao duoc promote thanh requirement de chay matching/scoring
```

Muc tieu cua Phase 34 la:

```text
Khong de candidate pool technical responsibilities nam chet trong metadata nua,
ma dua mot phan signal manh nhat vao scoring input mot cach co kiem soat.
```

Rat quan trong:

```text
Phase 34 co cho phep thay doi scoring input
nhung chua sua score formula / weight calibration.
```

Tuc la:

- co the lam `must_have_skills` khong con rong o cac JD sparse;
- nhung chua thay doi cong thuc tinh diem;
- chua source-aware weighting day du;
- chua role-family expansion lon.

## 2. Vi tri cua Phase 34 trong cay dependency

Day la phase thu hai trong nhanh sua section-aware JD sourcing:

```text
Phase 33 -> Responsibility signal extraction foundation
Phase 34 -> Controlled responsibility-to-requirement promotion
Phase 35 -> IT support / infra role-family expansion
Phase 36 -> Source-aware scoring calibration
Phase 37 -> Confidence and diagnostics guardrails
Phase 38 -> Benchmark and regression pack
```

Nguyen tac de khong bi lech huong:

```text
Phase 34 chi sua:
- promotion gate
- promotion metadata
- scoring input sourcing

Phase 34 chua sua:
- role-family coverage rong hon
- score formula
- review card wording lon
- web integration lon
```

## 3. Van de can giai quyet

### 3.1 Candidate pool da co nhung chua giup ich cho matching/scoring

Sau Phase 33, Job 22 co the co:

```text
technical_responsibility_candidates:
- Active Directory
- DNS
- DHCP
- Firewall
- Router
- Switch
- VPN
- Google Workspace
```

Nhung neu scoring input van chi dung:

```text
must_have_technical
```

thi he thong van gap tinh trang:

- `must_have_skills = []`
- `open_set_requirements = []`
- score van baseline-heavy.

### 3.2 Neu promote bai bai se rat nguy hiem

Neu chi can co technical term trong responsibilities la promote ngay,
he thong rat de:

- over-promote;
- xem task phu thanh core requirement;
- phat sinh false negatives tren CV;
- lam score sut vo ly o nhung JD dang on.

Vi du:

```text
Collaborate with engineering teams on API rollout
```

khong nen tu dong bien thanh:

```text
API rollout = must-have skill
```

### 3.3 Can giu provenance ro rang ngay tu dau

Ngay khi bat dau promote,
he thong khong the de requirement moi mat nguon goc.

Can phan biet ro:

- requirement viet ro trong section `requirements`
- requirement duoc promote tu responsibilities
- requirement unknown/open-set

Neu khong, Phase 36 se khong con dat de lam source-aware calibration.

### 3.4 Open-set phai thay duoc promoted unknown requirement

Co nhung technical signals duoc promote nhung khong nam trong taxonomy.

Vi du:

```text
Virtualization
Google Workspace
Meraki VPN
```

Neu da promote,
ma pipeline open-set khong nhin thay,
thi promotion van chua giai quyet xong bai toan sourcing.

## 4. Vi sao Phase 34 la buoc tiep theo dung nhat

Sau Phase 33, he thong da tra loi duoc cau hoi:

```text
responsibilities co technical signals nao?
```

Buoc tiep theo hop ly nhat la:

```text
signal nao xung dang duoc dua vao requirement matching?
```

Neu bo qua Phase 34 va nhay thang sang:

- role-family expansion
- scoring calibration

thi cac phase do se van chay tren mot scoring input con thieu technical core.

Noi cach khac:

```text
Phase 33 cho minh biet co gi trong responsibilities
Phase 34 moi thuc su dua duoc mot phan gia tri do vao screening
```

## 5. Nguyen tac thiet ke

### 5.1 Requirements van la nguon chinh

Phase 34 khong duoc dao nguoc triet ly:

```text
requirements = explicit source chinh
responsibilities = fallback source co kiem soat
```

### 5.2 Chi promote khi explicit technical requirements qua yeu

Promotion gate nen chi bat khi:

- `must_have_technical` rong;
- hoac rat it, khong du technical core;
- responsibilities lai technical-rich.

Neu JD da co requirements ro rang,
Phase 34 nen han che hoac khong promote.

### 5.3 Chi promote signal co specificity cao

Uu tien promote:

- technical noun phrase ro;
- action + technical object ro;
- platform/system/protocol ro;
- signal co the hien core task cua role.

Khong promote:

- soft skill;
- generic coordination task;
- domain-only phrase khong co technical object.

### 5.4 Can luu source metadata ngay trong phase nay

Moi requirement duoc promote can co metadata toi thieu:

- `source_kind = promoted_responsibility`
- `source_text`
- `signal_type`
- `promotion_reason`
- `promotion_specificity`

### 5.5 Backward-compatible o layer API

Phase 34 co the bo sung output moi,
nhung khong nen pha:

- CLI output contract lon
- screening API contract lon
- recommendation API contract lon

## 6. Kien truc de xuat

### 6.1 Luong xu ly moi

```text
Raw JD
  -> section parser
  -> typed requirement extractor
  -> responsibility signal extractor
  -> promotion gate
  -> scoring requirement entries
  -> known skill extraction / open-set extraction
  -> matching / scoring
```

### 6.2 Lop du lieu moi de bo sung

Can them 2 lop du lieu:

#### A. `promoted_requirements`

Day la danh sach co cau truc:

```json
[
  {
    "text": "Active Directory",
    "priority": "must_have",
    "source_kind": "promoted_responsibility",
    "source_text": "Manage Active Directory and troubleshoot DNS/DHCP issues.",
    "signal_type": "TECHNICAL_TASK",
    "specificity": "high",
    "promotion_reason": "sparse_explicit_technical_requirements"
  }
]
```

#### B. `scoring_requirement_entries`

Day la version co provenance cua scoring input:

```json
[
  {
    "text": "Java",
    "priority": "must_have",
    "source_kind": "explicit_requirement"
  },
  {
    "text": "Active Directory",
    "priority": "must_have",
    "source_kind": "promoted_responsibility"
  }
]
```

Layer nay rat quan trong vi Phase 36 se dua vao day de source-aware scoring.

### 6.3 Build scoring requirement lines van giu compatibility

De khong pha pipeline cu,
he thong co the van xuat:

- `must_have_skills`
- `nice_to_have_skills`

nhung nguon sinh ra chung luc nay se tu:

- explicit requirement entries
- promoted requirement entries

## 7. Promotion gate de xuat

### 7.1 Dieu kien bat gate

Promotion gate nen bat khi tat ca hoac da so dieu kien sau dung:

1. `must_have_technical` rong hoac it hon mot nguong nho.
2. `technical_responsibility_candidates` khong rong.
3. co it nhat 1 `responsibility_signal` co:
   - `signal_type` = `TECHNICAL_TASK` hoac `TECHNICAL_CONTEXT`
   - `specificity` = `high`

### 7.2 Dieu kien chan gate

Khong promote neu:

1. requirements da co technical core ro rang;
2. responsibilities chi co operational/general tasks;
3. technical candidate qua generic;
4. candidate chi xuat hien trong line nhu:
   - collaborate
   - coordinate
   - report
   - support internal communication

### 7.3 Gioi han so luong promotion

Can cap so requirement duoc promote,
vi du:

```text
toi da 3-5 promoted must-have requirements / JD
```

Muc tieu:

- du de khoi tao technical core;
- khong de responsibilities nuot het explicit requirements.

### 7.4 Priority o Phase 34

Phase 34 nen uu tien:

- `must_have` promotion

Chua can mo rong manh sang:

- `nice_to_have` promotion

de tranh phuc tap hoa gate qua som.

## 8. Quan he voi role-family

Phase 34 chua phai phase mo rong role-family lon.
Tuy nhien promotion gate van co the dung:

- title heuristics nho;
- domain context co san;
- role-family hien tai neu da co confidence kha.

Nguyen tac:

```text
Phase 34 dung role-awareness nhe de chan promotion nham
nhung chua phu thuoc vao role-family expansion day du.
```

Phase 35 se lam manh hon logic nay cho:

- IT Support
- Helpdesk
- Infrastructure
- Sysadmin
- Network Operations

## 9. Open-set va taxonomy coverage sau promotion

Sau khi mot requirement duoc promote:

### 9.1 Neu requirement co trong taxonomy

thi no di vao:

- `must_have_skills`
- `taxonomy_coverage.known_requirements`

### 9.2 Neu requirement khong co trong taxonomy

thi no can di vao:

- `open_set_requirement_candidates`
- va co the thanh `open_set_requirements`

neu qua duoc filter technical.

Noi cach khac:

```text
promotion phai noi duoc vao ca 2 nhanh:
- known skill matching
- open-set semantic matching
```

## 10. File du kien sua

### Sua chinh

```text
src/jd_requirement_classifier.py
src/payload_pipeline.py
src/screening_pipeline.py
src/requirement_extractor.py
```

### Co the them moi

```text
src/requirement_promotion.py
```

### Co the sua them nhe

```text
src/job_catalog_loader.py
src/job_quality_gate.py
```

### Test

```text
tests/test_requirement_promotion.py
tests/test_payload_pipeline.py
tests/test_screening_pipeline.py
tests/test_core_logic_benchmark.py
tests/test_job_catalog_loader.py
```

## 11. Expected behavior sau phase

Sau Phase 34,
ta ky vong cac case nhu Job 22 se chuyen tu:

```text
must_have_skills = []
open_set_requirements = []
```

thanh:

```text
must_have_skills = [mot so promoted technical requirements manh]
```

hoac:

```text
open_set_requirements = [mot so promoted unknown technical requirements]
```

Dong thoi:

- scoring input co technical core de matcher;
- score formula van giu nguyen;
- metadata cho biet requirement do den tu explicit hay promoted source.

## 12. Benchmark can khoa o Phase 34

Can co benchmark cho it nhat 5 nhom:

### 12.1 Sparse requirements, technical-rich responsibilities

Case kieu Job 22.

Ky vong:

- promotion duoc bat;
- technical core duoc dua vao scoring input;
- khong con `must_have_skills` rong.

### 12.2 Explicit requirements da manh

Backend / Fullstack / AI jobs viet ro ky nang o requirements.

Ky vong:

- promotion khong bat hoac bat rat nhe;
- score khong bi regression.

### 12.3 Responsibilities generic khong technical

Ky vong:

- khong promote bat ky requirement nao.

### 12.4 Responsibilities co unknown technical terms

Ky vong:

- unknown signal duoc promote vao open-set path;
- open-set filter van hoat dong sach.

### 12.5 Domain-heavy nhung technical-light

Ky vong:

- khong promote domain phrase thanh hard skill chi vi co nganh nghe lien quan.

## 13. Risk va cach chan regression

### 13.1 Over-promotion

Nguy co:

- responsibilities chi can co technical term la bi promote het.

Cach chan:

- gate bat theo explicit technical scarcity;
- cap so luong promotion;
- specificity threshold.

### 13.2 Promote nham domain context thanh skill

Nguy co:

- banking
- eKYC workflow
- infrastructure support

bi coi la hard skill khi line khong co technical object ro.

Cach chan:

- source signal phai co technical terms ro;
- domain-only lines khong promote.

### 13.3 Lam score roi manh qua som

Nguy co:

- score tang lon vi input list tang, trong khi formula chua phan biet source.

Cach chan:

- gioi han promoted count;
- chua tang weight;
- de Phase 36 lo source-aware calibration.

### 13.4 Pha recommendation pipeline candidate-side

Nguy co:

- job catalog va reranking lay them promoted requirements gay nhiu.

Cach chan:

- benchmark employer screening va candidate recommendation song song.

## 14. Dependency sanity check trong qua trinh code

Moi khi code Phase 34, can hoi nguoc 5 cau:

1. Minh dang dua candidate pool vao scoring input, hay dang sua score formula?
2. Promotion gate co bat ca tren explicit-technical-rich jobs khong?
3. Requirement moi co con giu source/provenance ro rang khong?
4. Unknown promoted requirements co di duong open-set dung khong?
5. Job generic/gioi thieu/placeholder co bi promote ao khong?

Neu trong qua trinh code phat hien:

- can them 1 field provenance nho;
- can them 1 negative heuristic nho;
- can them 1 benchmark sparse-JD case;

thi co the bo sung ngay trong Phase 34,
mien la van giu dung boundary:

```text
promotion gate va scoring input sourcing
chu chua source-aware calibration day du
```

## 15. Pham vi thuc hien cua Phase 34

Phase 34 nen tap trung:

- xay promotion gate;
- tao promoted requirement metadata;
- dua promoted requirements vao scoring input;
- noi promoted unknown requirements vao open-set path;
- benchmark sparse-JD sourcing cases.

Phase 34 chua nen:

- sua weight scoring;
- sua hard-skill gate formula lon;
- mo rong role-family rong cho cac nhom helpdesk/infra;
- sua UI/web contract lon.

## 16. Phase 34 duoc xem la hoan thanh khi

1. Job sparse requirements co the tao duoc technical scoring input tu responsibilities.
2. Job explicit-technical-rich khong bi over-promotion.
3. Promoted requirements giu duoc source metadata ro rang.
4. Unknown promoted requirements van di dung qua open-set filtering.
5. Benchmark Phase 26-33 van pass.
6. Co test moi khoa lai sparse-JD promotion behavior.

## 17. Gia tri bao cao do an

Phase 34 co gia tri lon khi bao cao vi co the giai thich:

```text
He thong khong chi biet phat hien technical intent trong responsibilities,
ma con biet dua no vao matching mot cach co kiem soat khi JD viet thieu o phan requirements.
```

Day la buoc rat thuc te vi:

- recruiter va employer khong viet JD dong deu;
- technical core thuong nam trong task descriptions;
- nhung he thong screening van phai giu duoc tinh explainable va khong over-score.

## 18. Huong sau Phase 34

Neu Phase 34 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 35 - IT Support / Infrastructure Role-family Expansion
```

Phase 35 se tap trung:

- mo rong coverage cho nhom role dang yeu;
- giup promotion gate hieu ro hon role nao dang xung dang duoc promote;
- chan false promotion tot hon truoc khi sang Phase 36 scoring calibration.
