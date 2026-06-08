# Phase 15 - Human-in-the-loop Taxonomy Suggestion Queue

## 1. Muc tieu phase

Phase 15 them tang de xuat mo rong taxonomy khi he thong gap unknown requirements nhieu lan.

Huong tong the:

```text
Phase 14:
Unknown requirement
  -> open-set semantic matching
  -> taxonomy_coverage
  -> semantic-only evidence

Phase 15:
Unknown requirements over time
  -> normalize/group near-duplicates
  -> count frequency
  -> collect example contexts
  -> find nearest existing taxonomy skills
  -> create pending taxonomy suggestions
  -> Admin review later
```

Muc tieu quan trong:

- Khong auto them skill moi vao taxonomy.
- AI Python chi tao suggestion co giai thich.
- Admin/web moi la noi duyet approve/reject/merge.
- Giu audit-friendly output de bao ve do an.

## 2. Boi canh truoc Phase 15

Phase 14 da co:

- `job.taxonomy_coverage`.
- `candidate.open_set_requirement_matches`.
- `semantic_only_match`.
- `no_semantic_evidence`.
- `taxonomy_status = unknown`.

Vi du unknown requirements:

```json
{
  "unknown_requirements": [
    "carbon footprint analysis",
    "CO2 emission reporting",
    "phân tích phát thải carbon"
  ]
}
```

He thong hien da biet requirement nao ngoai taxonomy, nhung chua co co che de:

- Gom cac phrase tuong duong.
- Dem tan suat xuat hien.
- De xuat canonical skill moi.
- De xuat alias tieng Anh/Viet.
- Tim skill gan nhat trong taxonomy hien co.
- Xuat danh sach pending cho Admin.

Phase 15 se lam cac viec tren trong AI Python project.

## 3. Co so tham khao

Huong human-in-the-loop taxonomy expansion phu hop voi cach cac he thong skill taxonomy duoc duy tri:

- ESCO/O*NET lam taxonomy co cau truc, concept id va du lieu occupation/skill ro rang.
  - <https://esco.ec.europa.eu/en/use-esco>
  - <https://www.onetcenter.org/database.html>
- Research ve skill extraction cho thay taxonomy coverage khong the hoan hao va can domain-specific handling.
  - SkillSpan: <https://arxiv.org/abs/2204.12811>
  - Weak supervision with ESCO latent representation: <https://arxiv.org/abs/2209.08071>
- Data-driven taxonomy research cua Nesta/ESCoE dung embedding, co-occurrence graph va clustering de phat hien skill group moi.
  - <https://ideas.repec.org/p/nsr/escoed/escoe-dp-2018-13.html>
- Commercial taxonomy nhu Lightcast co refresh cycle va taxonomists/review process, khong de model tu them skill khong kiem soat.
  - <https://kb.lightcast.io/en/articles/7216059-lightcast-skills-taxonomy>

Ket luan cho do an:

- De xuat taxonomy nen la human-in-the-loop.
- Embedding co the dung de gom nhom phrase gan nghia.
- Tan suat va example contexts giup Admin quyet dinh.
- Auto-update taxonomy la risk, khong lam trong phase nay.

## 4. Dinh nghia output

### 4.1 Unknown requirement observation

Mot lan he thong gap requirement ngoai taxonomy.

Vi du:

```json
{
  "phrase": "carbon footprint analysis",
  "job_id": 10,
  "job_title": "ESG Analyst",
  "source": "job.taxonomy_coverage.unknown_requirements",
  "context": "Experience with carbon footprint analysis and ESG reporting.",
  "matched_evidence_text": "Built carbon emission reports for ESG audits.",
  "similarity": 0.8421
}
```

### 4.2 Taxonomy suggestion

De xuat cho Admin xem.

Vi du:

```json
{
  "suggestion_id": "tax-sug-carbon-footprint-analysis",
  "suggested_canonical_name": "Carbon Footprint Analysis",
  "suggested_category": "Sustainability / ESG",
  "suggested_aliases": [
    "carbon footprint analysis",
    "CO2 emission reporting",
    "carbon accounting",
    "phân tích phát thải carbon"
  ],
  "frequency": 8,
  "confidence": 0.81,
  "nearest_existing_skills": [
    {
      "skill": "Data Analysis",
      "similarity": 0.71
    }
  ],
  "example_contexts": [
    "Experience with carbon footprint analysis and ESG reporting."
  ],
  "example_evidence": [
    "Built carbon emission reports for ESG audits."
  ],
  "status": "pending_review"
}
```

## 5. Pham vi thuc hien

Trong Phase 15 se lam:

- Them module de thu thap unknown requirement observations tu screening result.
- Them normalize/dedupe phrase logic.
- Them clustering/grouping nho dua tren:
  - exact normalized phrase.
  - optional embedding similarity neu matcher available.
- Them nearest existing taxonomy lookup bang embedding.
- Them suggestion builder.
- Them JSON read/write helpers cho suggestion queue local.
- Them CLI/helper command de generate suggestions tu mot hoac nhieu screening result JSON.
- Them tests bang fake embedding, khong download model that.
- Cap nhat README/dev log/refactoring plan.

Ngoai scope Phase 15:

- Chua lam Admin UI trong PHP web.
- Chua sua taxonomy JSON tu dong.
- Chua goi GPT.
- Chua import ESCO/O*NET full dataset.
- Chua tao database migration cho web.

## 6. Kien truc de xuat

### 6.1 Module moi

Co the tao:

```text
src/taxonomy_suggestion.py
```

Trach nhiem:

- Extract observations.
- Group phrase variants.
- Build suggestions.
- Save/load suggestion queue JSON.

Ham de xuat:

```python
def collect_unknown_requirement_observations(screening_result: dict) -> list[dict]:
    ...

def build_taxonomy_suggestions(
    observations: list[dict],
    taxonomy: dict,
    embedding_matcher: SemanticEmbeddingMatcher | None = None,
    min_frequency: int = 2,
) -> list[dict]:
    ...

def save_taxonomy_suggestions(suggestions: list[dict], output_path: str | Path) -> str:
    ...

def load_taxonomy_suggestions(path: str | Path) -> list[dict]:
    ...
```

### 6.2 CLI integration

Co 2 cach:

#### Option A - Them subcommand vao `main.py`

Vi du:

```powershell
python main.py suggest-taxonomy --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Nhung `main.py` hien dang la screening command voi required `--jd` va `--cv-dir`. Them subcommand co the lam CLI phuc tap.

#### Option B - Tao file CLI rieng

Vi du:

```text
taxonomy_suggest.py
```

Lenh:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Option B it rui ro hon cho Phase 15, vi khong lam doi behavior `main.py`.

De xuat chon Option B.

### 6.3 Suggestion queue storage

MVP local file:

```text
outputs/taxonomy_suggestions.json
```

Format:

```json
{
  "version": 1,
  "suggestions": [...]
}
```

Sau nay web/Admin co the import vao database.

### 6.4 Grouping strategy

MVP grouping:

1. Normalize phrase:
   - lowercase/casefold.
   - strip punctuation.
   - collapse whitespace.
   - remove bullet markers.
2. Exact normalized grouping.
3. Neu embedding matcher co san:
   - group phrases co similarity >= 0.86.

Khong nen group qua manh trong phase nay.

### 6.5 Canonical name strategy

Without GPT:

- Chon phrase xuat hien nhieu nhat.
- Title-case neu phrase tieng Anh.
- Giu phrase goc neu tieng Viet nhieu dau.

Vi du:

```text
carbon footprint analysis -> Carbon Footprint Analysis
phân tích phát thải carbon -> Phân Tích Phát Thải Carbon
```

Trong phase sau co GPT, co the improve canonical naming.

### 6.6 Alias strategy

Aliases gom:

- Tat ca phrases trong group.
- Deduped normalized.
- Gioi han so luong, vi du max 10 aliases.

### 6.7 Category strategy

Without GPT/ESCO import:

- Neu nearest existing skill similarity cao, lay category cua nearest skill.
- Neu khong, dung:

```text
"Uncategorized"
```

Hoac:

```text
"Pending Classification"
```

De xuat dung `Pending Classification` de Admin ro can duyet.

### 6.8 Nearest existing skills

Neu embedding matcher available:

- Encode suggested canonical phrase.
- Encode taxonomy skill names.
- Lay top 3 skill co similarity cao nhat.

Neu embedding unavailable:

- Dung token overlap nho hoac de list rong.

Output:

```json
[
  {"skill": "Data Analysis", "similarity": 0.71},
  {"skill": "Machine Learning", "similarity": 0.64}
]
```

## 7. Web/Admin boundary

Phase 15 Python chi tao suggestion queue.

Ben web sau nay se lam:

```text
Admin Taxonomy Suggestions
  -> xem pending suggestions
  -> approve as new skill
  -> add as alias to existing skill
  -> reject
  -> merge
  -> audit log
```

Khi Admin approve, web co the:

- Ghi vao DB custom taxonomy.
- Hoac export overlay JSON.
- Hoac tao PR/manual update vao `data/taxonomy/skills.json`.

Khong nen de Python auto sua taxonomy canonical file trong Phase 15.

## 8. Test plan

Them:

```text
tests/test_taxonomy_suggestion.py
```

Cases:

1. Collect observations tu `job.taxonomy_coverage.unknown_requirements`.
2. Collect evidence tu `candidate.open_set_requirement_matches`.
3. Deduplicate phrase variants.
4. Build suggestion khi frequency >= min_frequency.
5. Khong build suggestion neu frequency thap.
6. Aliases gom cac phrase trong group.
7. Status mac dinh la `pending_review`.
8. Nearest existing skills voi fake embedding.
9. Save/load suggestion queue JSON.
10. CLI suggestion command doc input JSON va tao output JSON.

Full regression:

```powershell
pytest
```

Manual test:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

## 9. Rui ro va giam thieu

### 9.1 Suggestion sai / skill khong phai skill

Risk:

```text
Requirement la soft-skill hoac general sentence bi de xuat thanh taxonomy skill.
```

Giam thieu:

- `min_frequency`.
- Status `pending_review`.
- Admin approve moi cap nhat taxonomy.
- Example contexts giup Admin doc lai.

### 9.2 Group sai phrase khac nghia

Risk:

```text
Embedding group hai phrase gan nhau nhung khac skill.
```

Giam thieu:

- Threshold group cao.
- Group exact normalized la default.
- Embedding grouping optional.
- Hien aliases/context cho Admin.

### 9.3 Over-engineering

Risk:

```text
Lam ca taxonomy management system qua lon.
```

Giam thieu:

- Phase 15 chi tao JSON suggestion queue.
- Web/Admin UI de phase sau.

### 9.4 Privacy

Risk:

```text
Example contexts co the chua thong tin nhay cam tu CV.
```

Giam thieu:

- Chi luu short snippets.
- Khong luu email/phone.
- Sau nay web co the mask PII.
- Output local, khong goi third-party.

## 10. Acceptance criteria

Phase 15 hoan thanh khi:

- Co module suggestion builder.
- Co the trich unknown requirements tu screening result.
- Co the tao pending taxonomy suggestions.
- Suggestions co:
  - suggested canonical name.
  - aliases.
  - frequency.
  - confidence.
  - nearest existing skills.
  - example contexts/evidence.
  - status `pending_review`.
- Co JSON save/load.
- Co CLI command rieng de tao suggestion queue tu result JSON.
- Tests pass bang fake embedding.
- Full `pytest` pass.
- Khong auto sua `data/taxonomy/skills.json`.

## 11. Ghi chu cho bao cao

Co the trinh bay:

```text
Sau khi he thong danh gia open-set requirements, cac requirement ngoai taxonomy duoc ghi nhan lai. Neu mot cum skill la xuat hien nhieu lan, he thong gom nhom cac bien the gan nghia, thong ke tan suat va de xuat cho Admin them vao taxonomy. Tuy nhien, he thong khong tu dong cap nhat taxonomy; Admin phai duyet de dam bao chat luong va tranh sai lech.
```

Day la human-in-the-loop design:

```text
AI proposes, human approves.
```

## 12. Sau khi code Phase 15

Da trien khai:

- Them `src/taxonomy_suggestion.py`.
- Them CLI rieng `taxonomy_suggest.py`.
- Them versioned suggestion queue JSON:

```json
{
  "version": 1,
  "suggestions": []
}
```

Module moi ho tro:

- `collect_unknown_requirement_observations`
- `collect_unknown_requirement_observations_from_results`
- `build_taxonomy_suggestions`
- `load_screening_results`
- `save_taxonomy_suggestions`
- `load_taxonomy_suggestions`

CLI moi:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Co the bat embedding optional cho grouping/nearest lookup:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

Giu dung boundary:

- Khong sua `/screening` API.
- Khong doi `main.py` arguments.
- Khong auto sua `data/taxonomy/skills.json`.
- Khong lam Admin UI trong Python phase nay.

Test da them:

```text
tests/test_taxonomy_suggestion.py
```

Manual check voi `JD_1`:

```text
python taxonomy_suggest.py --input-json outputs/phase15-ranking-results.json --output-json outputs/phase15-taxonomy-suggestions.json --min-frequency 1

Unknown observations: 7
Suggestions: 7
```

`--min-frequency 1` chi nen dung de demo nho. Mac dinh `min-frequency = 2` de tranh de xuat cac one-off/general requirements qua som.
