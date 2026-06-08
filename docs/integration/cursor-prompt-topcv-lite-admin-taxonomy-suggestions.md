# Cursor Prompt - Admin Taxonomy Suggestion Management for TOPCV Lite

Copy prompt duoi day vao Cursor trong project PHP:

```text
Ban dang lam trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

AI Python Phase 15 da tao duoc taxonomy suggestion queue bang CLI:

cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json

Task nay la them Admin UI trong TOPCV Lite de quan ly taxonomy suggestions:

- Import suggestion queue JSON.
- Hien danh sach suggestions.
- Admin approve/reject/merge/add-as-alias.
- Luu audit log.
- Luu custom taxonomy vao DB.
- Export merged taxonomy JSON de AI CLI/API co the dung.

Khong sua code AI Python trong task nay.
Khong auto sua file goc:

C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json

Web chi nen tao file merged taxonomy rieng, vi du:

C:\topcv_ai_runtime\taxonomy\skills_merged.json

Rat quan trong:

- Chi co MOT file merged taxonomy chinh: `skills_merged.json`.
- Khong tao 1 file moi cho moi skill.
- Moi lan Admin approve/reject/merge/add-alias, web luu decision vao DB.
- Khi can export, web rebuild lai `skills_merged.json` tu:
  1. base taxonomy `C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json`
  2. tat ca custom skills/aliases da duoc Admin approve trong DB
- Web ghi de `skills_merged.json` bang ban moi nhat.
- AI CLI/API chi doc `skills_merged.json`, khong doc dong thoi 2 file taxonomy.

## 1. Boi canh Phase 15

AI Python tao suggestion queue JSON dang:

```json
{
  "version": 1,
  "suggestions": [
    {
      "suggestion_id": "tax-sug-carbon-footprint-analysis",
      "suggested_canonical_name": "Carbon Footprint Analysis",
      "suggested_category": "Pending Classification",
      "suggested_aliases": [
        "carbon footprint analysis",
        "CO2 emission reporting"
      ],
      "frequency": 2,
      "confidence": 0.7,
      "nearest_existing_skills": [
        {
          "skill": "Data Analysis",
          "similarity": 0.71
        }
      ],
      "example_contexts": [
        "carbon footprint analysis"
      ],
      "example_evidence": [
        "Built carbon emission reports for ESG audits."
      ],
      "status": "pending_review"
    }
  ]
}
```

Admin workflow can hieu:

```text
AI proposes
Admin reviews
Web stores decision
Web rebuilds one latest skills_merged.json
AI uses that one merged taxonomy file in future screening
```

## 2. Viec dau tien: inspect project web

Hay inspect truoc:

- Admin login/session hien co.
- Folder admin hien co.
- Config DB hien co.
- Helper connect DB.
- CSRF pattern neu co.
- Flash message pattern neu co.
- UI table/button/modal style hien co.
- AI screening integration hien dang goi CLI hay API.

Search:

```text
admin
is_admin
role
csrf
flash
config
database
ai_screening
taxonomy
```

Khong tao style/UI qua khac voi project hien tai.

## 3. Database schema de xuat

Hay tao migration SQL hoac file docs SQL tuy theo cach project dang lam.

### 3.1 Bang suggestions

```sql
CREATE TABLE IF NOT EXISTS ai_taxonomy_suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    suggestion_id VARCHAR(191) NOT NULL UNIQUE,
    suggested_canonical_name VARCHAR(255) NOT NULL,
    suggested_category VARCHAR(255) NULL,
    suggested_aliases_json LONGTEXT NULL,
    frequency INT NOT NULL DEFAULT 0,
    confidence DECIMAL(5,4) NULL,
    nearest_existing_skills_json LONGTEXT NULL,
    example_contexts_json LONGTEXT NULL,
    example_evidence_json LONGTEXT NULL,
    raw_json LONGTEXT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending_review',
    decision_type VARCHAR(50) NULL,
    decision_note TEXT NULL,
    target_skill_name VARCHAR(255) NULL,
    reviewed_by INT NULL,
    reviewed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL
);
```

Status values:

```text
pending_review
approved_new_skill
approved_alias
merged
rejected
```

Decision type values:

```text
approve_new_skill
add_alias_to_existing
merge_to_existing
reject
```

### 3.2 Bang custom taxonomy skills

```sql
CREATE TABLE IF NOT EXISTS ai_custom_taxonomy_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL UNIQUE,
    category VARCHAR(255) NOT NULL DEFAULT 'Pending Classification',
    aliases_json LONGTEXT NULL,
    related_json LONGTEXT NULL,
    transferable_json LONGTEXT NULL,
    source_suggestion_id VARCHAR(191) NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_by INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL
);
```

### 3.3 Bang audit log

```sql
CREATE TABLE IF NOT EXISTS ai_taxonomy_audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    suggestion_id VARCHAR(191) NULL,
    action VARCHAR(100) NOT NULL,
    old_status VARCHAR(50) NULL,
    new_status VARCHAR(50) NULL,
    payload_json LONGTEXT NULL,
    admin_id INT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Neu project da co migration system, dung system do. Neu khong, tao file:

```text
docs/sql/ai_taxonomy_suggestions.sql
```

hoac:

```text
database/migrations/...
```

## 4. Config de xuat

Tao hoac them config:

```php
<?php

return [
    'base_taxonomy_path' => 'C:\\SEMANTIC_SKILLS_RESUME\\data\\taxonomy\\skills.json',
    'suggestion_queue_path' => 'C:\\SEMANTIC_SKILLS_RESUME\\outputs\\taxonomy_suggestions.json',
    'merged_taxonomy_path' => 'C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json',
];
```

Goi y file:

```text
config/ai_taxonomy.php
```

Khong cho user nhap arbitrary filesystem path tu request.

## 5. Admin pages de them

Tuy theo structure project, tao cac trang:

```text
admin/ai_taxonomy_suggestions.php
admin/ai_taxonomy_suggestion_import.php
admin/ai_taxonomy_suggestion_review.php
admin/ai_taxonomy_export.php
```

Neu project co router/action pattern, dung pattern hien co.

### 5.1 List page

`admin/ai_taxonomy_suggestions.php`

Can co:

- Filter status.
- Search by canonical name/alias.
- Sort by frequency/confidence/created_at.
- Columns:
  - Suggested skill.
  - Category.
  - Aliases.
  - Frequency.
  - Confidence.
  - Nearest existing skills.
  - Status.
  - Actions.
- Buttons:
  - Import suggestions JSON.
  - Export merged taxonomy.
  - View detail.

### 5.2 Import page/action

`admin/ai_taxonomy_suggestion_import.php`

Co 2 cach import:

1. Read configured path:

```text
C:\SEMANTIC_SKILLS_RESUME\outputs\taxonomy_suggestions.json
```

2. Upload JSON file from Admin.

For MVP, nen lam ca hai neu don gian; neu khong, lam read configured path truoc.

Import rules:

- Validate JSON co `version` va `suggestions`.
- Moi suggestion phai co `suggestion_id`, `suggested_canonical_name`.
- Upsert theo `suggestion_id`.
- Neu suggestion da reviewed, khong overwrite status/quyet dinh.
- Neu suggestion pending, co the update frequency/confidence/examples/raw_json.
- Ghi audit log action `import_suggestions`.

### 5.3 Detail/review page

`admin/ai_taxonomy_suggestion_review.php?id=...`

Hien:

- Suggested canonical name.
- Suggested category.
- Aliases.
- Frequency.
- Confidence.
- Nearest existing skills.
- Example contexts.
- Example evidence.
- Raw JSON collapse/debug.

Actions:

1. Approve as new skill.
2. Add aliases to existing skill.
3. Merge to existing custom skill.
4. Reject.

Forms can co CSRF neu project co.

## 6. Decision behavior

### 6.1 Approve as new skill

Admin co the sua truoc khi approve:

- Canonical skill name.
- Category.
- Aliases.
- Related skills optional.
- Transferable skills optional.

Khi approve:

- Insert/update `ai_custom_taxonomy_skills`.
- Update suggestion:
  - status = `approved_new_skill`
  - decision_type = `approve_new_skill`
  - target_skill_name = canonical skill name
  - reviewed_by
  - reviewed_at
- Ghi audit log.
- Export merged taxonomy JSON hoac hien nut de export.

### 6.2 Add aliases to existing skill

Admin chon existing skill tu:

- Base taxonomy skills.
- Custom taxonomy skills.

Khi approve alias:

- Neu target la custom skill: update aliases_json trong `ai_custom_taxonomy_skills`.
- Neu target la base taxonomy skill: khong sua file base. Tao custom overlay entry cung skill_name va aliases bo sung.
- Update suggestion:
  - status = `approved_alias`
  - decision_type = `add_alias_to_existing`
  - target_skill_name
- Ghi audit log.

### 6.3 Merge to existing custom skill

Tuong tu add alias, nhung status = `merged`.

### 6.4 Reject

Khi reject:

- Update status = `rejected`.
- Luu decision_note bat buoc hoac optional.
- Khong them vao custom taxonomy.
- Ghi audit log.

## 7. Export merged taxonomy JSON

Can tao helper:

```text
includes/ai_taxonomy_service.php
```

Ham de xuat:

```php
load_base_taxonomy(): array
load_custom_taxonomy_skills(): array
merge_taxonomy(array $base, array $custom): array
export_merged_taxonomy(): string
```

`skills_merged.json` la MOT file tong hop moi nhat, khong phai file moi cho tung skill.

Moi lan export, helper phai lam lai tu dau:

```text
base skills.json
  + all approved custom skills/aliases from DB
  = overwrite C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Khong append truc tiep vao file cu. Khong sua file base taxonomy.

Vi du theo thoi gian:

```text
Ban dau:
  base taxonomy co 100 skills
  skills_merged.json co 100 skills

Admin approve skill A:
  DB custom co A
  export lai skills_merged.json co 101 skills

Admin approve skill B:
  DB custom co A + B
  export lai skills_merged.json co 102 skills
```

AI van chi dung:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Merged taxonomy format phai dung format AI Python dang can:

```json
{
  "Java": {
    "aliases": ["java"],
    "category": "Programming Language",
    "related": [],
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

Rules:

- Base taxonomy loaded tu `base_taxonomy_path`.
- Custom skill moi duoc add vao object.
- Custom aliases cho base skill duoc merge vao aliases cua base skill.
- Deduplicate aliases case-insensitive/accent-insensitive neu co helper, neu khong case-insensitive la du.
- Moi skill object phai co:
  - aliases array
  - category string
  - related array
  - transferable array
- Tao parent dir neu chua co:

```text
C:\topcv_ai_runtime\taxonomy
```

- Ghi file UTF-8 JSON pretty print vao dung 1 file:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

- Nen ghi atomic de tranh file dang viet giua chung bi AI doc loi:
  1. Ghi vao `skills_merged.tmp.json`.
  2. Validate JSON vua ghi.
  3. Rename/replace sang `skills_merged.json`.
  4. Ghi audit log `export_merged_taxonomy`.

## 8. Cho AI CLI/API dung merged taxonomy

Sau khi export merged taxonomy:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

AI Python chi doc file nay nhu mot taxonomy hoan chinh. File nay da gom ca base taxonomy va custom taxonomy da duyet.

### 8.1 Neu web goi CLI

Trong command AI CLI, doi:

```text
--taxonomy C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json
```

thanh:

```text
--taxonomy C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Neu merged file chua ton tai, fallback ve base taxonomy path.

Khong truyen ca hai file. Chi truyen mot `--taxonomy` path.

### 8.2 Neu web goi API

Trong payload POST `/screening`, them:

```php
$payload['taxonomy_path'] = 'C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json';
```

Neu merged file chua ton tai, co the omit `taxonomy_path` de AI dung default.

Khong gui ca base taxonomy va merged taxonomy. Chi gui `taxonomy_path` cua merged file khi file da ton tai.

## 9. Security

Bat buoc:

- Chi Admin moi duoc vao cac trang nay.
- Validate CSRF cho action POST neu project co CSRF.
- Khong cho request truyen arbitrary file path.
- Khong expose raw stack trace.
- JSON import phai validate shape.
- Output merged taxonomy path phai nam trong path config.
- Escape HTML moi value hien ra UI.
- Audit log moi action approve/reject/import/export.

## 10. UX de xuat

Admin list nen co badge:

```text
Pending
Approved New Skill
Alias Added
Merged
Rejected
```

Mau sac nen theo style hien co cua TOPCV Lite.

Detail page nen co 4 sections:

```text
Suggestion
Evidence & Context
Nearest Existing Skills
Decision
```

Decision form:

- Radio/select action.
- Canonical name input.
- Category input/select.
- Aliases textarea, moi dong 1 alias.
- Target existing skill select for alias/merge.
- Note textarea.

## 11. Error handling

Xu ly:

- Suggestion JSON khong ton tai.
- JSON invalid.
- Missing `suggestions`.
- Suggestion thieu required fields.
- DB insert/update fail.
- Base taxonomy file khong ton tai.
- Merged taxonomy write fail.
- Permission denied.
- Duplicate skill name.

UI message than thien:

```text
Khong the import taxonomy suggestions. Vui long kiem tra file JSON hoac thu lai.
```

Log technical detail vao log cua project.

## 12. Testing checklist

1. Chay AI Python tao suggestion queue:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
python taxonomy_suggest.py --input-json outputs\ranking_results.json --output-json outputs\taxonomy_suggestions.json --min-frequency 1
```

2. Vao Admin page import suggestions.
3. Confirm DB co records trong `ai_taxonomy_suggestions`.
4. Open detail cua 1 suggestion.
5. Approve as new skill.
6. Confirm DB co record trong `ai_custom_taxonomy_skills`.
7. Export merged taxonomy.
8. Confirm file ton tai:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

9. Validate JSON co skill moi va dung fields:

```text
aliases, category, related, transferable
```

10. Approve them suggestion thu 2.
11. Export merged taxonomy lai.
12. Confirm van chi co file chinh:

```text
C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

Va file nay da co ca skill duyet lan 1 + skill duyet lan 2.

Khong duoc tao file kieu:

```text
skills_merged_skill_a.json
skills_merged_skill_b.json
skills_merged_1.json
skills_merged_2.json
```

Neu co backup thi backup nam trong folder `backups`, nhung AI van chi dung file chinh `skills_merged.json`.

13. Chay AI screening lai voi merged taxonomy:

CLI:

```powershell
python main.py --jd data/jobs/JD_1.txt --cv-dir data/cvs --taxonomy C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

API:

```json
{
  "taxonomy_path": "C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json",
  "job": {},
  "candidates": []
}
```

## 13. Acceptance criteria

Hoan thanh khi:

- Admin co the import suggestion queue JSON.
- Admin xem duoc danh sach pending suggestions.
- Admin xem detail suggestion voi aliases, frequency, confidence, examples, nearest skills.
- Admin approve new skill.
- Admin add aliases to existing skill.
- Admin reject suggestion.
- Moi action co audit log.
- Custom taxonomy luu DB.
- Export duoc merged taxonomy JSON dung schema AI Python.
- Moi lan export ghi de/rebuild 1 file `skills_merged.json` moi nhat.
- Khong tao mot merged file rieng cho tung skill.
- Web AI screening co the dung merged taxonomy path.
- Khong sua file base taxonomy cua AI Python.

Sau khi lam xong, bao lai:

- File PHP nao da them/sua.
- SQL migration/schema da tao.
- Admin URL de test.
- Merged taxonomy path.
- Cach web AI screening dang dung taxonomy path moi.
```
