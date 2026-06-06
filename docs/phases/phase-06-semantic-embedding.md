# Phase 06 - Semantic Matching with Embeddings

## 1. Muc tieu phase

Phase 06 them kha nang semantic matching dua tren sentence embeddings de bo sung cho rule-based skill matching da co o Phase 05.

Muc tieu:

- Them semantic similarity cho truong hop rule-based matcher chua tim duoc match tot.
- Giu rule-based exact/related/transferable matching la baseline chinh.
- Them fallback ro rang neu embedding dependency hoac model khong kha dung.
- Khong de embedding tu quyet dinh final score/ranking.
- Them tests cho semantic matcher fallback va threshold logic.

Phase nay can lam than trong vi co the lien quan dependency nang nhu `sentence-transformers`.

## 2. Van de phase nay giai quyet

Rule-based matcher phu thuoc vao taxonomy. Neu taxonomy chua co du related/transferable skills, he thong co the bo sot mot so match gan nghia.

Vi du:

```text
JD: Backend API development
CV: Built RESTful services with Spring Boot
```

Neu taxonomy khong co dung relation, semantic similarity co the giup phat hien hai mo ta nay gan nhau ve nghia.

## 3. Vi sao phase nay quan trong voi do an

Semantic matching giup du an the hien yeu to AI/NLP ro hon, nhung van giu tinh minh bach bang rule-based score va fallback.

Trong bao cao, phase nay co the giai thich:

- Du an khong train model tu dau.
- Du an dung pretrained embedding model de bieu dien text/skill thanh vector.
- Cosine similarity dung de do muc do gan nghia.
- Rule-based matching van la baseline va co the chay khi model khong kha dung.

## 4. Pham vi thuc hien

Trong Phase 06 se lam neu ban duyet:

- Cap nhat `requirements.txt` voi dependency can thiet neu quyet dinh dung embedding.
- Tao module optional, vi du `src/embedding_matcher.py` hoac mo rong `src/semantic_matcher.py` co kiem soat.
- Implement wrapper load embedding model co fallback.
- Implement `calculate_semantic_similarity(text_a, text_b)`.
- Implement semantic match chi khi rule-based result la `no_match`.
- Them `semantic_match` voi score de xuat `0.85`.
- Them threshold ro rang, vi du `0.70` hoac `0.75`.
- Them tests co the mock embedding de khong phu thuoc model download.
- Cap nhat README va learning log.
- Tao refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong train model tu dau.
- Khong fine-tune model.
- Khong goi API tra phi.
- Khong dung LLM de cham diem.
- Khong thay final scoring weights.
- Khong evidence detection.
- Khong ranking/recommendation label.
- Khong bat buoc app phai co internet moi chay duoc.
- Khong xoa rule-based matching da co.

## 6. Module lien quan

Module chinh co the tao:

- `src/embedding_matcher.py`

Module co the chinh sua co kiem soat:

- `src/semantic_matcher.py`
- `requirements.txt`

Module input tu phase truoc:

- `src/document_loader.py`
- `src/resume_parser.py`
- `src/jd_parser.py`
- `src/skill_taxonomy.py`
- `src/skill_normalizer.py`

Tests:

- `tests/test_embedding_matcher.py`
- Co the cap nhat `tests/test_semantic_matcher.py` neu semantic match duoc tich hop vao matcher hien tai.

## 7. File du kien tao moi

- `src/embedding_matcher.py`
- `tests/test_embedding_matcher.py`
- `docs/phases/phase-06-semantic-embedding.md`
- `docs/refactoring/phase-06-refactoring-plan.md` sau khi code xong

## 8. File du kien chinh sua

- `requirements.txt`
- `README.md`
- `docs/dev-learning-log.md`
- Co the chinh sua `src/semantic_matcher.py` neu can them `semantic_match` vao flow hien tai.

Tam thoi khong chinh sua:

- Parser modules.
- Document loader.
- Taxonomy JSON, tru khi can them sample semantic phrase.
- UI.
- Scoring/ranking modules vi chua ton tai.

## 9. Flow xu ly sau phase nay

Flow mong muon:

```text
normalized JD skill
  -> rule-based matcher
  -> exact/related/transferable/no_match

Neu no_match:
  -> semantic similarity
  -> semantic_match neu similarity >= threshold
  -> no_match neu similarity < threshold hoac model unavailable
```

Fallback:

```text
Embedding model unavailable
  -> skip semantic matching
  -> keep rule-based result
```

## 10. Learning Plan

### 10.1 Toi can hoc gi trong phase nay?

Can hoc:

- Embedding la gi.
- Pretrained model la gi.
- Vi sao khong train model tu dau.
- Cosine similarity la gi.
- Threshold la gi.
- Vi sao can fallback.
- Vi sao semantic match chi bo sung, khong thay the rule-based matching.

### 10.2 Cac khai niem ky thuat can hieu

- Text embedding: vector so bieu dien nghia cua text.
- Sentence transformer: pretrained model sinh embedding cho cau/doan text.
- Cosine similarity: do do goc giua hai vector, dung de uoc luong muc do gan nhau ve nghia.
- Threshold: nguong quyet dinh co xem la semantic match hay khong.
- Fallback: cach he thong van chay khi model khong load duoc.
- Mock test: test logic ma khong can tai model that.

### 10.3 Cac logic nho can nam

- Input semantic similarity la hai chuoi text.
- Output semantic similarity la float tu 0 den 1.
- Neu similarity cao hon threshold thi co the tao `semantic_match`.
- Neu model khong kha dung thi khong crash app.
- Rule-based match co do uu tien cao hon semantic match.
- Semantic match khong duoc dung de final reject/pass ung vien.

### 10.4 Vi du input/output

Input:

```python
required_skill = "Backend API development"
candidate_skill = "REST API"
```

Output neu model kha dung va similarity du cao:

```python
{
    "required_skill": "Backend API development",
    "candidate_skill": "REST API",
    "match_type": "semantic_match",
    "score": 0.85,
    "similarity": 0.78
}
```

Output neu model khong kha dung:

```python
{
    "required_skill": "Backend API development",
    "candidate_skill": None,
    "match_type": "no_match",
    "score": 0.0
}
```

### 10.5 Noi dung co the dua vao bao cao

Semantic Matching with Embeddings giup he thong phat hien cac ky nang hoac mo ta gan nghia ngay ca khi khong trung keyword va chua co relation trong taxonomy. Du an dung pretrained embedding model thay vi train model tu dau, phu hop voi dieu kien du lieu han che cua MVP. Rule-based matching van duoc giu lam baseline de dam bao tinh minh bach va on dinh.

## 11. Cac buoc trien khai

1. Kiem tra branch hien tai la `phase/06-semantic-embedding`.
2. Quyet dinh dependency embedding co cai trong phase nay hay chi tao wrapper fallback truoc.
3. Cap nhat `requirements.txt` neu can.
4. Tao `src/embedding_matcher.py`.
5. Implement model loader optional.
6. Implement cosine similarity wrapper.
7. Implement semantic match voi threshold ro rang.
8. Tich hop co kiem soat vao `src/semantic_matcher.py` neu can.
9. Them tests dung mock embedding.
10. Chay `pytest`.
11. Test thu cong khi model co va khi model unavailable.
12. Cap nhat README.
13. Cap nhat `docs/dev-learning-log.md`.
14. Tao `docs/refactoring/phase-06-refactoring-plan.md`.
15. Dung lai cho ban test va xac nhan.

## 12. Cach test phase

Test tu dong:

```bash
pytest
```

Test thu cong fallback:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_name='unavailable-model'); print(matcher.is_available())"
```

Test thu cong semantic similarity neu model kha dung:

```bash
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(); print(matcher.similarity('Built RESTful services', 'Backend API development'))"
```

Luu y: lenh dung model that chi chay sau khi dependency va model duoc cai/tai thanh cong.

## 13. Tieu chi hoan thanh phase

Phase 06 chi hoan thanh khi:

- Co semantic embedding wrapper hoac fallback implementation ro rang.
- He thong khong crash khi model unavailable.
- Rule-based matcher van pass tat ca tests cu.
- Co tests cho semantic similarity logic hoac mock logic.
- `pytest` pass.
- README va learning log duoc cap nhat.
- Refactoring plan Phase 06 duoc tao.
- Ban test thu cong va xac nhan pass.
- Chi sau khi ban xac nhan moi commit.

## 14. Rui ro

- `sentence-transformers` co the nang va cai dat cham.
- Model download can internet va co the fail.
- Ket qua semantic similarity co the sai neu phrase qua ngan.
- Threshold qua thap se match sai.
- Threshold qua cao se bo sot match tot.
- Neu embedding thay the rule-based logic, he thong se kem minh bach.

## 15. Ghi chu cho bao cao

Phase Semantic Matching with Embeddings la buoc mo rong AI/NLP sau khi da co baseline rule-based. He thong dung pretrained embedding model de do muc do gan nghia giua skill/mo ta yeu cau va skill/mo ta ung vien. Tuy nhien, de dam bao tinh minh bach va on dinh, semantic match chi bo sung cho cac truong hop rule-based chua match va luon co fallback khi model khong kha dung.
