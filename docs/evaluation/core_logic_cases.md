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

### 6. `screening_sparse_infra_recovery`

- Loai: employer-side screening
- Muc tieu: sparse JD support/infra van phuc hoi duoc technical core tu responsibilities
- Ky vong:
  - `open_set_requirements` giu duoc `Active Directory`, `DNS`, `DHCP`, `Firewall`
  - `confidence_guardrails.level = low`
  - co cac reason code sparse/open-set/prompted-source quan trong
  - `decision_confidence` cua candidate khong duoc "tu tin ao"
- Failure taxonomy watch:
  - `OPEN_SET_NOISE`
  - `CONFIDENCE_GUARDRAIL_MISS`

### 7. `screening_open_set_identity_requirement`

- Loai: employer-side screening
- Muc tieu: requirement explicit nhung ngoai taxonomy van duoc giu lai va match dung
- Ky vong:
  - `identity verification` van nam trong `open_set_requirements`
  - candidate co the dat `Maybe Review`
  - `decision_confidence.level = low` vi evidence moi chi o muc keyword-level
  - day la case de bat `OPEN_SET_NOISE` va `CONFIDENCE_GUARDRAIL_MISS`

### 8. Confidence/Diagnostics contrast

- Loai: ca employer-side screening va candidate-side recommendation
- Muc tieu: tach ro `score` va `confidence`
- Ky vong:
  - strong explicit-rich case co the co `score` cao va `decision_confidence = high`
  - sparse/noisy/open-set-heavy case co the co `score` khong qua thap nhung van phai `review_required = true`
  - runtime diagnostics phai tong hop dung level counts va reason-code counts
- Failure taxonomy watch:
  - `CONFIDENCE_GUARDRAIL_MISS`
  - `DIAGNOSTICS_SUMMARY_DRIFT`

## Cac case payload-driven bo sung

Ngoai cac fixture file-backed cases o tren, test suite Phase 26 con giu them 2 case
payload-driven va duoc Phase 39 nang cap tiep:

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

Sau Phase 39, can hoi them 2 cau nua:

4. Case do co lam drift `confidence_guardrails` hay `decision_confidence` khong?
5. Runtime diagnostics co con tong hop dung level/reason codes cho case nay khong?
