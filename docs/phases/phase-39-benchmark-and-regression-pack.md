# Phase 39 - Benchmark and Regression Pack

## 1. Muc tieu phase

Sau Phase 33-38, he thong da sua duoc mot chuoi benh logic rat quan trong:

- tach requirement tot hon;
- loc open-set technical tot hon;
- hieu role-family tot hon;
- cham diem theo source;
- phuc hoi technical core cho sparse JD;
- expose confidence va diagnostics ro hon.

Noi ngan gon:

```text
Phase 33-38 da sua logic cot loi va lop guardrails
Phase 39 khoa lai nhung hanh vi dung do thanh benchmark song
```

Van de hien tai la:

```text
he thong da tot hon rat nhieu,
nhung neu khong co regression pack dung nghia,
thi moi lan sua phase sau rat de:
- lam dep case nay,
- vo case khac,
- ma khong biet ngay.
```

Muc tieu cua Phase 39 la:

```text
Dong bang nhung hanh vi mong doi quan trong nhat cua he thong
thanh mot benchmark/regression pack co the chay lai duoc,
bao gom:
- employer-side screening
- candidate-side recommendation
- sparse/noisy JD
- explicit-rich JD
- open-set / multilingual / evidence-recovery cases
- confidence / diagnostics expectations
```

Rat quan trong:

```text
Phase 39 khong sua core logic lon de "cai diem".
Phase 39 tap trung:
- benchmark fixtures
- regression expectations
- parity assertions
- confidence/diagnostics invariants
```

## 2. Vi tri cua Phase 39 trong cay dependency hien tai

Sau khi da hoan tat Phase 38, thu tu hop ly hien tai la:

```text
Phase 33 -> Responsibility signal extraction foundation
Phase 34 -> Controlled responsibility-to-requirement promotion
Phase 35 -> IT support / infra role-family expansion
Phase 36 -> Source-aware scoring calibration
Phase 37 -> Sparse-JD technical core recovery
Phase 38 -> Confidence and diagnostics guardrails
Phase 39 -> Benchmark and regression pack
```

Ly do Phase 39 dung sau Phase 38:

```text
neu benchmark truoc khi confidence/diagnostics on dinh,
thi benchmark moi khoa score ma chua khoa duoc ly do va warning.

sau Phase 38,
he thong da co du:
- score
- role/source impacts
- confidence guardrails
- diagnostics reason codes
=> luc nay moi nen khoa hanh vi toan dien.
```

Noi cach khac:

```text
Phase 37-38 giup he thong "dung hon va noi ro hon"
Phase 39 giup he thong "giu duoc cai dung do khi minh sua tiep"
```

## 3. Van de can giai quyet

### 3.1 Unit tests hien tai manh, nhung van chua du cho regression he thong

Repo hien tai da co rat nhieu test rat tot:

- parser tests
- matching tests
- scoring tests
- payload tests
- recommendation tests
- confidence guardrail tests

Nhung van can mot lop regression pack co tinh he thong hon,
de tra loi cau hoi:

```text
neu toi sua parser/scoring/guardrails sau nay,
toan bo bai toan employer + candidate co bi drift khong?
```

### 3.2 Cac case kho da duoc sua nhung chua duoc "dong bang" du chat

Trong qua trinh lam du an, da co nhieu case kho rat thuc te:

- JD placeholder / test / thieu requirement;
- JD support/infra sparse nhung responsibilities rat technical;
- CV khong co section Skills nhung evidence manh nam trong project/work;
- hard-skill thieu nhung experience nhieu;
- open-set technical skill chua nam trong taxonomy;
- employer-side screening va candidate-side recommendation phai giu core logic thong nhat;
- confidence/diagnostics phai noi dung muc do tin cay.

Neu nhung case nay chi "pass nho tri nho cua minh",
thi sau nay rat de bi mat.

### 3.3 Chua co expectation ro cho confidence va diagnostics regression

Sau Phase 38,
ket qua khong chi la:

- `final_score`
- `recommendation`

ma con co:

- `confidence_guardrails`
- `decision_confidence`
- `reason_codes`
- `diagnostics.runtime.*`

Nhung neu khong benchmark lop nay,
thi sau nay co the xay ra:

```text
score van pass
nhung warning code bi mat
confidence bi nham muc
diagnostics khong con phan biet duoc case kho
```

### 3.4 Chua co bo "acceptance cases" dai dien cho tung ho failure taxonomy

Phase 26 da tao benchmark foundation va failure taxonomy.
Nhung sau Phase 27-38, he thong da phuc tap hon nhieu.

Luc nay can nang cap benchmark thanh regression pack co chu dich:

- moi ho bug chinh phai co case dai dien;
- moi case phai khoa khong chi score,
  ma ca parse/match/explanation/confidence.

## 4. Vi sao Phase 39 la buoc tiep theo dung nhat

Sau khi core va guardrails da on hon,
neu tiep tuc mo rong tinh nang ngay ma khong benchmark,
thi se rat de roi vao tinh huong:

```text
moi phase moi deu "co ve on"
nhung khong co bang chung rang cac phase cu van an toan
```

Phase 39 la buoc hop ly nhat vi no:

1. khoa cac case da sua xong;
2. bao ve logic truoc khi sang phase moi;
3. giup web test sau nay de doi chieu nhanh;
4. giup phan bao cao/bao ve co tinh thuyet phuc hon.

Noi ngan gon:

```text
Phase 39 bien kinh nghiem sua bug thanh tai san ky thuat co the dung lai
```

## 5. Nguyen tac thiet ke

### 5.1 Benchmark khoa "y nghia nghiep vu", khong khoa score mot cach mong manh

Khong nen lam benchmark theo kieu:

```text
case nay phai dung chinh xac 66 diem
```

tru khi diem do that su la business invariant.

Nen uu tien khoa:

- score band
- recommendation band
- missing skills co/khong
- open-set kept/discarded behavior
- confidence level
- reason codes quan trong
- payload/runtime diagnostics quan trong

### 5.2 Regression pack phai bao phu ca employer-side va candidate-side

He thong hien tai co 2 bai toan lien thong:

1. screening CV theo JD cho nha tuyen dung
2. goi y Top JD theo CV cho ung vien

Regression pack phai khoa ca 2,
vi candidate-side dang reuse employer-side core scorer.

### 5.3 Case kho phai duoc tai hien bang fixture ro rang

Khong chi viet test inline.
Can co fixture de:

- tai hien ca kho that;
- de doc;
- de sau nay mo rong them;
- co the doi chieu voi web data/debug payload neu can.

### 5.4 Confidence/diagnostics cung la mot phan contract

Sau Phase 38,
`confidence_guardrails` va `decision_confidence`
khong con la field phu nua.

Chung da tro thanh:

- API contract logic
- debugging contract
- bridge contract cho web

Nen benchmark phai xem chung nhu first-class outputs.

### 5.5 Khong hard-code benchmark cho tung job_id that

Khong benchmark theo:

```text
job_id = 22 phai the nay
```

Ma benchmark theo:

```text
mot case sparse infra JD co tinh chat A/B/C
```

De benchmark giu gia tri tong quat,
khong tro thanh test cho mot record DB cu the.

## 6. Kien truc regression pack de xuat

### 6.1 Ba lop regression

Phase 39 nen co 3 lop:

#### A. Case fixtures

Mo ta du lieu va ky vong cho tung case.

#### B. Behavior assertions

Assert cac invariant nghiep vu.

#### C. Parity / stability assertions

Dam bao cung core logic giua:

- screening payload path
- recommendation payload path
- local pipeline path

### 6.2 Luong benchmark tong quat

```text
Fixture case
  -> parse / classify / extract
  -> match / evidence / score
  -> build review / confidence / diagnostics
  -> assert expected behavior
  -> assert khong drift so voi baseline nghiep vu
```

### 6.3 Luong benchmark recommendation

```text
candidate payload
  -> retrieve jobs
  -> rerank with core scorer
  -> produce skill-gap + decision confidence
  -> assert top-job ordering / exclusion / fit-label / confidence behavior
```

### 6.4 Luong benchmark diagnostics

```text
payload diagnostics
screening confidence
confidence guardrails
decision confidence
runtime diagnostics summary

-> assert reason codes / counts / level expectations
```

## 7. Nhom case bat buoc can co

### 7.1 Explicit-rich backend strong case

Ky vong:

- parse ro;
- must-have skill list sach;
- final score cao;
- decision confidence cao;
- confidence guardrails cao hoac it nhat khong can warning.

### 7.2 Explicit-rich hard-skill deficit case

Case:

- CV co experience/seniority tot;
- nhung thieu hard skills cot loi.

Ky vong:

- khong bi overrate;
- recommendation khong vuot nguong da quy dinh;
- concern / gate / decision confidence phan anh dung.

### 7.3 Sparse infra/support JD recovery case

Case:

- explicit technical requirements yeu;
- responsibilities technical manh.

Ky vong:

- sparse recovery active;
- promoted technical core xuat hien;
- open-set requirements duoc giu lai;
- confidence guardrails danh dau dung sparse/prompted-source nature.

### 7.4 Placeholder / weak JD exclusion case

Case:

- title `Test` / description rat ngan / requirements rong.

Ky vong:

- quality gate bat;
- candidate-side recommendation exclude dung;
- diagnostics va warnings thong nhat.

### 7.5 Open-set technical requirement preserved case

Case:

- requirement ky thuat chua co trong taxonomy;
- candidate co evidence lexical/semantic hop ly.

Ky vong:

- requirement khong bi mat;
- open-set filter keep dung;
- match type hop ly;
- confidence/diagnostics phan anh open-set nature.

### 7.6 Context-rich evidence recovery case

Case:

- skill nam o technologies/title/project context;
- action nam o description.

Ky vong:

- evidence level duoc recover dung;
- khong bi danh gia yeu oan;
- review/evidence highlights van hop ly.

### 7.7 Multilingual / cross-lingual case

Case:

- JD Anh, CV Viet hoac nguoc lai.

Ky vong:

- he thong khong crash;
- match semantic/open-set hop ly trong gioi han current system;
- benchmark khoa score band va warnings hop ly,
  khong can claim hoan hao.

### 7.8 Confidence guardrail contrast cases

Can co it nhat 3 cap:

1. high score + high confidence
2. medium/high score + medium confidence
3. low/medium score + low confidence

Muc tieu:

```text
tach ro score va confidence
```

### 7.9 Candidate-side top-jobs ordering case

Case:

- 1 job fit manh
- 1 job fit trung binh
- 1 job yeu / placeholder

Ky vong:

- thu hang hop ly;
- job placeholder bi exclude;
- job fit trung binh co decision confidence thap hon job fit manh.

## 8. Regression invariants de xuat

Phase 39 nen khoa mot bo invariants ro rang.

### 8.1 Invariants ve parsing / extraction

- soft requirement khong chen vao missing hard skills;
- sparse recovery chi bat khi explicit technical khong usable;
- promoted requirements khong duoc vuot boundary qua muc;
- open-set requirement technical khong bi mat oan.

### 8.2 Invariants ve scoring

- hard-skill deficit case khong duoc nang score cao chi nho experience;
- explicit-rich strong case khong duoc bi drift xuong oan;
- sparse promoted-source case duoc score cong bang hon truoc,
  nhung khong over-score.

### 8.3 Invariants ve confidence

- clean explicit-rich case -> `decision_confidence = high`
- sparse/open-set-heavy case -> `confidence_guardrails.review_required = true`
- semantic-only heavy case -> phai co reason code phu hop

### 8.4 Invariants ve diagnostics

- runtime diagnostics phai tong hop duoc level counts;
- reason code quan trong phai xuat hien dung cho case kho;
- screening/recommendation diagnostics khong duoc im lang khi payload co van de.

### 8.5 Invariants ve candidate-side recommendation

- excluded jobs khong duoc lot vao `top_jobs`
- top job phai giu rank on dinh cho case fixture chuan
- fit label va decision confidence khong mau thuan nhau mot cach vo ly

## 9. File / module du kien can sua

### 9.1 File test kha nang cao se sua

```text
tests/test_core_logic_benchmark.py
tests/test_cli_api_parity.py
tests/test_payload_pipeline.py
tests/test_job_recommendation_pipeline.py
tests/test_runtime_diagnostics.py
tests/test_api.py
```

### 9.2 Fixture / manifest kha nang cao se sua/them

```text
tests/fixtures/core_logic_benchmark/
tests/fixtures/core_logic_benchmark/manifests/
```

Co the them:

```text
tests/fixtures/core_logic_benchmark/payloads/
tests/fixtures/core_logic_benchmark/jds/
tests/fixtures/core_logic_benchmark/cvs/
```

### 9.3 Tai lieu co the cap nhat

```text
docs/evaluation/core_logic_cases.md
docs/evaluation/failure_taxonomy.md
README.md
docs/dev-learning-log.md
```

Neu repo chua co `docs/evaluation/`,
co the tao moi trong phase nay.

## 10. Muc tieu implementation cu the

### 10.1 Nang cap `test_core_logic_benchmark.py`

Khong chi assert score/recommendation nua,
ma bo sung assert cho:

- `confidence_guardrails`
- `decision_confidence`
- `reason_codes`
- sparse recovery
- diagnostics significance

### 10.2 Them manifest-driven benchmark expectations

Neu phu hop,
co the mo rong manifest de luu them:

- expected score band
- expected recommendation
- expected confidence level
- expected reason codes
- expected exclusion behavior

De test de doc hon va de mo rong hon.

### 10.3 Them regression helper neu can

Neu assert lap lai nhieu,
co the them helper nho de viet expectation gon hon, vi du:

```text
assert_confidence_level(...)
assert_reason_codes_include(...)
assert_score_band(...)
```

Nhung helper phai nho, de doc, khong tru tuong hoa qua muc.

### 10.4 Khoa benchmark cho candidate-side recommendation

Can bo sung assert ro hon cho:

- `top_jobs`
- `excluded_jobs`
- `fit_label`
- `decision_confidence`
- `job_confidence_guardrails`
- diagnostics level counts

### 10.5 Khoa benchmark cho API contract logic

Can dam bao:

- health endpoint phase/version dung;
- screening/recommend-jobs van backward-compatible;
- field moi cua Phase 38 duoc benchmark o muc can thiet.

## 11. Test plan de xuat

### 11.1 Focused benchmark tests

Chay:

- `tests/test_core_logic_benchmark.py`
- `tests/test_cli_api_parity.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_payload_pipeline.py`
- `tests/test_runtime_diagnostics.py`

### 11.2 Full suite regression

Bat buoc chay full:

```text
pytest
```

de dam bao benchmark pack moi khong gay false assumptions len test cu.

### 11.3 Manual sanity cases de xuat

Sau khi code xong,
co the manual-check them 3 nhom:

1. backend clean case
2. sparse infra/support case
3. placeholder job candidate-side case

Muc tieu la doi chieu:

- score
- confidence
- diagnostics

## 12. Acceptance criteria

Phase 39 duoc xem la hoan thanh khi:

1. Co regression cases dai dien cho explicit-rich, sparse-JD, placeholder-JD, open-set, context-evidence, candidate-side recommendation.
2. Benchmark khoa duoc khong chi score/recommendation ma ca confidence/diagnostics behavior quan trong.
3. Co it nhat mot nhom assert cho sparse recovery va promoted-source guardrails.
4. Candidate-side top-jobs ordering/exclusion behavior duoc regression-test ro rang.
5. Failure taxonomy/benchmark docs duoc cap nhat neu can.
6. Full `pytest` pass.

## 13. Dependency sanity check trong qua trinh code

Moi khi code Phase 39, can hoi nguoc it nhat 6 cau:

1. Test nay dang khoa nghiep vu quan trong hay chi khoa implementation detail mong manh?
2. Expectation nay co qua phu thuoc vao mot score exact de sau nay kho sua khong?
3. Case nay dai dien cho mot nhom bug that su da gap hay chua?
4. Candidate-side va employer-side co dang duoc benchmark can bang khong?
5. Confidence/diagnostics da duoc benchmark nhu first-class outputs chua?
6. Fixture nay co tong quat du hay dang tro thanh test cho mot DB record cu the?

Neu trong qua trinh code phat hien:

- can them 1 fixture moi;
- can them 1 reason-code assertion moi;
- can tach them 1 helper benchmark nho;

thi duoc phep bo sung,
mien la van giu boundary:

```text
benchmark + regression hardening
chu khong quay lai sua core logic lon
```

## 14. Rui ro va cach giam rui ro

### 14.1 Rui ro: benchmark qua chat, khoa ca implementation detail

Neu assert qua nhieu exact values,
sau nay moi cai thien nho deu gay vo test du logic van dung.

Cach giam:

- uu tien band/invariant/reason code;
- chi khoa exact score khi that su can.

### 14.2 Rui ro: benchmark qua long, mat gia tri regression

Neu chi assert chung chung,
test se xanh nhung bug van lot.

Cach giam:

- voi moi case kho, phai co 1-2 invariant that su “canh cua”.

### 14.3 Rui ro: chi benchmark screening ma bo quen recommendation

Vi recommendation reuse core scorer,
bo quen candidate-side se tao lo hong lon.

Cach giam:

- bat buoc co candidate-side regression cases.

### 14.4 Rui ro: benchmark tro thanh test cho data tam thoi

Neu fixture qua gan DB/web data tam thoi,
regression pack se som loi thoi.

Cach giam:

- anonymize / tong quat hoa case;
- dat ten theo tinh chat nghiep vu, khong theo ID that.

## 15. Khong nam trong pham vi Phase 39

Phase nay chua lam:

- UI web moi
- thay doi scorer lon
- taxonomy moi
- role-family moi
- GPT enhancement
- multilingual embedding improvement moi
- dashboard admin moi

Phase nay chi khoa hanh vi cua nhung gi he thong da co.

## 16. Gia tri nghiep vu va gia tri bao cao

Phase 39 co gia tri rat lon khi bao cao vi co the giai thich:

```text
He thong cua em khong chi chay duoc tren vai demo case.
Em da xay dung mot bo benchmark va regression pack de khoa lai
nhung tinh huong kho da gap trong qua trinh phat trien.
Moi lan sua parser, matching, scoring hay diagnostics,
em deu co the chay lai bo benchmark nay de dam bao he thong khong bi regress.
```

Day la mot diem rat “phong cach di lam”:

- khong fix bang cam tinh;
- co case tai hien;
- co regression pack;
- co ky luat bao ve chat luong.

## 17. Dau ra mong doi cua phase

Sau khi xong Phase 39, repo nen co:

- benchmark/regression pack chat hon cho employer-side screening;
- benchmark/regression pack chat hon cho candidate-side recommendation;
- expectation ro cho confidence/diagnostics behavior;
- fixture/manifests de mo rong ve sau;
- nen ky thuat rat tot truoc khi mo rong phase moi.

## 18. Huong sau Phase 39

Sau khi Phase 39 xong,
he thong se o trang thai rat dep de:

1. tiep tuc mo rong logic moi mot cach an toan;
2. nang cap web UI dua tren confidence/diagnostics da on dinh;
3. hoac quay lai xu ly nhung bai toan nang hon nhu:
   - multilingual improvement sau,
   - GPT/VIP augmentation,
   - hoac them role families moi.

Nhung du huong nao,
Phase 39 se la diem khoa chat luong rat quan trong truoc khi di tiep.
