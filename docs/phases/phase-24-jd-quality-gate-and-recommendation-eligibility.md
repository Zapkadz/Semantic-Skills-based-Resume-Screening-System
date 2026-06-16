# Phase 24 - JD Quality Gate and Recommendation Eligibility

## 1. Muc tieu phase

Sau Phase 23, candidate-side recommendation da co:

```text
1 CV
  -> retrieval top-N jobs
  -> reranking bang core scorer
  -> fit_label + fit_score
  -> skill-gap explanation
  -> CV improvement suggestions
```

Tuy nhien, khi dua vao du lieu web that, da xuat hien van de quan trong:

```text
Nhieu tin tuyen dung test / placeholder / gan nhu khong co noi dung
van duoc AI cham 20-35 diem va xep vao danh sach goi y.
```

Muc tieu cua Phase 24 la giai quyet dung van de nay:

```text
Truoc khi xep hang job theo do phu hop,
he thong phai danh gia chat luong JD.
Neu JD khong du du lieu, job do khong du dieu kien de AI recommendation cham diem binh thuong.
```

Noi ngan gon:

```text
Phase 23 = job nao hop voi CV
Phase 24 = job nao DU DU LIEU de duoc AI danh gia hop le
```

## 2. Van de can giai quyet

### 2.1 Job rong van co diem nen

Voi cac job chi co title nhu:

```text
Test
Demo
Tin dang thu nghiem
```

hoac mo ta gan nhu rong:

```text
Mo ta cong viec: test
Yeu cau ung vien: rong
Quyen loi: rong
```

he thong hien tai van co the tra:

- `Low Fit`
- `25-35 diem`

ly do la scorer hien tai co nhieu thanh phan trung tinh khi JD thieu thong tin:

- experience co the thanh `1.0`
- domain co the thanh `1.0`
- seniority co the thanh `0.75`
- nice_to_have co the thanh `0.5`

Ve mat toan hoc thi nhat quan, nhung ve mat san pham thi khong dung y nghia.

### 2.2 "Khong co thieu hut lon" la thong diep sai nghia

Khi JD gan nhu khong co requirement, candidate-side UI co the hien:

```text
Khong co thieu hut lon
```

Dieu nay de gay hieu nham:

- khong phai vi job hop
- ma vi job KHONG CO DU requirement de tim thieu hut

Can tach ro:

```text
Low Fit
```

va

```text
Insufficient JD Data
```

### 2.3 Du lieu web that co nhieu tin test / placeholder

Trong data web that, khong phai job nao cung duoc nhap nghiem tuc.
Neu khong co quality gate, retrieval va reranking se bi nhieu:

- job test
- job title placeholder
- job text qua ngan
- job khong co must-have skills
- job chi co dia diem/luong ma khong co noi dung cong viec

## 3. Vi sao Phase 24 nay phu hop hon preference-aware ranking

Preference-aware ranking can du lieu ma hien tai CV/web chua co day du:

- muc luong mong muon
- noi muon lam viec
- remote/hybrid/onsite preference
- level mong muon

Trong khi do, van de JD rong la van de that dang anh huong truc tiep chat luong ket qua.

Vi vay, Phase 24 nen uu tien:

```text
Data quality gate truoc
Preference layer sau
```

Day la huong hop ly hon voi du lieu that hien tai.

## 4. Nguyen tac thiet ke

### 4.1 Quality before ranking

Job truoc khi vao candidate-side ranking phai di qua mot lop:

```text
JD quality analysis
  -> eligible hoac ineligible
```

Chi cac job `eligible` moi duoc vao recommendation flow binh thuong.

### 4.2 Khong suy dien noi dung JD khi JD thieu du lieu

Neu JD rong, he thong khong duoc co gang "doan" requirement.
Khong duoc nang diem vi gia su job de tinh.

Can trung thuc:

```text
Job nay khong du du lieu de AI danh gia chinh xac.
```

### 4.3 Tach "job khong du du lieu" khoi "job low fit"

Day la nguyen tac quan trong nhat cua phase nay.

Hai trang thai khac nhau:

1. `Low Fit`
   - JD co du du lieu
   - AI da doi sanh duoc
   - ket qua cho thay CV khong hop

2. `Insufficient JD Data`
   - JD khong du du lieu
   - AI khong nen dua ra fit score binh thuong

### 4.4 Giai thich duoc

Output phai noi ro:

- job bi loai vi ly do gi
- quality flags nao duoc bat
- score quality la bao nhieu

khong chi silently bo job di.

## 5. Kien truc de xuat

### 5.1 Luong candidate-side moi

```text
Candidate CV
  -> build candidate query profile
  -> load active jobs
  -> Phase 24 JD quality gate
      -> eligible jobs
      -> ineligible jobs
  -> retrieval tren eligible jobs
  -> reranking bang AI core
  -> Phase 23 explanation layer
  -> final response
```

### 5.2 Anh huong mong muon

Sau Phase 24:

- `top_jobs` chi nen gom cac job du dieu kien recommendation
- cac job test/rong nen ra mot nhom rieng:
  - `excluded_jobs`
  - hoac `ineligible_jobs`

## 6. Module moi de xuat

Them:

```text
src/job_quality_gate.py
tests/test_job_quality_gate.py
```

Cap nhat:

```text
src/job_catalog_loader.py
src/job_recommendation_pipeline.py
src/job_retriever.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
README.md
docs/dev-learning-log.md
```

Neu can cho debug web:

```text
docs/integration/...
```

## 7. Trach nhiem cua module moi

`src/job_quality_gate.py` nen lam:

1. nhan `job_payload`, `job_card`, `job_text`, `requirement_groups`;
2. tinh `job_quality_score`;
3. phat hien `quality_flags`;
4. quyet dinh:
   - `recommendation_eligible = true/false`
5. tra ve reason code + message.

## 8. Tieu chi danh gia chat luong JD

Phase 24 nen danh gia theo nhieu tin hieu ket hop, khong chi 1 rule.

### 8.1 Placeholder title detection

Vi du title nhu:

```text
test
demo
sample
abc
job test
tin test
```

nen bi flag manh.

### 8.2 Description qua ngan

Vi du sau khi clean HTML xong, text mo ta chi con:

```text
test
...
ok
```

hoac tong so token qua it.

### 8.3 Khong co must-have technical requirements

Neu `must_have_technical` rong
va `open_set_requirements` cung rong,
thi job khong co nen tang de AI doi sanh.

### 8.4 Khong co line requirement/co trach nhiem co y nghia

Neu JD chi co:

- title
- company
- dia diem
- luong

ma khong co:

- requirement
- responsibilities
- technical context

thi job nay khong nen duoc recommendation binh thuong.

### 8.5 Low-signal repetitive text

Vi du:

```text
test
test
test
```

hoac title va description lap lai placeholder.

### 8.6 HTML-cleaned empty sections

Sau khi strip HTML:

- `mo ta cong viec` rong
- `yeu cau ung vien` rong
- `quyen loi` rong

thi quality phai giam manh.

## 9. Output contract de xuat

### 9.1 Moi job co them metadata quality

Voi moi job candidate-side, bo sung:

```json
{
  "job_quality": {
    "quality_score": 82,
    "quality_label": "eligible",
    "recommendation_eligible": true,
    "flags": [],
    "reasons": []
  }
}
```

Voi job bi loai:

```json
{
  "job_quality": {
    "quality_score": 18,
    "quality_label": "insufficient_jd_data",
    "recommendation_eligible": false,
    "flags": [
      "placeholder_title",
      "description_too_short",
      "missing_requirements"
    ],
    "reasons": [
      "Job title looks like a placeholder.",
      "JD content is too short after cleaning.",
      "No meaningful must-have requirements were detected."
    ]
  }
}
```

### 9.2 Response candidate-side tong the

`/recommend-jobs` nen co them:

```json
{
  "top_jobs": [],
  "excluded_jobs": [],
  "job_quality_stats": {
    "jobs_received": 40,
    "eligible_jobs": 27,
    "excluded_jobs": 13
  }
}
```

### 9.3 Cach xu ly `top_jobs`

Khuyen nghi:

- `top_jobs` chi chua job eligible
- `excluded_jobs` chua job bi loai do quality

Nhu vay web se de render dung nghia hon.

## 10. Candidate-side UI logic de xuat

Phase 24 chua code web trong AI repo, nhung output phai ho tro UI sau nay:

### 10.1 Cho job eligible

Render binh thuong:

- fit label
- fit score
- why fit
- skill gaps
- next best actions

### 10.2 Cho job ineligible

Khong render nhu mot matching result binh thuong.
Thay vao do render:

```text
Khong du du lieu JD de AI danh gia
```

co the cho recruiter/nguoi dung xem chi tiet:

- title placeholder
- mo ta qua ngan
- khong co yeu cau ky thuat

## 11. Rule xu ly de xuat

### 11.1 Hard exclusion

Loai khoi recommendation neu gap nhieu co:

- placeholder title
- cleaned JD text qua ngan
- tong requirement technical = 0
- responsibilities = 0
- open_set_requirements = 0

### 11.2 Soft downgrade

Van cho recommendation nhung kem warning neu:

- only 1 requirement ngan
- title hop le nhung JD rat so sai
- quality score thap nhung chua toi muc exclusion

### 11.3 Fallback khi tat ca job deu xau

Neu toan bo active jobs deu ineligible:

response khong nen co `top_jobs` ao.
Can tra:

```text
Khong co tin tuyen dung du du lieu de AI goi y luc nay.
```

## 12. Pham vi thuc hien cua Phase 24

### 12.1 Trong scope

- phat hien JD placeholder/rong
- quality score cho JD
- recommendation eligibility gate
- loai hoac tach rieng ineligible jobs
- response metadata de web hien dung nghia
- tests va docs

### 12.2 Ngoai scope

- chua lam candidate preference-aware ranking
- chua lam salary/location preference
- chua can feedback loop
- chua auto-rewrite JD

## 13. Test plan

Them/cap nhat:

```text
tests/test_job_quality_gate.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
tests/test_job_catalog_loader.py
```

### 13.1 Cases can co

1. Job title `Test` + description `test` -> ineligible.
2. Job co title that nhung khong co requirement nao -> ineligible.
3. Job co HTML content nhung clean xong van co requirement that -> eligible.
4. Job co 1 requirement ngan va 1 mo ta rat ngan -> low quality warning.
5. Candidate-side response khong dua job test vao `top_jobs`.
6. Candidate-side response co `excluded_jobs`.
7. `job_quality_stats` dem dung eligible/excluded counts.
8. Neu tat ca jobs ineligible -> `top_jobs` rong va co warning ro.
9. Employer-side `/screening` khong bi anh huong.

### 13.2 Manual benchmark de xuat

Test voi web data that co cac job:

- `Test`
- `Test migrate`
- `Test xoa tin`

va 1 job that co mo ta day du.

Ky vong:

- cac job test khong vao `top_jobs`
- hoac hien `Insufficient JD Data`
- job that van duoc cham fit binh thuong

## 14. Acceptance criteria

Phase 24 hoan thanh khi:

- candidate-side recommendation khong con dua job placeholder/rong vao ket qua binh thuong;
- top_jobs khong bi nhieu boi tin test;
- system tach ro `Low Fit` va `Insufficient JD Data`;
- web co du metadata de hien thong diep dung nghia;
- full `pytest` pass.

## 15. Rui ro va giam thieu

### 15.1 Loai nham job ngan nhung that

Risk:

```text
Mot so JD viet ngan nhung van la tin that.
```

Giam thieu:

- dung nhieu tin hieu ket hop, khong dua vao 1 rule duy nhat;
- phan biet hard exclusion va soft warning;
- co `quality_flags` de debug.

### 15.2 Overfit vao tu "test"

Risk:

```text
Job co title co tu test theo nghia that, vi du Software Testing Engineer.
```

Giam thieu:

- chi flag placeholder title khi title qua ngan hoac trung exact cac mau:
  `test`, `demo`, `sample`, ...
- khong flag may moc theo substring.

### 15.3 Web van gui JD HTML ban

Risk:

```text
Quality gate danh gia sai vi input web chua clean.
```

Giam thieu:

- tiep tuc nhac web clean plain text truoc khi gui AI;
- su dung cleaned text cho quality analysis trong Python;
- log request/response de debug.

## 16. Ghi chu cho bao cao

Co the trinh bay:

```text
Tren du lieu web thuc te, khong phai tin tuyen dung nao cung duoc nhap day du va
chuan hoa. Vi vay, truoc khi xep hang cong viec theo muc do phu hop giua CV va JD,
he thong bo sung mot lop danh gia chat luong JD. Lop nay phat hien cac tin tuyen dung
placeholder, qua ngan, hoac khong co du yeu cau ky thuat de AI doi sanh. Cac job
khong du du lieu se khong duoc dua vao recommendation binh thuong, ma duoc danh dau
la khong du du lieu de danh gia. Cach thiet ke nay giup ket qua goi y cong viec
thuc te hon va tranh gay hieu nham giua "job khong hop" va "job khong du du lieu".
```

Mot cau ngan khi bao ve:

```text
Truoc khi goi y job cho ung vien, he thong kiem tra xem JD co du chat luong de AI
danh gia hay khong; neu khong, he thong khong cham fit score binh thuong cho tin do.
```
