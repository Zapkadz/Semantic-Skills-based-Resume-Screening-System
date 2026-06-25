# Phase 28 - Open-set Technical Requirement Filtering

## 1. Muc tieu phase

Sau Phase 27, he thong da:

- tach section JD ro hon;
- gan typed requirement schema;
- loai education / language / soft skill ra khoi hard-skill path tot hon.

Nhung van con 1 lop benh logic rat quan trong:

```text
open-set requirement pool chua du sach
```

Noi ngan gon:

```text
Phase 27 = biet requirement thuoc loai nao
Phase 28 = chi giu unknown requirement technical that su
```

Muc tieu cua Phase 28 la:

```text
Dat mot bo loc technicality vao giua typed requirements va open-set matching,
de semantic matching, scoring, va taxonomy suggestion chi lam viec voi unknown
technical units co y nghia.
```

## 2. Van de can giai quyet

### 2.1 Open-set van con gom nhieu requirement khong du technical

Mac du Phase 27 da loc tot hon, he thong van co the giu lai cac cum nhu:

- broad clause
- generic noun phrase
- domain sentence dai
- action phrase mo ho
- requirement line tron nhieu y

Nhung cum nay khi vao open-set se gay:

- matching nhiu;
- semantic evidence sai nghia;
- giam do tin cay cua score;
- recruiter thay AI giai thich khong sac.

### 2.2 Unknown technical units dang bi tron voi context line

Vi du:

```text
Experience working in banking domain
```

khac voi:

```text
Experience with Qualys, Commvault, PAM, SIEM
```

Neu khong loc dung, he thong de:

- giu ca dong domain/context lam open-set technical;
- hoac cat mot requirement ky thuat thanh nhieu manh vo nghia.

### 2.3 Taxonomy suggestion queue co nguy co bi ban du lieu

Admin suggestion queue cua Phase 15 chi nen nhan:

- unknown technical skill
- unknown tool/platform
- unknown certification/capability co kha nang them vao taxonomy

No khong nen nhan:

- soft phrase
- generic domain clause
- long sentence
- context note

Neu dau vao queue ban, admin se:

- mat thoi gian duyet rac;
- them nham taxonomy;
- lam xau merged taxonomy.

### 2.4 Candidate-side recommendation cung bi anh huong

Tinh nang CV -> Top JD phu hop da dung chung core scorer.

Neu open-set requirement pool nhiu, candidate-side se de gap:

- gap summary bi sai;
- optional growth phinh to vo nghia;
- explanation cho ung vien bi kem chat luong.

### 2.5 He thong can uu tien precision hon recall trong open-set dau vao

Voi taxonomy skill da biet, he thong da co rule-based + evidence.

Voi unknown requirement, neu giu nham 1 cum khong technical, hau qua lon hon bo sot
mot cum bien:

- giu nham -> semantic match sai, score sai, suggestion queue ban;
- bo sot -> van con co the xu ly o phase sau bang role-family hoac taxonomy expansion.

Vi vay, Phase 28 can chon:

```text
precision cao hon mot chut so voi recall
```

cho open-set technical input.

## 3. Vi sao Phase 28 la buoc tiep theo dung nhat

Phase 27 da sua:

```text
requirement type
```

Nhung chua sua triet de:

```text
quality cua unknown technical units
```

Neu chuyen ngay sang:

- role-family inference
- scorer calibration moi
- taxonomy auto-suggestion thong minh hon

thi cac phase do van phai xu ly tren input unknown requirement chua du sach.

Noi cach khac:

```text
typed requirement dung truoc
open-set technical filter dung ke tiep
semantic matching / scorer / admin queue moi dung sau
```

## 4. Nguyen tac thiet ke

### 4.1 Khong phai unknown nao cung xung dang vao semantic matching

Phase nay khong hoi:

```text
line nay unknown hay khong
```

ma hoi:

```text
unknown nay co du technical de dua vao open-set matching hay khong
```

### 4.2 Explainable filtering

Moi unit duoc giu hoac loai nen co ly do:

- kept because explicit tool/platform signal
- kept because acronym/certification signal
- dropped because generic clause
- dropped because domain/context only
- dropped because low technical confidence

De sau nay debug va benchmark de hon.

### 4.3 Giu backward-compatible output

Phase 28 nen giu:

- `open_set_requirements` la `list[str]`

nhung co the bo sung metadata moi:

- `open_set_candidates`
- `open_set_filter_summary`
- `discarded_open_set_candidates`

de UI / diagnostics co the dung dan.

### 4.4 Chua dua role-family inference vao phase nay

Phase 28 chi tap trung:

- loc unknown technical units
- khong suy luan sau theo nghe nghiep

Role-family inference la phase sau.

### 4.5 Dung chung cho screening va recommendation

Bo loc moi phai duoc reuse cho:

- employer screening
- candidate-side recommendation
- taxonomy suggestion observation

khong duoc de moi flow mot logic loc rieng.

## 5. Kien truc de xuat

### 5.1 Luong xu ly moi

```text
Typed requirements (must_have / nice_to_have)
  -> requirement unit extraction
  -> open-set technical filter
  -> canonicalize + dedupe
  -> open_set_requirements
  -> semantic matcher / taxonomy suggestion / diagnostics
```

### 5.2 Hai lop output

#### Lop 1 - semantic/scoring input

```json
{
  "open_set_requirements": [
    "Qualys",
    "Commvault",
    "Nutanix administration"
  ]
}
```

#### Lop 2 - diagnostics/debug

```json
{
  "open_set_candidates": [
    {
      "text": "Qualys",
      "status": "kept",
      "technical_confidence": 0.95,
      "reason": "explicit_tool_signal"
    },
    {
      "text": "working in banking domain",
      "status": "discarded",
      "technical_confidence": 0.10,
      "reason": "domain_context_only"
    }
  ]
}
```

### 5.3 Muc tieu cua bo loc

Bo loc can tra loi 3 cau hoi:

1. Unit nay co phai technical khong?
2. Unit nay co du ngan gon / cu the de semantic matching khong?
3. Unit nay co nen dua vao taxonomy suggestion queue sau nay khong?

## 6. Module du kien can tao / cap nhat

Them:

```text
src/open_set_requirement_filter.py
tests/test_open_set_requirement_filter.py
```

Cap nhat:

```text
src/requirement_extractor.py
src/screening_pipeline.py
src/payload_pipeline.py
src/job_catalog_loader.py
src/job_recommendation_pipeline.py
src/taxonomy_suggestion.py
tests/test_requirement_extractor.py
tests/test_screening_pipeline.py
tests/test_payload_pipeline.py
tests/test_job_catalog_loader.py
tests/test_core_logic_benchmark.py
tests/test_api.py
```

Neu can:

```text
docs/evaluation/failure_taxonomy.md
```

de danh dau symptom nao da duoc xu ly.

## 7. Trach nhiem cua tung phan

### 7.1 `src/open_set_requirement_filter.py`

Module moi nay nen:

- nhan danh sach requirement units unknown;
- tinh technical confidence;
- quyet dinh `kept` / `discarded`;
- ghi `reason`;
- gom va dedupe cac unit trung/gan trung;
- tra ve metadata ro rang.

### 7.2 `src/requirement_extractor.py`

Cap nhat de:

- goi bo loc technical moi;
- khong tra thang unknown units nua;
- co the tra:
  - final `open_set_requirements`
  - diagnostics candidates
  - filter summary

### 7.3 `src/screening_pipeline.py`

Cap nhat de:

- dung `open_set_requirements` da qua filter;
- dua metadata filter vao output `job`.

### 7.4 `src/payload_pipeline.py`

Cap nhat de API screening cung tra metadata giong CLI pipeline.

### 7.5 `src/job_catalog_loader.py`

Candidate-side recommendation phai dung chung bo loc.

Neu khong, employer flow va candidate flow se cho ra hanh vi lech nhau.

### 7.6 `src/taxonomy_suggestion.py`

Cap nhat de:

- chi thu thap observation tu unknown units da qua technical filter;
- uu tien unit `kept`;
- bo qua unit `discarded`.

## 8. Heuristic / rule filtering de xuat

### 8.1 Strong keep signals

Neu gap cac tin hieu sau, unit nen duoc giu voi confidence cao:

- explicit product/vendor/tool names
- framework/platform/database/cloud names
- certification acronyms
- uppercase acronyms hop ly
- parenthetical examples co technical anchor
- noun phrase ngan gon co technical headword

Vi du:

- `Qualys`
- `Commvault`
- `Nutanix administration`
- `PAM`
- `SIEM`
- `Security+`

### 8.2 Medium keep signals

Unit co the duoc giu neu:

- la capability phrase ky thuat ngan;
- co dong tu ky thuat + object ky thuat;
- co tu khoa strong technical nouns.

Vi du:

- `vulnerability management`
- `access control`
- `patch upgrades for Windows`

### 8.3 Strong discard signals

Unit nen loai neu:

- la soft phrase;
- la pure domain phrase;
- la education/language fragment;
- la generic sentence qua dai;
- la action phrase chung chung khong co technical anchor;
- la metadata job cua web.

Vi du:

- `good communication`
- `work under pressure`
- `banking domain`
- `team coordination`
- `full time`
- `team lead level`

### 8.4 Boundary / split rules

Can co quy tac tach khon hon cho cac line:

```text
Proficiency in Linux, Nutanix administration, Commvault, and Qualys
```

De he thong lay duoc:

- `Linux`
- `Nutanix administration`
- `Commvault`
- `Qualys`

nhung khong lay:

- `Proficiency`
- `administration` dung mot minh

### 8.5 Canonicalization rules

Can gom / chuan hoa nhe:

- `Qualys platform` -> `Qualys`
- `ISO 27001 certification` -> `ISO 27001`
- `PAM procedures` -> `PAM`

nhung khong duoc over-normalize den muc mat nghia technical.

## 9. Output schema de xuat

### 9.1 Job output

Bo sung:

```json
{
  "open_set_requirements": ["Qualys", "Commvault"],
  "open_set_filter_summary": {
    "candidate_count": 7,
    "kept_count": 2,
    "discarded_count": 5
  },
  "open_set_candidates": [
    {
      "text": "Qualys",
      "status": "kept",
      "reason": "explicit_tool_signal",
      "technical_confidence": 0.95
    }
  ]
}
```

### 9.2 Taxonomy suggestion input

Chi observation co:

- `status = kept`
- confidence du nguong

moi di tiep vao suggestion queue.

## 10. Test plan

Them:

```text
tests/test_open_set_requirement_filter.py
```

Cap nhat:

```text
tests/test_requirement_extractor.py
tests/test_screening_pipeline.py
tests/test_payload_pipeline.py
tests/test_job_catalog_loader.py
tests/test_core_logic_benchmark.py
tests/test_api.py
```

### 10.1 Cac case bat buoc phai pass

1. Soft/general phrases khong vao `open_set_requirements`.
2. Education/language/domain context khong vao `open_set_requirements`.
3. Unknown technical tool names van duoc giu.
4. Security role nhu `Qualys`, `Commvault`, `Nutanix administration`, `PAM` duoc giu.
5. Candidate-side recommendation dung chung filter voi employer screening.
6. Taxonomy suggestion khong nhan unit `discarded`.

### 10.2 Benchmark quan trong

Can chay lai:

- `screening_backend_strong`
- `screening_backend_evidence_without_skills_section`
- `screening_backend_hard_skill_deficit`
- `screening_cross_lingual_cv`
- `recommendation_placeholder_jobs_excluded`

Va them benchmark cho:

- JD security dai, nhieu unknown technical tools
- JD placeholder / low-signal
- JD moi ngoai taxonomy nhung technical that

### 10.3 Case thuc te can cover

- `JD_3.txt`: khong duoc tao open-set requirement rac.
- `JD_4.txt`: van phai giu unknown technical units co y nghia, khong duoc bo mat het.

## 11. Acceptance criteria

Phase 28 duoc xem la hoan thanh khi:

1. `open_set_requirements` sach hon ro rang so voi truoc;
2. soft/general/domain context khong con lot vao open-set technical flow;
3. unknown technical units quan trong van duoc giu;
4. taxonomy suggestion queue giam rac;
5. CLI va API cung tra metadata filter on dinh;
6. employer screening va candidate recommendation dung chung filter;
7. full `pytest` pass.

## 12. Dau ra mong muon sau phase nay

Sau Phase 28, khi he thong gap 1 requirement unknown, no khong chi biet:

```text
cai nay ngoai taxonomy
```

ma biet ro hon:

```text
cai nay la unknown technical unit nen giu
hoac
cai nay la generic/context phrase nen loai
```

Day la buoc chuyen rat quan trong de:

- semantic matching dung nghia hon;
- score bieu dien dung hon;
- admin queue sach hon;
- explanation cho recruiter va ung vien sac hon.

## 13. Ngoai scope

Phase 28 chua lam:

- role-family technical inference;
- scorer weight redesign;
- multilingual reranking moi;
- auto taxonomy insertion;
- UI visualization moi tren web.

## 14. Huong sau Phase 28

Sau khi open-set technical pool da du sach, buoc tiep theo hop ly la:

```text
Phase 29 - Role-family Technical Intent Inference
```

Muc tieu:

- hieu ro hon y nghia technical cua requirement theo tung nhom role;
- phan biet context phrase voi capability phrase tot hon;
- bo sung domain-aware interpretation cho open-set va scorer.
