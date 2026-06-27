# Failure Taxonomy

## Muc tieu

Failure taxonomy dung de goi ten dung benh logic cua he thong. Khi ket qua bat
thuong xuat hien, team khong dung nhan chung chung la "AI cham chua on", ma map no
vao mot nhom loi ro rang.

## Danh sach nhom loi

### `PARSER_ERROR`

Dung khi:

- section bi tach sai
- title/requirements/responsibilities bi mat
- parser tra ve qua it signal du du lieu goc khong yeu

### `REQUIREMENT_TYPE_ERROR`

Dung khi:

- soft skill bi xem la technical requirement
- tool/platform bi xep sai loai
- experience requirement bi tinh nhu skill

### `OPEN_SET_NOISE`

Dung khi:

- unknown requirement khong phai ky thuat nhung van vao open-set technical flow
- queue suggestion cho admin bi nhieu boi cum chung chung

### `EVIDENCE_MISSED`

Dung khi:

- CV co bang chung trong project/work experience nhung he thong khong bat duoc
- skill match co score nhung evidence level thap hon muc hop ly

### `SCORING_OVERRATE`

Dung khi:

- score qua cao du thieu hard skill cot loi
- JD yeu van co diem nen qua dang ke
- recommendation cao hon y nghia nghiep vu

### `JD_QUALITY_GATE_MISS`

Dung khi:

- JD placeholder / qua ngan van vao ranking binh thuong
- excluded logic bo sot job yeu

### `CLI_API_PARITY_MISMATCH`

Dung khi:

- local file path va API payload path cho ket qua lech lon
- web payload va CLI path parse ra khac nhau ma khong co canh bao ro

### `CONFIDENCE_GUARDRAIL_MISS`

Dung khi:

- score co the van dung, nhung `confidence_guardrails` khong phan anh dung muc do tin cay cua case
- sparse/open-set-heavy/noisy case dang thieu reason code quan trong
- case can review nhung `review_required` lai khong bat

### `DIAGNOSTICS_SUMMARY_DRIFT`

Dung khi:

- runtime diagnostics khong tong hop dung level counts hoac reason-code counts
- screening/recommendation response van co output chinh, nhung lop diagnostics tong hop bi drift
- web/doc diagnostics khong con noi dung duoc case kho nhu benchmark mong doi

## Cach dung trong quy trinh

Khi gap mot bug, nen ghi log hoac note theo mau:

```text
Case: job-22
Primary failure taxonomy: REQUIREMENT_TYPE_ERROR
Secondary failure taxonomy: OPEN_SET_NOISE
Symptom: soft requirements entered the open-set technical path
```

Hoac:

```text
Case: sparse-infra-benchmark
Primary failure taxonomy: CONFIDENCE_GUARDRAIL_MISS
Secondary failure taxonomy: DIAGNOSTICS_SUMMARY_DRIFT
Symptom: sparse recovery did run, but response did not surface the low-confidence warning set
```

Lam nhu vay giup:

- tranh fix theo cam tinh
- de phan pha phase sau
- de bao ve truoc giang vien vi co logic debug ro rang

## Luu y

Mot case co the co nhieu nhom loi cung luc, nhung nen co:

- 1 nhom loi chinh
- 0-2 nhom loi phu

Neu mot bug khong map duoc vao taxonomy nay, do la dau hieu can mo rong benchmark
hoac cap nhat taxonomy o phase tiep theo.
