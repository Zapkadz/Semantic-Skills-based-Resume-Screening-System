# Phase 29 - Role-family Technical Intent Inference

## 1. Muc tieu phase

Sau Phase 28, he thong da:

- tach requirement theo type tot hon;
- loc open-set technical sach hon;
- giam nhieu requirement rac di vao semantic matching.

Nhung van con 1 lop benh logic lon:

```text
he thong da biet requirement nao la technical
nhung chua hieu requirement do phuc vu kieu vai tro ky thuat nao
```

Noi ngan gon:

```text
Phase 27 = biet requirement thuoc loai nao
Phase 28 = chi giu unknown requirement technical that su
Phase 29 = hieu requirement technical do dang thuoc role-family nao
```

Muc tieu cua Phase 29 la:

```text
Them lop role-family va technical intent inference vao giua
typed requirement/open-set matching va scoring,
de he thong khong chi match duoc chu,
ma con biet match do co dung "nghe ky thuat" cua JD hay khong.
```

## 2. Van de can giai quyet

### 2.1 Match dung tu nhung sai nghia nghe nghiep

Vi du:

- JD thuoc nhom `Computer Vision / eKYC`
- CV co nhieu keyword AI chung, Python, deployment, analytics

He thong co the match duoc nhieu term,
nhung van chua du co so de ket luan ung vien phu hop voi role
`Computer Vision / Face Liveness / Anti-Spoofing`.

Neu khong co role-family layer:

- score de bi dep gia tao;
- explanation chua sac;
- recruiter thay AI "co ve hop ly" nhung chua dung ban chat role.

### 2.2 Cung mot term co the mang y nghia khac nhau theo role

Vi du:

- `Python`
- `Docker`
- `AWS`
- `monitoring`

Nhung term nay co the xuat hien trong:

- Backend
- Data/ML
- Computer Vision
- DevOps
- Security engineering

Neu he thong chi thay tu khoa ma khong co role-family:

- de overrate CV co stack chung chung;
- kho phan biet core role fit va peripheral overlap.

### 2.3 Open-set technical da sach hon nhung van chua co ngu canh nghe

Phase 28 da giu lai cac cum ky thuat nhu:

- `face recognition`
- `anti-spoofing`
- `vulnerability management`
- `identity verification`

Nhung he thong van chua biet:

- cum nay la core cho role nao;
- cum nay la hard-core requirement hay chi la supporting capability;
- candidate evidence co that su nam trong role-family do hay khong.

### 2.4 Scoring hien tai van chua co role-aware control

Scoring hien tai da co:

- hard-skill gate;
- evidence;
- experience;
- domain;
- nice-to-have;
- weighted scoring.

Nhung van thieu:

```text
candidate nay co dung "loai ky su / loai chuyen mon"
ma JD dang can hay khong
```

Day la diem ma giang vien de hoi:

- vi sao cung la AI engineer ma role computer vision khac NLP?
- vi sao cung la security ma GRC khac hands-on security operations?
- vi sao cung co Python ma backend Python khac ML Python?

### 2.5 Taxonomy suggestion queue cung can them ngu canh role-family

Neu mot unknown technical term xuat hien:

- chi biet no la technical thi chua du;
- can biet no hay xuat hien trong role-family nao.

Vi du:

- `ArcFace` nghieng ve `Computer Vision / Biometrics`
- `Qualys` nghieng ve `Security / Vulnerability Management`
- `Spring Boot` nghieng ve `Backend`

Neu co role-family context, admin de:

- review suggestion nhanh hon;
- group skill dung hon;
- tranh them skill vao sai category.

## 3. Vi sao Phase 29 la buoc tiep theo dung nhat

Sau Phase 28:

- requirement typing da co;
- open-set technical pool da sach hon;
- benchmark regression da duoc khoa.

Luc nay moi co the them lop:

```text
role-family interpretation
```

neu khong se gap 2 nguy co:

1. them qua som khi open-set con rac -> role-family suy luan tren du lieu ban;
2. de qua muon -> scoring tiep tuc dep ben ngoai nhung sai nghia role.

Vi vay, Phase 29 la buoc tiep theo hop ly nhat vi:

- dau vao da du sach;
- benchmark da san;
- pain point nghiep vu hien tai rat ro;
- phu hop voi nhung case user dang gap tren web that.

## 4. Muc tieu cu the cua Phase 29

Phase 29 can dat duoc:

1. Suy ra `job_role_family` cho moi JD.
2. Suy ra `candidate_role_family_signals` tu CV/evidence.
3. Gan `technical_intent` cho requirement technical/open-set requirement.
4. Dung role-family de kiem soat semantic matching va scoring.
5. Giai thich duoc ly do:
   - match dung role-family;
   - match chenh role-family;
   - unknown requirement thuoc role-family nao.

## 5. Ket qua dau ra mong muon

Sau Phase 29, output screening/recommendation nen co them:

- `job_role_profile`
- `candidate_role_profile`
- `requirement_intent_summary`
- `role_family_alignment`
- `role_alignment_notes`

Muc tieu khong phai la "doan nghe nghiep tuyet doi chinh xac",
ma la:

```text
co mot lop suy luan role-family co kiem soat,
du de cai thien scoring va explanation
```

## 6. Kien truc nghiep vu de xuat

### 6.1 Luong tong quat

```text
JD text
-> section-aware parsing
-> typed requirements
-> open-set technical filtering
-> job role-family inference
-> requirement technical-intent inference

CV text
-> resume parsing
-> skill extraction
-> evidence detection
-> candidate role-family evidence inference

Sau do:
-> role-aware matching / weighting
-> scoring
-> review card / candidate recommendation explanation
```

### 6.2 Nguyen tac

Phase 29 uu tien:

- rule-based / heuristic co giai thich duoc;
- role-family nho, co kiem soat;
- khong dung model generative de doan role;
- khong lam scorer qua "ma thuat".

## 7. Role-family schema de xuat

Khong nen tao qua nhieu role-family ngay.

Phase 29 nen bat dau voi tap nho, gan voi data hien tai:

- `BACKEND_ENGINEERING`
- `FRONTEND_ENGINEERING`
- `FULLSTACK_ENGINEERING`
- `DATA_AI_ENGINEERING`
- `COMPUTER_VISION_EKYC`
- `SECURITY_GRC`
- `DEVOPS_CLOUD`
- `MOBILE_ENGINEERING`
- `QA_AUTOMATION`
- `GENERIC_TECH`

### 7.1 Vi sao khong can qua nhieu role-family

Neu role-family qua chi tiet qua som:

- heuristic rat de vo;
- benchmark it;
- web/debug kho doc;
- kho bao ve voi giang vien.

Phase 29 chi can:

- role-family du lon de tach nhom role quan trong;
- du nho de suy luan on dinh.

## 8. Technical intent schema de xuat

Ngoai `role_family`, moi requirement technical nen co:

- `intent_type`
- `intent_strength`
- `intent_reason`

### 8.1 `intent_type`

Co the bat dau voi:

- `CORE_STACK`
- `TOOLING_PLATFORM`
- `METHOD_CAPABILITY`
- `SECURITY_CONTROL`
- `MODEL_TECHNIQUE`
- `DEPLOYMENT_RUNTIME`
- `GENERIC_TECHNICAL`

### 8.2 `intent_strength`

Gia tri don gian:

- `core`
- `supporting`
- `contextual`

Y nghia:

- `core`: thieu la rat anh huong fit
- `supporting`: co gia tri lon nhung khong dinh nghia toan bo role
- `contextual`: co lien quan ky thuat nhung khong nen over-weight

## 9. Luat suy luan role-family cho JD

### 9.1 Dau vao dung de suy luan

He thong nen dung:

- job title;
- must-have technical requirements;
- open-set technical requirements;
- responsibilities;
- known taxonomy skills;
- typed requirements.

### 9.2 Luat suy luan uu tien

He thong co the chay theo thu tu:

1. title signals
2. explicit technical requirement signals
3. responsibility signals
4. open-set technical signals
5. fallback to `GENERIC_TECH`

### 9.3 Vi du luat

Neu JD co:

- `face recognition`
- `liveness detection`
- `anti-spoofing`
- `ArcFace`
- `eKYC`

thi role-family nghieng manh ve:

```text
COMPUTER_VISION_EKYC
```

Neu JD co:

- `Qualys`
- `ISO 27001`
- `vulnerability management`
- `access control`
- `compliance`

thi role-family nghieng ve:

```text
SECURITY_GRC
```

Neu JD co:

- `Java`
- `Spring Boot`
- `REST API`
- `SQL`
- `microservice`

thi role-family nghieng ve:

```text
BACKEND_ENGINEERING
```

## 10. Luat suy luan role-family cho candidate

Candidate profile khong nen doan chi tu `candidate_name` hoac title mo ho.

Nen dua tren:

- extracted skills;
- matched evidence text;
- project/work experience evidence;
- open-set semantic evidence;
- headline/summary neu co.

### 10.1 Khong can ep candidate vao 1 role duy nhat

Candidate co the co:

- primary role-family
- secondary role-family
- signal distribution

Vi du:

```json
{
  "primary_role_family": "BACKEND_ENGINEERING",
  "secondary_role_families": ["DEVOPS_CLOUD"],
  "signals": {
    "BACKEND_ENGINEERING": 0.82,
    "DEVOPS_CLOUD": 0.41,
    "DATA_AI_ENGINEERING": 0.10
  }
}
```

## 11. Cach dua role-family vao matching

Phase 29 khong nen viet lai toan bo matcher.

Nen bo sung co kiem soat:

### 11.1 Exact / related / transferable match

Van giu nhu hien tai.

Nhung co the them metadata:

- requirement role-family
- candidate evidence role-family
- role alignment status

### 11.2 Semantic/open-set matching

Day la noi can role-family nhat.

Can them rule:

- semantic match cung role-family -> tin cay cao hon
- semantic match role-family lan can -> trung lap xet tiep
- semantic match lech role-family ro -> giam do tin cay hoac note de recruiter review

### 11.3 Khong cap score chi vi similarity dep

Can tranh tinh huong:

- cosine similarity dep
- nhung evidence thuoc role-family khac
- he thong van cham cao

## 12. Cach dua role-family vao scoring

Phase 29 nen them 1 lop nho, khong pha base scorer.

### 12.1 Huong de xuat

Them 3 thanh phan metadata:

- `job_role_family`
- `candidate_role_alignment`
- `requirement_intent_summary`

Sau do chi can:

1. them `role_alignment_modifier`
2. them `review notes`
3. cap/giam nhe cho semantic-only cases

### 12.2 Nguyen tac scoring

Phase 29 khong nen:

- thay doi manh weighted scoring tong;
- lam score nhay qua lon;
- de role-family ghi de hard-skill gate.

Nen uu tien:

- hard-skill gate van la lop chan cung;
- role-family la lop calibration;
- open-set semantic score la noi duoc dieu chinh ro nhat.

### 12.3 Vi du

Candidate co:

- Python
- AWS
- analytics

JD can:

- face recognition
- liveness detection
- anti-spoofing

Thi:

- co the van co overlap technical nho;
- nhung role-family alignment phai thap;
- khong duoc de score dep nhu CV computer vision that.

## 13. Review card / explanation can thay doi gi

Sau Phase 29, review card nen co note kieu:

- `Technical evidence is present, but most evidence appears closer to Backend than Computer Vision.`
- `Candidate shows Security/GRC alignment, but hands-on Vulnerability Management evidence is still limited.`
- `The JD is strongly Computer Vision/eKYC-oriented and the CV has matching project evidence in the same role family.`

Candidate-side recommendation cung nen co:

- `why_fit` role-aware hon
- `what_to_improve` dung role-family hon

## 14. Admin taxonomy suggestion layer co the dung gi tu phase nay

Suggestion queue co the bo sung:

- `observed_role_families`
- `dominant_role_family`

Vi du:

```json
{
  "suggested_canonical_name": "ArcFace",
  "dominant_role_family": "COMPUTER_VISION_EKYC"
}
```

Phase 29 chua can sua toan bo admin flow,
nhung nen de san metadata.

## 15. File/module du kien can tao hoac sua

### 15.1 File moi de xuat

- `src/role_family.py`
- `src/technical_intent.py`

### 15.2 File can sua

- `src/jd_requirement_classifier.py`
- `src/requirement_extractor.py`
- `src/open_set_matcher.py`
- `src/evidence_detector.py`
- `src/scorer.py`
- `src/review_card_generator.py`
- `src/payload_pipeline.py`
- `src/screening_pipeline.py`
- `src/job_catalog_loader.py`
- `src/candidate_job_reranker.py`
- `src/job_recommendation_pipeline.py`
- `src/runtime_diagnostics.py`

### 15.3 Tests de xuat

- `tests/test_role_family.py`
- `tests/test_technical_intent.py`
- `tests/test_payload_pipeline.py`
- `tests/test_screening_pipeline.py`
- `tests/test_job_recommendation_pipeline.py`
- `tests/test_core_logic_benchmark.py`

## 16. Contract output de xuat

### 16.1 Job output

```json
{
  "job_role_profile": {
    "primary_role_family": "COMPUTER_VISION_EKYC",
    "confidence": 0.91,
    "signals": {
      "COMPUTER_VISION_EKYC": 0.91,
      "DATA_AI_ENGINEERING": 0.34
    }
  }
}
```

### 16.2 Candidate output

```json
{
  "candidate_role_profile": {
    "primary_role_family": "DATA_AI_ENGINEERING",
    "secondary_role_families": ["COMPUTER_VISION_EKYC"],
    "signals": {
      "DATA_AI_ENGINEERING": 0.73,
      "COMPUTER_VISION_EKYC": 0.52
    }
  },
  "role_family_alignment": {
    "status": "partial_alignment",
    "job_role_family": "COMPUTER_VISION_EKYC",
    "candidate_primary_role_family": "DATA_AI_ENGINEERING"
  }
}
```

### 16.3 Requirement-level metadata

```json
{
  "required_skill": "face recognition",
  "taxonomy_status": "unknown",
  "role_family": "COMPUTER_VISION_EKYC",
  "intent_type": "MODEL_TECHNIQUE",
  "intent_strength": "core"
}
```

## 17. Benchmark can khoa o Phase 29

### 17.1 CV/eKYC case

JD:

- face recognition
- liveness detection
- anti-spoofing

Ky vong:

- `job_role_family = COMPUTER_VISION_EKYC`
- CV computer vision that duoc boost hop ly
- CV AI chung chung khong duoc overrate

### 17.2 Security/GRC case

JD:

- Qualys
- access control
- ISO 27001
- vulnerability management

Ky vong:

- `job_role_family = SECURITY_GRC`
- candidate governance chung chung khong duoc an diem nhu hands-on role fit

### 17.3 Backend case

JD:

- Java
- Spring Boot
- REST API

Ky vong:

- `job_role_family = BACKEND_ENGINEERING`
- candidate backend that van score on dinh
- regression benchmark cu khong vo

## 18. Manual benchmark de xuat

Sau khi code, nen chay:

1. `JD_2 + CV_1/CV_3`
2. `JD_3 + CV_3_1/CV_3_3`
3. `JD_4 + CV_4_1/CV_4_2/CV_4_3`
4. web employer screening voi role `IT Security`
5. web candidate recommendation voi job `Computer Vision / eKYC`

Can xem:

- role-family suy ra co hop ly khong;
- score co giam overrate khong;
- review card co giai thich de hieu hon khong;
- candidate recommendation co xep hang thuyet phuc hon khong.

## 19. Pham vi thuc hien cua Phase 29

Phase 29 nen tap trung:

- role-family inference cho JD;
- role-family signal inference cho candidate;
- requirement technical intent metadata;
- role-aware calibration cho matching/scoring/explanation;
- benchmark regression.

Phase 29 chua nen:

- train model classification role-family;
- dung LLM/GPT de doan role-family;
- mo rong taxonomy hang loat;
- cho admin auto-merge skill;
- thay doi weighted scoring qua manh.

## 20. Tieu chi hoan thanh

Phase 29 duoc xem la hoan thanh khi:

1. He thong suy ra duoc `job_role_profile` co y nghia cho cac case benchmark chinh.
2. CV lech role-family khong con de bi overrate khi chi co overlap chung chung.
3. Review card / recommendation explanation co role-aware notes doc duoc.
4. Benchmark Phase 26-28 van pass.
5. Full test suite van pass.

## 21. Rui ro va cach kiem soat

### 21.1 Rui ro

- role-family heuristic qua cung;
- overfit theo bo JD hien tai;
- candidate da multi-role that bi ep ve 1 nhom;
- scorer bi phuc tap qua muc.

### 21.2 Cach kiem soat

- giu tap role-family nho;
- uu tien metadata + calibration nhe;
- benchmark regression lien tuc;
- neu mo ho thi fallback `GENERIC_TECH`.

## 22. Gia tri cho bao cao va phan bien

Phase 29 rat co gia tri khi di bao cao vi co the giai thich:

```text
He thong khong chi match keyword va embedding.
No con co mot lop role-family inference co kiem soat
de phan biet dung boi canh nghe ky thuat cua requirement.
```

Day la diem rat de thuyet phuc giang vien khi hoi:

- vi sao cung la Python nhung role khac nhau;
- vi sao cung la security nhung khac GRC va hands-on;
- vi sao candidate co AI chung chung khong duoc xep cao cho CV/eKYC role.

## 23. Huong sau Phase 29

Sau khi role-family va technical intent da co,
buoc tiep theo hop ly la:

```text
Phase 30 - Role-aware Scoring Calibration and Explanation Hardening
```

Phase 30 se tap trung:

- dua role-family vao scorer ro hon;
- giam overrate/underrate co he thong;
- lam review card va candidate recommendation explanation sac hon nua.
