# Phase 23 - Skill-gap Explanation and CV Improvement Suggestions

## 1. Muc tieu phase

Sau Phase 22, he thong da co candidate-side flow kha day du:

```text
1 CV
  -> retrieval top-N jobs
  -> reranking bang core scorer
  -> fit_score + fit_label + fit_summary
```

Tuy nhien, candidate-side recommendation moi chi dung o muc:

- job nao hop hon;
- muc do fit la gi;
- mot vai ly do tong quat.

Muc tieu cua Phase 23 la nang cap candidate-side output thanh:

```text
Top jobs
  + giai thich ro skill-gap
  + noi ro missing skill / weak evidence / optional strengths
  + de xuat nen bo sung gi vao CV
```

Noi ngan gon:

```text
Phase 22 = xep hang dung
Phase 23 = giai thich de ung vien hanh dong duoc
```

## 2. Van de can giai quyet

Neu he thong chi tra:

- `Strong Fit`
- `Good Fit`
- `Stretch`

thi ung vien van se hoi:

```text
Cu the thieu gi?
Toi nen sua CV o dau?
Toi can bo sung skill that hay chi can viet ro hon?
```

Day la khoang trong rat lon cua candidate-side recommendation.

Can phan biet ro 3 tinh huong:

### 2.1 Thieu hard skill that

Vi du JD can:

- `ONNX`
- `AWS`
- `React`

nhung CV khong co skill nay.

Can noi ro:

```text
Missing skill
```

### 2.2 Khong thieu skill, nhung thieu evidence ro rang

Vi du ung vien co:

- Python
- Computer Vision

nhung CV chi liet ke keyword, khong co project/work evidence.

Can noi ro:

```text
Weak evidence
```

chu khong chi noi chung chung la "chua hop".

### 2.3 Chi thieu cach trinh bay CV, khong nhat thiet thieu nang luc

Vi du ung vien da tung lam:

- deployment
- optimization
- cloud integration

nhung CV viet qua ngan, khong mention:

- ket qua
- cong nghe
- metric
- trach nhiem

Can goi y theo huong:

```text
Rewrite / surface stronger evidence
```

khong duoc danh dong voi viec "ban khong biet skill nay".

## 3. Nguyen tac thiet ke

### 3.1 Explainable-first, khong GPT-first

Phase 23 van phai local-first:

- dua tren matched skills
- missing skills
- evidence level
- requirement groups
- hard-skill gate

Khong phu thuoc GPT de sinh explanation.

GPT neu co thi chi la tang nang cao sau nay.

### 3.2 Phan biet ro "missing skill" va "missing evidence"

Day la nguyen tac cuc ky quan trong de bao ve do an.

He thong phai tach:

- `missing_must_have_skills`
- `weak_evidence_skills`
- `optional_missing_skills`
- `cv_presentation_suggestions`

Neu khong tach, giang vien co the hoi:

```text
Tai sao ung vien co skill roi ma he thong van bao thieu?
```

### 3.3 Candidate-facing wording

Employer-side review card noi theo kieu:

- concerns
- recommendation
- interview questions

Candidate-side phai noi theo kieu:

- what you already match
- what is missing
- what you should make more explicit
- what to improve in your CV

### 3.4 Khong "hua" qua muc

He thong khong nen noi:

```text
Chi can them dong nay la dau job.
```

Can noi theo huong trung thuc hon:

```text
This would improve your fit signal.
This would make your evidence more explicit.
This is a likely gap for this role.
```

## 4. Kien truc de xuat

### 4.1 Luong xu ly tong the

```text
Candidate CV
  -> retrieval
  -> reranking
  -> Phase 23 explanation layer
      -> classify gaps
      -> classify weak evidence
      -> classify optional strengths
      -> build CV improvement suggestions
  -> final candidate-facing explanation payload
```

### 4.2 Module moi de xuat

Them:

```text
src/skill_gap_explainer.py
tests/test_skill_gap_explainer.py
```

Co the cap nhat:

```text
src/candidate_job_reranker.py
src/job_recommendation_pipeline.py
tests/test_candidate_job_reranker.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
README.md
docs/dev-learning-log.md
```

### 4.3 Trach nhiem module moi

`src/skill_gap_explainer.py` nen lam:

1. nhan candidate-side scored job result;
2. phan loai:
   - missing must-have
   - weak evidence
   - optional missing
   - domain/context notes
3. build explanation payload;
4. build CV improvement suggestions theo rule.

## 5. Skill-gap taxonomy de xuat

Phase 23 nen chuan hoa gap thanh 4 nhom:

### 5.1 Missing Must-have Skills

Skill bat buoc ma CV khong co match.

Vi du:

```json
{
  "skill": "AWS",
  "gap_type": "missing_must_have"
}
```

### 5.2 Weak Evidence Skills

Skill da co match, nhung evidence level yeu.

Vi du:

```json
{
  "skill": "Docker",
  "gap_type": "weak_evidence",
  "current_evidence_level": 1
}
```

### 5.3 Optional Growth Skills

Skill nice-to-have ma role uu tien.

Vi du:

```json
{
  "skill": "Kafka",
  "gap_type": "optional_growth"
}
```

### 5.4 CV Presentation Gaps

Khong nhat thiet la thieu skill, ma thieu cach dien dat.

Vi du:

```json
{
  "gap_type": "presentation",
  "message": "Add project outcomes, metrics, and technologies more explicitly."
}
```

## 6. CV improvement suggestion engine de xuat

### 6.1 Muc tieu

Khong chi bao "thieu", ma phai goi y:

```text
ban nen them gi vao CV
```

### 6.2 Rule-based suggestion groups

#### A. Add missing hard skills if they are real

Neu `missing_must_have_skill = AWS`

goi y:

```text
If you have used AWS in real work or projects, add it explicitly in your Skills section and mention one concrete usage example in experience or projects.
```

#### B. Surface stronger evidence

Neu skill da match nhung evidence level <= 1:

```text
Move this skill from keyword-only mention to a work/project bullet with technologies, responsibilities, and outcomes.
```

#### C. Add metrics/results

Neu role can deployment/performance/scale:

```text
Add measurable outcomes such as latency reduction, model accuracy, throughput, cost savings, or scale.
```

#### D. Add context/domain wording

Neu role co domain context manh nhu:

- banking
- eKYC
- security
- fintech

va candidate da co domain lien quan nhung CV noi qua mo:

```text
Mention the business/domain context more explicitly so the job fit is easier to detect.
```

### 6.3 Khong sinh "de xuat ao"

He thong khong nen invent noi dung.

Khong duoc noi:

```text
Hay viet rang ban da dung AWS
```

Neu CV khong co dau vet nao.

Phai noi:

```text
If you have real experience with AWS, add it explicitly...
```

Day la diem quan trong de dam bao tinh dao duc va tranh "lam dep CV ao".

## 7. Output contract de xuat

Moi `top_job` nen co them:

```json
{
  "skill_gap_summary": {
    "missing_must_have_count": 2,
    "weak_evidence_count": 1,
    "optional_growth_count": 2
  },
  "skill_gaps": {
    "missing_must_have": [],
    "weak_evidence": [],
    "optional_growth": [],
    "presentation_gaps": []
  },
  "cv_improvement_suggestions": [],
  "next_best_actions": []
}
```

### 7.1 `next_best_actions`

Nen co 2-4 action uu tien nhat, vi UI web se can rat nhieu phan nay.

Vi du:

```text
1. Add explicit AWS usage if you have real project experience.
2. Rewrite Docker bullets with deployment evidence and outcomes.
3. Mention backend system scale or database responsibility more clearly.
```

## 8. Candidate-side UI logic de xuat

Phase 23 chua code web, nhung output nen phuc vu UI sau nay:

- badge `fit_label`
- section `Why this job fits`
- section `What is missing`
- section `How to improve your CV`

Khong can render recruiter `review_card` cho ung vien.

## 9. Pham vi thuc hien cua Phase 23

### 9.1 Trong scope

- them skill-gap explainer module;
- build structured skill-gap output;
- build CV improvement suggestions;
- them `next_best_actions`;
- tich hop vao candidate-side reranker/output;
- tests va docs.

### 9.2 Ngoai scope

- chua rewrite CV tu dong;
- chua tao bullet text bang GPT;
- chua phan tich full sentence-level rewrite quality;
- chua can preference-aware ranking;
- chua can feedback loop.

## 10. Test plan

Them/cap nhat:

```text
tests/test_skill_gap_explainer.py
tests/test_candidate_job_reranker.py
tests/test_job_recommendation_pipeline.py
tests/test_api.py
```

### 10.1 Cases can co

1. Missing skill duoc dua vao `missing_must_have`.
2. Match co `evidence_level = 1` duoc dua vao `weak_evidence`.
3. Nice-to-have missing duoc dua vao `optional_growth`.
4. Evidence score thap sinh ra `presentation_gap`.
5. Suggestion cho missing skill dung wording `If you have real experience...`.
6. Suggestion cho weak evidence nhan manh them project/work bullet.
7. Candidate-side output co `skill_gap_summary`.
8. Candidate-side output co `cv_improvement_suggestions`.
9. Candidate-side output co `next_best_actions`.
10. `/screening` van khong bi anh huong.

### 10.2 Benchmark thu cong de xuat

Sau khi code:

```powershell
$body = Get-Content docs\integration\sample-recommend-jobs-request.json -Raw
Invoke-RestMethod http://127.0.0.1:8000/recommend-jobs -Method Post -ContentType "application/json" -Body $body
```

Can inspect:

- `top_jobs[0].skill_gap_summary`
- `top_jobs[0].skill_gaps`
- `top_jobs[0].cv_improvement_suggestions`
- `top_jobs[0].next_best_actions`

## 11. Acceptance criteria

Phase 23 hoan thanh khi:

- candidate-side output co skill-gap structure ro rang;
- phan biet duoc missing skill va weak evidence;
- co CV improvement suggestions co y nghia va trung thuc;
- co `next_best_actions` de web render gon;
- employer-side screening khong bi anh huong;
- full `pytest` pass.

## 12. Rui ro va giam thieu

### 12.1 Suggestion qua chung chung

Risk:

```text
Output giong mot danh sach loi khuyen chung chung, khong dung du lieu cua role.
```

Giam thieu:

- build suggestion tu gap that cua job
- uu tien top 2-4 actions
- tan dung requirement groups va evidence levels

### 12.2 Suggestion "ao"

Risk:

```text
He thong khuyen ung vien them skill ma khong co that.
```

Giam thieu:

- dung wording co dieu kien:
  `If you have real experience...`
- khong invent project/metric

### 12.3 Nhieu text qua cho UI

Risk:

```text
Output qua dai, web kho render gon.
```

Giam thieu:

- giu `skill_gap_summary` cho tong quan
- giu `next_best_actions` cho UI compact
- de `cv_improvement_suggestions` chi tiet hon cho modal/detail page

## 13. Ghi chu cho bao cao

Co the trinh bay:

```text
Sau khi da xac dinh muc do phu hop cua CV voi tung JD, he thong tiep tuc bo
sung mot lop giai thich skill-gap cho candidate-side. Lop nay phan biet giua
ky nang bat buoc con thieu, ky nang da co nhung bang chung con yeu, va cac ky
nang uu tien co the bo sung them. Tren co so do, he thong dua ra cac goi y
cai thien CV theo huong trung thuc va co the hanh dong duoc, vi du bo sung
bang chung tu du an/kinh nghiem, them metric, hoac surface ro hon phan cong
nghe da tung dung. Cach lam nay bien candidate-side recommendation tu muc
"goi y cong viec" sang muc "goi y cong viec + goi y cai thien CV".
```

Mot cau ngan khi bao ve:

```text
Phase 23 bien candidate-side recommendation thanh co kha nang hanh dong:
he thong khong chi noi job nao hop, ma con noi ro dang thieu gi va nen sua CV
the nao de tang fit signal.
```

