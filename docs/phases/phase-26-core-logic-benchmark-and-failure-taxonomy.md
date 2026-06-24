# Phase 26 - Core Logic Benchmark and Failure Taxonomy

## 1. Muc tieu phase

Sau Phase 25, he thong da co them payload diagnostics va runtime trace de debug
tot hon khi dua AI vao web that.

Tuy nhien, van de lon nhat hien tai khong con nam o viec:

```text
"co log hay khong"
```

ma nam o viec:

```text
"co mot bo benchmark logic on dinh de biet he thong dang sai o dau hay khong"
```

Thuc te da xuat hien nhieu nhom loi logic:

- soft skill bi tinh nhu hard skill;
- JD qua yeu nhung van co score nen;
- API/Web/CLI co the cho ket qua lech nhau;
- open-set gom ca requirement ky thuat va cau chung chung;
- scorer co the overrate ung vien khi hard skill chua du;
- mot so case chi sai khi dua qua payload web that.

Muc tieu cua Phase 26 la:

```text
Dong bang cac loi logic hien tai thanh mot bo benchmark co the chay lai duoc,
do lai duoc, va dung de regression cho moi phase sua logic tiep theo.
```

Noi ngan gon:

```text
Phase 25 = debug duoc request that
Phase 26 = bien loi logic thanh thu co the benchmark duoc
```

## 2. Vi sao phase nay can lam truoc khi sua parser/scoring

Neu di sua ngay parser, open-set hay scorer ma chua khoa benchmark thi rat de gap:

```text
Sua duoc Job 22
nhung vo Job 18
hoac local pass nhung web lai lech
hoac diem dep hon nhung logic van sai nghia
```

Phase 26 khong phai phase "lam AI thong minh hon" ngay lap tuc.
No la phase giup:

1. biet chinh xac he thong dang hong o lop nao;
2. sua cac phase sau co co so do luong ro rang;
3. tranh viec fix theo tung case rieng le;
4. de bao ve hon truoc giang vien vi moi claim deu co case benchmark di kem.

## 3. Van de can giai quyet

### 3.1 Chua co benchmark logic loi

Hien tai da co unit tests cho tung module, nhung van thieu mot bo case theo goc nhin
nghiep vu va logic he thong, vi du:

- JD manh + CV manh;
- JD manh + CV thieu hard skill;
- JD test / JD placeholder / JD qua ngan;
- JD co nhieu soft skill;
- JD co skill la ngoai taxonomy;
- CV khong co section Skills nhung co evidence trong experience/project;
- JD tieng Anh, CV tieng Viet;
- payload web gui sang co HTML ban.

Neu khong co bo benchmark nay, moi phase sua logic se kho danh gia co that su
tot len hay chi "doi kieu sai".

### 3.2 Chua tach ro loi parser, loi typing, loi matching, loi scoring

Khi mot case cho ket qua xau, hien tai thuong chi ket luan chung chung:

```text
AI cham chua on
```

Trong khi thuc te co the la:

1. parser nhin sai section;
2. requirement type sai;
3. open-set gom nham soft skill;
4. evidence bi bo sot;
5. scorer overrate;
6. web payload khac local fixture.

Phase 26 can dat ten ro cho tung nhom failure.

### 3.3 Chua co parity test giua local file path va web payload path

Mot van de da gap la:

```text
CLI local test cho 46 diem
nhung web API chi cho 34 diem
```

Neu khong co parity benchmark, cac phase sau rat de sua local dep nhung web van
khong giong.

## 4. Nguyen tac thiet ke

### 4.1 Chua sua logic, chi khoa benchmark va failure taxonomy

Phase 26 khong nen:

- viet lai parser;
- doi scoring formula;
- them taxonomy moi de "cuu diem";
- doi contract lon cua API.

Phase nay tap trung vao:

- benchmark fixtures;
- expected behavior;
- parity checks;
- failure taxonomy;
- docs danh gia.

### 4.2 Benchmark theo nghiep vu, khong chi theo ham

Unit test cho tung ham la can thiet, nhung chua du.

Phase 26 can bo sung benchmark theo use-case:

- employer-side screening;
- candidate-side recommendation;
- web payload thuc te;
- bad-case nghiep vu.

### 4.3 Expected behavior nen khoa "y nghia", khong nhat thiet khoa exact score

Voi nhieu case, khong nen dong bang:

```text
phai dung chinh xac 34 diem
```

Ma nen dong bang nhung dieu quan trong hon, vi du:

- job nay phai bi quality warning;
- soft skill nay khong duoc vao hard-skill core;
- candidate nay khong duoc vuot qua nguong Good Fit;
- case nay phai co open-set technical requirement;
- CLI va API khong duoc lech qua nguong cho phep.

### 4.4 Benchmark phai de mo rong

Sau nay Phase 27-33 se sua:

- typed requirement schema;
- open-set technical filtering;
- role-family inference;
- evidence enrichment;
- scoring gates;
- taxonomy suggestion governance;
- parity diagnostics.

Vi vay benchmark phase nay phai du de mo rong ma khong can viet lai tu dau.

## 5. Kien truc de xuat

### 5.1 Hai lop benchmark

Phase 26 nen co 2 lop:

1. **Fixture benchmark**
   - JD/CV/payload mau de tai hien bug

2. **Failure taxonomy**
   - ten va nhom loi de phan loai case

### 5.2 Luong benchmark tong quat

```text
Fixture case
  -> chay qua pipeline local
  -> chay qua payload pipeline neu co
  -> doi chieu expected behavior
  -> gan failure taxonomy neu sai
```

### 5.3 Luong parity benchmark

```text
Raw local file input
  vs
API-style payload input
  vs
web debug payload input

-> compare parsed requirements
-> compare warnings
-> compare score bands
-> compare match explanations
```

## 6. Module va tai lieu de xuat

Them:

```text
tests/fixtures/core_logic_benchmark/
tests/test_core_logic_benchmark.py
tests/test_cli_api_parity.py
docs/evaluation/core_logic_cases.md
docs/evaluation/failure_taxonomy.md
```

Neu can, co the them helper nho:

```text
tests/helpers/benchmark_assertions.py
```

Cap nhat:

```text
tests/test_api.py
tests/test_payload_pipeline.py
README.md
docs/dev-learning-log.md
```

## 7. Cac nhom case bat buoc phai co

### 7.1 Strong JD + Strong CV

Case nen cho thay:

- requirement duoc parse ro;
- hard skill match hop ly;
- evidence co chat luong;
- score nam o nhom cao;
- explanation dung nghia.

### 7.2 Strong JD + CV thieu hard skill

Case nay rat quan trong de bat benh:

```text
nhieu nam kinh nghiem nhung thieu ky nang cot loi van bi cham cao
```

Ky vong:

- score khong duoc vuot nguong qua cao;
- review phai noi ro thieu hard skill;
- overrate case phai bi benchmark bat lai.

### 7.3 JD test / placeholder / qua ngan

Vi du:

- title `Test`
- description `mo ta test`
- requirement rong

Ky vong:

- quality flag phai bat;
- recommendation/screening khong duoc nhin nhu mot JD manh;
- score nen neu co phai nam trong nguong duoc chap nhan hoac bi exclude.

### 7.4 JD nhieu soft skill

Vi du:

- enthusiastic
- eager to learn
- good communication

Ky vong:

- khong duoc di thang vao hard-skill scoring;
- neu vao open-set thi phai duoc danh dau dung loai;
- case nay sau nay se dung de verify Phase 27-28.

### 7.5 JD co skill la ngoai taxonomy

Ky vong:

- requirement la duoc giu lai;
- neu la technical thi co open-set signal hop ly;
- khong bi bo qua hoan toan;
- khong can them taxonomy moi o Phase 26.

### 7.6 CV khong co section Skills nhung co project/evidence manh

Ky vong:

- he thong van nhan ra mot phan fit;
- evidence tu experience/project co tac dung;
- nhung strength phai duoc noi dung nghia, khong "an may" vi seniority.

### 7.7 Cross-lingual case

Ky vong:

- he thong khong crash logic;
- semantic fallback neu bat embedding co tac dung;
- output it nhat phai hop ly theo muc benchmark hien tai.

### 7.8 Web payload dirty case

Case nay mo phong:

- JD con HTML;
- CV text bi cat;
- requirement field map sai;
- title/description duoc gui theo format tu DB.

Ky vong:

- diagnostics phai noi ro input issue;
- ket qua local payload path va web payload path khong duoc lech vo ly ma khong co warning.

## 8. Failure taxonomy de xuat

Phase 26 can tao tai lieu failure taxonomy on dinh de nhung phase sau cung dung chung.

De xuat cac nhom:

### 8.1 `PARSER_ERROR`

Dung khi:

- section bi doc sai;
- title/requirements/responsibilities bi mat;
- parser tra ve qua it signal du du lieu goc khong yeu.

### 8.2 `REQUIREMENT_TYPE_ERROR`

Dung khi:

- soft skill bi xem la technical requirement;
- tool/platform bi xep sai nhom;
- requirement kinh nghiem bi xem nhu skill.

### 8.3 `OPEN_SET_NOISE`

Dung khi:

- open-set gom cau chung chung;
- requirement khong phai ky thuat van vao queue technical;
- unknown requirement signal bi nhieu.

### 8.4 `EVIDENCE_MISSED`

Dung khi:

- CV co evidence trong project/experience nhung he thong khong bat duoc;
- matched skill khong keo theo evidence hop ly.

### 8.5 `SCORING_OVERRATE`

Dung khi:

- score qua cao du hard skill chua du;
- score nen qua cao voi JD quality yeu;
- recommendation cao hon y nghia nghiep vu.

### 8.6 `JD_QUALITY_GATE_MISS`

Dung khi:

- JD placeholder/qua ngan van vao ranking binh thuong;
- job yeu khong bi canh bao du muc.

### 8.7 `CLI_API_PARITY_MISMATCH`

Dung khi:

- local fixture va API payload tuong duong nhung ket qua lech lon;
- web path va CLI path parse khac nhau ro ret.

## 9. Cau truc fixture benchmark de xuat

De xuat:

```text
tests/fixtures/core_logic_benchmark/
  jds/
  cvs/
  payloads/
  manifests/
```

### 9.1 `jds/`

Luu cac JD text benchmark.

### 9.2 `cvs/`

Luu cac CV text benchmark.

### 9.3 `payloads/`

Luu sample JSON payload:

- screening payload
- recommend-jobs payload
- web debug payload da anonymize neu can

### 9.4 `manifests/`

Moi case nen co metadata, vi du:

```json
{
  "case_id": "jd_test_placeholder_01",
  "tags": ["jd_quality_low", "placeholder_title"],
  "expected": {
    "should_warn": true,
    "should_exclude": true,
    "max_fit_score": 20
  }
}
```

## 10. Expected behavior can khoa o benchmark

Phase nay khong can dong bang tung dong text review card,
nhung nen khoa nhung y nghia sau:

### 10.1 Parse expectations

- co/khong co must-have meaningful;
- co/khong co open-set requirement;
- co/khong co soft-skill contamination.

### 10.2 Score expectations

- score band toi da / toi thieu;
- label khong duoc vuot nguong;
- JD yeu khong duoc co fit score "dep".

### 10.3 Warning expectations

- payload issue nao phai bat;
- quality flag nao phai co;
- parity mismatch nao phai duoc thong bao.

### 10.4 Explanation expectations

- neu thieu hard skill thi review phai noi ro;
- neu chi co weak evidence thi review phai phan biet duoc;
- neu JD khong du du lieu thi phai noi dung nghia.

## 11. Parity benchmark de xuat

Phase 26 can co test rieng cho parity.

### 11.1 Parity local file vs API payload

Cung mot noi dung:

- chay bang `main.py` hoac pipeline local;
- chay bang JSON payload tuong duong;
- so sanh:
  - parsed skill counts
  - warnings
  - score band
  - recommendation

### 11.2 Parity payload pipeline vs web debug payload

Neu da co file debug trong:

```text
C:\topcv_ai_runtime\api-debug
```

thi co the lay mot vai case dai dien de tao regression sample anonymized.

## 12. Pham vi thuc hien cua Phase 26

### 12.1 Trong scope

- tao benchmark fixture cho cac case logic loi;
- tao failure taxonomy;
- viet tests benchmark;
- viet parity tests;
- viet docs danh gia benchmark;
- cap nhat docs de nhung phase sau dung lai.

### 12.2 Ngoai scope

- chua sua parser;
- chua tach typed requirement schema;
- chua sua open-set filter;
- chua doi scoring formula;
- chua doi admin taxonomy queue;
- chua them role-family inference.

## 13. Test plan

Them:

```text
tests/test_core_logic_benchmark.py
tests/test_cli_api_parity.py
```

Cap nhat:

```text
tests/test_api.py
tests/test_payload_pipeline.py
```

### 13.1 Cac assert nen co

1. Case JD test phai bi quality warning hoac bi exclude.
2. Case soft skill noise khong duoc xem nhu hard-skill success.
3. Case CV thieu hard skill khong duoc vuot score band quy dinh.
4. Case CV khong co skills section nhung co evidence manh van giu duoc mot muc fit hop ly.
5. Case open-set technical duoc giu lai thay vi bien mat.
6. CLI va API payload tuong duong khong duoc lech score qua nguong cho phep.
7. Web dirty payload neu co lech phai co warning/diagnostic ro rang.

### 13.2 Manual benchmark de xuat

Test lai cac case da tung gap:

- Job 22 / JD_4 va CV_4_1, CV_4_2, CV_4_3;
- JD test placeholder tren web candidate-side;
- case CV xoa section skills nhung van con project evidence;
- case employer-side CV diem cao bat thuong du thieu skill.

## 14. Acceptance criteria

Phase 26 duoc xem la hoan thanh khi:

1. co benchmark fixture cho cac nhom case logic quan trong;
2. co failure taxonomy ro rang va duoc tai lieu hoa;
3. co parity test giua local file path va API payload path;
4. co the tai hien cac bug logic da gap gan day bang test/fixture;
5. moi phase sua logic sau nay co diem tu benchmark de so sanh regression;
6. full `pytest` van pass.

## 15. Dau ra mong muon sau phase nay

Sau Phase 26, khi gap mot case bat thuong, ta co the noi ro:

```text
Case nay hong vi REQUIREMENT_TYPE_ERROR
```

hoac:

```text
Case nay hong vi JD_QUALITY_GATE_MISS
```

hoac:

```text
Case nay la CLI_API_PARITY_MISMATCH
```

thay vi chi noi chung:

```text
AI cham chua on
```

Day la buoc rat quan trong de chuyen he thong tu muc:

```text
co the demo
```

sang muc:

```text
co the sua logic mot cach co kiem soat va bao ve duoc
```

## 16. Huong sau Phase 26

Sau khi benchmark logic da duoc khoa, phase tiep theo hop ly nhat la:

```text
Phase 27 - Typed Requirement Schema and Section-aware JD Parsing
```

Muc tieu cua phase do la sua tan goc van de parser va requirement typing:

- tach hard skill / soft skill / experience / education / language;
- uu tien section requirements dung nghia;
- khong de soft skill di vao hard-skill scoring nua.
