# Phase 10 - CLI Pipeline and Output

## 1. Muc tieu phase

Phase 10 ket noi cac module da hoan thanh thanh mot CLI pipeline chay duoc that.

Sau Phase 09, du an da co cac module rieng:

- Document Loader
- Resume Parser
- JD Parser
- Skill Taxonomy
- Skill Normalizer
- Skill Matcher
- Evidence Detector
- Scorer and Ranking
- Review Card Generator

Muc tieu Phase 10 la cho nguoi dung chay mot lenh CLI:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Va nhan duoc ranking + review cards.

## 2. Van de phase nay giai quyet

Hien tai cac module da duoc test rieng, nhung chua co luong xu ly dau-cuoi trong `main.py`. Nguoi dung phai dung lenh `python -c` rat dai de test demo.

Phase 10 giai quyet bai toan:

```text
JD path + CV directory
  -> load JD
  -> parse JD
  -> load CV files
  -> parse each CV
  -> normalize skills
  -> match must-have and nice-to-have skills
  -> detect evidence
  -> score candidates
  -> rank candidates
  -> generate review cards
  -> print summary
  -> optionally save JSON/Markdown outputs
```

## 3. Vi sao phase nay quan trong voi do an

Du an can mot cach chay demo gon va chuyen nghiep. CLI pipeline giup:

- Chung minh cac module co the lam viec cung nhau.
- Giam viec test thu cong bang command dai.
- Tao output co the nop bao cao/demo.
- Tao nen tang cho Streamlit UI sau nay.
- Giu business logic trong module pipeline, khong hard-code trong `main.py`.

## 4. Pham vi thuc hien

Trong Phase 10 se lam:

- Cap nhat `main.py` de nhan tham so CLI:
  - `--jd`
  - `--cv-dir`
  - `--taxonomy`
  - `--output-json`
  - `--output-dir`
  - `--show-review-cards`
- Tao module pipeline, du kien `src/screening_pipeline.py`.
- Implement `run_screening_pipeline(...) -> dict`.
- Implement xu ly mot JD va nhieu CV `.txt`.
- Rank candidates bang `rank_candidates`.
- Generate review card cho tung candidate.
- In ranking summary ra terminal.
- Save JSON output neu user truyen `--output-json`.
- Save Markdown review cards neu user truyen `--output-dir`.
- Them tests cho pipeline.
- Them tests cho CLI parser/main behavior.
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong tao Streamlit UI.
- Khong support PDF/DOCX.
- Khong thay doi scoring formula.
- Khong thay doi matching/evidence rules.
- Khong dung LLM.
- Khong tao database.
- Khong upload file qua web.
- Khong tao PR automation.
- Khong merge branch vao main.

## 6. Module lien quan

Module chinh du kien tao:

- `src/screening_pipeline.py`

Module se cap nhat:

- `main.py`

Module input tu phase truoc:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`
- `src/semantic_matcher.py`
- `src/evidence_detector.py`
- `src/scorer.py`
- `src/review_card_generator.py`

Tests:

- `tests/test_screening_pipeline.py`
- Co the cap nhat hoac them `tests/test_main.py`

## 7. File du kien tao moi

- `src/screening_pipeline.py`
- `tests/test_screening_pipeline.py`
- `docs/phases/phase-10-cli-pipeline-output.md`
- `docs/refactoring/phase-10-refactoring-plan.md` sau khi code xong

Co the tao them neu can:

- `tests/test_main.py`

## 8. File du kien chinh sua

- `main.py`
- `README.md`
- `docs/dev-learning-log.md`

Tam thoi khong chinh sua:

- `src/scorer.py`
- `src/review_card_generator.py`
- `src/evidence_detector.py`
- Parser modules, tru khi tests phat hien bug that.
- `app.py`
- Taxonomy JSON.

## 9. CLI interface de xuat

Lenh mac dinh:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Lenh co save JSON:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

Lenh co save review cards Markdown:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-dir outputs/reports
```

Lenh in review cards ra terminal:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --show-review-cards
```

Tham so:

```text
--jd             Required. Path toi JD .txt.
--cv-dir         Required. Path toi folder chua CV .txt.
--taxonomy       Optional. Default data/taxonomy/skills.json.
--output-json    Optional. Path de save ranking JSON.
--output-dir     Optional. Folder de save Markdown review cards.
--show-review-cards Optional flag de in review cards ra terminal.
```

## 10. Output terminal de xuat

Khi chay lenh mac dinh:

```text
Semantic Skills-based Resume Screening System
Phase 10 - CLI Pipeline and Output

Job: Backend Java Developer
Candidates analyzed: 1

Ranking:
1. Nguyen Van A - 87/100 - Strong Review
```

Neu dung `--show-review-cards`, in them Markdown review card sau ranking.

## 11. Output JSON de xuat

Neu user truyen `--output-json`, file JSON nen co schema:

```python
{
    "job": {
        "title": "Backend Java Developer",
        "must_have_skills": [...],
        "nice_to_have_skills": [...]
    },
    "candidates": [
        {
            "rank": 1,
            "candidate_name": "Nguyen Van A",
            "final_score": 87,
            "recommendation": "Strong Review",
            "scores": {...},
            "matched_skills": [...],
            "missing_skills": [...],
            "review_card": {...}
        }
    ]
}
```

Generated output files nam trong `outputs/` va da duoc `.gitignore`, nen khong commit runtime result.

## 12. Pipeline API de xuat

`src/screening_pipeline.py` nen co public API:

```python
def run_screening_pipeline(
    jd_path: str,
    cv_dir: str,
    taxonomy_path: str = "data/taxonomy/skills.json",
) -> dict:
    pass
```

Co the them:

```python
def save_pipeline_result_json(result: dict, output_path: str) -> None:
    pass

def save_review_cards(result: dict, output_dir: str) -> list[str]:
    pass
```

`main.py` se chi lam:

1. Parse args.
2. Goi pipeline.
3. Print summary.
4. Save output neu co args.

## 13. Learning Plan

### 13.1 Toi can hoc gi trong phase nay?

Can hoc:

- CLI khac module logic nhu the nao.
- Cach viet pipeline orchestration ma khong tron logic tung module.
- Cach luu JSON output co schema on dinh.
- Cach test CLI/pipeline ma khong phu thuoc terminal.
- Cach tranh commit runtime output.

### 13.2 Cac khai niem ky thuat can hieu

- Orchestration: noi cac module thanh luong xu ly.
- CLI arguments: nhan input tu command line.
- Structured output: JSON co schema ro rang.
- Markdown report: format review card de doc.
- Side effects: print terminal va write file nen duoc tach khoi core logic khi co the.

### 13.3 Nguyen tac thiet ke

- `screening_pipeline.py` chua flow nghiep vu.
- `main.py` chua CLI adapter.
- Output dict phai test duoc.
- Print output nen ngan gon, khong day toan bo JSON ra terminal mac dinh.
- Save output chi lam khi user truyen flag.
- Error message nen ro rang khi JD path/CV dir/taxonomy sai.

## 14. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/10-cli-pipeline-output`.
2. Tao `src/screening_pipeline.py`.
3. Implement helper process mot CV.
4. Implement `run_screening_pipeline`.
5. Implement ranking va review card generation trong pipeline.
6. Implement save JSON.
7. Implement save Markdown review cards.
8. Cap nhat `main.py` CLI parser.
9. Implement terminal summary output.
10. Them `tests/test_screening_pipeline.py`.
11. Them/cap nhat tests cho `main.py` neu can.
12. Chay `pytest`.
13. Test thu cong lenh CLI mac dinh.
14. Test thu cong save JSON/output dir.
15. Cap nhat README.
16. Cap nhat `docs/dev-learning-log.md`.
17. Tao `docs/refactoring/phase-10-refactoring-plan.md`.
18. Dung lai cho ban test va xac nhan.

## 15. Cach test phase

Test tu dong:

```bash
pytest
```

Test CLI mac dinh:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Test save JSON:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-json outputs/ranking_results.json
```

Test save review cards:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --output-dir outputs/reports
```

Test in review cards:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --show-review-cards
```

## 16. Tieu chi hoan thanh phase

Phase 10 hoan thanh khi:

- Co `src/screening_pipeline.py`.
- `main.py` nhan `--jd` va `--cv-dir`.
- CLI chay duoc demo JD/CV.
- Terminal in ranking summary.
- Co option save JSON.
- Co option save Markdown review cards.
- Co option show review cards.
- Co tests tu dong.
- `pytest` pass.
- README duoc cap nhat.
- Learning log duoc cap nhat.
- Refactoring plan Phase 10 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 17. Rui ro

- `main.py` bi phinh to neu dua het logic vao CLI file.
- Runtime output co the lam dirty git neu khong nam trong `.gitignore`.
- JSON output qua lon neu include full evidence voi nhieu CV.
- CLI error handling co the kho doc neu exception raw bi in thang.
- Pipeline co the bi test kho neu print/write file tron voi core logic.

## 18. Ghi chu cho bao cao

CLI Pipeline and Output la buoc tich hop cac module cua he thong thanh mot ung dung co the chay dau-cuoi. Phase nay chung minh flow tu JD va nhieu CV den ranking, scoring va review card. Viec tach pipeline khoi `main.py` giup he thong de test, de mo rong sang Streamlit UI va de bao tri theo phong cach chuyen nghiep.
