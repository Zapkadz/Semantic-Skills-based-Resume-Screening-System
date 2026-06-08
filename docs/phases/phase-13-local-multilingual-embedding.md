# Phase 13 - Local Multilingual Embedding

## 1. Muc tieu phase

Phase 13 them local multilingual embedding vao pipeline de cai thien semantic matching Viet-Anh sau khi Phase 12 da lam tot parser, taxonomy, skill extraction va evidence.

Huong tong the van giu:

```text
Rule-based + taxonomy + evidence
        +
Local multilingual embedding
```

Embedding chi la tin hieu bo sung. He thong khong de model thay the hoan toan taxonomy/evidence, vi do an can giai thich duoc:

- JD yeu cau skill nao.
- CV co skill nao.
- Bang chung nam o cau nao.
- Vi sao ung vien duoc diem do.

## 2. Boi canh truoc Phase 13

Phase 12 da giai quyet cac loi nen:

- Parser doc duoc heading Anh/Viet.
- Taxonomy co AI, Computer Vision, eKYC, biometrics, model optimization.
- Full-text skill extraction fallback tim duoc skill tu raw JD/CV.
- Evidence detector nhan aliases va action verbs tieng Viet.

Benchmark `JD_1 + CV_30/CV_70/CV_85` sau Phase 12:

```text
1. Le Hoang Nam - 89/100 - Strong Review
2. Tran Quoc Bao - 66/100 - Maybe Review
3. Nguyen Van Minh - 26/100 - Not Enough Evidence
```

Tuy vay, he thong van co han che:

- Neu JD va CV dung hai cach dien dat khac nhau ma taxonomy chua co alias, rule-based co the bo sot.
- Neu cau CV tieng Viet mo ta nang luc nhung khong noi dung skill keyword, evidence co the chua du manh.
- Neu skill domain moi xuat hien ngoai taxonomy, system chua co cach so sanh ngu nghia tot.

Phase 13 se them local multilingual embedding de so sanh ngu nghia cross-language.

## 3. Co so tham khao

Nguon chinh:

- BGE-M3 Hugging Face model card: <https://huggingface.co/BAAI/bge-m3>
  - Model card ghi `BAAI/bge-m3` co dimension 1024, sequence length 8192, multilingual, va ho tro dense/sparse/ColBERT style representation.
- Multilingual-E5 large instruct Hugging Face model card: <https://huggingface.co/intfloat/multilingual-e5-large-instruct>
  - Model card cho vi du dung `SentenceTransformer("intfloat/multilingual-e5-large-instruct")`, embedding size 1024, va luu y query nen co instruction.
- Sentence Transformers Retrieve & Re-Rank docs: <https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html>
  - Tai lieu giai thich bi-encoder/dense retrieval encode query/doc rieng roi so sanh trong vector space.

Ket luan cho do an:

- Uu tien BGE-M3 lam default de xu ly long text va multilingual.
- Multilingual-E5 large instruct la fallback/alternative tot nhung can instruction prefix cho query.
- Tests khong duoc download model that; dung fake model nhu Phase 06.

## 4. Van de phase nay giai quyet

Vi du:

```text
JD English:
Experience with face recognition, liveness detection, and anti-spoofing.

CV Vietnamese:
Xay dung he thong nhan dien khuon mat va chong gia mao trong quy trinh eKYC.
```

Rule-based co the match neu taxonomy co alias. Nhung neu CV viet:

```text
Phat trien module xac minh danh tinh bang anh selfie va giay to tuy than.
```

Thi co the khong co exact alias `face matching` hay `liveness detection`. Multilingual embedding co the giup phat hien cau nay gan nghia voi yeu cau identity verification/eKYC.

## 5. Pham vi thuc hien

Trong Phase 13 se lam:

- Mo rong `src/embedding_matcher.py` de support multilingual model config.
- Doi default model de xuat sang local multilingual model, du kien `BAAI/bge-m3`.
- Them config ro rang:
  - model name.
  - threshold.
  - enable/disable embedding.
  - local-only mode neu model da duoc tai san vao Hugging Face cache.
  - query instruction neu dung E5.
- Them batch encode/cache nho de tranh encode lap lai qua nhieu candidate.
- Tich hop embedding matcher vao CLI pipeline va API payload pipeline o che do optional.
- Semantic match chi chay sau exact/related/transferable rule-based match.
- Them semantic signal cho skill matching.
- Co the them semantic evidence helper de tim sentence evidence gan nghia neu keyword evidence chua tim duoc.
- Cap nhat README, dev learning log, refactoring plan.
- Them tests khong phu thuoc model download.

## 6. Khong lam trong phase nay

Phase nay khong lam:

- Khong dung GPT API.
- Khong dich JD/CV bang GPT.
- Khong train model tu dau.
- Khong fine-tune model.
- Khong bat buoc download model trong tests.
- Khong thay API request/response schema.
- Khong sua web PHP.
- Khong them database/vector database.
- Khong dung FAISS/Chroma trong phase nay.
- Khong thay the rule-based scoring bang black-box model.
- Khong merge branch.

## 7. Model strategy de xuat

### 7.1 Default: BGE-M3

Default de xuat:

```text
BAAI/bge-m3
```

Ly do:

- Multilingual.
- Ho tro input dai hon E5 large instruct theo model card.
- Phu hop retrieval/semantic matching.
- Co the dung qua `sentence-transformers`.

Rui ro:

- Model nang hon, co the tai cham lan dau.
- May khong co GPU van chay duoc nhung co the cham.

### 7.2 Alternative: multilingual-E5 large instruct

Alternative:

```text
intfloat/multilingual-e5-large-instruct
```

Ly do:

- Pho bien trong multilingual embedding.
- Model card co huong dan dung voi SentenceTransformer.

Can luu y:

- Query nen them instruction, vi model card noi neu khong them instruction co the giam performance.
- Long texts bi truncate toi 512 tokens theo model card.

### 7.3 Phase 13 default decision

De don gian va phu hop voi Phase 12:

```text
Default model: BAAI/bge-m3
Fallback option: intfloat/multilingual-e5-large-instruct
```

Neu model unavailable:

```text
Skip embedding
Keep rule-based result
Do not crash CLI/API
```

## 8. Design de xuat

### 8.1 Mo rong `SemanticEmbeddingMatcher`

Hien tai `src/embedding_matcher.py` da co:

- lazy loading.
- `similarity(text_a, text_b)`.
- `best_match(required_skill, candidate_skills)`.
- fallback khi model unavailable.

Phase 13 co the mo rong:

```python
DEFAULT_MULTILINGUAL_EMBEDDING_MODEL = "BAAI/bge-m3"
DEFAULT_MULTILINGUAL_THRESHOLD = 0.72

class SemanticEmbeddingMatcher:
    ...
    def encode_texts(self, texts: list[str]) -> list[list[float]]:
        ...

    def similarity_matrix(self, queries: list[str], documents: list[str]) -> list[list[float]]:
        ...
```

Can giu backward compatibility voi tests Phase 06.

### 8.2 Query/document formatting

Voi BGE-M3:

```text
query = required skill / JD sentence
document = candidate skill / CV sentence
```

Voi E5 instruct:

```text
query = "Instruct: Given a job requirement, retrieve matching candidate resume evidence.\nQuery: ..."
document = raw candidate text
```

Phase 13 co the implement formatting nho:

```python
def format_embedding_query(text: str, model_name: str) -> str:
    ...

def format_embedding_document(text: str, model_name: str) -> str:
    ...
```

### 8.3 Matching levels

Rule priority van giu:

```text
exact_match
related_match
transferable_match
semantic_match
no_match
```

`semantic_match` chi duoc dung khi rule-based khong match.

### 8.4 Pipeline integration

Hien tai pipeline goi:

```python
matches = match_skills(required_skills, candidate_skills, taxonomy)
```

Phase 13 se them optional:

```python
embedding_matcher = build_embedding_matcher_from_config()
matches = match_skills(
    required_skills,
    candidate_skills,
    taxonomy,
    embedding_matcher=embedding_matcher,
)
```

Default de tranh cham bat ngo:

- Trong tests: model fake hoac disabled.
- Trong CLI/API: co the enable mac dinh neu dependency/model co san, nhung fallback neu khong co.
- Neu muon than trong hon, co CLI flag `--enable-embedding` va API config sau.

De phu hop do an va demo:

```text
CLI/API co the auto-attempt load local model.
Neu load that bai thi fallback rule-based.
```

### 8.5 Semantic evidence fallback

Hien tai evidence detector tim cau co keyword/alias.

Phase 13 co the them fallback:

```text
Neu matched skill co evidence_level = 0 hoac 1:
  - Lay cac candidate evidence sentences tu work/projects/summary.
  - So sanh required skill/JD phrase voi sentence bang embedding.
  - Neu similarity >= evidence threshold:
      evidence_level = 2 hoac 3 tuy source/action verb.
      evidence_text = sentence gan nghia nhat.
      evidence_source = source.
      evidence_similarity = ...
```

Can than trong:

- Evidence semantic khong nen nang len level 3 neu cau khong co action verb.
- Review card nen ghi `match_type = semantic_match` hoac co `similarity` de minh bach.

## 9. Config de xuat

Co the them constants trong `src/embedding_matcher.py`:

```python
DEFAULT_EMBEDDING_MODEL = "BAAI/bge-m3"
DEFAULT_SEMANTIC_THRESHOLD = 0.72
DEFAULT_EVIDENCE_THRESHOLD = 0.68
```

Hoac them module:

```text
src/embedding_config.py
```

Bien moi truong de override:

```text
SEMANTIC_EMBEDDING_MODEL=BAAI/bge-m3
SEMANTIC_EMBEDDING_THRESHOLD=0.72
SEMANTIC_EMBEDDING_ENABLED=1
SEMANTIC_EMBEDDING_LOCAL_ONLY=1
```

Khong bat buoc trong phase nay, nhung neu lam thi README phai ghi ro.

## 10. Test plan

### 10.1 Automated tests

Mo rong:

- `tests/test_embedding_matcher.py`
  - default multilingual model constant.
  - query/document formatting cho BGE-M3 va E5.
  - batch encode/cache neu implement.
  - fallback khi model loader fail.
- `tests/test_semantic_matcher.py`
  - semantic match Viet-Anh bang fake embedding.
  - rule-based priority van cao hon semantic.
  - no_match khi similarity duoi threshold.
- `tests/test_payload_pipeline.py`
  - pipeline van chay khi embedding unavailable.
  - pipeline dung embedding matcher fake neu inject duoc.
- Co the them `tests/test_semantic_evidence.py`
  - evidence semantic fallback tim cau Viet gan nghia voi JD English.

Tests khong download real model.

### 10.2 Manual tests

Test fallback:

```powershell
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_name='bad-model'); print(matcher.similarity('face recognition', 'nhận diện khuôn mặt')); print(matcher.unavailable_reason)"
```

Test real model neu may da cai dependency/model:

```powershell
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_name='BAAI/bge-m3'); print(round(matcher.similarity('face recognition', 'nhận diện khuôn mặt') or 0, 4)); print(matcher.unavailable_reason)"
```

Benchmark `JD_1/CV_30/CV_70/CV_85`:

```text
Ky vong ranking van la:
CV_85 > CV_70 > CV_30
```

Muc tieu khong phai tang diem tuyet doi bat buoc, ma la:

- semantic_match xuat hien trong mot so truong hop cross-language.
- evidence/review_card ro hon khi keyword alias khong du.
- system khong crash neu model unavailable.

## 11. Tieu chi hoan thanh

Phase 13 hoan thanh khi:

- Co local multilingual embedding config ro rang.
- Default/khuyen nghi model la BGE-M3.
- E5 instruct duoc ghi/ho tro nhu alternative neu can.
- Embedding matcher van fallback an toan khi model unavailable.
- Rule-based match van uu tien hon semantic match.
- CLI/API khong doi schema va khong crash khi model chua download.
- Tests dung fake model pass.
- Full `pytest` pass.
- Manual fallback test pass.
- Manual real model test duoc huong dan ro; neu may chua tai model thi khong tinh la fail.
- README, dev learning log, refactoring plan duoc cap nhat.

## 12. Ruit ro va cach giam thieu

### 12.1 Model nang va tai cham

Risk:

- BGE-M3 co the tai/chay cham tren CPU.

Giam thieu:

- Lazy loading.
- Fallback rule-based.
- Cache embeddings trong mot request.
- Huong dan manual test rieng.

### 12.2 Diem bi thay doi qua manh

Risk:

- Semantic match co the lam ung vien diem cao vi cau nghe co ve gan nghia nhung evidence yeu.

Giam thieu:

- Semantic score chi la 0.85 nhu Phase 06, thap hon exact match.
- Evidence van can sentence cu the.
- Threshold can than trong.

### 12.3 Kho bao ve do an

Risk:

- Thay co hoi vi sao model quyet dinh ung vien phu hop.

Giam thieu:

- Giai thich embedding chi tinh cosine similarity.
- Output van co taxonomy skill, evidence_text, match_type, similarity.
- Rule-based/taxonomy van la backbone.

### 12.4 Environment khong co internet

Risk:

- Lan dau load model can download tu Hugging Face.

Giam thieu:

- Khong require model trong tests.
- Neu model unavailable, pipeline van chay.
- README ghi cach tai model truoc khi demo neu can.

## 13. Cac buoc trien khai

1. Kiem tra branch `phase/13-local-multilingual-embedding`.
2. Mo rong constants/config trong `src/embedding_matcher.py`.
3. Them query/document formatting cho BGE-M3/E5.
4. Them batch encode/cache neu phu hop.
5. Tich hop optional matcher vao file-based pipeline.
6. Tich hop optional matcher vao payload/API pipeline.
7. Neu can, them semantic evidence fallback co threshold rieng.
8. Them tests fake model.
9. Chay full `pytest`.
10. Chay CLI regression.
11. Chay API regression.
12. Chay manual fallback embedding test.
13. Chay manual real model test neu model tai duoc.
14. Chay benchmark `JD_1/CV_30/CV_70/CV_85`.
15. Cap nhat README.
16. Cap nhat dev learning log.
17. Tao refactoring plan Phase 13.
18. Dung lai cho ban test va xac nhan truoc commit.

## 14. Ghi chu cho bao cao

Phase 13 la buoc them pretrained multilingual embedding vao he thong. He thong encode JD skill/sentence va CV skill/evidence sentence vao cung vector space, sau do dung cosine similarity de do do gan nghia. Cach nay giup xu ly truong hop JD va CV khac ngon ngu hoac khac cach dien dat.

Tuy nhien, do an van giu tinh minh bach:

- Taxonomy quy dinh skill canonical.
- Rule-based match co uu tien cao.
- Semantic match co similarity score.
- Evidence text van lay tu CV.
- Final review card van giai thich duoc.

## 15. Ket qua implementation

Sau khi code Phase 13:

- `src/embedding_matcher.py` dung `BAAI/bge-m3` lam default recommended model.
- Ho tro `intfloat/multilingual-e5-large-instruct` bang query instruction formatting.
- Them `encode_texts` va `similarity_matrix`.
- Them in-memory cache cho embedding vectors trong mot matcher instance.
- CLI co flag:
  - `--enable-embedding`
  - `--embedding-model`
  - `--embedding-threshold`
  - `--embedding-local-only`
- API co the bat embedding bang env vars:
  - `SEMANTIC_EMBEDDING_ENABLED`
  - `SEMANTIC_EMBEDDING_MODEL`
  - `SEMANTIC_EMBEDDING_THRESHOLD`
  - `SEMANTIC_EMBEDDING_LOCAL_ONLY`
- `run_screening_pipeline` va `run_screening_payload` nhan optional `embedding_matcher`.
- Tests dung fake model nen khong download model that.

Embedding mac dinh khong tu bat trong CLI/API. Ly do:

- Tranh tai model nang khi nguoi dung chi chay tests.
- Tranh lan dau API bi cham vi download.
- Giu rule-based/taxonomy/evidence la default on dinh.

Muon bat local multilingual embedding:

```powershell
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs --enable-embedding --embedding-model BAAI/bge-m3 --embedding-local-only
```

Manual fallback test:

```powershell
python -c "from src.embedding_matcher import SemanticEmbeddingMatcher; matcher=SemanticEmbeddingMatcher(model_loader=lambda name: (_ for _ in ()).throw(RuntimeError('model unavailable'))); print(matcher.similarity('face recognition', 'nhan dien khuon mat')); print(matcher.unavailable_reason)"
```

Expected:

```text
None
<unavailable reason>
```
