# Phase 38 - Confidence and Diagnostics Guardrails

## 1. Muc tieu phase

Sau Phase 33-37, he thong da di duoc mot doan rat quan trong:

- biet tach section trong JD;
- biet phan loai requirement theo type;
- biet lay technical signal tu responsibilities;
- biet promote co kiem soat;
- biet role-family cua cac JD technical sparse;
- biet cham diem theo source;
- biet phuc hoi technical core cho sparse JD.

Noi ngan gon:

```text
Phase 33-37 da sua logic "he thong nhin thay gi va cham gi"
Phase 38 sua logic "he thong tu tin den muc nao, canh bao gi, va web can doc gi"
```

Van de hien tai la:

```text
core logic da dung hon,
nhung confidence va diagnostics van con phan tan,
chua du ro de recruiter / web / developer doc nhanh.
```

Muc tieu cua Phase 38 la:

```text
Dat mot lop guardrails ro rang cho:
- do tin cay cua ket qua
- ly do can canh bao
- khi nao score cao nhung confidence khong cao
- khi nao sparse-JD recovery dang duoc kich hoat
- khi nao open-set / semantic path dang chiem ti le lon
```

Rat quan trong:

```text
Phase 38 khong viet lai scorer.
Phase 38 khong doi parser lon.
Phase 38 khong benchmark rong.
Phase 38 tap trung vao confidence contract va diagnostics contract.
```

## 2. Vi tri cua Phase 38 trong cay dependency hien tai

Sau khi chen them Phase 37 de chua sparse-JD technical core, thu tu hop ly hien tai la:

```text
Phase 33 -> Responsibility signal extraction foundation
Phase 34 -> Controlled responsibility-to-requirement promotion
Phase 35 -> IT support / infra role-family expansion
Phase 36 -> Source-aware scoring calibration
Phase 37 -> Sparse-JD technical core recovery
Phase 38 -> Confidence and diagnostics guardrails
Phase 39 -> Benchmark and regression pack
```

Ly do Phase 38 phai dung sau Phase 37:

```text
neu guardrails som hon,
he thong chi "giai thich cai chua dung" mot cach dep hon.

neu sparse recovery chua xong,
confidence se do tren mot scoring input van con loi.
```

Noi cach khac:

```text
Phase 37 sua dung logic cot loi
Phase 38 moi expose dung confidence va warning cho logic do
```

## 3. Van de can giai quyet

### 3.1 Score va confidence hien tai chua duoc tach ro

Trong thuc te nghiep vu:

- score tra loi cau hoi: `ung vien/job fit den dau?`
- confidence tra loi cau hoi: `he thong chac chan den dau voi nhan dinh do?`

Hien tai cac field lien quan da co mot phan:

- `screening_confidence`
- `taxonomy_coverage`
- `open_set_filter_summary`
- `explicit_technical_recovery_summary`
- `role_alignment_impact`
- `source_alignment_impact`
- `payload_diagnostics`
- `job_quality`

Nhung chung van chua duoc ket lai thanh mot lop guardrail ro rang.

Hau qua la:

```text
mot ket qua co the trong "co ve on"
nhung recruiter/web khong biet:
- score nay dua nhieu vao promoted source hay explicit source
- score nay dang co semantic-only ratio cao hay thap
- score nay dang duoc sparse recovery cuu hay khong
- score nay co nen can recruiter review ky hon khong
```

### 3.2 Diagnostics dang ton tai, nhung van phan tan va kho doc nhanh

Phase 25 da tao runtime diagnostics rat co ich.
Nhung sau Phase 33-37, so lop metadata da tang len rat nhieu.

Vi du mot request employer-side co the da co:

- payload warning
- job quality flag
- screening confidence warning
- open-set filter summary
- recovery summary
- role alignment impact
- source alignment impact

Neu khong tong hop lai, web se phai:

```text
tu suy dien tu nhieu field nho
```

va rat de:

- hien sai thong diep;
- bo sot warning quan trong;
- hoac render score nhu binh thuong du confidence dang thap.

### 3.3 Sparse-JD recovery da co, nhung recruiter chua biet no dang bat

Phase 37 da lam duoc viec rat quan trong:

```text
neu explicit technical core qua ngheo nhung responsibilities co technical signal manh,
he thong co the recover technical core mot cach co kiem soat.
```

Nhung hien tai neu recruiter chi nhin score / review card,
ho khong chac da biet:

- recovery co dang bat hay khong;
- explicit requirement technical co bi contamination hay khong;
- ket qua nay co phu thuoc manh vao promoted-source hay khong.

Day la mot lo hong debug va giai thich.

### 3.4 Open-set va semantic fallback da manh hon, nhung can guardrail

Sau cac phase truoc, he thong da co:

- open-set technical filtering;
- role-aware unknown skill governance;
- lexical evidence recovery cho unknown requirement;
- local multilingual embedding option.

Day la nang luc manh.
Nhung no cung can guardrail ro:

```text
khi nao match nay la confirmed fit
khi nao match nay chi la semantic directional evidence
```

Neu khong, recruiter hoac web se de nhin nham:

```text
co overlap nghia = da xac nhan skill
```

trong khi day khong phai dieu he thong dang muon noi.

### 3.5 Candidate-side recommendation cung can confidence,
khong chi employer-side screening

Phase 20-25 da mo them bai toan:

```text
CV -> Top 10 JD phu hop
```

Luc nay candidate-side khong chi can:

- fit score

ma con can:

- job nao dang bi sparse signal;
- job nao bi excluded;
- job nao fit nhung do tin cay con can review;
- job nao dung role-family nhung evidence con yeu.

Neu chi co employer-side diagnostics,
thi candidate-side van con mot nua bai toan chua hoan thanh.

## 4. Vi sao Phase 38 la buoc tiep theo dung nhat

Sau Phase 37, core logic da kha dung cho nhung ca sparse / noisy kho.
Luc nay dieu can nhat khong phai them scoring moi,
ma la:

```text
lam cho he thong biet cach tu "xep muc do tin cay"
va "noi ly do can canh bao" mot cach co cau truc.
```

Neu bo qua Phase 38 ma nhay sang benchmark ngay:

- benchmark van pass/fail theo so;
- nhung web va recruiter van kho doc ly do;
- khi gap ca kho van phai moi nguoi mo log tay.

Neu bo qua Phase 38 ma tiep tuc UI lon ngay:

- web de render sai nghia field;
- hoac phai suy luan tay tu metadata raw.

Noi ngan gon:

```text
Phase 38 la lop "operational safety" giua core logic va benchmark/UI.
```

## 5. Nguyen tac thiet ke

### 5.1 Confidence khong duoc dong nhat voi score

Day la nguyen tac rat quan trong.

Vi du:

- score co the kha cao vi candidate co domain + experience + role alignment;
- nhung confidence van trung binh vi hard-skill fit chu yeu dua vao promoted/open-set path.

He thong phai noi ro duoc dieu nay.

### 5.2 Guardrails khong duoc tu y doi ket qua nghiep vu chinh

Phase 38 co the:

- them warning
- them confidence label
- them diagnostics summary
- them reason code

Nhung khong nen:

- viet lai final score formula
- tu dong loai ung vien/job ma truoc do khong bi loai

Neu can exclusion / gating nghiep vu moi,
phai de sang phase khac.

### 5.3 Stable reason code quan trong hon thong diep dai

Web va log can reason code on dinh.

Vi du:

- `sparse_recovery_active`
- `promoted_source_dominant`
- `explicit_technical_contamination_detected`
- `open_set_heavy_embedding_disabled`
- `semantic_only_ratio_high`
- `weak_hard_skill_confirmation`
- `jd_quality_warning_present`

Thong diep hien thi cho nguoi dung co the doi sau,
nhung reason code nen giu on dinh.

### 5.4 Guardrails phai co the dung lai cho ca screening va recommendation

Khong nen viet 2 logic confidence tach roi.
Nen co mot bo helper co the reuse:

- employer-side screening
- candidate-side recommendation
- review card
- diagnostics runtime

### 5.5 Backward-compatible voi web hien tai

Phase 38 nen uu tien:

- them field moi dang optional
- giu field cu
- khong bat web phai sua ngay de endpoint van chay

Web co the nang cap sau,
nhung API phai tu than khong pha contract cu.

## 6. Kien truc de xuat

### 6.1 Mot lop guardrail summary moi

Nen them mot helper/module moi de tong hop metadata da co thanh:

```text
confidence profile
guardrail warnings
decision confidence summary
```

Co the dat ten kieu:

```text
src/confidence_guardrails.py
```

hoac ten tuong tu, mien la doc phat hieu ngay nhiem vu.

### 6.2 Hai tang confidence can tach ro

#### A. Job / request confidence

Tra loi:

- JD nay co du explicit technical core khong?
- sparse recovery co dang kich hoat khong?
- open-set ratio co cao khong?
- embedding co bat khi can khong?
- payload quality co warning khong?

#### B. Candidate / decision confidence

Tra loi:

- diem cua candidate nay duoc xac nhan den dau?
- hard-skill fit dang confirmed hay chu yeu semantic-only?
- evidence dang manh hay keyword-level?
- role/source adjustment co dang anh huong manh khong?

### 6.3 Screening confidence can duoc mo rong thanh guardrail-ready summary

Hien tai `screening_confidence` da co:

- `level`
- `known_requirement_count`
- `open_set_requirement_count`
- `embedding_enabled`
- `warnings`

Phase 38 nen mo rong theo huong:

- khong pha shape cu;
- co them summary de recruiter/web doc ro hon.

Vi du:

```json
{
  "screening_confidence": {...},
  "confidence_guardrails": {
    "level": "medium",
    "reason_codes": [
      "sparse_recovery_active",
      "promoted_source_dominant"
    ],
    "review_required": true
  }
}
```

### 6.4 Candidate result cung can co decision confidence rieng

Moi candidate result employer-side,
va moi top job candidate-side,
nen co mot summary compact nhu:

```json
{
  "decision_confidence": {
    "level": "medium",
    "reason_codes": [
      "weak_hard_skill_confirmation",
      "semantic_only_ratio_high"
    ],
    "confirmed_core_ratio": 0.42,
    "semantic_only_ratio": 0.33
  }
}
```

Khong can full chi tiet raw,
chi can du de:

- web render badge / note;
- log doc nhanh;
- recruiter biet khi nao can tin va khi nao can xem them.

### 6.5 Top-level diagnostics can tong hop mot lop canh bao de doc nhanh

`src/runtime_diagnostics.py` hien da co khung rat tot.
Phase 38 nen tang them:

- screening guardrail summary
- recommendation guardrail summary
- warning counts theo reason code
- sparse recovery counts / open-set heavy counts trong top jobs neu co

Muc tieu:

```text
khong can mo raw api-debug van biet request nay "dang co van de gi"
```

## 7. Cac nhom guardrail can co

### 7.1 Sparse JD / promoted-source guardrails

Canh bao cho cac case:

- `sparse_recovery_active`
- `promoted_source_dominant`
- `explicit_technical_core_sparse`
- `explicit_technical_contamination_detected`

Y nghia:

```text
JD nay van xu ly duoc,
nhung technical core cua no dang phai duoc cuu / suy ra co kiem soat,
nen recruiter nen doc ket qua voi muc review cao hon.
```

### 7.2 Open-set / embedding guardrails

Canh bao cho cac case:

- `open_set_heavy_embedding_disabled`
- `open_set_heavy_semantic_path`
- `unknown_requirement_count_high`
- `semantic_only_ratio_high`

Y nghia:

```text
he thong dang xu ly nhieu requirement ngoai taxonomy
hoac dang phu thuoc nhieu vao semantic path.
```

### 7.3 Evidence-strength guardrails

Canh bao cho cac case:

- `weak_hard_skill_confirmation`
- `evidence_mostly_keyword_level`
- `confirmed_core_ratio_low`
- `direct_evidence_sparse`

Y nghia:

```text
candidate co the co overlap,
nhung bang chung manh de xac nhan hard-skill van chua day.
```

### 7.4 Payload / quality guardrails

Canh bao cho cac case:

- `jd_quality_warning_present`
- `candidate_payload_warning_present`
- `job_payload_placeholder_signal`
- `cv_text_too_short`

Y nghia:

```text
van de co the nam o chat luong du lieu dau vao,
khong nen vo tinh quy tat ca cho scorer.
```

### 7.5 Role / source calibration guardrails

Canh bao cho cac case:

- `role_alignment_adjustment_applied`
- `source_alignment_adjustment_applied`
- `role_family_low_confidence`

Y nghia:

```text
score cuoi dang bi anh huong boi layer calibration,
can minh bach de giai thich.
```

## 8. API/output contract de xuat

### 8.1 Employer-side `/screening`

Top-level response nen co them metadata dang optional:

- `job.confidence_guardrails`
- `diagnostics.runtime.confidence_guardrails`

Moi candidate nen co them:

- `decision_confidence`

Khong doi structure co ban cua:

- `job`
- `candidates`
- `review_card`
- `diagnostics`

Chi them field.

### 8.2 Candidate-side `/recommend-jobs`

Moi `top_job` nen co them:

- `decision_confidence`
- neu can, `job_confidence_guardrails`

Top-level `diagnostics.runtime` nen tong hop:

- so job sparse recovery
- so job open-set-heavy
- so job bi warning payload/chat luong

### 8.3 Review card / explanation metadata

Phase 38 chua bat buoc web sua UI ngay,
nhung response nen co du metadata de:

- employer modal co the render badge confidence sau nay;
- candidate detail modal co the render "why review is needed";
- team web khong phai doc lai raw scoring internals.

## 9. File / module du kien can sua

### 9.1 File kha nang cao se sua

```text
src/runtime_diagnostics.py
src/payload_pipeline.py
src/job_recommendation_pipeline.py
src/screening_pipeline.py
src/candidate_job_reranker.py
src/review_card_generator.py
src/requirement_extractor.py
```

### 9.2 File moi co kha nang them

```text
src/confidence_guardrails.py
```

### 9.3 Test can sua / them

```text
tests/test_runtime_diagnostics.py
tests/test_payload_pipeline.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
tests/test_review_card_generator.py
tests/test_core_logic_benchmark.py
```

Neu can,
co the them file test rieng:

```text
tests/test_confidence_guardrails.py
```

de khoa behavior cho sach.

## 10. Hanh vi mong doi sau Phase 38

### 10.1 Sparse JD da duoc cuu se duoc danh dau ro

He thong nen noi duoc:

- sparse recovery dang bat;
- explicit technical core dang yeu;
- promoted-source dang dong vai tro lon.

Dieu nay giup recruiter:

- khong nhin score nhu mot chan ly tuyet doi;
- biet khi nao can doc review card ky hon.

### 10.2 High score nhung weak confirmation se duoc canh bao

Co nhieu case diem khong thap,
nhung hard-skill evidence van chua that su chac.

Phase 38 nen giup hien ro:

```text
score co the on,
nhung decision confidence khong nhat thiet cao
```

### 10.3 Candidate-side top job se co ly do de tin hoac review

Top jobs khong chi co:

- fit label
- fit score

ma con co:

- muc do tin cay
- ly do can review

de tranh tinh huong:

```text
job vao top nhung candidate/web khong biet vi sao AI chua that su chac
```

### 10.4 Log va diagnostics de doc nhanh hon

Khi gap case kho,
ta co the doc:

- `trace_id`
- `confidence_guardrails`
- `decision_confidence`
- `payload warnings`

ma chua can mo tung layer raw.

## 11. Acceptance criteria

Phase 38 duoc xem la hoan thanh khi:

1. He thong co mot lop confidence/guardrail summary ro rang cho screening.
2. He thong co decision-confidence summary cho candidate result va top job.
3. Sparse recovery / promoted-source dominance / semantic-heavy cases duoc danh dau bang reason code on dinh.
4. API van backward-compatible.
5. Runtime diagnostics tong hop duoc warning de doc nhanh.
6. Full test suite pass.
7. Khong doi nghia scoring cot loi trong phase nay.

## 12. Test plan de xuat

### 12.1 Unit test cho screening guardrails

Test cac case:

- explicit-rich JD, confidence cao, khong warning lon;
- sparse recovery active -> co `sparse_recovery_active`;
- open-set-heavy va embedding tat -> co `open_set_heavy_embedding_disabled`.

### 12.2 Unit test cho candidate decision confidence

Test cac case:

- confirmed hard-skill coverage cao -> level cao;
- semantic-only ratio cao -> level giam / co warning;
- evidence chu yeu keyword-level -> co `evidence_mostly_keyword_level`.

### 12.3 API regression test

Dam bao:

- field moi xuat hien dang optional;
- shape cu van doc duoc;
- trace_id van thong nhat giua response va diagnostics.

### 12.4 Screening + recommendation parity test

Can khoa mot so case ma:

- employer-side screening da gan warning;
- candidate-side recommendation cung nhin thay guardrail hop ly.

### 12.5 Review-card metadata test

Neu review card da co metadata moi,
test dam bao:

- metadata co mat;
- noi dung warning khong pha summary cu.

## 13. Dependency sanity check trong qua trinh code

Moi khi code Phase 38, can hoi nguoc it nhat 6 cau:

1. Warning nay dang noi ve score hay dang noi ve confidence?
2. Warning nay co duoc suy ra tu metadata da ton tai, hay dang phai sang tac them logic moi?
3. Sparse recovery dang duoc expose ro hay van bi chon trong diagnostics raw?
4. Candidate decision confidence co bi nham voi job/request confidence khong?
5. Field moi co backward-compatible voi web hien tai khong?
6. Reason code nay co on dinh de web map UI ve sau khong?

Neu trong qua trinh code phat hien:

- can them 1 helper confidence rieng;
- can normalize them 1 warning code;
- can expose them 1 field nho vao diagnostics;

thi duoc phep bo sung,
mien la van giu boundary:

```text
confidence + diagnostics guardrails
chu khong quay lai doi core scoring lon
```

## 14. Rui ro va cach giam rui ro

### 14.1 Rui ro: warning qua nhieu, response bi noisy

Neu moi dau hieu deu thanh warning,
web se roi va recruiter se bo qua het.

Cach giam:

- uu tien reason code co gia tri nghiep vu that;
- co lop summary thay vi dump het raw field;
- chia ro top-level guardrail va chi tiet runtime.

### 14.2 Rui ro: web nham warning thanh ket luan score

Vi du:

```text
confidence medium
```

khong co nghia:

```text
candidate yeu
```

Cach giam:

- tach ten field ro rang;
- khong dung label gay hieu nham;
- viet test contract ro.

### 14.3 Rui ro: duplicate logic giua screening va recommendation

Neu moi ben tu build warning rieng,
he thong se drift.

Cach giam:

- tach helper chung;
- unit test tren helper thay vi test tay tung endpoint la chinh.

### 14.4 Rui ro: guardrail vo tinh doi nghiep vu

Neu trong luc them confidence ma chen penalty/gate moi,
phase se vuot boundary.

Cach giam:

- keep Phase 38 chi o lop metadata / warning / summary;
- moi thay doi score lon de phase khac.

## 15. Khong nam trong pham vi Phase 38

Phase nay chua lam:

- benchmark dataset rong
- score recalibration moi
- UI recruiter/candidate polish day du
- dich toan bo review card song ngu
- GPT-assisted diagnostics rewrite
- mo rong role-family moi lon

Nhung phase sau moi lam:

```text
Phase 39 -> Benchmark and regression pack
```

va neu sau do can,
co the co them phase UI/UX rieng cho web.

## 16. Gia tri nghiep vu va gia tri bao cao

Phase 38 co gia tri rat lon khi bao cao vi co the giai thich:

```text
He thong khong chi tra ra diem.
No con tu danh gia muc do tin cay cua chinh ket qua do,
dua tren chat luong payload, nguon requirement, sparse recovery,
open-set ratio, va suc manh bang chung hard-skill.
```

Day la diem rat thuc te,
vi trong bai toan HR:

- du lieu JD/CV khong dong deu;
- he thong tot khong chi can score,
- ma con phai biet khi nao nen "tu tin",
- khi nao nen "review them".

## 17. Dau ra mong doi cua phase

Sau khi xong Phase 38, repo nen co:

- mot confidence/guardrail helper ro rang;
- screening diagnostics de doc nhanh hon;
- recommendation diagnostics de doc nhanh hon;
- decision-confidence metadata o level candidate/job;
- stable reason codes de web co the tich hop sau.

## 18. Huong sau Phase 38

Neu Phase 38 xong dung huong,
phase tiep theo hop ly nhat la:

```text
Phase 39 - Benchmark and Regression Pack
```

Phase 39 se tap trung:

- khoa cac case sparse JD da duoc chua;
- khoa cac case explicit-rich JD tranh regression;
- khoa candidate-side recommendation logic;
- dam bao cac guardrails vua them khong lam drift hanh vi toan he thong.
