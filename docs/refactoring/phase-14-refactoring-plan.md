# Phase 14 Refactoring Plan - Open-set Requirement Matching

## 1. Muc tieu refactor

Them kha nang xu ly JD requirement ngoai taxonomy ma khong lam roi pipeline hien co.

Nguyen tac:

- Taxonomy/rule-based matching van la backbone.
- Unknown requirement di qua module rieng.
- Semantic-only match co metadata ro va score gioi han.
- Khong auto cap nhat taxonomy trong Phase 14.

## 2. Thay doi module

### 2.1 Them `src/open_set_matcher.py`

Trach nhiem:

- `split_known_and_unknown_requirements`
- `build_taxonomy_coverage`
- `find_semantic_requirement_evidence`

Module nay khong doc file, khong cham final score truc tiep, va khong sua taxonomy.

### 2.2 Mo rong `src/evidence_detector.py`

Expose helper:

- `collect_evidence_candidates`
- `calculate_candidate_evidence_level`

Ly do:

- Open-set matcher can tai su dung evidence candidate va evidence-level logic hien co.
- Tranh duplicate logic collect work/projects/summary/skills.

### 2.3 Cap nhat pipelines

Cap nhat:

- `src/screening_pipeline.py`
- `src/payload_pipeline.py`

Flow moi:

```text
parse JD
build known taxonomy skills
split unknown requirements
build taxonomy coverage
process each candidate
append semantic-only matches when embedding returns evidence
score candidate
```

### 2.4 Cap nhat review card

`src/review_card_generator.py` them concern khi co:

```text
match_type = semantic_only_match
```

De recruiter biet day la evidence ngoai taxonomy, can doc bang chung.

### 2.5 Cap nhat scorer

`src/scorer.py` tinh `no_semantic_evidence` nhu missing requirement khi no duoc dua vao scored matches.

## 3. API/CLI compatibility

Khong them required input moi.

Output co field moi:

```text
job.taxonomy_coverage
candidate.open_set_requirement_matches
```

Existing fields van giu:

```text
final_score
recommendation
matched_skills
missing_skills
review_card
```

Web cu doc cac field tren van chay. Web moi co the hien them taxonomy coverage.

## 4. Test strategy

Them:

- `tests/test_open_set_matcher.py`

Cap nhat:

- `tests/test_screening_pipeline.py`
- `tests/test_payload_pipeline.py`
- `tests/test_review_card_generator.py`

Khong dung model that trong tests. Fake embedding model phai cover:

- semantic-only match du threshold.
- no semantic evidence duoi threshold.
- embedding disabled.

## 5. Risk

### 5.1 False positive semantic match

Giam thieu:

- threshold open-set cao hon semantic skill matching.
- score cap `0.65`.
- evidence text bat buoc hien trong output.
- `taxonomy_status = unknown`.

### 5.2 Score thay doi qua manh

Giam thieu:

- Unknown requirement chi scoring khi embedding matcher that su tra similarity matrix.
- Khi embedding disabled/unavailable, unknown requirement chi report trong coverage.

### 5.3 Requirement qua dai

Giam thieu:

- Loc unknown requirement qua dai.
- Phase sau co the tach clauses/LLM-assisted extraction neu can.

## 6. Sau Phase 14

Phase 15 nen them:

```text
Human-in-the-loop Taxonomy Suggestion
```

AI Python:

- gom nhom unknown requirements.
- tinh tan suat.
- tim nearest existing taxonomy skills.
- tao suggestion object.

Web/Admin:

- hien pending suggestions.
- approve/reject/merge.
- ghi audit log.

