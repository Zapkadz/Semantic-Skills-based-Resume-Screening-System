# Phase 16 - Admin Taxonomy Review and Merged Taxonomy Integration

## 1. Muc tieu phase

Phase 16 noi tiep Phase 15 de bien taxonomy suggestions thanh mot luong cap nhat taxonomy co kiem soat.

Huong tong the:

```text
Phase 15:
AI detects unknown requirements
  -> groups repeated phrases
  -> creates pending taxonomy suggestions

Phase 16:
Admin reviews suggestions
  -> approves/rejects/merges/adds aliases
  -> approved custom taxonomy is exported
  -> Python validates and merges taxonomy
  -> AI screening uses one latest skills_merged.json
```

Muc tieu quan trong:

- Khong sua truc tiep file taxonomy goc `data/taxonomy/skills.json`.
- Khong tao mot file merged rieng cho tung skill.
- Chi co mot file taxonomy runtime moi nhat, vi du:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

- AI CLI/API chi doc mot file taxonomy hoan chinh qua `--taxonomy` hoac `taxonomy_path`.
- Admin/web la noi quyet dinh approve/reject; Python chi ho tro validate/merge/export an toan.

## 2. Boi canh truoc Phase 16

Hien tai da co:

- Base taxonomy:

```text
data/taxonomy/skills.json
```

- CLI da ho tro taxonomy tuy chon:

```powershell
python main.py --jd data/jobs/JD_1.txt --cv-dir data/cvs --taxonomy C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

- API payload da ho tro:

```json
{
  "taxonomy_path": "C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json",
  "job": {},
  "candidates": []
}
```

- Phase 15 da tao suggestion queue:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Nhung con thieu:

- Chua co helper Python de merge base taxonomy voi custom taxonomy.
- Chua co validator rieng de web/Admin kiem tra merged taxonomy truoc khi AI dung.
- Chua co CLI rieng de tao `skills_merged.json` tu base + custom overlay.
- Chua co test bao ve cac case nguy hiem nhu duplicate aliases, missing fields, overwrite sai base taxonomy.

## 3. Ranh gioi trach nhiem voi web PHP

Phase 16 trong AI Python project khong lam Admin UI.

Ben web PHP/Cursor se lam:

- Trang Admin xem suggestions.
- Approve new skill.
- Add alias to existing skill.
- Merge suggestion vao skill co san.
- Reject suggestion.
- Luu DB va audit log.
- Goi hoac dung output cua Python helper de export merged taxonomy.

Ben AI Python project se lam:

- Dinh nghia format custom taxonomy overlay de web co the export.
- Validate base taxonomy va custom overlay.
- Merge custom skills/aliases vao base taxonomy.
- Ghi ra mot file merged taxonomy JSON hop le.
- Cung cap CLI de web co the goi neu muon.
- Cap nhat docs cho Cursor/web tich hop dung luong.

Nguyen tac:

```text
AI proposes, Admin approves, Python validates, AI reuses.
```

## 4. Format custom taxonomy overlay de xuat

Web co the export mot file custom overlay, vi du:

```text
C:\topcv_ai_runtime\taxonomy\custom_taxonomy.json
```

Format:

```json
{
  "version": 1,
  "custom_skills": [
    {
      "skill_name": "Carbon Footprint Analysis",
      "category": "Sustainability / ESG",
      "aliases": [
        "carbon footprint analysis",
        "CO2 emission reporting",
        "carbon accounting"
      ],
      "related": [],
      "transferable": [],
      "source": "admin_approved",
      "source_suggestion_id": "tax-sug-carbon-footprint-analysis"
    }
  ],
  "alias_updates": [
    {
      "target_skill_name": "Face Recognition",
      "aliases": [
        "nhan dien khuon mat",
        "face verification"
      ],
      "source": "admin_approved",
      "source_suggestion_id": "tax-sug-face-verification"
    }
  ]
}
```

Giai thich:

- `custom_skills`: skill moi duoc Admin approve.
- `alias_updates`: alias moi duoc Admin approve cho skill da co.
- `source_suggestion_id`: giup trace ve suggestion ban dau.
- `source`: giup bao cao/audit.

File merged output van giu dung schema AI dang doc:

```json
{
  "Java": {
    "aliases": ["Core Java", "Java SE"],
    "category": "Programming Language",
    "related": ["Spring Boot"],
    "transferable": []
  },
  "Carbon Footprint Analysis": {
    "aliases": ["carbon footprint analysis", "CO2 emission reporting"],
    "category": "Sustainability / ESG",
    "related": [],
    "transferable": []
  }
}
```

## 5. Pham vi thuc hien

Trong Phase 16 se lam:

- Them module merge/validate taxonomy overlay.
- Them CLI rieng de export merged taxonomy.
- Them atomic write de tranh AI doc file dang ghi do.
- Them tests cho merge, alias update, conflict, invalid overlay.
- Cap nhat docs integration cho Cursor/web Admin.
- Cap nhat README/dev log/refactoring plan.

Ngoai scope Phase 16:

- Khong lam UI Admin PHP trong repo Python.
- Khong tao DB migration PHP.
- Khong goi GPT.
- Khong import full ESCO/O*NET.
- Khong auto approve suggestions.
- Khong sua base taxonomy `data/taxonomy/skills.json`.

## 6. Kien truc de xuat

### 6.1 Module moi

Co the tao:

```text
src/taxonomy_merge.py
```

Trach nhiem:

- Validate custom overlay shape.
- Normalize/dedupe aliases.
- Merge custom skills vao base taxonomy.
- Merge alias updates vao skill ton tai.
- Reject ambiguous aliases.
- Export merged taxonomy JSON.

Ham de xuat:

```python
def load_custom_taxonomy_overlay(path: str | Path) -> dict:
    ...

def merge_taxonomies(
    base_taxonomy: dict[str, dict],
    custom_overlay: dict,
) -> dict[str, dict]:
    ...

def save_merged_taxonomy(
    taxonomy: dict[str, dict],
    output_path: str | Path,
) -> str:
    ...

def build_taxonomy_merge_report(
    base_taxonomy: dict[str, dict],
    custom_overlay: dict,
    merged_taxonomy: dict[str, dict],
) -> dict:
    ...
```

### 6.2 CLI moi

Co the tao:

```text
taxonomy_merge.py
```

Lenh:

```powershell
python taxonomy_merge.py ^
  --base data/taxonomy/skills.json ^
  --custom C:\topcv_ai_runtime\taxonomy\custom_taxonomy.json ^
  --output C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Output terminal vi du:

```text
Base skills: 120
Custom skills added: 2
Alias updates applied: 5
Merged skills: 122
Output: C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

### 6.3 Atomic write

Khi ghi merged taxonomy:

```text
skills_merged.tmp.json
  -> validate JSON/schema
  -> replace skills_merged.json
```

Ly do:

- Web co the dang export.
- API/CLI co the dang doc taxonomy.
- Tranh truong hop AI doc trung file JSON chua ghi xong.

### 6.4 Validation rules

Base taxonomy va merged taxonomy phai dung schema:

```text
aliases: list
category: string
related: list
transferable: list
```

Custom overlay rules:

- `version` phai la number/int.
- `custom_skills` neu co phai la list.
- `alias_updates` neu co phai la list.
- `skill_name` / `target_skill_name` phai non-empty string.
- `aliases` phai la list string.
- Custom skill moi khong duoc trung canonical skill cua base, tru khi logic la alias update.
- Alias khong duoc map sang hai canonical skills khac nhau.
- Related/transferable neu thieu thi mac dinh `[]`.
- Category neu thieu thi mac dinh `Pending Classification`.

## 7. Luong tich hop voi web

### 7.1 Cach 1 - Web tu export merged taxonomy

Web:

```text
DB approved custom taxonomy
  -> web builds skills_merged.json
```

Python Phase 16 van huu ich vi co CLI validate:

```powershell
python taxonomy_merge.py --base ... --custom ... --output ...
```

Hoac web chi can goi validation truoc khi luu file runtime.

### 7.2 Cach 2 - Web export custom overlay, Python merge

Web:

```text
DB approved custom taxonomy
  -> custom_taxonomy.json
  -> call python taxonomy_merge.py
  -> skills_merged.json
```

Day la cach de xuat cho MVP vi:

- Web khong can duplicate qua nhieu logic merge.
- Python dung chung validator voi AI.
- De test va bao ve do an hon.

### 7.3 Sau khi co skills_merged.json

Neu web goi CLI:

```powershell
python main.py --jd ... --cv-dir ... --taxonomy C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Neu web goi API:

```json
{
  "taxonomy_path": "C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json"
}
```

Neu file merged chua ton tai:

- Fallback ve base taxonomy.
- Hien warning/log cho Admin.

## 8. Test plan

Them:

```text
tests/test_taxonomy_merge.py
```

Cases:

1. Merge custom skill moi vao base taxonomy.
2. Add alias vao existing base skill.
3. Add alias vao existing custom skill.
4. Deduplicate aliases case-insensitive.
5. Reject custom overlay invalid JSON/shape.
6. Reject alias conflict map sang hai skills khac nhau.
7. Reject custom skill canonical name empty.
8. Default missing category thanh `Pending Classification`.
9. Default missing related/transferable thanh `[]`.
10. Save merged taxonomy va load lai bang `load_taxonomy`.
11. CLI tao output file hop le.
12. CLI report dung so luong custom skills/alias updates.

Full regression:

```powershell
pytest
```

Manual test:

```powershell
python taxonomy_merge.py --base data/taxonomy/skills.json --custom docs/integration/sample-custom-taxonomy-overlay.json --output outputs/skills_merged.json
python main.py --jd data/jobs/JD_1.txt --cv-dir data/cvs --taxonomy outputs/skills_merged.json
```

## 9. Rui ro va giam thieu

### 9.1 Admin approve sai skill

Risk:

```text
Skill moi khong phai skill that hoac alias bi sai nghia.
```

Giam thieu:

- Admin review bat buoc.
- Audit log ben web.
- Python chi validate structure/conflict, khong auto approve.

### 9.2 Alias conflict

Risk:

```text
"JS" vua la JavaScript vua la Job Scheduler.
```

Giam thieu:

- Dung `build_alias_map` de reject ambiguous aliases.
- Fail fast khi export merged taxonomy.

### 9.3 Ghi file merged bi loi giua chung

Risk:

```text
API doc taxonomy khi web dang ghi file.
```

Giam thieu:

- Atomic write bang temp file + replace.
- Validate merged JSON truoc khi replace.

### 9.4 Web va Python khac schema

Risk:

```text
Web export custom taxonomy sai format lam AI loi.
```

Giam thieu:

- Co sample overlay JSON.
- Co CLI validate/merge.
- Cap nhat Cursor prompt voi exact format.

## 10. Acceptance criteria

Phase 16 hoan thanh khi:

- Co module Python de merge base taxonomy + custom overlay.
- Co CLI `taxonomy_merge.py`.
- CLI tao duoc mot file `skills_merged.json` dung schema AI.
- Merged taxonomy load duoc bang `load_taxonomy`.
- Alias conflicts bi reject ro rang.
- Custom skills/aliases duoc dedupe.
- Base taxonomy khong bi sua.
- Co sample custom overlay JSON cho Cursor/web.
- Docs integration Admin taxonomy duoc cap nhat.
- Full `pytest` pass.

## 11. Ghi chu cho bao cao

Co the trinh bay:

```text
He thong su dung taxonomy nen tang de dam bao kha nang giai thich. Tuy nhien,
taxonomy khong the bao phu toan bo ky nang/nganh nghe ngay tu dau. Vi vay,
he thong thiet ke co che human-in-the-loop: AI phat hien va de xuat skill moi,
Admin duyet, sau do cac skill da duyet duoc ghi vao custom taxonomy va merge
thanh mot runtime taxonomy. File runtime nay duoc AI su dung trong cac lan
sang loc tiep theo, trong khi taxonomy goc van duoc giu nguyen de dam bao
kiem soat phien ban va kha nang truy vet.
```

Tom tat:

```text
Base taxonomy + Admin-approved custom taxonomy = Merged runtime taxonomy.
```

## 12. Sau khi code Phase 16

Da trien khai:

- Them `src/taxonomy_merge.py`.
- Them CLI rieng `taxonomy_merge.py`.
- Them sample overlay:

```text
docs/integration/sample-custom-taxonomy-overlay.json
```

- Them tests:

```text
tests/test_taxonomy_merge.py
```

Module moi ho tro:

- `load_custom_taxonomy_overlay`
- `merge_taxonomies`
- `save_merged_taxonomy`
- `build_taxonomy_merge_report`

CLI moi:

```powershell
python taxonomy_merge.py --base data/taxonomy/skills.json --custom docs/integration/sample-custom-taxonomy-overlay.json --output outputs/skills_merged.json
```

Output CLI gom:

- Base skills.
- Custom skills added.
- Alias updates applied.
- Merged skills.
- Output path.

Giu dung boundary:

- Khong sua `/screening` API.
- Khong doi `main.py` arguments.
- Khong auto sua `data/taxonomy/skills.json`.
- Khong lam Admin UI trong Python repo.

Manual check de xuat:

```powershell
python taxonomy_merge.py --base data/taxonomy/skills.json --custom docs/integration/sample-custom-taxonomy-overlay.json --output outputs/skills_merged.json
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --taxonomy outputs/skills_merged.json
```
