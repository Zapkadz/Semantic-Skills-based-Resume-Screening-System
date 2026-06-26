# Phase 37 - Sparse-JD Technical Core Recovery

## 1. Muc tieu phase

Sau Phase 33-36, he thong da co:

- section-aware JD parsing;
- typed requirement grouping;
- responsibility signal extraction;
- controlled promotion;
- IT support / infra role-family expansion;
- source-aware scoring calibration.

Tuy nhien, van con mot nhom benh logic chua duoc xu ly dut diem:

```text
JD co technical signal manh trong responsibilities / description,
nhung explicit requirements lai:
- ngheo technical,
- lan soft skill,
- hoac technical qua mo ho de dua thang vao scoring.
```

Ket qua la:

```text
upstream parser van thay technical responsibility candidates,
nhung scoring input cuoi cung lai co the gan nhu rong.
```

Muc tieu cua Phase 37 la:

```text
Phuc hoi "technical core" cho cac sparse JD mot cach co kiem soat,
ma khong hard-code theo tung job,
khong pha vo scoring logic da on dinh cua cac JD tot.
```

Rat quan trong:

```text
Phase 37 chua sua web UI lon.
Phase 37 chua vao benchmark rong.
Phase 37 tap trung sua core extraction / promotion gate / recovery logic.
```

Noi ngan gon:

```text
Phase 33 = thay technical signal trong responsibilities
Phase 34 = promotion co kiem soat
Phase 35 = dat signal do vao dung role-family
Phase 36 = cham diem theo nguon requirement
Phase 37 = dam bao sparse JD van tao duoc technical core dung de cham
```

## 2. Vi tri cua Phase 37 trong cay dependency moi

Day la phase duoc chen vao giua de chua dung benh logic truoc khi lam guardrails va benchmark:

```text
Phase 33 -> Responsibility signal extraction foundation
Phase 34 -> Controlled responsibility-to-requirement promotion
Phase 35 -> IT support / infra role-family expansion
Phase 36 -> Source-aware scoring calibration
Phase 37 -> Sparse-JD technical core recovery
Phase 38 -> Confidence and diagnostics guardrails   (Phase 37 cu)
Phase 39 -> Benchmark and regression pack           (Phase 38 cu)
```

Ly do phai chen Phase 37 vao day:

```text
Neu lam guardrails truoc:
- he thong chi giai thich cai sai tot hon
- nhung diem van sai

Neu lam benchmark truoc:
- minh benchmark mot logic chua duoc chua dut diem
```

Nguyen tac de khong bi lech huong:

```text
Phase 37 chi sua:
- requirement typing / cleanup
- explicit-technical usability gating
- sparse-JD recovery trigger
- role-aware responsibility-to-core recovery

Phase 37 chua sua:
- web contract lon
- benchmark rong
- admin taxonomy flow lon
- recommendation preference ranking
```

## 3. Van de can giai quyet

### 3.1 Benh hien tai khong phai cache, ma la scoring input bi rong

Case job 22 cho thay:

- web van goi API moi;
- request / response van tao trace_id moi;
- nhung `must_have_skills`, `open_set_requirements`, `requirement_provenance_summary`
  co the ve gan nhu rong.

Dieu nay co nghia la:

```text
benh nam o lop tao scoring input,
khong phai o DB cache hay session cache.
```

### 3.2 Soft-skill contamination dang chan recovery

Mot so line nhu:

- `Enthusiastic and eager to learn`
- `Hard working`
- `Good attitude`
- `Can work independently`

co the bi roi vao `must_have_technical`
neu classifier khong tach du soft skill.

Khi do, promotion gate hien tai thay:

```text
da co explicit technical roi
```

va dung recovery,
du thuc chat explicit technical do khong the dung de cham hard-skill fit.

### 3.3 Promotion gate hien tai dang dua tren "non-empty", chua dua tren "usable"

Trong `src/requirement_promotion.py`,
gate hien tai chu yeu co logic:

```text
neu explicit_required_lines khac rong thi khong promote
```

Dieu do dung voi JD tot,
nhung sai voi sparse JD contaminated.

Thieu sot logic la:

```text
explicit technical co the "co text"
nhung khong "du dac hieu de dung cho scoring".
```

### 3.4 Responsibilities co technical core that su, nhung dang bi de o context

Nhieu JD ngoai doi viet:

- requirement section rat ngan;
- responsibilities section lai liet ke tool / platform / task rat ky.

Vi du:

- DNS
- DHCP
- Firewall
- Router
- Switch
- VPN
- Server
- Active Directory
- SAP

Nhung neu khong co recovery dung cach,
he thong chi biet day la context,
ma khong dua duoc vao matching/scoring input.

### 3.5 Source-aware scoring khong cuu duoc neu upstream khong co requirement core

Phase 36 da lam scorer hieu:

- explicit > promoted > semantic-only

Nhung neu Phase 37 khong tao duoc technical core hop le,
thi scorer van khong co gi de tinh.

Noi cach khac:

```text
Phase 36 giai bai toan "cham requirement nao nang hon"
Phase 37 giai bai toan "co requirement technical hop le nao de cham hay chua"
```

## 4. Co so lua chon huong giai quyet

Huong cua phase nay phu hop voi cach bai toan duoc xu ly trong tai lieu:

1. `JobFormer` xem JD gom nhieu item duties va requirements rieng,
   khong nen dap thanh mot khoi text duy nhat.
   Dieu nay ung ho huong section-aware hien tai cua minh.

2. Nghien cuu `job-task-skill pattern` lap luan rang
   job tasks la cau noi giua cong viec va ky nang yeu cau.
   Dieu nay ung ho viec dung responsibilities lam nguon phuc hoi technical core,
   nhung phai co kiem soat.

3. `Skill Extraction from Job Postings using Weak Supervision`
   cho thay taxonomy la anchor tot,
   nhung khong du neu chi dua vao exact lexical match.
   Can co retrieval / latent similarity / skill recovery.

4. Nghien cuu ve soft skills trong job ads cho thay
   soft skill xuat hien rat nhieu va de lam ban hard-skill extraction
   neu khong tach rieng.

5. ESCO va O*NET deu tach:
   - tasks / work activities
   - worker requirements / skills / knowledge
   - occupation context

   Dieu nay rat phu hop voi huong:

```text
explicit requirements la nguon chinh
responsibilities la nguon phuc hoi co provenance
scoring phai biet requirement do den tu dau
```

## 5. Nguyen tac thiet ke cua Phase 37

### 5.1 Khong hard-code theo job

Khong duoc sua theo kieu:

```text
neu job_id = 22 thi promote them DNS, DHCP, Firewall...
```

Huong dung phai la:

```text
neu JD thuoc nhom sparse technical,
explicit technical khong usable,
va responsibilities co technical signals du manh,
thi kich hoat recovery.
```

### 5.2 Explicit requirement van la nguon uu tien so 1

Recovery khong duoc lat nguoc nghiep vu.

He thong van phai giu:

- explicit must-have la nguon manh nhat;
- promoted responsibility chi la fallback technical source;
- semantic-only chi la evidence bo tro.

### 5.3 Recovery phai role-aware

Khong phai bat ky technical term nao trong responsibilities cung duoc dua vao core.

Vi du:

- `DNS`, `DHCP`, `Firewall`, `Router`, `Switch`, `VPN`
  hop ly voi `IT_SUPPORT_INFRA`
- `Spring Boot`, `REST API`, `SQL`
  hop ly voi `BACKEND_ENGINEERING`
- `Face Recognition`, `Liveness Detection`
  hop ly voi `COMPUTER_VISION_EKYC`

### 5.4 Recovery phai bounded

Neu promote qua nhieu term,
he thong se over-score sparse JD
va bien responsibilities thanh requirements mot cach vo to chuc.

Vi vay can:

- cap so requirement duoc promote;
- uu tien theo intent bucket;
- tranh promote toan bo line hoac toan bo term.

### 5.5 Soft skill, language, education, experience phai tiep tuc tach rieng

Phase 37 khong phai "ky thuat hoa" moi thu.

Can bao toan cac nhom:

- education
- experience
- language
- soft skills
- domain context

Chi technical core moi duoc recovery vao matching/scoring.

## 6. Pham vi implementation de xuat

## 6.1 Tang "explicit technical usability"

Can bo sung mot lop danh gia moi:

```text
explicit technical line co ton tai khong?
va neu co thi co usable cho scoring hard-skill hay khong?
```

De xuat metadata moi:

- `raw_explicit_technical_count`
- `usable_explicit_technical_count`
- `explicit_technical_contamination_count`
- `explicit_technical_recovery_triggered`
- `explicit_technical_recovery_reason`

`usable_explicit_technical_count` chi tang khi line:

- thuc su thuoc technical requirement type;
- khong match soft-skill contamination;
- co du specificity;
- hoac map vao taxonomy / curated technical terms / role-aware intent signal.

## 6.2 Chua contamination o requirement classifier

Can sua `src/jd_requirement_classifier.py` de:

- mo rong soft-skill markers cho nhom:
  - enthusiastic
  - eager to learn
  - proactive
  - willing to learn
  - positive attitude
  - hard working
  - careful
- khong de generic human-quality lines roi vao `TECH_SKILL`
  chi vi chung dang nam trong section `requirements`

Nguyen tac moi:

```text
khong classify sang must_have_technical
neu line khong co technical substance du dung.
```

## 6.3 Sua promotion gate tu "non-empty" sang "usable"

Can sua `src/requirement_promotion.py`:

Truoc day:

```text
neu explicit_required_lines != []
=> khong promote
```

Sau Phase 37:

```text
neu usable_explicit_technical_count dat nguong toi thieu
=> khong promote

neu explicit technical chi la contamination / low specificity / discarded
=> cho phep recovery tu responsibilities
```

Nguong toi thieu de xuat:

- `usable_explicit_technical_count >= 1` cho role da rat ro va JD ngan
- `usable_explicit_technical_count >= 2` cho role technical dau vao phong phu

Nguong cu the co the role-aware,
nhung implementation dau nen giu don gian, on dinh.

## 6.4 Role-aware technical core recovery

Can dung:

- `responsibility_signals`
- `technical_responsibility_candidates`
- `job_role_profile`
- `requirement_intent_summary`

de chon nhung term technical hop le dua vao scoring input.

De xuat:

- voi `IT_SUPPORT_INFRA`
  - uu tien `NETWORK_OPERATIONS`
  - sau do `INFRA_IDENTITY_ADMIN`
  - sau do `SYSTEM_OPERATIONS`
- voi role khac,
  - tiep tuc dung intent bucket da co

Khong phai cu co term la promote.
Can them luat:

- uu tien da dang bucket;
- tranh trung nghia;
- tranh term qua generic;
- tranh promote line-day du thay vi term technical.

## 6.5 Keep provenance ro rang

Moi requirement duoc recovery phai tiep tuc mang:

- `source_kind = promoted_responsibility`
- `source_text`
- `intent_type`
- `intent_strength`
- `promotion_reason`

De Phase 36 scorer va cac phase sau van dung duoc.

## 6.6 Khong doi web/API contract lon trong phase nay

Phase 37 nen co gang giu:

- endpoint cu;
- payload shape chinh cu;
- web khong can sua de moi logic chay duoc.

Neu can metadata moi,
chi nen them dang optional.

## 7. File / module du kien can sua

Nhung file kha nang cao se duoc dong vao:

- `src/jd_requirement_classifier.py`
- `src/requirement_promotion.py`
- `src/open_set_requirement_filter.py`
- `src/responsibility_signal_extractor.py`
- `src/technical_intent.py`
- `src/screening_pipeline.py`
- `src/payload_pipeline.py`
- `src/job_catalog_loader.py`

Co the can dong nhe vao:

- `src/review_card_generator.py`
- `src/scorer.py`

nhung chi khi can preserve metadata moi cho log/explanation.

Web/PHP:

```text
khong bat buoc sua trong Phase 37
```

neu API contract van backward-compatible.

## 8. Hanh vi mong doi sau Phase 37

### 8.1 Voi sparse IT support / infra JD

He thong nen:

- khong xem soft skill la explicit technical core;
- cho phep recovery technical core tu responsibilities;
- tao ra mot bo requirement technical hop ly de match:
  - DNS
  - DHCP
  - Firewall
  - Router
  - Switch
  - VPN
  - Server
  - SAP / AD / Workspace tuy theo signal

Nhung:

- khong can lay het;
- khong can nang thanh explicit 100%;
- van giu source-aware scoring.

### 8.2 Voi JD backend / CV / security da viet dep

He thong nen:

- gan nhu khong thay doi hanh vi;
- khong kich hoat recovery neu explicit technical da du usable;
- giu score on dinh.

### 8.3 Voi JD toan soft skill / toan metadata

He thong nen:

- khong "tu ve" ra technical core;
- recovery khong kich hoat neu responsibilities khong co technical signal hop le;
- tiep tuc score thap hoac confidence thap.

## 9. Acceptance criteria

Phase 37 duoc xem la dat neu:

1. Case job 22 khong con roi vao trang thai:
   - `must_have_skills = []`
   - `open_set_requirements = []`
   - `promoted_requirements = []`
   trong khi `technical_responsibility_candidates` lai phong phu.

2. Soft-skill contamination giam ro:
   - `Enthusiastic and eager to learn`
   - `Willing to learn`
   - `Good attitude`
   khong con chan recovery technical.

3. Role support / infra sparse co the tao duoc technical core recover hop le.

4. Cac JD explicit technical manh (backend, CV, security) khong bi drift score lon.

5. API/web contract van backward-compatible.

6. Full test suite pass.

## 10. Test plan de xuat

### 10.1 Unit test cho contamination cleanup

Them test dam bao:

- `enthusiastic and eager to learn` -> `SOFT_SKILL`
- `good attitude` -> `SOFT_SKILL` hoac `ignored`
- khong roi vao `must_have_technical`

### 10.2 Unit test cho explicit usability gate

Them test dam bao:

- explicit technical generic / soft-only -> `usable_explicit_technical_count = 0`
- explicit technical dung nghia -> `usable_explicit_technical_count > 0`

### 10.3 Unit test cho sparse recovery trigger

Them test cho JD dang:

- requirements = education + experience + language + soft skill
- responsibilities = DNS / DHCP / Firewall / VPN / Server

Ky vong:

- recovery trigger bat;
- co promoted requirements / open-set requirements hop le.

### 10.4 Negative test cho over-promotion

Them test dam bao:

- responsibilities chi chung chung (`coordinate`, `report`, `support users`)
  thi khong recovery technical core.

### 10.5 Regression test cho job families cu

Them regression test:

- backend JD
- CV/eKYC JD
- security JD
- IT support / infra JD

Muc tieu:

- sparse JD duoc cai thien;
- cac JD khac khong bi pha logic.

### 10.6 API / payload test

Them test dam bao:

- metadata moi co the xuat hien ma khong pha schema cu;
- response van map duoc vao web hien tai.

## 11. Rui ro va cach giam rui ro

### 11.1 Rui ro over-promotion

Neu recover qua nhieu term,
score co the bi nang oan.

Giam rui ro bang:

- cap so term recover;
- role-aware bucket priority;
- source-aware scoring van giu promoted < explicit.

### 11.2 Rui ro drift score tren JD tot

Neu gate moi qua hung,
co the thay doi score cua backend/CV/security JD tot.

Giam rui ro bang:

- recovery chi bat khi explicit technical khong usable;
- them regression tests cho cac job da on.

### 11.3 Rui ro soft-skill list chua du

Khong the liet ke het soft-skill phrasings ngay lap tuc.

Giam rui ro bang:

- bat dau tu nhom phrasings generic pho bien;
- uu tien gate "usable explicit technical"
  de du soft-skill marker chua bao phu het
  thi van kho chan recovery mot cach sai.

## 12. Khong nam trong pham vi Phase 37

Phase nay chua lam:

- UI recruiter confidence badges moi
- web diagnostics panels moi
- benchmark dataset rong
- import full ESCO / O*NET
- GPT refinement / rewrite JD
- admin flow moi

Nhung phase sau moi lam:

- Phase 38 = confidence / diagnostics guardrails
- Phase 39 = benchmark / regression pack

## 13. Gia tri nghiep vu va gia tri bao cao

Phase 37 co gia tri rat lon vi co the giai thich:

```text
He thong khong chi doc xem requirement co ton tai hay khong.
No con danh gia requirement do co du chat technical de dung cham hay khong.
Neu requirement viet qua ngheo nhung responsibilities cho technical signal ro,
he thong se phuc hoi technical core mot cach co kiem soat.
```

Day la mot huong rat thuc te,
vi ngoai doi employer viet JD khong dong deu.

Neu khong co Phase 37:

- sparse JD bi cham thieu;
- support / infra role de bi roi vao low-score oan;
- guardrails chi "bao loi" ma khong chua loi.

## 14. Dau ra mong doi cua phase

Sau khi xong Phase 37, repo nen co:

- core logic phat hien sparse technical JD chac hon;
- recovery gate dua tren `usable explicit technical`;
- regression tests cho contamination va sparse recovery;
- metadata noi bo du de Phase 38 tiep tuc expose confidence / diagnostics.

## 15. Huong sau Phase 37

Neu Phase 37 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 38 - Confidence and Diagnostics Guardrails
```

Phase 38 se tap trung:

- expose ro hon sparse-JD recovery da kich hoat hay chua;
- canh bao recruiter khi requirement technical explicit yeu / contaminated;
- dua confidence / diagnostics ra API/web ro hon;
- giup debug nhanh ma khong can doc file raw trong `api-debug`.

Sau do moi den:

```text
Phase 39 - Benchmark and Regression Pack
```

de khoa hanh vi dung cho:

- backend JD
- CV/eKYC JD
- security JD
- IT support / infra sparse JD
- noisy / low-quality JD
