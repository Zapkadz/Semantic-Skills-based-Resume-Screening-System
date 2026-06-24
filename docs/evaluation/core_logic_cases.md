# Core Logic Benchmark Cases

## Muc tieu

Tai lieu nay dong bang cac case nghiep vu quan trong de regression cho Phase 26
tro di. Moi case duoc chon vi no tung bat ra mot nhom benh logic that:

- parser nhin sai requirement
- soft skill di nham vao hard-skill scoring
- JD yeu van co diem nen
- CV khong co section Skills nhung co evidence that
- local file path va web/API payload path bi lech nhau

## Nhom case chinh

### 1. `screening_backend_strong`

- Loai: employer-side screening
- Muc tieu: baseline strong JD + strong CV
- Ky vong:
  - `must_have_skills` duoc parse dung
  - candidate dat `Strong Review`
  - score nam o band cao
- Failure taxonomy watch:
  - `SCORING_OVERRATE`
  - `CLI_API_PARITY_MISMATCH`

### 2. `screening_backend_evidence_without_skills_section`

- Loai: employer-side screening
- Muc tieu: CV khong co section `Skills` nhung van co project/work evidence manh
- Ky vong:
  - he thong van match dung Java / Spring Boot / REST API / SQL / Docker
  - score van nam o band cao
  - day la case de bat `EVIDENCE_MISSED`

### 3. `screening_backend_hard_skill_deficit`

- Loai: employer-side screening
- Muc tieu: ung vien co mot phan overlap nhung thieu hard skill cot loi
- Ky vong:
  - score khong duoc bi doi len qua muc
  - recommendation phai o band thap hon strong cases
  - day la case de bat `SCORING_OVERRATE`

### 4. `screening_cross_lingual_cv`

- Loai: employer-side screening
- Muc tieu: JD tieng Anh, CV tieng Viet
- Ky vong:
  - parser va taxonomy van nhin ra skill cot loi
  - ket qua khong duoc rot ve band thap mot cach vo ly
  - day la case de bat `EVIDENCE_MISSED` va `CLI_API_PARITY_MISMATCH`

### 5. `recommendation_placeholder_jobs_excluded`

- Loai: candidate-side recommendation
- Muc tieu: placeholder JD khong duoc len top jobs
- Ky vong:
  - job `Test` / `mo ta test` bi dua vao `excluded_jobs`
  - chi job that moi vao `top_jobs`
  - day la case de bat `JD_QUALITY_GATE_MISS`

## Cac case payload-driven bo sung

Ngoai cac fixture file-backed cases o tren, test suite Phase 26 con giu them 2 case
payload-driven:

### Soft-skill separation case

Kiem tra:

- `education`
- `soft_skills`
- `experience`

duoc tach khoi hard-skill matching, khong bi dua vao `missing_skills`.

### Open-set technical preservation case

Kiem tra requirement la ngoai taxonomy nhu `identity verification`:

- khong bi bo qua
- duoc giu trong `open_set_requirements`
- co the semantic-match khi co embedding

## Cach dung tai lieu nay

Moi phase sua logic sau Phase 26 nen hoi nguoc 3 cau:

1. Case nao duoc cai thien?
2. Case nao bi regress?
3. Regress do thuoc failure taxonomy nao?

Neu mot thay doi parser/scoring khong tra loi duoc 3 cau nay, thay doi do chua du
an toan de merge.
