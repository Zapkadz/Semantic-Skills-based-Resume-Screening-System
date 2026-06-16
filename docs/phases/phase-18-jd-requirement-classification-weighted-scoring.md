# Phase 18 - JD Requirement Classification and Weighted Scoring Refinement

## 1. Muc tieu phase

Phase 18 giai quyet van de phat hien khi test `JD_3.txt` voi `CV_3_1.txt` va `CV_3_3.txt`:

```text
He thong dang lay qua nhieu dong trong JD lam must-have skill.
Dieu nay lam diem ung vien bi keo thap boi cac dong khong phai skill bat buoc.
```

Vi du trong JD Fullstack:

```text
Tot nghiep Dai hoc nganh CNTT...
Ky nang giao tiep, trinh bay, thuyet trinh
Nhiet tinh, dam me hoc hoi, chiu duoc ap luc
Dieu kien uu tien: .NET, ASP, JSP, Ajax, Cloud, GitLab...
```

Hien tai nhieu dong nhu tren bi dua vao matching nhu requirement bat buoc. Phase 18 se tach JD thanh cac nhom requirement ro rang hon:

```text
must_have_technical
nice_to_have_technical
soft_skills
education
experience
certifications
domain_context
responsibilities
noise
```

Muc tieu cuoi cung:

```text
Score phan anh dung muc do phu hop nghe nghiep,
khong phat nang ung vien vi thieu soft skill hoac nice-to-have.
```

## 2. Ly do can Phase 18

Sau Phase 17, he thong da co open-set semantic matching nen co the xu ly skill ngoai taxonomy. Nhung Phase 17 van chua phan biet duoc do quan trong cua tung dong JD.

Case `JD_3.txt` cho thay:

- `CV_3_3` phu hop hon `CV_3_1`, ranking dung.
- Nhung diem `CV_3_3 = 55/100` hoi thap so voi cam nhan tuyen dung.
- Nguyen nhan chinh la `open_set_requirement_count = 39`.
- Nhieu dong soft skill, education, nice-to-have bi tinh nhu must-have.
- `Dieu kien uu tien` chua duoc tach sang nice-to-have.

Neu khong lam Phase 18:

- JD dai se tao qua nhieu missing skills.
- Review card se hoi "nang tay".
- Recruiter co the thay ung vien phu hop nhung diem AI thap.
- Bao cao do an kho giai thich vi system khong phan biet bat buoc/uu tien.

## 3. Co so thiet ke

Huong Phase 18 dua tren cac mo hinh/job taxonomy dang duoc dung rong rai:

### 3.1 ESCO

ESCO chia skills pillar thanh:

- Knowledge.
- Language skills and knowledge.
- Skills.
- Transversal skills.

Y tuong ap dung:

```text
Technical skills != soft/transversal skills != knowledge/education.
```

Nguon: https://esco.ec.europa.eu/en/classification/skill_main

### 3.2 O*NET Content Model

O*NET to chuc thong tin nghe nghiep thanh cac nhom:

- Skills.
- Knowledge.
- Education.
- Experience and Training.
- Licensing.
- Tasks.
- Work Activities.

Y tuong ap dung:

```text
JD parser can tach skill, knowledge, education, experience, task/responsibility.
```

Nguon: https://www.onetcenter.org/content.html

### 3.3 SkillSpan

SkillSpan xem skill extraction trong job posting la bai toan span extraction, co hard skill va soft skill. Paper cung nhan manh viec can cover emerging skills ngoai predefined taxonomy.

Y tuong ap dung:

```text
Khong chi extract keyword, ma can gan loai cho span/line requirement.
```

Nguon: https://arxiv.org/abs/2204.12811

## 4. Nguyen tac thiet ke

### 4.1 Khong bien moi dong JD thanh skill bat buoc

Moi dong JD sau khi parse phai co classification:

```json
{
  "text": "Thanh thao Java, Spring Boot, Angular, Javascript.",
  "category": "must_have_technical",
  "priority": "required",
  "weight": "high"
}
```

Khong con mac dinh:

```text
JD line -> must-have skill
```

### 4.2 Nice-to-have la cong diem, khong phat nang

Cac dong duoi:

```text
Dieu kien uu tien
Nice to have
Preferred
Plus
La loi the
```

Phai vao `nice_to_have_technical`.

Neu ung vien co match thi cong diem. Neu khong co thi chi hien trong review card nhu optional gap, khong keo manh `skill_semantic`.

### 4.3 Soft skill nen report nhe hoac interview question

Soft skills nhu:

```text
communication
teamwork
presentation
independent work
work under pressure
detail-oriented
analytical mindset
dam me hoc hoi
chiu duoc ap luc
```

Khong nen scoring ngang voi Java/Spring/Oracle.

Huong scoring:

- Soft skill co evidence: cong nhe.
- Soft skill thieu evidence: khong phat nang.
- Review card co the goi y cau hoi phong van.

### 4.4 Education va experience la component rieng

Education:

```text
Tot nghiep Dai hoc CNTT, Toan tin, Dien tu vien thong...
```

Khong nen dua vao missing skill nhu:

```text
Missing skill: CNTT
Missing skill: Toan tin
```

Experience:

```text
Toi thieu 02 nam kinh nghiem...
Co tu 01 nam kinh nghiem...
```

Phai vao `minimum_experience_years` hoac `experience_requirements`, khong dua vao skill list.

### 4.5 Rule-first, explainable-first

Phase 18 uu tien:

- Rule-based section parser.
- Keyword/pattern classifier.
- Taxonomy/open-set extractor hien co.
- Fake embedding trong tests.

Khong dung GPT trong core.

Ly do:

- Local-first.
- Giai thich duoc khi bao ve.
- Khong ton cost.
- Khong lo CV/JD privacy.

## 5. Pham vi thuc hien

Trong Phase 18 se lam:

- Them module classification cho JD requirements.
- Tach section `Dieu kien bat buoc` va `Dieu kien uu tien`.
- Phan loai line thanh technical/soft/education/experience/certification/domain/noise.
- Cap nhat JD parser output de co structured requirement groups.
- Cap nhat screening pipeline de chi dua `must_have_technical` vao must-have scoring.
- Dua `nice_to_have_technical` vao nice-to-have scoring.
- Soft skill/education/experience hien rieng trong job output/review card.
- Cap nhat review card de concerns khong liet ke soft skill/education nhu missing technical skill.
- Them tests cho JD_3-like cases.
- Cap nhat README/dev log.

Ngoai scope Phase 18:

- Khong import full ESCO/O*NET dataset.
- Khong train NER model.
- Khong goi GPT.
- Khong lam UI web.
- Khong thay doi DB PHP neu khong can.
- Khong sua diem bang hard-code rieng cho JD_3.

## 6. Kien truc de xuat

### 6.1 Module moi: jd_requirement_classifier

De xuat tao:

```text
src/jd_requirement_classifier.py
```

Trach nhiem:

- Nhan parsed JD sections hoac raw requirement lines.
- Gan section priority.
- Gan category cho tung line.
- Tra ve structured groups.

Ham de xuat:

```python
def classify_jd_requirements(
    job_criteria: dict,
    jd_text: str,
    taxonomy: dict,
) -> dict:
    ...
```

Output de xuat:

```json
{
  "must_have_technical": ["Java", "Spring Boot", "Angular", "Oracle"],
  "nice_to_have_technical": ["JSP", "Ajax", "GitLab", "Docker"],
  "soft_skills": ["communication", "teamwork"],
  "education": ["Bachelor degree in IT or equivalent"],
  "experience": ["2 years application development"],
  "certifications": [],
  "domain_context": ["banking/finance"],
  "ignored": ["Dieu kien bat buoc:"]
}
```

### 6.2 Section priority detection

Can nhan cac heading:

Required:

```text
Yeu cau cong viec
Dieu kien bat buoc
Yeu cau bat buoc
Must-have
Required
Requirements
Qualifications
```

Preferred:

```text
Dieu kien uu tien
Uu tien
Nice to have
Preferred
Plus
Advantage
La loi the
```

Responsibilities:

```text
Mo ta cong viec
Responsibilities
Job description
Tasks
```

### 6.3 Line category detection

Rule examples:

Education:

```text
tot nghiep
dai hoc
cao dang
bachelor
degree
major in
nganh CNTT
```

Experience:

```text
toi thieu 2 nam
at least 2 years
co kinh nghiem
years of experience
```

Soft skill:

```text
giao tiep
trinh bay
thuyet trinh
lam viec nhom
doc lap
chiu ap luc
dam me hoc hoi
analytical
communication
teamwork
presentation
problem solving
```

Certification:

```text
certificate
certification
chung chi
Security+
CEH
ISO 27001
AWS Certified
```

Technical:

```text
Any taxonomy skill or open-set technical unit:
Java, Spring Boot, Angular, Oracle, OOP, CI/CD, API, Linux...
```

Domain/context:

```text
banking
finance
eKYC
healthcare
logistics
ngan hang
tai chinh
```

Noise/heading:

```text
Dieu kien bat buoc:
Dieu kien uu tien:
Skills:
Qualifications:
```

## 7. Scoring refinement

### 7.1 De xuat component scores

Hien tai:

```text
skill_semantic 40%
evidence       20%
experience     15%
seniority      10%
domain         10%
nice_to_have    5%
```

Phase 18 co the giu khung nay nhung thay input:

```text
skill_semantic = only must_have_technical
evidence       = evidence for must_have_technical
experience     = experience requirements
education      = optional/light component hoac report-only
soft_skills    = optional/light component hoac report-only
nice_to_have   = nice_to_have_technical coverage
```

Option an toan cho phase nay:

```text
Khong them component moi vao final score ngay.
Chi thay doi input de:
- soft skill khong nam trong must-have.
- education khong nam trong must-have.
- nice-to-have khong nam trong must-have.
```

Neu can them component moi thi de Phase 19.

### 7.2 Expected behavior voi JD_3

Truoc Phase 18:

```text
CV_3_3 = 55
CV_3_1 = 46
```

Sau Phase 18 ky vong:

```text
CV_3_3: 65-75
CV_3_1: 45-55
```

Ly do:

- CV_3_3 co Java, Spring Boot, Angular/Fullstack evidence, Oracle, Docker, experience.
- CV_3_1 co backend API/Java/Spring/MySQL/Docker nhung thieu Angular/JavaScript/Oracle va nhieu fullstack/front-end evidence.
- Nice-to-have .NET/JSP/Ajax/GitLab khong con phat nang.
- Soft skills khong con tao missing skills dai.

## 8. Output sau Phase 18

Job output nen co them:

```json
{
  "requirement_groups": {
    "must_have_technical": [],
    "nice_to_have_technical": [],
    "soft_skills": [],
    "education": [],
    "experience": [],
    "certifications": [],
    "domain_context": [],
    "ignored": []
  }
}
```

Candidate output co the them:

```json
{
  "soft_skill_matches": [],
  "education_matches": [],
  "requirement_group_summary": {
    "must_have_matched": 8,
    "must_have_total": 10,
    "nice_to_have_matched": 3,
    "nice_to_have_total": 8
  }
}
```

Review card can hien:

```text
Missing must-have technical skills:
- Angular
- Oracle

Optional gaps:
- GitLab
- Cloud

Recruiter review:
- Education requirement: Bachelor in IT or equivalent
- Soft skills should be verified in interview
```

Khong nen hien:

```text
Missing skills: giao tiep, nhiet tinh, dam me hoc hoi...
```

## 9. Test plan

Them/cap nhat tests:

```text
tests/test_jd_requirement_classifier.py
tests/test_jd_parser.py
tests/test_screening_pipeline.py
tests/test_payload_pipeline.py
tests/test_review_card_generator.py
tests/test_scorer.py
```

Cases can co:

1. Detect `Dieu kien bat buoc` la required section.
2. Detect `Dieu kien uu tien` la preferred section.
3. `Java, Spring Boot, Angular, Javascript` vao must-have technical.
4. `.NET, C#, ASP.NET, GitLab, Docker` trong preferred section vao nice-to-have.
5. `Tot nghiep Dai hoc...` vao education, khong vao missing skills.
6. `Toi thieu 02 nam kinh nghiem` vao experience, khong vao open-set skill.
7. `giao tiep, trinh bay, lam viec nhom` vao soft_skills.
8. Heading `Dieu kien bat buoc:` khong vao skill.
9. JD_3-like payload co must-have count giam hop ly.
10. CV_3_3 score tang so voi truoc hoac missing skills giam ro.
11. CV_3_3 van xep tren CV_3_1.
12. Nice-to-have thieu khong keo skill_semantic xuong manh.
13. API payload co `requirement_groups`.
14. Review card tach Missing must-have va Optional gaps.

Manual regression:

```powershell
python main.py --jd data\jobs\JD_3.txt --cv-dir outputs\test_jd3_cv3 --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only --output-json outputs\jd3_cv3_phase18_result.json --show-review-cards
```

Full regression:

```powershell
pytest
```

## 10. Acceptance criteria

Phase 18 hoan thanh khi:

- JD parser/classifier tach duoc required vs preferred sections.
- Soft skills khong bi tinh nhu must-have technical.
- Education khong bi tinh nhu missing skill.
- Experience khong bi tinh nhu skill.
- Nice-to-have chi cong diem/optional gap, khong phat nang.
- `JD_3.txt` khong con tao 39 open-set requirements rac.
- Review card ngan gon va dung ban chat hon.
- Ranking `CV_3_3 > CV_3_1` van giu dung.
- Score cua candidate phu hop hon voi cam nhan tuyen dung.
- API/CLI output backward-compatible o muc can thiet.
- Full tests pass.

## 11. Rui ro va giam thieu

### 11.1 Classifier loc qua tay

Risk:

```text
Mot requirement technical bi gan nham thanh soft/noise.
```

Giam thieu:

- Neu co taxonomy skill trong line thi uu tien technical.
- Neu co token technical viet hoa/cau truc tool/framework thi giu technical.
- Them tests voi JD tieng Viet that.

### 11.2 Nice-to-have tach sai

Risk:

```text
Mot requirement bat buoc sau heading uu tien bi dua nham nice-to-have.
```

Giam thieu:

- Section state chi doi khi gap heading ro.
- Tests voi `Dieu kien bat buoc` -> `Dieu kien uu tien`.

### 11.3 Soft skill van can trong mot so role

Risk:

```text
Sales/HR/PM role soft skills rat quan trong.
```

Giam thieu:

- Phase 18 chi khong phat nang soft skill trong technical scoring.
- Van report soft skills va co the scoring nhe.
- Future phase co role-aware weights.

### 11.4 Diem tang qua cao

Risk:

```text
Bo qua qua nhieu requirement lam score ao.
```

Giam thieu:

- Giu education/soft/nice-to-have trong review card.
- Recruiter van thay optional gaps.
- Evidence level van bat buoc cho match tot.

## 12. Ghi chu cho bao cao

Co the viet:

```text
Trong tin tuyen dung, khong phai moi cau yeu cau deu co vai tro nhu nhau.
De tranh cham diem sai, he thong phan loai JD thanh cac nhom: ky nang
chuyen mon bat buoc, ky nang uu tien, ky nang mem, hoc van, kinh nghiem,
chung chi va ngu canh nganh nghe. Diem phu hop duoc tinh chu yeu tren ky
nang chuyen mon bat buoc va bang chung trong CV; cac yeu cau uu tien chi
dong vai tro cong diem, con ky nang mem/hoc van duoc dung de ho tro review
va phong van. Cach nay giup ket qua xep hang cong bang hon va giai thich
duoc hon.
```

Mot cau ngan khi bao ve:

```text
He thong khong so khop JD theo kieu keyword phang; moi yeu cau duoc phan
loai truoc khi scoring de dam bao hard skill, soft skill, hoc van, kinh
nghiem va nice-to-have co trong so khac nhau.
```

## 13. Sau khi code Phase 18

Da trien khai:

- Them `src/jd_requirement_classifier.py`.
- Them `tests/test_jd_requirement_classifier.py`.
- Cap nhat `src/jd_parser.py` de nhan `Dieu kien bat buoc` va `Dieu kien uu tien`.
- Cap nhat CLI/API pipeline de dung `requirement_groups` truoc scoring.
- Must-have scoring chi dung `must_have_technical` va required certifications.
- Nice-to-have technical duoc dua vao optional scoring.
- Soft skills, education, experience, domain context khong con bi tinh nhu missing technical skill.
- Cap nhat `src/requirement_extractor.py` de strip Vietnamese technical lead-ins:
  - `Thanh thao`
  - `Co kien thuc ve`
  - `Co hieu biet co ban ve`
  - `co so du lieu`
- Cap nhat review card them `Requirement Notes`.
- Candidate output co `requirement_group_summary`.

Manual benchmark voi `JD_3.txt`, `CV_3_1.txt`, `CV_3_3.txt`:

```text
CV_3_3 / Le Quoc Bao     - 76/100 - Review
CV_3_1 / Nguyen Van Hung - 51/100 - Low Priority
```

So voi truoc Phase 18:

```text
CV_3_3 / Le Quoc Bao     - 55/100 - Maybe Review
CV_3_1 / Nguyen Van Hung - 46/100 - Low Priority
```

Nhan xet:

- Ranking van dung.
- Diem CV_3_3 phu hop hon voi cam nhan tuyen dung.
- Review card khong con liet ke hoc van/soft skills nhu missing hard skill.
- Optional gaps van duoc bao cao rieng.

