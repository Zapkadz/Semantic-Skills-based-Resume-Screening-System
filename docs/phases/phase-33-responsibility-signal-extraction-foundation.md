# Phase 33 - Responsibility Signal Extraction Foundation

## 1. Muc tieu phase

Sau Phase 32, he thong da sua duoc mot cum logic quan trong:

- typed requirement schema;
- open-set technical filtering;
- role-family technical intent inference;
- role-aware scoring calibration;
- role-aware unknown skill governance;
- context-rich evidence recovery.

Nhung khi replay cac case kho nhu Job 22, van con mot nhom benh chua duoc sua dut diem:

```text
JD_REQUIREMENT_SOURCING_GAP
```

Noi ngan gon:

```text
Phase 27-32 = requirement typing, open-set, role-aware scoring, CV evidence da tot hon
Phase 33 = bat dau sua tan goc phan responsibilities cua JD
```

Muc tieu cua Phase 33 la:

```text
Khong de phan responsibilities / description chi dung vai tro context nua,
ma phai nhan dien duoc technical task signals ben trong no de phuc vu
promotion co kiem soat o phase sau.
```

Rat quan trong:

```text
Phase 33 CHUA promote responsibilities thanh scoring requirements.
Phase 33 chi xay nen tang extraction va candidate pool.
```

## 2. Vi tri cua Phase 33 trong cay dependency

Day la phase dau tien cua nhanh sua section-aware JD sourcing:

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
Phase 33 chi sua upstream extraction.
Khong nhay thang vao scoring.
Khong vao hard-skill gate.
Khong vao review card wording tru khi can metadata toi thieu de debug.
```

## 3. Van de can giai quyet

### 3.1 Responsibilities hien tai dang bi xem la context gan nhu "dong hang"

Trong logic hien tai, line nam trong section:

- `description`
- `responsibilities`

thuong di vao:

```text
RESPONSIBILITY_CONTEXT
```

Dieu nay an toan cho nhieu case,
nhung lam he thong mat kha nang nhin thay technical core that su duoc viet trong task.

### 3.2 Nhieu JD thuc te dat technical core o description, khong dat o requirements

Case thuc te da lo ra:

```text
Title: IT Staff / IT Support / IT Helpdesk
Requirements:
- 3 years experience
- good English
- enthusiastic

Responsibilities:
- manage Active Directory
- support DNS / DHCP
- maintain firewall / router / switch
- handle VPN / Google Workspace / server issues
```

Neu he thong chi dung `requirements` de tao scoring input,
thi:

- hard-skill core bi rong;
- open-set khong co du requirement de chay;
- scoring chi con baseline experience / domain / seniority.

### 3.3 Technical task va general duty dang chua duoc tach ro

Trong responsibilities thuong co lan:

- technical task;
- domain task;
- coordination / collaboration task;
- generic operational task;
- soft / attitude phrasing.

Vi du:

```text
Collaborate with internal teams
```

khong nen duoc xem giong muc:

```text
Administer Active Directory and troubleshoot DNS/DHCP
```

Neu khong tach ro ngay tu dau,
Phase 34 se rat de promote nham.

### 3.4 He thong chua co "candidate pool" rieng cho technical responsibilities

Hien tai pipeline co:

- typed requirements
- requirement groups
- must-have technical
- nice-to-have technical

Nhung chua co lop trung gian kieu:

```text
technical_responsibility_candidates
```

Day la lo hong kien truc.
Khong co candidate pool rieng thi:

- hoac bo sot technical signals;
- hoac pha vo boundary va dua thang tat ca vao must-have.

## 4. Vi sao Phase 33 la buoc tiep theo dung nhat

Sau Phase 32, neu diem van thap o cac case kho,
thi can hoi nguoc:

```text
CV co bang chung hay khong?
```

voi Job 22, cau tra loi la:

```text
Co kha nang CV co bang chung,
nhung JD chua phat bieu du technical requirements de he thong hoi dung cau hoi.
```

Noi cach khac:

```text
Evidence detector da tot hon,
nhung job-side chua tao du technical intent de matcher va scorer dung.
```

Neu nhay thang sang Phase 34 promotion ngay bay gio ma khong co foundation,
he thong rat de:

- promote qua tay;
- keo nham non-technical duties vao must-have;
- lam regression o nhung job dang on.

Vi vay Phase 33 la buoc tiep theo hop ly nhat vi:

1. no sua dung upstream gap;
2. no khong pha scorer ngay;
3. no tao du du lieu de Phase 34 lam promotion co kiem soat;
4. no giu duoc logic sach theo dung dependency tree.

## 5. Nguyen tac thiet ke

### 5.1 Requirements van la nguon scoring chinh

Phase 33 khong doi triet ly nay:

```text
requirements = nguon chinh
responsibilities = nguon bo tro co kiem soat
```

### 5.2 Tach extraction khoi promotion

Phase 33 chi can tra loi:

```text
Trong responsibilities nay co technical task signal nao dang de y?
```

Chu chua tra loi:

```text
Signal nao se duoc dua vao scoring?
```

### 5.3 Uu tien high-specificity technical spans

Candidate pool nen uu tien:

- tool / platform / protocol / system names;
- infra components;
- engineering operations;
- model / deployment operations;
- concrete technical action-object pairs.

Khong uu tien:

- vague coordination verbs;
- soft skill language;
- generic business duties.

### 5.4 Backward-compatible voi output hien tai

Phase 33 nen bo sung metadata moi,
nhung khong pha:

- screening API contract lon;
- recommendation API contract lon;
- scorer inputs hien tai.

Cho phep:

- them field moi vao parser / pipeline output;
- them diagnostics/debug payload;
- tests moi.

### 5.5 Co benchmark khoa lai ngay tu phase nay

Ngay ca khi chua promote,
Phase 33 van phai benchmark duoc:

```text
technical responsibility candidate pool co duoc tao dung hay khong
```

## 6. Kien truc de xuat

### 6.1 Luong xu ly moi tren phia JD

```text
Raw JD text
  -> section parser
  -> typed requirement extractor
  -> responsibility signal extractor
  -> technical_responsibility_candidates
  -> requirement groups + diagnostics
```

### 6.2 Lop output moi de bo sung

De xuat them metadata moi trong `job_criteria`:

```json
{
  "responsibility_signals": [
    {
      "text": "Manage Active Directory and troubleshoot DNS/DHCP",
      "signal_type": "TECHNICAL_TASK",
      "technical_terms": ["Active Directory", "DNS", "DHCP"],
      "specificity": "high",
      "section": "responsibilities"
    }
  ],
  "technical_responsibility_candidates": [
    "Active Directory",
    "DNS",
    "DHCP"
  ]
}
```

### 6.3 Hai lop thong tin can giu

#### A. Responsibility signal block

Dung cho:

- debug;
- benchmark;
- role-family support;
- giai thich vi sao phase sau promote hay khong.

#### B. Flattened technical responsibility candidates

Dung cho:

- Phase 34 promotion gate;
- Phase 35 role-family alignment;
- diagnostics.

## 7. Rule huong dan extraction o Phase 33

### 7.1 Nen nhan dien cac mau technical responsibility nhu:

- action + technical object
- maintain / operate / deploy / monitor + system
- troubleshoot / administer / configure + infra component
- build / develop / integrate + technical module

Vi du:

```text
configure firewall
monitor servers
maintain VPN connectivity
deploy ONNX models on edge devices
```

### 7.2 Nen nhan dien technical noun phrases manh

Vi du:

- Active Directory
- DNS
- DHCP
- router
- switch
- firewall
- virtualization
- Google Workspace
- ONNX
- PyTorch
- Kubernetes

### 7.3 Can discard hoac danh dau muc thap voi:

- collaborate with team
- support business growth
- communicate with stakeholders
- eager to learn
- work under pressure

### 7.4 Nen giu domain task rieng, khong tron vao technical candidate

Vi du:

- support eKYC onboarding workflows
- handle fraud-review escalation

nhung neu line dong thoi chua technical terms manh,
thi tach:

- domain context
- technical terms

## 8. File du kien sua

### Sua chinh

```text
src/jd_requirement_classifier.py
src/technical_intent.py
src/requirement_types.py
```

### Co the them moi

```text
src/responsibility_signal_extractor.py
```

### Pipeline can cap nhat nhe

```text
src/payload_pipeline.py
src/screening_pipeline.py
src/job_catalog_loader.py
```

### Test

```text
tests/test_jd_requirement_classifier.py
tests/test_payload_pipeline.py
tests/test_screening_pipeline.py
tests/test_core_logic_benchmark.py
```

Neu can,
co the them test file rieng:

```text
tests/test_responsibility_signal_extractor.py
```

## 9. Expected behavior sau phase

Sau Phase 33,
he thong chua scoring khac di qua nhieu,
nhung parser/pipeline phai bieu lo duoc:

1. responsibilities nao co technical task signal;
2. technical terms nao duoc trich ra tu responsibilities;
3. candidate pool technical responsibilities co duoc tao on dinh;
4. candidate pool nay chua tu dong bien thanh must-have.

Vi du voi Job 22,
ta ky vong thay:

```text
technical_responsibility_candidates ~
[
  "Active Directory",
  "DNS",
  "DHCP",
  "Firewall",
  "Router",
  "Switch",
  "VPN",
  "Google Workspace",
  "Virtualization"
]
```

Nhung:

```text
must_have_skills
```

co the van chua doi o Phase 33.

Dieu do la dung,
vi promotion la viec cua Phase 34.

## 10. Benchmark can khoa o Phase 33

Can co benchmark cho it nhat 4 nhom:

### 10.1 Responsibilities technical-rich, requirements sparse

Case kieu Job 22:

- requirements yeu / chung chung;
- responsibilities technical-rich.

Ky vong:

- candidate pool duoc tao dung;
- technical signals khong bi bo sot.

### 10.2 Responsibilities generic, khong technical

Vi du:

- coordinate with teams
- report progress
- support internal communication

Ky vong:

- khong tao candidate pool technical ao.

### 10.3 Responsibilities co technical va domain context tron lan

Vi du:

```text
Support eKYC onboarding systems and monitor liveness detection service health
```

Ky vong:

- tach duoc domain context;
- giu duoc technical terms manh.

### 10.4 Job dang on voi requirements ro rang

Backend / Fullstack / AI jobs dang chay on.

Ky vong:

- typed requirements cu van on;
- candidate pool moi neu co thi cung khong anh huong score o Phase 33.

## 11. Risk va cach chan regression

### 11.1 Over-extraction

Nguy co:

- line nao trong responsibilities cung bi coi la technical.

Cach chan:

- uu tien specificity;
- can technical noun phrases / action-object patterns;
- test negative cases.

### 11.2 Lech boundary voi soft skill

Nguy co:

- `eager to learn`
- `good communication`

bi lot vao candidate pool.

Cach chan:

- reuse soft-skill markers tu Phase 27-28;
- benchmark ro nong/lanh.

### 11.3 Pha role-family truoc khi role-family duoc mo rong

Nguy co:

- extractor gan technical term qua manh cho role chua co coverage.

Cach chan:

- Phase 33 chi extract candidate pool;
- chua dung candidate pool de score.

## 12. Dependency sanity check trong qua trinh code

Moi khi code Phase 33, can hoi nguoc 4 cau:

1. Minh dang extract signal hay da lén promote vao scoring?
2. Minh dang bo sung metadata hay da thay doi diem?
3. Case generic responsibilities co bi tao technical candidate ao khong?
4. Case requirements ro rang co bi anh huong hanh vi cu khong?

Neu trong qua trinh code phat hien:

- can them 1 signal type nho;
- can them 1 negative heuristic nho;
- can them 1 benchmark fixture nho;

thi co the bo sung ngay trong Phase 33,
mien la van giu dung ranh gioi:

```text
extraction foundation, chua promotion, chua scoring calibration
```

## 13. Pham vi thuc hien cua Phase 33

Phase 33 nen tap trung:

- extraction foundation cho responsibilities;
- candidate pool technical responsibilities;
- metadata va diagnostics toi thieu de benchmark;
- benchmark parser/pipeline cho nhom benh sourcing gap.

Phase 33 chua nen:

- promote candidate pool thanh must-have;
- sua score formula;
- sua review card wording lon;
- sua web integration lon.

## 14. Phase 33 duoc xem la hoan thanh khi

1. Parser/pipeline co duoc `technical_responsibility_candidates`.
2. Case Job 22 va cac case cung nhom trich duoc technical signals hop ly.
3. Case responsibilities generic khong tao candidate pool technical ao.
4. Screening/recommendation outputs van backward-compatible.
5. Benchmark Phase 26-32 van pass.
6. Co test moi khoa lai nhom sourcing gap foundation.

## 15. Gia tri bao cao do an

Phase 33 co gia tri lon khi bao cao vi co the giai thich:

```text
He thong khong gia dinh rang ky thuat chi nam o section requirements.
No bat dau hoc cach doc responsibilities nhu mot nguon technical intent,
nhung van giu co che kiem soat de khong lam score bi ao.
```

Day la mot buoc rat thuc te,
vi research va JD ngoai doi deu cho thay:

- recruiter viet skill khong deu tay;
- title co the mo ho;
- technical core thuong nam trong task descriptions.

## 16. Huong sau Phase 33

Neu Phase 33 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 34 - Controlled Responsibility-to-Requirement Promotion
```

Phase 34 se tap trung:

- khi nao candidate pool duoc dua vao scoring;
- dua bao nhieu;
- gan source cho requirement;
- khong de over-promotion gay score ao.
