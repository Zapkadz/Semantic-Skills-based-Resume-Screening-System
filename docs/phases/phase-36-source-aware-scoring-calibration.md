# Phase 36 - Source-aware Scoring Calibration

## 1. Muc tieu phase

Sau Phase 33-35, he thong da co them 3 nang luc rat quan trong:

- phat hien technical signals trong responsibilities;
- promote mot phan responsibilities thanh scoring input;
- hieu ro hon role-family cua cac JD support / infrastructure sparse.

Noi ngan gon:

```text
Phase 33 = thay technical signals trong responsibilities
Phase 34 = dua mot phan signal do vao requirement matching
Phase 35 = dat technical core do vao dung role-family
Phase 36 = cham diem khac nhau tuy theo nguon requirement
```

Van de hien tai la:

```text
scorer da co them technical core moi,
nhung van dang xem phan lon requirement nhu "cung mot loai"
du nguon goc cua chung khac nhau.
```

Muc tieu cua Phase 36 la:

```text
Lam cho he thong biet rang:
- explicit requirement la nguon manh nhat
- promoted responsibility la fallback technical source
- semantic-only open-set match la bang chung hop le, nhung do chac chan thap hon
```

Rat quan trong:

```text
Phase 36 sua scorer va provenance propagation,
nhung khong viet lai parser,
khong mo rong taxonomy,
khong doi web contract lon.
```

Tuc la Phase 36 se tap trung vao:

- phan biet do tin cay cua requirement theo nguon;
- tranh over-penalize cac JD sparse duoc khoi tao technical core tu responsibilities;
- dong thoi tranh over-score chi vi co semantic overlap yeu.

## 2. Vi tri cua Phase 36 trong cay dependency

Day la phase thu tu trong nhanh sua "section-aware JD sourcing -> role-aware scoring":

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
Phase 36 chi sua:
- scoring provenance propagation
- source-aware score adjustment
- source-aware hard-skill gate refinement
- explanation metadata nho de noi dung logic moi

Phase 36 chua sua:
- parser section logic lon
- role-family taxonomy moi
- web UI lon
- admin taxonomy workflow lon
```

## 3. Van de can giai quyet

### 3.1 Hien tai scorer van source-blind

Trong code hien tai:

- `calculate_skill_semantic_score(matches)`
- `calculate_evidence_score(matches)`
- `calculate_hard_skill_gate_metrics(matches)`

deu nhin vao mot `matches` list phang.

Dieu do co nghia la:

```text
mot skill viet ro trong Requirements
va
mot skill duoc promote tu Responsibilities

co the dang bi tinh trong rat gan nhau o layer scoring.
```

Day la van de logic cot loi.

Vi thuc te nghiep vu:

- requirement viet ro trong section `Requirements` co do rang buoc cao hon;
- signal duoc promote tu `Responsibilities` la mot fallback hop ly,
  nhung khong nen bi xem ngang 100% voi explicit must-have.

### 3.2 Open-set unknown requirements van chua mang provenance du manh vao scorer

Phase 34 da dua promoted unknown requirements vao open-set path.

Vi du:

- `Active Directory`
- `DNS`
- `DHCP`
- `Firewall`

co the di vao `open_set_requirements`.

Nhung sau do:

- open-set matcher tra ve `semantic_only_match`;
- scorer chu yeu thay `required_skill`, `score`, `evidence_level`, `match_type`;
- scorer chua thay ro requirement nay den tu:
  - `explicit_requirement`
  - hay `promoted_responsibility`

Neu provenance bi mat hoac bi mo,
Phase 36 se khong the cham diem dung nghia.

### 3.3 Sparse JD dang co nguy co bi phat qua nang

Case kieu Job 22 cho thay:

- explicit technical requirements rat yeu hoac gan nhu rong;
- technical core phai duoc khoi tao tu responsibilities.

Neu luc nay he thong treat tat ca promoted requirements nhu explicit must-have,
thi candidate co the bi:

- mat qua nhieu diem skill/evidence;
- bi hard-skill gate cap diem qua nang;
- nhan `Not Enough Evidence` du CV khong toi den muc do.

Noi cach khac:

```text
Phase 34-35 da giup he thong thay technical core,
nhung scorer hien tai co the dang phat promoted-source deficits
giong nhu explicit-source deficits.
```

### 3.4 Nguoc lai, semantic-only overlap cung co nguy co duoc nhin dep qua muc

Neu he thong bat dau nhin thay nhieu unknown requirements,
nhung lai khong phan biet:

- explicit unknown requirement
- promoted unknown requirement
- semantic-only evidence

thi mot so case co the:

- nhin nhu da "match duoc technical core"
- trong khi thuc chat bang chung van con mem.

Vi vay Phase 36 phai giai 2 bai toan cung luc:

1. khong phat sparse promoted-source qua tay;
2. khong nang semantic-only overlap len thanh strong explicit fit.

### 3.5 Explanation hien tai chua noi du "vi sao diem nay bi giam / duoc giu"

Recruiter can phan biet:

- thieu explicit must-have;
- thieu promoted responsibility signal;
- chi co semantic-only overlap;
- role-family dung nhung requirement source con yeu.

Neu explanation khong noi ra duoc dieu nay,
thi score se kho bao ve khi:

- recruiter hoi;
- giang vien hoi;
- debug tren web gap case kho.

## 4. Vi sao Phase 36 la buoc tiep theo dung nhat

Sau Phase 35, he thong da co du 3 lop du lieu dau vao:

1. `responsibility_signals`
2. `scoring_requirement_entries`
3. `job_role_profile`

Luc nay moi co the lam:

```text
score calibration dua tren "requirement nay den tu dau"
```

Neu lam Phase 36 som hon:

- chua co promotion provenance;
- chua co role-family support/infra;
- khong du du lieu de benchmark.

Neu bo qua Phase 36 va nhay thang sang Phase 37:

- diagnostics se chi "do" mot cong thuc tinh diem chua dung nghia;
- guardrails se khoa lai mot logic scoring con source-blind.

Noi ngan gon:

```text
Phase 34-35 tao ra requirement core moi
Phase 36 moi dat duoc "trong so nghiep vu" cho requirement core do
```

## 5. Nguyen tac thiet ke

### 5.1 Explicit requirement van la nguon manh nhat

Day la nguyen tac bat buoc.

He thong phai giu:

```text
explicit requirement > promoted responsibility
```

ve muc do rang buoc trong scoring.

### 5.2 Promoted responsibility la fallback technical core, khong phai "skill ao"

Khong duoc xem promoted responsibility la vo gia tri.

No la:

- rat quan trong voi sparse JD;
- can thiet de he thong khong bo sot bai toan thuc te;
- nhung do chac chan nghiep vu thap hon explicit requirement.

### 5.3 Semantic-only open-set evidence hop le, nhung khong duoc gia vo la explicit confirmed fit

Can giu logic:

- semantic-only = co overlap nghia va co gia tri;
- nhung khong duoc xem ngang voi:
  - explicit exact/related/transferable match co evidence manh.

### 5.4 Khong viet lai cong thuc weighted scoring tu dau

Phase 36 nen mo rong scorer hien tai,
khong nen tao scorer moi.

Uu tien:

- them mot lop calibration sau `raw_base_score`;
- hoac refine `hard_skill_gate`;
- nhung giu lai nhung thanh phan da on dinh o Phase 18-30.

### 5.5 Moi thay doi phai benchmark duoc

Khong chap nhan kieu:

```text
co ve score da dep hon
```

ma phai co:

- test moi;
- regression benchmark;
- case sparse JD va explicit JD song song.

## 6. Kien truc de xuat

### 6.1 Propagate provenance tu requirement entry den match result

Luong moi can ro rang:

```text
scoring_requirement_entries
  -> known/open-set requirement extraction
  -> match objects
  -> fit summary
  -> scorer
  -> review card / recommendation output
```

Muc tieu:

```text
moi match can biet:
- requirement nay den tu explicit hay promoted source
- requirement nay la known taxonomy hay open-set
- priority cua requirement la gi
```

Co the bo sung metadata kieu:

- `requirement_source_kind`
- `requirement_source_text`
- `requirement_priority`
- `requirement_taxonomy_status`

tren ca:

- known-skill match path;
- open-set semantic match path.

### 6.2 Tach ro 2 chieu provenance

Phase 36 nen phan biet ro:

#### A. Requirement source

- `explicit_requirement`
- `promoted_responsibility`

#### B. Match evidence style

- `exact_match`
- `related_match`
- `transferable_match`
- `semantic_match`
- `semantic_only_match`

Nghia la:

```text
source cua requirement
khong giong voi
kieu match cua candidate
```

Day la 2 truc logic khac nhau,
va scorer can thay ca hai.

### 6.3 Source-aware fit summary

Ngoai `core_requirement_fit_summary` hien tai,
Phase 36 nen bo sung them lop tong hop theo nguon.

Vi du:

```json
{
  "source_requirement_fit_summary": {
    "explicit_requirement": {
      "total": 4,
      "confirmed_coverage": 0.75
    },
    "promoted_responsibility": {
      "total": 3,
      "confirmed_coverage": 0.33
    }
  }
}
```

Khong nhat thiet phai doi API contract lon ngay,
nhung scorer va diagnostics noi bo nen co du data de su dung.

### 6.4 Source-aware score adjustment

Phase 36 nen bo sung 1 lop calibration dung nghia:

```text
raw_base_score
  -> role_calibrated_score
  -> source_calibrated_score
  -> final_score (sau gate)
```

Huong de xuat:

- missing explicit core -> penalty manh nhat;
- missing promoted core -> penalty nhe hon;
- semantic-only positive o explicit unknown requirement -> chap nhan, nhung khong tinh nhu confirmed explicit fit;
- semantic-only positive o promoted requirement -> tinh la directional evidence, khong phai proof manh.

### 6.5 Hard-skill gate can biet "deficit den tu dau"

Day la cho quan trong nhat voi case sparse JD.

Phase 36 nen sua theo huong:

#### Neu JD co explicit technical core ro

thi hard-skill gate giu nghiem nhu hien tai.

#### Neu JD chu yeu dua vao promoted technical core

thi gate:

- van hoat dong;
- nhung khong cap diem manh nhu khi thieu explicit requirements;
- uu tien xem promoted deficits la "need verification"
  hon la "hard fail".

Noi ngan gon:

```text
explicit deficits = phat manh hon
promoted deficits = phat mem hon
```

### 6.6 Explicit unknown requirements van phai duoc bao ve

Can tranh mot regression quan trong:

Vi du JD viet ro:

- `Qualys`
- `Vulnerability management`

nhung vi chung la open-set,
he thong lai lam nhu chung "chi la soft signal".

Phase 36 phai giu ro:

```text
explicit unknown requirement
van la explicit requirement
```

Nghia la:

- unknown taxonomy khong dong nghia voi low importance;
- importance phai nhin theo source,
  khong chi theo known-vs-unknown.

## 7. Huong scoring de xuat

### 7.1 Giữ `raw_base_score` lam diem goc

Khong can pha vo logic cu.

Van de cua hien tai khong nam o cho weighted formula sai hoan toan,
ma nam o cho scorer chua thay duoc provenance.

Vi vay:

- `raw_base_score` van giu;
- Phase 36 them calibration layer dua tren provenance.

### 7.2 Them `source_score_adjustment`

Co the bo sung:

- `source_score_adjustment`
- `source_alignment_impact`
- `source_calibrated_score`

de debug ro:

- diem goc la bao nhieu;
- role-aware da dieu chinh bao nhieu;
- source-aware da dieu chinh bao nhieu;
- hard-skill gate da cap them hay khong.

### 7.3 Rule tong quat cho penalty

Huong penalty de xuat:

1. explicit core missing + confirmed coverage thap -> penalty ro.
2. explicit core chi semantic-only -> penalty vua.
3. promoted core missing -> penalty nhe hon explicit.
4. promoted core chi semantic-only -> co caution, nhung khong xu nhu explicit hard fail.
5. explicit unknown open-set co evidence manh -> van duoc giu diem kha tot.

### 7.4 Nguong xet gate theo source profile cua JD

JD co the duoc nhin theo profile:

- `explicit_dominant`
- `mixed_source`
- `promoted_dominant`

Phase 36 co the khong can expose cong khai ngay,
nhung scorer noi bo nen nhin thay profile nay
de quyet dinh muc do gate.

### 7.5 Khong bonus ao cho promoted-source chi vi candidate co overlap chung chung

Can tranh tinh huong:

- JD sparse promote duoc `Firewall`, `DNS`, `DHCP`
- CV co vai keyword lan can
- he thong nang score qua nhanh

vi luc do promoted-source van la fallback source.

## 8. File/module du kien sua

### 8.1 File chinh

```text
src/scorer.py
src/open_set_matcher.py
src/payload_pipeline.py
src/screening_pipeline.py
src/job_recommendation_pipeline.py
```

### 8.2 File co the sua them

```text
src/semantic_matcher.py
src/requirement_extractor.py
src/candidate_job_reranker.py
src/review_card_generator.py
src/runtime_diagnostics.py
```

### 8.3 File co the them moi neu can

```text
src/requirement_provenance.py
```

hoac mot helper nho tuong tu,
neu can tach logic lookup provenance cho sach.

### 8.4 Test can sua/them

```text
tests/test_scorer.py
tests/test_payload_pipeline.py
tests/test_screening_pipeline.py
tests/test_job_recommendation_pipeline.py
tests/test_open_set_matcher.py
tests/test_core_logic_benchmark.py
```

## 9. Expected behavior sau phase

Sau Phase 36,
he thong nen co hanh vi nhu sau:

### 9.1 Jobs explicit-technical-rich van on dinh

Backend / Fullstack / CV / Security jobs viet ro requirements
khong bi regression lon.

### 9.2 Sparse JD duoc score cong bang hon

Case kieu Job 22:

- van thay technical core tu responsibilities;
- nhung candidate khong bi phat giong nhu dang thieu mot explicit must-have list day du.

### 9.3 Explicit unknown requirements duoc bao ve dung muc

Case nhu:

- `Qualys`
- `Vulnerability management`
- `Identity verification`

neu la explicit requirement,
van phai duoc xem la requirement quan trong,
du taxonomy chua co.

### 9.4 Review card giai thich duoc "thieu cai gi" sac hon

He thong nen noi duoc:

- missing explicit must-have
- promoted technical signals need verification
- semantic-only overlap is present but not fully confirmed

thay vi gom chung tat ca thanh "missing skills".

### 9.5 Candidate-side recommendation duoc huong loi

Vi candidate recommendation dung lai core scorer,
nen khi employer-side score dung nghia hon,
candidate-side reranking cung se sach hon.

## 10. Benchmark can khoa o Phase 36

Can co benchmark cho it nhat 6 nhom:

### 10.1 Explicit backend strong case

Ky vong:

- score gan nhu giu on;
- khong regression vo ly.

### 10.2 Sparse IT support / infra JD

Case giong Job 22.

Ky vong:

- promoted technical core van duoc tinh;
- nhung score khong bi baseline-heavy chi vi promoted deficits.

### 10.3 Explicit unknown security requirement case

Vi du:

- `Qualys`
- `Vulnerability management`

Ky vong:

- explicit open-set requirements van co suc nang trong score;
- khong bi ha thanh "signal phu" chi vi khong co trong taxonomy.

### 10.4 Promoted unknown requirement case

Vi du:

- `Active Directory`
- `DNS`
- `DHCP`

Ky vong:

- van di dung qua open-set path;
- score co su thuan tay hon explicit path.

### 10.5 Placeholder / weak JD

Ky vong:

- Phase 24 quality gate van giu;
- Phase 36 khong lam placeholder jobs bat ngo tang diem.

### 10.6 Candidate recommendation regression

Ky vong:

- top job ranking van hop ly;
- sparse jobs khong bi len hoac xuong vo ly.

## 11. Risk va cach chan regression

### 11.1 Rui ro: underweight promoted responsibilities qua muc

Neu phat qua mem,
he thong se quay lai benh cu:

- sparse JD co technical core nhung van nhu "khong co gi".

Cach chan:

- promoted source van co weight that;
- chi khac explicit o muc gate va calibration.

### 11.2 Rui ro: explicit open-set bi ha thanh low-confidence oan

Neu scorer chi thay:

- `taxonomy_status = unknown`

ma khong thay:

- `source_kind = explicit_requirement`

thi se phat sai.

Cach chan:

- provenance 2 chieu bat buoc phai duoc propagate.

### 11.3 Rui ro: explanation qua phuc tap

Neu expose qua nhieu field moi len web ngay,
UI se roi.

Cach chan:

- Phase 36 chi can output metadata ro rang;
- web/UI de Phase 37 hoac sau nua moi can hien day du.

### 11.4 Rui ro: score thay doi qua manh tren job cu

Cach chan:

- benchmark employer-side va candidate-side song song;
- uu tien calibration co gioi han;
- co regression test cho explicit-rich cases.

## 12. Dependency sanity check trong qua trinh code

Moi khi code Phase 36, can hoi nguoc 6 cau:

1. Match nay co biet requirement den tu explicit hay promoted khong?
2. Open-set match nay co giu duoc source-kind goc khong?
3. Explicit unknown requirement co bi xu ly oan giong promoted unknown khong?
4. Sparse JD co con bi phat nhu explicit-rich JD khong?
5. Placeholder / generic jobs co vo tinh tang diem khong?
6. Candidate recommendation co bi dao rank vo ly khong?

Neu trong qua trinh code phat hien:

- can them 1 provenance field nho;
- can them 1 lookup map requirement->source;
- can them 1 benchmark sparse case nho;

thi co the bo sung ngay trong Phase 36,
mien la van giu boundary:

```text
source-aware scoring calibration
chu chua sang diagnostics/web hardening lon
```

## 13. Pham vi thuc hien cua Phase 36

Phase 36 nen tap trung:

- propagate requirement provenance vao known/open-set match outputs;
- bo sung source-aware fit summary;
- bo sung source-aware score adjustment;
- refine hard-skill gate theo source profile;
- benchmark sparse JD / explicit JD / open-set explicit cases.

Phase 36 chua nen:

- sua parser section logic lon;
- sua web UI lon;
- sua admin taxonomy review workflow;
- mo rong them nhieu role-family moi.

## 14. Phase 36 duoc xem la hoan thanh khi

1. Moi must-have match duoc scorer su dung co provenance du de phan biet explicit vs promoted source.
2. Explicit unknown requirements van giu duoc vai tro manh trong scoring.
3. Sparse JD promoted-source cases khong con bi over-penalize nhu explicit-rich cases.
4. Candidate recommendation van giu parity logic voi employer screening.
5. Full test suite va benchmark regression van pass.

## 15. Gia tri bao cao do an

Phase 36 co gia tri lon khi bao cao vi co the giai thich:

```text
He thong khong xem moi requirement trong JD la ngang nhau.
No danh gia muc do rang buoc cua requirement theo nguon goc:
viet ro trong Requirements hay duoc suy ra co kiem soat tu Responsibilities.
```

Day la diem rat thuc te,
vi ngoai doi employer viet JD khong dong deu.

Neu khong co source-aware scoring,
he thong screening de:

- phat oan ung vien trong sparse JD;
- hoac nang diem oan cho overlap mem.

## 16. Huong sau Phase 36

Neu Phase 36 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 37 - Confidence and Diagnostics Guardrails
```

Phase 37 se tap trung:

- expose ro confidence theo source profile;
- canh bao recruiter khi JD dang sparse / promoted-heavy / open-set-heavy;
- giup web/API debug de hon ma khong can mo code.
