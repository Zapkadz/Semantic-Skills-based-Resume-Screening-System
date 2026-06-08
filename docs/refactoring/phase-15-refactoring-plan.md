# Phase 15 Refactoring Plan - Taxonomy Suggestion Queue

## 1. Muc tieu refactor

Them kha nang tao pending taxonomy suggestions tu unknown requirements ma khong lam thay doi pipeline screening hien tai.

Nguyen tac:

- Khong auto sua `data/taxonomy/skills.json`.
- Khong gan trach nhiem Admin UI cho Python core.
- Suggestion queue la JSON artifact doc/lap, de web/Admin xu ly sau.
- Tests khong download embedding model that.

## 2. Module moi

### 2.1 `src/taxonomy_suggestion.py`

Trach nhiem:

- Collect unknown requirement observations tu screening result.
- Merge evidence tu `open_set_requirement_matches`.
- Group exact/semantic-similar phrases.
- Build pending suggestion objects.
- Save/load versioned suggestion queue JSON.

API chinh:

```python
collect_unknown_requirement_observations(...)
collect_unknown_requirement_observations_from_results(...)
build_taxonomy_suggestions(...)
load_screening_results(...)
save_taxonomy_suggestions(...)
load_taxonomy_suggestions(...)
```

### 2.2 `taxonomy_suggest.py`

CLI rieng de tranh lam phuc tap `main.py`.

Lenh:

```powershell
python taxonomy_suggest.py --input-json outputs/ranking_results.json --output-json outputs/taxonomy_suggestions.json
```

Ho tro:

- Nhieu input JSON.
- `--min-frequency`.
- Optional embedding grouping/nearest lookup.
- Local-only embedding mode.

## 3. Output contract

Suggestion queue:

```json
{
  "version": 1,
  "suggestions": [
    {
      "suggestion_id": "tax-sug-carbon-footprint-analysis",
      "suggested_canonical_name": "Carbon Footprint Analysis",
      "suggested_category": "Pending Classification",
      "suggested_aliases": ["carbon footprint analysis"],
      "frequency": 2,
      "confidence": 0.7,
      "nearest_existing_skills": [],
      "example_contexts": [],
      "example_evidence": [],
      "status": "pending_review"
    }
  ]
}
```

## 4. Compatibility

Khong doi API `/screening`.

Khong doi `main.py` command arguments.

Chi them:

- Module moi.
- CLI moi.
- Docs/tests.

## 5. Test strategy

Them:

```text
tests/test_taxonomy_suggestion.py
```

Cover:

- Observation collection.
- Evidence merge.
- Min frequency.
- Pending suggestion shape.
- Embedding grouping voi fake model.
- Nearest existing skills voi fake model.
- Save/load JSON.
- CLI output.

## 6. Risk

### 6.1 Suggestion khong phai skill

Giam thieu:

- `min_frequency`.
- `status = pending_review`.
- Example context/evidence.
- Admin approve moi cap nhat taxonomy.

### 6.2 Group sai

Giam thieu:

- Exact grouping la default.
- Embedding grouping optional.
- Group threshold cao.

### 6.3 Privacy

Giam thieu:

- Chi luu short evidence/context tu screening result.
- Khong luu email/phone.
- Khong goi third-party.

## 7. Sau Phase 15

Phase sau nen lam:

```text
Admin Taxonomy Suggestion Review
```

Web/Admin se doc suggestion queue hoac DB table va cho phep:

- Approve as new skill.
- Add as alias.
- Merge.
- Reject.
- Audit log.

