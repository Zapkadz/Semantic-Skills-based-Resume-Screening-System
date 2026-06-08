# Phase 14 - Open-set Requirement Matching

## 1. Muc tieu phase

Phase 14 xu ly truong hop JD co requirement/skill chua nam trong taxonomy hien tai.

Huong thiet ke:

```text
Known taxonomy requirement
  -> rule-based matching
  -> evidence detection
  -> explainable score

Unknown requirement
  -> giu nguyen requirement goc
  -> multilingual embedding tim evidence gan nghia trong CV
  -> gan nhan semantic-only / unknown-taxonomy
  -> cong diem co gioi han
```

Muc tieu quan trong:

- Khong bo qua requirement la.
- Khong ep requirement la vao taxonomy sai.
- Van danh gia duoc bang semantic evidence khi JD/CV khac ngon ngu hoac khac cach dien dat.
- Giu tinh minh bach: ket qua ngoai taxonomy phai duoc danh dau ro.

## 2. Boi canh truoc Phase 14

Phase 13 da co:

- Local multilingual embedding voi `BAAI/bge-m3`.
- CLI flag `--enable-embedding`, `--embedding-model`, `--embedding-local-only`.
- API env vars de bat embedding.
- Optional embedding matcher trong file-based pipeline va payload pipeline.
- Semantic match fallback cho candidate skills.

Han che con lai:

- `_build_job_skill_list` dang uu tien taxonomy extraction.
- Requirement la co the bi bo qua neu khong duoc xem la skill label ngan.
- Embedding hien match skill list voi skill list, chua match requirement sentence voi CV evidence sentence.
- Neu unknown requirement duoc dua vao must-have nhu skill binh thuong, scoring co the qua khat hoac kho giai thich.

Phase 14 can tach ro:

```text
taxonomy_matched_requirements
unknown_requirements
semantic_only_requirement_matches
taxonomy_coverage
```

## 3. Co so tham khao

Huong nay phu hop voi cac cach lam trong he thong skills-based matching:

- ESCO cung cap taxonomy skill/occupation da ngon ngu, co API va unique concept identifiers.
  - <https://esco.ec.europa.eu/en/use-esco>
- O*NET mo ta occupation theo knowledge, skills, abilities, tasks va work activities.
  - <https://www.dol.gov/agencies/eta/onet?lang=en>
  - <https://www.onetcenter.org/database.html>
- Skill extraction research nhu SkillSpan cho thay skill extraction can annotation ro va domain-specific handling.
  - <https://arxiv.org/abs/2204.12811>
- Weak supervision/latent representation voi ESCO cho thay co the dung representation/embedding de tim skill tuong tu trong job ads.
  - <https://arxiv.org/abs/2209.08071>
- Data-driven taxonomy research cua Nesta/ESCoE dung word embeddings, skill co-occurrence graph va clustering de mo rong taxonomy theo du lieu job ads.
  - <https://ideas.repec.org/p/nsr/escoed/escoe-dp-2018-13.html>

Ket luan cho do an:

- Taxonomy la backbone de giai thich.
- Embedding la open-set fallback khi taxonomy chua phu du.
- Unknown match phai duoc danh dau va score co gioi han.
- Taxonomy expansion nen tach sang human-in-the-loop phase sau.

## 4. Dinh nghia trong phase nay

### 4.1 Known taxonomy requirement

Requirement/skill tu JD co the map vao taxonomy canonical skill.

Vi du:

```text
Java -> Java
Spring Boot -> Spring Boot
nhan dien khuon mat -> Face Recognition
```

Xu ly:

```text
rule-based exact/related/transferable
semantic skill fallback neu bat embedding
evidence detection theo taxonomy aliases
```

### 4.2 Unknown requirement

Requirement tu JD khong map duoc vao taxonomy, nhung van co kha nang la mot ky nang/nang luc can danh gia.

Vi du:

```text
carbon footprint analysis
reflection cues for anti-spoofing
robot navigation with SLAM
drone mission planning
```

Xu ly:

```text
giu nguyen text goc
trich candidate evidence sentences tu CV
embedding similarity requirement <-> evidence sentence
neu dat threshold thi tao semantic-only evidence match
```

### 4.3 Semantic-only match

Match duoc tao bang embedding cho unknown requirement.

Day khong phai taxonomy skill da chuan hoa.

Vi du output:

```json
{
  "required_skill": "carbon footprint analysis",
  "candidate_skill": null,
  "match_type": "semantic_only_match",
  "taxonomy_status": "unknown",
  "score": 0.65,
  "similarity": 0.8421,
  "evidence_text": "Thuc hien phan tich phat thai CO2 va lap bao cao ESG.",
  "evidence_source": "work_experience"
}
```

## 5. Pham vi thuc hien

Trong Phase 14 se lam:

- Them module/helper xu ly unknown requirements.
- Tach job requirements thanh:
  - known taxonomy requirements.
  - unknown requirements.
- Them sentence/evidence candidate extraction tu CV profile.
- Dung `SemanticEmbeddingMatcher` de so sanh unknown requirement voi CV evidence sentences.
- Them match type moi:
  - `semantic_only_match`.
  - `no_semantic_evidence`.
- Them metadata:
  - `taxonomy_status`.
  - `similarity`.
  - `evidence_text`.
  - `evidence_source`.
- Them `taxonomy_coverage` trong output job/result.
- Gioi han diem cua semantic-only match de tranh over-credit.
- Cap nhat review card de hien ro unknown-taxonomy/semantic-only evidence.
- Cap nhat tests voi fake embedding model, khong download model that.

Ngoai scope Phase 14:

- Chua tao Admin UI.
- Chua auto ghi skill moi vao taxonomy.
- Chua import ESCO/O*NET full dataset.
- Chua dung GPT de de xuat taxonomy.
- Chua thay doi schema API bat buoc.

Phase 15 se xu ly human-in-the-loop taxonomy suggestion.

## 6. Thiet ke du kien

### 6.1 Requirement analyzer

Co the tao file moi:

```text
src/open_set_matcher.py
```

Trach nhiem:

- Lay raw JD requirement lines.
- Xac dinh requirement nao da map vao taxonomy.
- Giu unknown requirement co kha nang la skill/nang luc.
- Chay semantic evidence search.

Ham du kien:

```python
def split_known_and_unknown_requirements(
    raw_requirements: list[str],
    known_skills: list[str],
    taxonomy: dict[str, dict],
) -> dict:
    ...

def find_semantic_requirement_evidence(
    unknown_requirements: list[str],
    resume_profile: dict,
    embedding_matcher: SemanticEmbeddingMatcher | None,
    threshold: float = 0.72,
) -> list[dict]:
    ...
```

### 6.2 Evidence sentence extraction

Can helper lay evidence candidates tu CV:

```text
summary
skills
work_experience descriptions
projects descriptions
certifications
```

Output co source:

```json
{
  "text": "Built face anti-spoofing module using texture and motion cues.",
  "source": "projects"
}
```

Can tranh encode cau qua ngan/vo nghia.

### 6.3 Matching threshold

De xuat config:

```python
DEFAULT_OPEN_SET_SIMILARITY_THRESHOLD = 0.74
OPEN_SET_MATCH_SCORE = 0.65
```

Ly do:

- Unknown requirement khong duoc tin nhu exact taxonomy match.
- Similarity threshold nen cao hon default semantic skill threshold mot chut.
- Score 0.65 giup ung vien duoc ghi nhan nhung khong vuot exact/related evidence.

Co the tinh match score theo similarity:

```text
similarity >= 0.85 -> score 0.70
0.74 <= similarity < 0.85 -> score 0.60-0.65
```

Nhung MVP nen bat dau bang constant de de test.

### 6.4 Output taxonomy coverage

Them output:

```json
{
  "taxonomy_coverage": {
    "known_count": 7,
    "unknown_count": 3,
    "coverage_ratio": 0.7,
    "unknown_requirements": [
      "carbon footprint analysis",
      "ESG reporting"
    ]
  }
}
```

Nen dat trong:

```text
result["job"]["taxonomy_coverage"]
```

Va co the copy vao top-level sau nay neu web can.

### 6.5 Review card

Review card nen them hoac hien trong concerns:

```text
Some requirements were evaluated using semantic-only evidence because they are not yet in the taxonomy.
```

Candidate review co the hien:

```text
Semantic-only evidence:
- carbon footprint analysis matched evidence: ...
```

Quan trong: khong ghi nhu exact skill match.

## 7. Scoring strategy

Khong nen thay doi weight lon trong Phase 14 neu chua can.

Phuong an an toan:

- Semantic-only matches duoc append vao `matched_skills`.
- `match_type = semantic_only_match`.
- `score = 0.65`.
- Evidence level dua tren evidence source:
  - work/projects: level 2 hoac 3 neu co action verb.
  - summary/skills: level 1.
- Existing scorer se tinh diem theo match score/evidence.

Can test regression de dam bao:

- JD/CV backend Java demo khong doi diem qua manh.
- JD_1/CV_85 khong bi giam do unknown requirements qua nhieu neu co semantic evidence phu hop.
- Candidate khong lien quan khong duoc semantic-only match sai.

## 8. Test plan

Them tests:

```text
tests/test_open_set_matcher.py
```

Cases:

1. Tach known/unknown requirements.
2. Unknown requirement khong bi bo qua.
3. Fake embedding tim semantic-only evidence Viet-Anh.
4. Similarity duoi threshold thi khong match.
5. Output co `taxonomy_status = unknown`.
6. Semantic-only score bi gioi han.
7. Taxonomy coverage ratio tinh dung.
8. Pipeline output co `taxonomy_coverage`.
9. Review card co note semantic-only khi co unknown matches.
10. Khi embedding disabled, unknown requirements duoc report nhung khong crash.

Full regression:

```powershell
pytest
```

Manual CLI:

```powershell
python main.py --jd data/jobs/JD_1.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

Manual API:

```powershell
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'
uvicorn api:app --host 127.0.0.1 --port 8000
```

## 9. Rui ro va giam thieu

### 9.1 Semantic false positive

Risk:

```text
Embedding thay hai cau gan nghia nhung thuc te khong phai skill phu hop.
```

Giam thieu:

- Threshold cao hon.
- Score gioi han.
- Gan nhan `semantic_only_match`.
- Hien evidence text de nha tuyen dung kiem tra.

### 9.2 Requirement la qua dai

Risk:

```text
Ca cau dai gom nhieu skill lam embedding match mo ho.
```

Giam thieu:

- Cat requirement theo bullet/sentence.
- Bo qua cau qua dai hoac tach thanh clauses neu can.
- Phase sau co the them GPT/NER extraction.

### 9.3 Diem thay doi kho giai thich

Risk:

```text
Bat unknown semantic match lam final score nhay bat ngo.
```

Giam thieu:

- Ghi `taxonomy_coverage`.
- Ghi `semantic_only_count`.
- Score cap.
- Review card noi ro semantic-only la tin hieu bo sung.

### 9.4 Embedding unavailable

Risk:

```text
Khong co model local hoac API chua bat embedding.
```

Giam thieu:

- Unknown requirements van duoc report.
- Khong crash pipeline.
- Match semantic-only chi chay khi matcher available.

## 10. Acceptance criteria

Phase 14 hoan thanh khi:

- Pipeline khong bo qua unknown requirements.
- Known requirements van dung taxonomy/rule/evidence nhu cu.
- Unknown requirements co the duoc match bang multilingual embedding voi CV evidence sentences.
- Semantic-only match co metadata ro:
  - `match_type`.
  - `taxonomy_status`.
  - `similarity`.
  - `evidence_text`.
  - `evidence_source`.
- Output co `taxonomy_coverage`.
- Review card phan biet taxonomy match va semantic-only match.
- Tests dung fake embedding pass.
- Full `pytest` pass.
- CLI/API regression pass.

## 11. Ghi chu cho bao cao

Co the mo ta:

```text
Taxonomy khong the bao phu toan bo nganh nghe ngay tu dau, nen he thong duoc thiet ke theo huong open-set. Voi skill da co trong taxonomy, he thong dung rule-based matching va evidence detection de danh gia chinh xac, giai thich duoc. Voi requirement chua co trong taxonomy, he thong giu nguyen text goc va dung multilingual embedding de tim bang chung gan nghia trong CV. Ket qua nay duoc danh dau la semantic-only/unknown-taxonomy de tranh nham voi skill da chuan hoa.
```

Phase 15 se tiep tuc:

```text
Neu unknown requirements xuat hien nhieu lan, he thong gom nhom bang embedding, thong ke tan suat va de xuat cho Admin them vao taxonomy. Admin phai duyet truoc khi taxonomy duoc cap nhat.
```

## 12. Sau khi code Phase 14

Da trien khai:

- Them `src/open_set_matcher.py`.
- Them `taxonomy_coverage` vao job output.
- Them `open_set_requirement_matches` vao candidate output.
- Unknown requirement khong con bi dua vao `must_have_skills` nhu skill taxonomy thuong.
- Neu embedding matcher available:
  - unknown requirement duoc so sanh voi CV evidence sentences.
  - similarity du threshold tao `semantic_only_match`.
  - similarity duoi threshold tao `no_semantic_evidence`.
- Neu embedding disabled/unavailable:
  - unknown requirement van nam trong `taxonomy_coverage`.
  - pipeline khong crash va khong phat sinh semantic-only score.
- Review card them concern khi co `semantic_only_match`.
- Scorer xem `no_semantic_evidence` la missing requirement khi no duoc scoring.

Ket qua manual voi `JD_1` va BGE-M3 local:

```text
taxonomy_coverage:
known_count = 15
unknown_count = 7
coverage_ratio = 0.6818

Top candidate:
Le Hoang Nam - 72/100 - Review
```

Diem giam nhe so voi Phase 13 vi unknown requirements khong duoc cong diem neu khong co semantic evidence du threshold. Day la hanh vi co chu y: he thong khong tu cong diem cho requirement ngoai taxonomy khi bang chung chua du manh.
