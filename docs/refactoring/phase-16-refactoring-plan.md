# Phase 16 Refactoring Plan - Admin Taxonomy Review and Merged Runtime Taxonomy

## 1. Muc tieu refactor

Them tang merge/validate taxonomy rieng de web/Admin co the dua cac skill da duyet quay lai vao AI screening ma khong sua taxonomy goc.

Nguyen tac:

- `data/taxonomy/skills.json` la base taxonomy, khong auto mutate.
- Custom taxonomy den tu Admin approval.
- Runtime AI chi dung mot file merged taxonomy moi nhat.
- Python cung cap validator/merge helper de giam logic lap lai ben web.

## 2. Module moi

### 2.1 `src/taxonomy_merge.py`

Trach nhiem:

- Load custom taxonomy overlay JSON.
- Validate overlay shape.
- Merge custom skills vao base taxonomy.
- Merge aliases vao skill co san.
- Dedupe aliases bang taxonomy lookup semantics.
- Reject ambiguous aliases.
- Atomic write merged taxonomy.

API chinh:

```python
load_custom_taxonomy_overlay(...)
merge_taxonomies(...)
save_merged_taxonomy(...)
build_taxonomy_merge_report(...)
```

### 2.2 `taxonomy_merge.py`

CLI rieng de web/Admin co the goi sau khi Admin approve suggestions.

Lenh:

```powershell
python taxonomy_merge.py --base data/taxonomy/skills.json --custom C:\topcv_ai_runtime\taxonomy\custom_taxonomy.json --output C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

## 3. Overlay contract

Web export approved custom taxonomy theo format:

```json
{
  "version": 1,
  "custom_skills": [],
  "alias_updates": []
}
```

`custom_skills` dung khi Admin approve skill moi.

`alias_updates` dung khi Admin gan alias moi vao skill da co.

## 4. Compatibility

Khong doi `/screening` API.

Khong doi `main.py` behavior.

CLI/API hien tai da co san co che dung merged taxonomy:

```powershell
python main.py --jd ... --cv-dir ... --taxonomy C:\topcv_ai_runtime\taxonomy\skills_merged.json
```

```json
{
  "taxonomy_path": "C:\\topcv_ai_runtime\\taxonomy\\skills_merged.json"
}
```

## 5. Test strategy

Them:

```text
tests/test_taxonomy_merge.py
```

Cover:

- Add custom skill.
- Add alias to base skill.
- Add alias to custom skill.
- Dedupe aliases.
- Reject existing canonical skill as custom skill.
- Reject missing alias target.
- Reject ambiguous aliases.
- Load overlay validation.
- Save/load merged taxonomy.
- CLI output.

## 6. Risk

### 6.1 Alias conflict

Vi du `Python` bi them lam alias cho skill khac.

Giam thieu:

- `build_alias_map` validate final merged taxonomy.
- CLI fail fast voi error ro rang.

### 6.2 Runtime file dang ghi bi AI doc

Giam thieu:

- Ghi temp file.
- Validate temp file.
- Replace sang file output.

### 6.3 Web export sai schema

Giam thieu:

- Co `docs/integration/sample-custom-taxonomy-overlay.json`.
- CLI validate va thong bao loi.

## 7. Sau Phase 16

Phase tiep theo nen la:

```text
Phase 17 - Web Integration Hardening and End-to-end Admin AI Flow
```

Muc tieu Phase 17:

- Test tu luong web tao suggestion.
- Admin approve.
- Export merged taxonomy.
- Web goi API/CLI voi `skills_merged.json`.
- Kiem tra ranking thay doi sau khi taxonomy duoc cap nhat.

