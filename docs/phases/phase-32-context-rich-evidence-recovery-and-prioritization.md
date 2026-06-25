# Phase 32 - Context-rich Evidence Recovery and Prioritization

## 1. Muc tieu phase

Sau Phase 31, he thong da sua duoc rat nhieu lop logic:

- typed requirement schema;
- open-set technical filtering;
- role-family technical intent;
- role-aware scoring calibration;
- role-aware taxonomy governance.

Nhung trong failure taxonomy van con 1 benh chua duoc sua tan goc:

```text
EVIDENCE_MISSED
```

Noi ngan gon:

```text
Phase 27-31 = requirement-side logic ngay cang dung hon
Phase 32 = CV-side evidence retrieval phai giau ngu canh hon
```

Muc tieu cua Phase 32 la:

```text
Khong de he thong bo sot bang chung that chi vi skill khong nam tren cung mot dong,
ma nam rai ra trong title / project name / technologies / action bullet.
```

## 2. Van de can giai quyet

### 2.1 Evidence detector hien tai qua "flat"

Hien tai `src/evidence_detector.py` chu yeu nhin tung candidate text rieng le:

- work description bullet
- project description bullet
- project technology item
- summary
- headline
- raw skill
- certification

Dieu nay on cho case de,
nhung de bo sot evidence that trong nhieu CV thuc te.

### 2.2 Skill nam o mot phan, action nam o phan khac

Vi du trong CV:

```text
Project: eKYC Face Platform
Description: Built fraud detection and onboarding workflows.
Technologies: PyTorch, ONNX
```

Neu JD can `PyTorch`,
he thong hien tai thay:

- description co action verb nhung khong co tu `PyTorch`
- technology co `PyTorch` nhung khong co action verb

ket qua de bi ha evidence xuong muc thap hon muc hop ly.

### 2.3 Role/title cung la bang chung ngu canh nhung chua duoc tan dung du

Vi du:

```text
Title: Computer Vision Engineer
Description: Built eKYC onboarding and liveness workflows.
```

Neu can skill `Computer Vision`,
title la mot bang chung role-context rat manh.
Nhung neu detector chi nhin tung description bullet don le,
he thong co the bo sot.

### 2.4 Can recover evidence nhung khong duoc lam review card xau di

Neu ta chi noi candidate texts lai mot cach tho,
review card co the ra:

```text
Computer Vision Engineer. Built eKYC onboarding... Technologies: ONNX, PyTorch...
```

qua dai, qua on ao, va mat tinh giai thich.

Vi vay Phase 32 phai giai duoc 2 viec cung luc:

1. recover evidence that bi bo sot;
2. van uu tien evidence text ngan, dep, truc tiep neu no da ton tai.

## 3. Vi sao Phase 32 la buoc tiep theo dung nhat

Sau Phase 31,
phia requirement/JD da sach hon rat nhieu.
Neu diem van chua thuyet phuc o cac case kho,
thi van de tiep theo thuong nam o phia:

```text
CV evidence retrieval
```

Noi cach khac:

```text
requirement da du dung
thi tiep theo phai sua cach tim bang chung trong CV
```

Day cung la buoc hop ly nhat theo failure taxonomy:

- `REQUIREMENT_TYPE_ERROR` -> da sua manh
- `OPEN_SET_NOISE` -> da sua manh
- `SCORING_OVERRATE` -> da chan va calibration
- `EVIDENCE_MISSED` -> la lo hong trung tam tiep theo

## 4. Muc tieu cu the cua Phase 32

Phase 32 can dat duoc:

1. Tong hop duoc evidence candidate giau ngu canh hon tu CV.
2. Recover duoc case skill nam o `technologies` con action nam o `description`.
3. Recover duoc case skill nam o `title/project name` con bang chung hanh dong nam o bullet.
4. Van uu tien evidence text truc tiep, ngan, dep neu no da ton tai.
5. Reuse logic moi cho ca:
   - rule-based evidence detection
   - open-set semantic evidence matching

## 5. Nguyen tac thiet ke

### 5.1 Khong dua LLM vao evidence retrieval

Phase 32 van giu dung tinh than:

```text
rule-based, explainable, local-first
```

### 5.2 Context synthesis phai bao thu

Chi synthesize nhung context co nghia nhu:

- work title + description
- project name + description
- project description + technologies
- project name + technologies

Khong ghep bai bai ca doan CV thanh mot blob lon.

### 5.3 Uu tien direct evidence hon synthesized evidence

Neu mot bullet da tu no co skill + action ro rang,
he thong nen giu bullet do lam evidence_text.

Synthesized context chi de:

- recover evidence missed;
- khong duoc cuop uu tien cua direct evidence dep hon.

### 5.4 Backward-compatible voi scorer va review card

Phase 32 khong nen thay API contract lon.
Van giu:

- `evidence_level`
- `evidence_text`
- `evidence_source`

Chi cai thien cach tim ra 3 field do.

### 5.5 Phai benchmark duoc

Can co test khoa lai it nhat 3 nhom:

1. direct evidence van duoc uu tien;
2. title/project-context evidence duoc recover;
3. technology + action split evidence duoc recover.

## 6. Kien truc de xuat

### 6.1 Luong evidence moi

```text
Parsed resume
  -> direct evidence candidates
  -> context-synthesized candidates
  -> evidence ranking / prioritization
  -> best evidence
```

### 6.2 Hai lop evidence candidates

#### A. Direct candidates

Giu nhu hien tai:

- work bullet
- project bullet
- technology item
- summary
- headline
- skill item
- certification

#### B. Context-synthesized candidates

Bo sung co kiem soat:

- `work_title + description`
- `work_title + company + description`
- `project_name + description`
- `project_description + technologies`
- `project_name + technologies`

### 6.3 Priority ranking

Khi 2 evidence candidates cung dat cung `evidence_level`,
uu tien:

1. direct candidate
2. candidate ngan hon / sach hon
3. synthesized candidate

Muc tieu la:

```text
recover dung evidence
nhung review card van dep va de doc
```

## 7. File du kien sua

### Sua chinh

```text
src/evidence_detector.py
src/open_set_matcher.py
```

### Test

```text
tests/test_evidence_detector.py
tests/test_open_set_matcher.py
tests/test_core_logic_benchmark.py
```

Neu can,
co the them 1 benchmark payload nho cho case:

- skill o technologies
- action o description

## 8. Expected behavior sau phase

Sau Phase 32, he thong nen:

- cham dung hon cho CV co evidence that trong project/work context,
  du skill khong nam tren cung mot dong;
- giam false weak-evidence trong cac case project technologies;
- review card van uu tien highlight bullet dep hon context ghép dai;
- open-set evidence matching co bo candidate tot hon ma khong can mo rong taxonomy.

## 9. Tieu chi hoan thanh

Phase 32 duoc xem la xong khi:

1. Co plan file phase nay.
2. Evidence detector support context-rich candidates co uu tien.
3. Co test cho:
   - direct evidence preferred
   - work-title context recovery
   - project technologies + action recovery
4. Regression test pass.
5. Khong yeu cau web sua ngay.
