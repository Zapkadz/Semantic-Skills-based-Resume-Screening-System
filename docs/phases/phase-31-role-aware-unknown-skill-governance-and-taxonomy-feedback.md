# Phase 31 - Role-aware Unknown Skill Governance and Taxonomy Feedback

## 1. Muc tieu phase

Sau Phase 30, he thong da:

- hieu role-family cua JD va CV;
- biet requirement technical nao la `core`, `supporting`, `contextual`;
- dua role-aware calibration vao score va explanation.

Nhung taxonomy feedback loop hien tai van con mot diem yeu:

```text
he thong da role-aware khi cham diem
nhung khi de xuat skill moi cho taxonomy
thi queue suggestion van chua role-aware du muc
```

Noi ngan gon:

```text
Phase 15 = co suggestion queue
Phase 16 = co merged taxonomy integration
Phase 29-30 = co role-family + intent-aware scoring
Phase 31 = dua role-awareness do quay nguoc lai governance cua unknown skills
```

Muc tieu cua Phase 31 la:

```text
Lam cho unknown skill governance thong minh hon,
giam rac trong suggestion queue,
va uu tien dung nhung requirement technical la, lap lai, dung role-family.
```

## 2. Van de can giai quyet

### 2.1 Suggestion queue hien tai van dem tan suat theo phrase la chinh

Hien tai `src/taxonomy_suggestion.py` chu yeu dua tren:

- phrase unknown
- frequency
- nearest existing skills
- example contexts

Dieu nay tot o giai doan dau,
nhung chua du cho cac case that:

- cung mot phrase xuat hien o nhieu role-family khac nhau;
- phrase nay la technical core hay chi la context chung chung;
- phrase do co bang chung semantic that hay chi la noise.

### 2.2 Queue de bi rac boi generic phrases

Vi du:

- `governance`
- `compliance exposure`
- `optimization`
- `integration`
- `customer onboarding`

Nhung phrase nay co the:

- co gia tri ngu canh;
- co lien quan role;
- nhung khong nen thanh mot taxonomy skill doc lap qua som.

Neu khong role-aware governance:

- Admin queue se nhieu muc de nham;
- de them skill chung chung vao taxonomy;
- taxonomy mo rong nhanh nhung chat luong giam.

### 2.3 He thong chua uu tien unknown requirement theo role-family

Sau Phase 29-30,
he thong da biet:

- JD nay la `COMPUTER_VISION_EKYC`
- unknown requirement nay la `core`
- overlap semantic nay chi xuat hien trong role nay

Nhung suggestion queue hien tai chua uu tien:

- skill la trong role-family cu the;
- skill core technical lap lai nhieu lan trong cung vai tro;
- skill co evidence that trong CV.

### 2.4 Chua tach ro "nen dua vao taxonomy" va "chi nen giu la context"

He thong can phan biet:

1. unknown technical skill that su
2. unknown alias cua skill da co
3. unknown requirement sentence qua dai
4. domain context / business context
5. generic action phrase

Phase 28 da loc technical open-set tot hon,
nhung Phase 31 can di them mot buoc:

```text
khong chi loc de matching,
ma con loc de governance taxonomy
```

### 2.5 Candidate-side recommendation cung can feedback loop sach

Feature `CV -> Top JD` da co.
Neu queue taxonomy van nhan nhieu noise,
thi ve lau dai:

- recommendation se hoc sai pattern role;
- custom merged taxonomy se de phinh to;
- unknown skill duoc them vao taxonomy nhung khong giup fit logic that.

## 3. Vi sao Phase 31 la buoc tiep theo dung nhat

Sau Phase 30, minh da co day du 3 lop metadata ma suggestion governance truoc day chua co:

1. `job_role_profile`
2. `requirement_intent_summary`
3. `role_alignment_impact`

Luc nay moi co the noi:

```text
skill la nao nen dua vao taxonomy truoc
va skill nao chi nen de Admin xem sau
```

Neu lam Phase 31 truoc Phase 29-30:

- suggestion chi dua tren frequency va embedding;
- kho giai thich vi sao skill nay uu tien hon skill kia.

Vi vay Phase 31 la buoc tiep theo hop ly nhat.

## 4. Muc tieu cu the cua Phase 31

Phase 31 can dat duoc:

1. Gan role-family vao tung unknown skill observation.
2. Gan technical intent vao suggestion governance.
3. Giam uu tien cho phrase generic/contextual.
4. Uu tien cho unknown skills:
   - technical
   - core/supporting hop ly
   - lap lai trong cung role-family
   - co evidence semantic that
5. Xuat suggestion queue giau metadata hon de Admin de review hon.

## 5. Nguyen tac thiet ke

### 5.1 Khong auto them skill vao taxonomy

Phase 31 van giu dung nguyen tac:

```text
AI de xuat
Admin duyet
Python validate/merge
```

### 5.2 Governance phai giai thich duoc

Moi suggestion uu tien cao phai tra loi duoc:

- xuat hien bao nhieu lan
- trong role-family nao
- technical intent la gi
- co evidence CV khong
- gan skill nao da co nhat

### 5.3 Uu tien precision hon recall

Voi queue cho Admin,
uu tien:

- it nhung sach

hon la:

- nhieu nhung rac

### 5.4 Khong pha vo queue va merged taxonomy cu

Phase 31 can mo rong output,
nhung:

- khong duoc lam hong `load_taxonomy_suggestions`
- khong duoc pha format merged taxonomy Phase 16
- khong duoc bat buoc web phai sua gap moi doc duoc queue cu

### 5.5 Metadata moi phai benchmark duoc

Khong chap nhan kieu:

```text
co ve queue dep hon
```

Ma phai co:

- benchmark case
- expected priority
- expected filtered suggestions

## 6. Huong governance de xuat

### 6.1 Role-aware observation payload

Observation hien tai nen duoc nang cap de co them:

- `job_role_family`
- `job_role_family_confidence`
- `intent_type`
- `intent_strength`
- `technical_candidate_status`
- `keep_for_suggestion`

Vi du:

```json
{
  "phrase": "face anti spoofing",
  "job_id": 22,
  "job_title": "AI Computer Vision Engineer - eKYC",
  "job_role_family": "COMPUTER_VISION_EKYC",
  "intent_type": "MODEL_TECHNIQUE",
  "intent_strength": "core",
  "technical_candidate_status": "kept_for_matching",
  "keep_for_suggestion": true
}
```

### 6.2 Role-family concentration scoring

Mot unknown skill nen duoc xem la manh hon neu:

- lap lai nhieu lan;
- phan lon xuat hien trong cung mot role-family;
- role-family do co confidence on dinh.

Vi du:

- `liveness detection` xuat hien 5 lan,
  4/5 lan trong `COMPUTER_VISION_EKYC`
  -> priority cao

- `optimization` xuat hien 6 lan,
  trai ra backend/devops/data/security
  -> priority thap

### 6.3 Intent-aware priority

Priority governance nen uu tien:

1. `core`
2. `supporting`
3. `contextual`

Va uu tien them theo `intent_type`, vi du:

- `MODEL_TECHNIQUE`
- `SECURITY_CONTROL`
- `CORE_STACK`

cao hon:

- `GENERIC_TECHNICAL`

### 6.4 Evidence-backed suggestion

Neu unknown requirement co semantic evidence that trong CV,
do la dau hieu skill nay:

- co kha nang la skill that;
- khong chi nam tren JD;
- co gia tri screening that.

Vi vay suggestion nen track:

- bao nhieu observation co evidence
- similarity trung binh / cao nhat
- example evidence theo role-family

### 6.5 Alias-vs-new-skill distinction

Can them logic governance de tach:

1. co kha nang la alias cua skill da co
2. co kha nang la skill moi that su

Vi du:

- `face anti spoofing`
  co nearest skill rat gan `Anti-Spoofing`
  -> uu tien de xuat alias/merge

- `passkey authentication`
  khong gan skill nao da co
  -> uu tien de xuat skill moi

## 7. Output metadata de xuat

Suggestion Phase 31 nen co them:

- `role_family_distribution`
- `dominant_role_family`
- `dominant_role_family_ratio`
- `intent_distribution`
- `evidence_support_count`
- `alias_candidate`
- `governance_priority`
- `governance_priority_score`
- `review_reason`

Vi du:

```json
{
  "suggestion_id": "tax-sug-face-anti-spoofing",
  "suggested_canonical_name": "Face Anti-Spoofing",
  "frequency": 4,
  "dominant_role_family": "COMPUTER_VISION_EKYC",
  "dominant_role_family_ratio": 1.0,
  "intent_distribution": {
    "core": 4
  },
  "evidence_support_count": 3,
  "alias_candidate": true,
  "governance_priority": "high",
  "governance_priority_score": 0.91,
  "review_reason": "Repeated core technical signal concentrated in one role family with supporting evidence."
}
```

## 8. Luat priority de xuat

### 8.1 High priority

Mot suggestion nen la `high` khi:

- frequency >= 2
- dominant role-family ratio cao
- intent nghieng ve `core`
- co evidence support
- phrase khong qua generic

### 8.2 Medium priority

Mot suggestion nen la `medium` khi:

- frequency du
- technical signal co
- nhung role-family con phan tan
  hoac evidence chua manh

### 8.3 Low priority

Mot suggestion nen la `low` khi:

- phrase qua generic
- intent chu yeu `contextual`
- role-family phan tan
- khong co evidence

### 8.4 Suppress / do not suggest

Mot candidate phrase nen bi loai khoi queue neu:

- la generic action phrase
- la business context phrase
- la requirement sentence qua dai
- da bi discard tu filter technical

## 9. File/module du kien can sua

### 9.1 File chinh

- `src/taxonomy_suggestion.py`

### 9.2 File ho tro pipeline metadata

- `src/payload_pipeline.py`
- `src/screening_pipeline.py`
- `src/job_catalog_loader.py`
- `src/job_recommendation_pipeline.py`
- co the can `src/requirement_extractor.py`
- co the can `src/open_set_requirement_filter.py`

### 9.3 CLI / docs

- `taxonomy_suggest.py`
- `docs/phases/phase-31-role-aware-unknown-skill-governance-and-taxonomy-feedback.md`

### 9.4 Tests

- `tests/test_taxonomy_suggestion.py`
- `tests/test_payload_pipeline.py`
- `tests/test_job_catalog_loader.py`
- `tests/test_job_recommendation_pipeline.py`
- co the them `tests/test_unknown_skill_governance.py`

## 10. Huong implementation de xuat

### 10.1 Nang cap observation collection

`collect_unknown_requirement_observations(...)`
nen lay them tu screening result:

- `job.job_role_profile`
- `job.requirement_intent_summary`
- `job.open_set_candidates`
- `job.open_set_filter_summary`

De moi observation khong chi biet phrase,
ma con biet phrase do xuat hien trong loai role nao.

### 10.2 Them requirement-intent lookup cho suggestion builder

Khi phrase unknown da co trong `requirement_intent_summary`,
observation nen ke thua:

- `intent_type`
- `intent_strength`

De suggestion builder dung duoc ngay,
khong can suy doan lai tu dau.

### 10.3 Them governance scoring

Trong `src/taxonomy_suggestion.py`,
them mot ham kieu:

```text
calculate_governance_priority(...)
```

No se tong hop:

- frequency
- dominant role-family ratio
- intent strength
- evidence support
- nearest skill closeness

### 10.4 Them alias candidate detection

Neu nearest skill similarity rat cao,
suggestion nen duoc danh dau:

- `alias_candidate = true`

De Admin biet:

- co the them alias vao skill cu
- khong nhat thiet tao skill moi

### 10.5 Them review reason

Queue cho Admin nen co `review_reason` ngan gon.

Vi du:

- `Repeated core security-control signal concentrated in SECURITY_GRC jobs.`
- `Likely alias of existing skill Anti-Spoofing based on high nearest-skill similarity.`

## 11. Benchmark can khoa o Phase 31

### 11.1 Core unknown skill trong mot role-family cu the

Vi du:

- `face anti spoofing`
- `face liveness`

Chi tap trung trong `COMPUTER_VISION_EKYC`

Ky vong:

- suggestion duoc uu tien cao
- review reason ro

### 11.2 Generic phrase xuat hien nhieu role-family

Vi du:

- `optimization`
- `integration`

Ky vong:

- khong len high priority
- co the low priority
  hoac bi suppress

### 11.3 Security control alias case

Vi du:

- `vuln management`
- `vulnerability management`

Ky vong:

- duoc nhan la alias candidate
- nearest existing skill ro

### 11.4 Requirement da bi discard khong duoc vao queue

Ky vong:

- Phase 28 filter da discard roi
  thi Phase 31 governance khong nhan lai

## 12. Manual benchmark de xuat

Sau khi code, nen chay:

1. `JD_4 + CV_4_1/CV_4_2/CV_4_3`
2. 1 bo security/GRC unknown requirements
3. 1 bo generic placeholder/generic phrases
4. `taxonomy_suggest.py` tren nhieu result JSON gop lai

Can doi chieu:

- phrase nao vao queue
- priority nao
- role-family nao chi phoi
- phrase nao bi suppress

## 13. Pham vi thuc hien cua Phase 31

Phase 31 nen tap trung:

- role-aware taxonomy governance
- role-aware suggestion priority
- alias-vs-new-skill distinction
- queue metadata giau hon

Phase 31 chua nen:

- sua Admin web UI
- sua merged taxonomy schema Phase 16
- auto approve skill
- dua GPT vao governance loop

## 14. Tieu chi hoan thanh

Phase 31 duoc xem la hoan thanh khi:

1. Suggestion queue co role-aware metadata moi.
2. Generic/contextual phrase bi ha uu tien hoac suppress hop ly.
3. Core unknown skills tap trung trong mot role-family duoc uu tien cao.
4. Alias candidate duoc danh dau ro hon.
5. Full test suite van pass.

## 15. Gia tri cho bao cao va phan bien

Phase 31 co gia tri rat lon khi bao cao vi co the noi:

```text
He thong khong chi mo rong taxonomy theo tan suat phrase,
ma mo rong theo dung ngu canh role-family,
technical intent, va bang chung thuc te.
```

Day la diem rat manh de tra loi cac cau hoi:

- Tai sao skill la nay duoc de xuat them vao taxonomy?
- Tai sao phrase nay khong duoc de xuat du xuat hien nhieu?
- Lam sao tranh taxonomy bi phinh boi phrase chung chung?

## 16. Huong sau Phase 31

Sau khi queue unknown skill da role-aware hon,
buoc tiep theo hop ly la:

```text
Phase 32 - Taxonomy Governance Benchmark and Admin Review Contract Hardening
```

Phase 32 co the tap trung:

- benchmark governance data that hon;
- chot contract Python <-> Web/Admin cho import/review/export;
- them regression suite cho merged taxonomy feedback loop.
