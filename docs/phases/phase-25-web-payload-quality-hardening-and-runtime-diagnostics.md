# Phase 25 - Web Payload Quality Hardening and Runtime Diagnostics

## 1. Muc tieu phase

Sau Phase 24, candidate-side recommendation da co them JD quality gate de loai
bot cac job test / placeholder / thieu du lieu khoi `top_jobs`.

Tuy nhien, khi dua AI vao web that, da xuat hien mot nhom van de khac:

```text
Khong phai luc nao ket qua "sai" cung do scorer.
Rat nhieu luc van de nam o payload web gui sang AI:
- JD con HTML / text chua sach
- CV text bi cat, thieu section, hoac qua ngan
- field requirements / responsibilities khong duoc map dung
- web va AI kho debug vi khong thay ro cleaned text va parsed result
```

Muc tieu cua Phase 25 la:

```text
Lam cung luong web -> AI -> result
de moi lan ket qua bat thuong, he thong co the chi ro:
1. payload dau vao co van de gi
2. parser da nhin thay gi
3. job/candidate bi canh bao vi ly do nao
4. AI da ra ket qua dua tren du lieu nao
```

Noi ngan gon:

```text
Phase 24 = job nao du du lieu de duoc xep hang
Phase 25 = payload web co du chat luong va du debug de tin ket qua hay khong
```

## 2. Van de can giai quyet

### 2.1 Payload web va du lieu AI thuc te chua du trong suot

Trong qua trinh tich hop, da tung gap:

- JD lay tu DB con the HTML
- CV text bi rut gon qua muc
- `requirements` chi con 1 dong nhu `1 nam`
- `description` chua noi dung test
- web render ket qua nhung khong biet AI da nhan gi that su

Neu chi nhin UI thi de nham rang:

```text
AI cham sai
```

trong khi goc re co the la:

```text
web gui payload chua sach
```

### 2.2 Debug runtime hien tai van can mo file log thu cong

Hien tai da co log va file debug, nhung van de la:

- chua co schema diagnostics ro rang trong response
- chua co tong hop warning o muc payload
- chua co "health" cua tung request
- chua co de xuat ro:
  - CV qua ngan
  - JD thieu requirement source
  - title placeholder
  - text sau clean bi mat qua nhieu noi dung

### 2.3 Khi web co du lieu that, can phan biet 3 lop loi

Phase nay can tach ro 3 lop:

1. **Input issue**
   - payload gui sang AI thieu / ban / khong day du

2. **Parsing issue**
   - parser nhin thay qua it signal

3. **Matching issue**
   - du lieu tot nhung CV that su khong hop

Neu khong tach 3 lop nay, luc debug se rat ton thoi gian.

## 3. Vi sao Phase 25 nen lam truoc preference-aware ranking

Preference-aware ranking can them du lieu:

- location preference
- salary preference
- remote / hybrid / onsite preference
- desired seniority

Nhung neu payload goc chua on dinh thi preference layer se chi:

- lam output phuc tap hon
- kho debug hon
- kho bao ve hon truoc giang vien

Vi vay thu tu hop ly la:

```text
payload quality + diagnostics truoc
preference-aware ranking sau
```

Day cung phu hop voi tinh huong du lieu that hien tai cua web.

## 4. Nguyen tac thiet ke

### 4.1 Diagnostics khong duoc doi nghiep vu chinh

Phase 25 khong viet lai scorer.
Khong doi cong thuc fit score.
Khong doi hard-skill gate.

Phase nay chu yeu bo sung:

- validation
- diagnostics
- traceability
- canh bao chat luong payload

### 4.2 Local-first, de debug, de giai thich

Moi canh bao nen:

- co code on dinh
- co message de doc
- co metric cu the

Vi du:

```text
cv_text_too_short
jd_missing_requirements
job_description_placeholder
html_cleaning_changed_text_heavily
```

### 4.3 API tra ve du lieu de web va admin cung doc duoc

Diagnostics khong chi de xem trong terminal.
Can co cau truc de:

- web co the hien canh bao than thien
- admin co the debug payload
- developer co the doi chieu request / response nhanh

### 4.4 Khong lam noisy response qua muc

Phase 25 can can bang:

- du thong tin de debug
- nhung khong lam response qua nang

Can tach:

1. **response chinh cho san pham**
2. **runtime diagnostics co cau truc**
3. **debug file tren dia**

## 5. Kien truc de xuat

### 5.1 Luong employer-side sau Phase 25

```text
Web employer payload
  -> payload validator / cleaner audit
  -> screening payload diagnostics
  -> parser
  -> matching + scoring + review card
  -> response + diagnostics summary
  -> runtime trace file
```

### 5.2 Luong candidate-side sau Phase 25

```text
Web candidate payload
  -> payload validator / cleaner audit
  -> candidate + job catalog diagnostics
  -> Phase 24 JD quality gate
  -> retrieval
  -> reranking
  -> skill-gap explanation
  -> response + diagnostics summary
  -> runtime trace file
```

### 5.3 Hai lop diagnostics

Phase 25 nen co 2 lop:

1. **Payload diagnostics**
   - nhin vao input web gui sang

2. **Runtime diagnostics**
   - nhin vao viec AI xu ly payload do nhu the nao

## 6. Module moi de xuat

Them:

```text
src/payload_diagnostics.py
src/runtime_diagnostics.py
tests/test_payload_diagnostics.py
tests/test_runtime_diagnostics.py
```

Cap nhat:

```text
src/payload_pipeline.py
src/job_recommendation_pipeline.py
src/job_catalog_loader.py
src/job_quality_gate.py
api.py
tests/test_api.py
README.md
docs/dev-learning-log.md
docs/integration/...
```

Neu can, co the bo sung helper nho:

```text
src/debug_trace_writer.py
```

nhung khong bat buoc neu co the tai su dung cach log hien tai.

## 7. Trach nhiem cua module moi

### 7.1 `src/payload_diagnostics.py`

Module nay nen:

1. danh gia payload employer-side va candidate-side
2. do muc do day du cua:
   - title
   - description
   - requirements
   - responsibilities
   - cv_text
   - headline
3. phat hien placeholder / text qua ngan
4. phat hien cleaned text giam signal qua manh
5. tra ve:
   - flags
   - warnings
   - metrics
   - normalized summary

### 7.2 `src/runtime_diagnostics.py`

Module nay nen:

1. nhan output sau parse / match / score
2. tong hop diagnostics de doc nhanh
3. tao:
   - request summary
   - parsing summary
   - quality summary
   - ranking summary
4. ho tro ghi trace co cau truc

## 8. Diagnostics employer-side can co

Cho `POST /screening`, response nen co them mot nhom:

```text
diagnostics
```

gom cac nhanh nhu:

```json
{
  "diagnostics": {
    "payload": {
      "warnings": [],
      "flags": [],
      "metrics": {}
    },
    "job": {
      "title_quality": "...",
      "requirement_signal": "...",
      "responsibility_signal": "..."
    },
    "candidates": {
      "received_count": 12,
      "usable_count": 11,
      "low_text_count": 1
    }
  }
}
```

Khong can tra qua chi tiet tung token.
Chi can du de web / dev biet vi sao ket qua co the giam do tin cay.

## 9. Diagnostics candidate-side can co

Cho `POST /recommend-jobs`, response nen co:

```text
diagnostics
```

gom:

- candidate payload quality
- so luong job co du lieu manh / yeu
- so luong job bi excluded vi Phase 24
- warning neu nhieu job trong request qua ngan
- warning neu CV text qua ngan / thieu section

Vi du:

```json
{
  "diagnostics": {
    "candidate_payload": {
      "flags": ["cv_text_too_short"],
      "metrics": {
        "cv_word_count": 86
      }
    },
    "job_payloads": {
      "received_count": 25,
      "eligible_count": 17,
      "excluded_count": 8
    },
    "runtime": {
      "retrieved_count": 10,
      "reranked_count": 10
    }
  }
}
```

## 10. Cac rule payload quality de xet

Phase 25 nen uu tien cac rule de giai quyet van de that da gap.

### 10.1 CV text qua ngan

Vi du:

```text
cv_text < nguong toi thieu
```

Thi flag:

```text
cv_text_too_short
```

### 10.2 JD title placeholder

Vi du:

```text
Test
Demo
Sample
```

Thi flag:

```text
job_title_placeholder
```

### 10.3 Requirement source khong ro

Neu web gui:

```text
requirements = []
description = "mo ta test"
```

Thi flag:

```text
jd_missing_explicit_requirements
```

### 10.4 HTML cleaning lam thay doi text qua nhieu

Neu payload truoc clean co nhieu HTML,
sau clean chi con rat it noi dung,
can flag:

```text
html_cleaning_changed_text_heavily
```

Khong phai de chan request,
ma de thong bao payload dang co nguy co mat signal.

### 10.5 Candidate headline / title khong co

Khong bat buoc fail,
nhung can warning neu:

- candidate_name rong
- headline rong
- source_file khong co

### 10.6 Job list qua nhieu phan tu yeu

Neu request candidate-side co:

- nhieu job test
- nhieu job quality thap

thi top-level warning nen noi ro:

```text
Many jobs in this request do not contain enough JD signal for reliable recommendation.
```

## 11. Runtime trace can co nhung gi

Moi request tu web nen co trace file de debug.
Khong nhat thiet response phai tra het, nhung trace file nen co:

1. request metadata
2. endpoint
3. timestamp
4. cleaned text summary
5. parsed requirement summary
6. diagnostics flags
7. top result summary

Vi du:

```text
trace_id
endpoint
candidate_id / job_id
input_word_counts
flags
job_quality_stats
top_result_ids
excluded_job_ids
```

## 12. API contract de xuat

### 12.1 Employer-side `/screening`

Bo sung `diagnostics` o top-level.

Khong doi structure `candidates`.

### 12.2 Candidate-side `/recommend-jobs`

Bo sung `diagnostics` o top-level.

Khong doi nghia cua:

- `top_jobs`
- `excluded_jobs`
- `job_quality_stats`
- `warnings`

### 12.3 Nguyen tac backward-compatible

Phase 25 nen:

- them field moi
- khong xoa field cu
- khong doi ten field web dang dung

De web co the nang cap dan dan.

## 13. Web integration guidance can ho tro sau phase nay

Sau khi code xong Phase 25, web co the:

1. hien warning than thien neu payload CV/JD yeu
2. hien badge "du lieu CV qua ngan" hoac "JD chua du du lieu"
3. cho admin / developer mo diagnostics panel
4. link den trace id khi can debug

Phase nay rat hop de viet them prompt cho Cursor o repo PHP, vi diagnostics se
giup web team tu debug duoc ma khong can mo code Python sau moi lan.

## 14. Pham vi thuc hien cua Phase 25

### 14.1 Trong scope

- payload diagnostics cho employer-side
- payload diagnostics cho candidate-side
- runtime diagnostics summary
- traceability / trace id
- warning codes on dinh
- test cases cho payload that
- docs + huong dan tich hop web

### 14.2 Ngoai scope

- chua them user preference ranking
- chua them behavioral personalization
- chua dua GPT vao payload cleaning
- chua lam dashboard admin day du trong AI repo
- chua thay doi cong thuc scorer co ban

## 15. Chi tiet implementation de xuat

### 15.1 `src/payload_pipeline.py`

Bo sung hook de:

- tinh word count truoc / sau clean
- do so section co noi dung
- sinh payload flags

### 15.2 `src/job_recommendation_pipeline.py`

Bo sung:

- top-level diagnostics
- candidate payload summary
- job payload summary
- retrieval / rerank runtime summary

### 15.3 `api.py`

Cap nhat:

- tang phase len Phase 25
- tra `diagnostics`
- co `trace_id` on dinh cho moi request neu hop ly

### 15.4 Log / debug output

Neu dang co folder debug runtime:

```text
C:\topcv_ai_runtime\api-debug
```

thi Phase 25 nen chuan hoa naming hoac noi dung file de:

- doc nhanh request / response
- doi chieu bang `trace_id`
- biet request nay warning gi

## 16. Test cases can co

### 16.1 Employer-side

1. JD sach, CV sach -> diagnostics it hoac khong co warning
2. JD con HTML nhieu -> co warning cleaning
3. JD qua ngan -> diagnostics flag ro
4. danh sach CV co 1 CV qua ngan -> co candidate payload warning

### 16.2 Candidate-side

1. CV day du + job list tot -> diagnostics sach
2. CV qua ngan -> co `cv_text_too_short`
3. request co nhieu job placeholder -> co top-level warning
4. job bi excluded do Phase 24 -> diagnostics va excluded job thong nhat

### 16.3 Runtime trace

1. moi request co trace id
2. trace id xuat hien trong log / response
3. trace file co the map lai request va ket qua

## 17. Acceptance criteria

Phase 25 duoc xem la hoan thanh khi:

1. ca `/screening` va `/recommend-jobs` deu co `diagnostics` top-level;
2. he thong phat hien duoc payload CV/JD qua ngan hoac placeholder;
3. co warning code on dinh, de web co the map UI;
4. response van backward-compatible voi web hien tai;
5. moi request co the duoc debug bang trace id hoac runtime trace summary;
6. test payload that cho ket qua diagnostics hop ly;
7. khong lam gay scorer va cac phase truoc.

## 18. Dau ra mong muon sau phase nay

Sau Phase 25, khi gap mot case "tai sao diem la the nay?", ta co the tra loi theo
mot quy trinh ro rang:

```text
1. xem diagnostics payload
2. xem cleaned text con bao nhieu signal
3. xem requirement / responsibility parser da nhin thay gi
4. xem quality gate / hard-skill gate da tac dong chua
5. xem top result va warning tong hop
```

Day la buoc rat quan trong de san pham AI:

- tin cay hon
- de bao ve hon
- de tich hop web hon
- de debug du lieu that hon

## 19. Huong sau Phase 25

Sau khi payload quality va diagnostics da on dinh, luc do moi nen sang:

```text
Phase 26 - Preference-aware Ranking
```

de them:

- location preference
- salary preference
- work mode preference
- desired seniority

Luc do preference layer se co nen du lieu va debug tot hon, tranh tinh trang
"them logic moi trong khi input van chua on dinh".
