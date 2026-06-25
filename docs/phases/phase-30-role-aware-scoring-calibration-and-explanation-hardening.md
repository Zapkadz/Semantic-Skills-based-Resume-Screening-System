# Phase 30 - Role-aware Scoring Calibration and Explanation Hardening

## 1. Muc tieu phase

Sau Phase 29, he thong da co:

- `job_role_profile`
- `candidate_role_profile`
- `role_family_alignment`
- `requirement_intent_summary`

Tuc la he thong da bat dau:

```text
biet JD dang can role-family nao
va CV dang nghiêng ve role-family nao
```

Nhung Phase 29 moi dung lai o muc:

- them metadata role-family;
- calibration nhe;
- note role-aware trong review card.

Van con mot lop van de logic rat quan trong:

```text
role-family da co, nhung scorer va explanation van chua du sac
de chong overrate / underrate mot cach on dinh
```

Noi ngan gon:

```text
Phase 29 = biet role-family va technical intent
Phase 30 = dua role-family do vao score va explanation mot cach co kiem soat
```

Muc tieu cua Phase 30 la:

```text
Lam cho scorer, review card, va candidate recommendation
that su role-aware hon,
nhung khong pha vo hard-skill gate, weighted scoring,
va khong bien he thong thanh hop den kho giai thich.
```

## 2. Van de can giai quyet

### 2.1 Role-family da co nhung anh huong len score van chua du manh

Phase 29 da them `role_family_alignment`,
nhung hien tai no moi la 1 lop calibration nhe.

Van co nguy co:

- CV AI chung chung van an diem tu semantic overlap;
- CV security governance chung van gan diem voi role can hands-on;
- CV backend co Docker/Python/AWS van co the duoc nhin dep voi role Data/ML hoac CV/eKYC hon muc hop ly.

Neu khong lam Phase 30:

- metadata role-family chi de "trang tri output";
- score chua thay doi du muc voi cac ca benh logic kho;
- explanation va score co the con lech nhau.

### 2.2 Requirement intent da co nhung chua tham gia vao decision boundary

Phase 29 da gan:

- `intent_type`
- `intent_strength`
- `intent_reason`

Nhung he thong van chua su dung day du de phan biet:

- core requirement
- supporting requirement
- contextual technical signal

Neu khong dua phan nay vao scorer:

- `face recognition` va `Python` co the dang bi xem qua gan nhau trong mot so case;
- `Qualys` va `compliance exposure` co the chua tach du ro khi cham fit.

### 2.3 Explanation recruiter-side va candidate-side van chua dong nhat voi logic moi

Sau Phase 29,
review card da co them role note,
nhung van con thieu:

- note nao la core mismatch;
- note nao la adjacent-role overlap;
- note nao la semantic-only weak fit;
- note nao la transferable but not primary-fit.

Neu explanation khong sac:

- recruiter kho tin AI;
- candidate-side goi y cai thien CV chua that su dung role;
- giang vien hoi "score nay dua tren cai gi?" se kho tra loi gon va thuyet phuc.

### 2.4 Candidate-side recommendation can role-aware hon recruiter-side screening

Employer screening:

- co the chap nhan recruiter review them.

Candidate-side Top JD:

- can xep hang thuyet phuc hon ngay tu dau;
- khong nen de job "na na" len qua cao;
- can goi y improvement dung role-family cua tung job.

Vi vay Phase 30 rat quan trong voi:

- top 10 JD phu hop;
- fit label;
- skill-gap explanation;
- CV improvement suggestions.

### 2.5 He thong can tranh 2 kieu sai nguoc nhau

Phase 30 khong chi chong overrate.

Con phai tranh:

1. **Overrate**  
   CV co overlap chung chung nhung score cao qua.

2. **Underrate**  
   CV dung role-family, co evidence that, nhung vi taxonomy/open-set chua dep hoan hao nen bi ha diem qua tay.

Phase 30 phai giu can bang:

```text
precision cao hon,
nhung khong qua cứng den muc bo sot ung vien tot
```

## 3. Vi sao Phase 30 la buoc tiep theo dung nhat

Sau Phase 29, he thong da co du 3 lop nen:

1. typed requirement schema
2. open-set technical filter
3. role-family + technical intent

Luc nay moi co the lam:

```text
role-aware scoring calibration that su
```

Neu lam som hon:

- khong co du metadata;
- scoring se thanh "chinh tay theo cam giac".

Neu de muon hon:

- web/API se tiep tuc tra score chua du sac;
- candidate recommendation se khong dat muc thuyet phuc cao.

Vi vay Phase 30 la buoc tiep theo hop ly nhat.

## 4. Muc tieu cu the cua Phase 30

Phase 30 can dat duoc:

1. Dua `role_family_alignment` vao scorer ro hon.
2. Dua `intent_strength` vao viec phan biet core/supporting fit.
3. Giam diem hop ly cho semantic-only fit lech role-family.
4. Bao ve cac CV dung role-family co evidence that.
5. Lam review card / candidate recommendation explanation dong bo voi logic cham diem.

## 5. Nguyen tac thiet ke

Phase 30 phai tuan theo 5 nguyen tac:

### 5.1 Khong pha hard-skill gate

Hard-skill gate van la lop chan cung.

Role-aware calibration:

- khong duoc ghi de no;
- chi duoc calibration bo sung.

### 5.2 Khong viet lai scorer tu dau

Phase 30 nen mo rong scorer hien tai,
khong nen tao mot scorer moi.

### 5.3 Uu tien giam score trong cac case risk cao

Phase 30 uu tien xu ly cac case:

- semantic-only but wrong role;
- evidence weak but score dang dep;
- adjacent-role overlap bi hieu nham thanh strong fit.

### 5.4 Explanation phai noi trung cai scorer da lam

Neu score bi giam vi role-family mismatch,
review card va candidate recommendation phai noi ro ly do do.

### 5.5 Moi thay doi phai benchmark duoc

Khong chap nhan kieu:

```text
score co ve hop ly hon
```

ma phai co:

- test case
- benchmark case
- expected behavior

## 6. Huong scoring de xuat

### 6.1 Tach `raw_score`, `role_calibrated_score`, `final_score`

Hien tai he thong da co:

- `raw_base_score` / `base_score` / `final_score`

Phase 30 nen lam ro hon:

- `raw_base_score`: diem weighted goc
- `role_calibrated_score`: sau khi role-aware calibration
- `final_score`: sau hard-skill gate

Muc tieu:

- debug de;
- benchmark de;
- giang vien hoi de tra loi;
- web muon hien diagnostics cung ro hon.

### 6.2 Core-role penalty

Neu JD co nhieu `core` intents,
nhung candidate chi co:

- weak evidence
- semantic-only overlap
- lech role-family

thi he thong nen giam score hop ly.

Penalty nay khong nen dung cho moi case,
chi dung khi:

- core requirement count du lon;
- positive coverage co nhung weak;
- role-family mismatch ro.

### 6.3 Adjacent-role soft penalty

Khong phai role-family nao khac nhau cung phai giam manh.

Vi du:

- `DATA_AI_ENGINEERING` gan `COMPUTER_VISION_EKYC`
- `BACKEND_ENGINEERING` gan `FULLSTACK_ENGINEERING`
- `FRONTEND_ENGINEERING` gan `FULLSTACK_ENGINEERING`

Phase 30 nen co:

- mismatch manh
- adjacent mismatch nhe
- generic fallback trung lap xet sau

### 6.4 Evidence-quality amplification

Neu candidate dung role-family
va evidence manh o project/work sections,
Phase 30 co the:

- giu diem on dinh;
- hoac bonus rat nhe trong gioi han an toan.

Muc dich:

- tranh underrate CV that su dung role-family;
- uu tien evidence that hon keyword fit.

### 6.5 Semantic-only control

Semantic-only fit la noi nguy hiem nhat.

Phase 30 nen bo sung luat:

- semantic-only + strong same-role evidence -> chap nhan tot hon
- semantic-only + adjacent role -> xem la partial fit
- semantic-only + wrong role -> giam score ro rang

## 7. Huong explanation de xuat

### 7.1 Recruiter review card

Review card nen biet noi ro 4 tinh huong:

1. `Strong same-role fit`
2. `Adjacent-role overlap`
3. `Generic technical overlap only`
4. `Misaligned primary role-family`

Vi du:

- `The candidate has strong evidence in the same Computer Vision/eKYC role family as the JD.`
- `The profile overlaps with adjacent AI/ML capabilities, but direct Computer Vision/eKYC evidence is still limited.`
- `The candidate shows strong Backend evidence, while this JD is primarily Security/GRC-oriented.`

### 7.2 Candidate-side explanation

Candidate-side phai noi theo huong:

- vi sao job nay hop / chua hop;
- can bo sung gi de tang fit;
- thieu cai gi o core role-family cua job.

Vi du:

- `You already match the core Backend stack, but this role also expects production AWS exposure.`
- `Your profile overlaps with AI/ML, but this JD is specifically Computer Vision/eKYC-focused, so face recognition and liveness evidence matter more.`

### 7.3 Requirement notes role-aware hon

`requirement_notes` nen bo sung:

- core role-family mismatch
- adjacent-role caution
- semantic-only caution

nhung phai ngan gon,
khong lap lai `concerns`.

## 8. Metadata output de xuat

Phase 30 nen bo sung output:

- `role_calibrated_score`
- `role_score_adjustment`
- `core_requirement_fit_summary`
- `role_alignment_impact`

### 8.1 Screening candidate output

```json
{
  "raw_base_score": 76,
  "role_calibrated_score": 70,
  "final_score": 69,
  "role_score_adjustment": -6,
  "role_alignment_impact": {
    "status": "misaligned",
    "reason": "semantic-only overlap with a different primary role family"
  }
}
```

### 8.2 Recommendation top-job output

```json
{
  "fit_score": 70,
  "role_score_adjustment": -4,
  "role_alignment_impact": {
    "status": "partial_alignment",
    "reason": "adjacent role-family overlap"
  }
}
```

## 9. File/module du kien can sua

### 9.1 File chinh

- `src/scorer.py`
- `src/review_card_generator.py`
- `src/candidate_job_reranker.py`
- `src/skill_gap_explainer.py`

### 9.2 File pipeline/output

- `src/payload_pipeline.py`
- `src/screening_pipeline.py`
- `src/job_recommendation_pipeline.py`
- `src/runtime_diagnostics.py`
- `api.py`

### 9.3 Tests

- `tests/test_scorer.py`
- `tests/test_review_card_generator.py`
- `tests/test_payload_pipeline.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_core_logic_benchmark.py`

## 10. Benchmark can khoa o Phase 30

### 10.1 CV/eKYC dung role vs AI chung chung

Can co benchmark:

- 1 CV computer vision/eKYC that
- 1 CV AI/ML chung chung

Ky vong:

- CV dung role phai cao hon ro;
- CV chung chung khong duoc len ngang.

### 10.2 Security/GRC hands-on vs governance broad

Can co benchmark:

- 1 CV co `Qualys`, `vulnerability management`, `access control`, `ISO 27001`
- 1 CV broad governance/compliance khong co hands-on evidence

Ky vong:

- hands-on CV phai hon broad CV;
- broad CV co the van dat muc review,
  nhung khong duoc an diem nhu core hands-on fit.

### 10.3 Backend vs Fullstack adjacent-role

Can co benchmark:

- backend strong
- fullstack moderate

Ky vong:

- fullstack khong bi ha diem vo ly;
- nhung backend strong van dung top cho backend JD.

### 10.4 Placeholder/generic job van phai bi quality gate

Phase 30 khong duoc lam vo Phase 24.

## 11. Manual benchmark de xuat

Sau khi code, nen chay:

1. `JD_3 + CV_3_1/CV_3_3`
2. `JD_4 + CV_4_1/CV_4_2/CV_4_3`
3. Candidate recommendation voi bo job that tren web
4. Employer screening voi job security/GRC tren web

Can doi chieu:

- raw score
- role-calibrated score
- final score
- recommendation
- review notes

## 12. Pham vi thuc hien cua Phase 30

Phase 30 nen tap trung:

- role-aware score calibration
- explanation hardening
- diagnostics ro hon
- benchmark regression

Phase 30 chua nen:

- mo rong them nhieu role-family moi
- doi taxonomy structure lon
- them GPT/LLM layer
- sua UI web
- sua admin taxonomy workflow

## 13. Tieu chi hoan thanh

Phase 30 duoc xem la hoan thanh khi:

1. Score khong con de overrate cac CV overlap chung chung nhung lech role-family.
2. CV dung role-family co evidence that khong bi underrate vo ly.
3. Review card va candidate-side explanation noi ro vi sao role-aware calibration duoc ap dung.
4. Full benchmark Phase 26-29 van pass.
5. Full test suite van pass.

## 14. Rui ro va cach kiem soat

### 14.1 Rui ro

- penalty qua tay lam score tut qua manh;
- explanation dai dong;
- adjacent-role bi xu phat nhu wrong-role;
- web kho doc them metadata.

### 14.2 Cach kiem soat

- gioi han muc dieu chinh score;
- tach `raw_base_score` va `role_calibrated_score`;
- benchmark tren ca employer-side va candidate-side;
- explanation ngan, co cau truc on dinh.

## 15. Gia tri cho bao cao va phan bien

Phase 30 rat co gia tri khi bao cao vi co the noi:

```text
He thong khong chi biet role-family,
ma con dua role-family vao co che cham diem mot cach minh bach,
co benchmark va co ly do giai thich cu the.
```

Day la diem giup tra loi cac cau hoi kieu:

- Vi sao cung co Python ma diem khac nhau?
- Vi sao CV AI nay khong cao bang CV computer vision kia?
- Vi sao CV compliance broad lai thap hon CV security hands-on?

## 16. Huong sau Phase 30

Sau khi scorer va explanation da role-aware on hon,
buoc tiep theo hop ly la:

```text
Phase 31 - Role-aware Unknown Skill Governance and Taxonomy Feedback
```

Phase 31 se tap trung:

- dua role-family vao taxonomy suggestion queue;
- lam admin review de hon;
- uu tien unknown skill theo role-family va tan suat that.
