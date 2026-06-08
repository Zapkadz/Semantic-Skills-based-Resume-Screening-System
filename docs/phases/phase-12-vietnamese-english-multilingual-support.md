# Phase 12 - Vietnamese-English Parser, Taxonomy, and Evidence Foundation

## 1. Muc tieu phase

Phase 12 cai thien kha nang xu ly JD/CV song ngu Viet-Anh truoc khi dua multilingual embedding vao he thong.

Ket qua test gan nhat voi `JD_1.txt` va cac CV tieng Viet `CV_30.txt`, `CV_70.txt`, `CV_85.txt` cho thay diem cua ca 3 ung vien deu bi keo ve 35/100. Nguyen nhan chinh khong phai chi do embedding, ma do cac tang dau vao chua doc duoc noi dung:

- JD parser chua nhan heading khong co dau hai cham, vi du `Requirements`.
- JD parser chua nhan heading tieng Viet, vi du `Yeu cau`, `Mo ta cong viec`.
- Resume parser chua nhan heading tieng Viet, vi du `Ky nang`, `Kinh nghiem lam viec`, `Du an`.
- Taxonomy hien tai con thien ve backend/web, chua co nhom AI, Computer Vision, eKYC.
- Evidence detector chua nhan dong tu hanh dong tieng Viet, vi du `xay dung`, `phat trien`, `trien khai`, `toi uu`, `huan luyen`.

Phase nay dat muc tieu sua cac tang nen tren truoc. Khi input da duoc parse va normalize dung, Phase 13 moi them multilingual embedding de matching ngu nghia Viet-Anh tot hon.

## 2. Vi sao khong nhay thang vao multilingual embedding

Neu dua multilingual embedding vao ngay, model co the hieu ngu nghia Viet-Anh, nhung pipeline van gap cac loi nen:

- Parser tra ve skill rong thi embedding khong co du lieu tot de so sanh.
- Taxonomy thieu skill domain thi normalizer khong biet `face recognition`, `liveness detection`, `anti-spoofing` la gi.
- Evidence detector khong nhan dong tu tieng Viet thi CV co lam that van chi duoc evidence yeu.
- Review card se thieu ly do ro rang, lam he thong kho bao ve khi thuyet trinh.

Huong tot hon cho do an:

```text
Raw JD/CV
  -> bilingual parser
  -> taxonomy + aliases Viet-Anh
  -> full-text skill extraction fallback
  -> Vietnamese-English evidence detection
  -> scoring/ranking hien tai
  -> sau do moi them multilingual embedding
```

## 3. Co so tham khao tu nghien cuu

Phase 12 khong import truc tiep cac bo taxonomy lon, nhung hoc cach to chuc skill va nang luc tu cac nguon chinh thong:

- ESCO la he thong ky nang/nghe nghiep cua Chau Au, huu ich de tham khao cach tach skill, occupation, qualification: <https://esco.ec.europa.eu/en/use-esco>
- O*NET la nguon taxonomy nghe nghiep va skill cua U.S. Department of Labor: <https://www.dol.gov/agencies/eta/onet?lang=en>
- VnCoreNLP va PhoBERT cho thay xu ly ngon ngu tieng Viet nen tinh den dau tieng Viet, bien the khong dau, va ngu canh cau tieng Viet:
  - <https://arxiv.org/abs/1801.01331>
  - <https://arxiv.org/abs/2003.00744>

Phase 13 co the tham khao cac multilingual embedding model:

- BGE-M3: multilingual, multi-functionality, multi-granularity: <https://huggingface.co/BAAI/bge-m3>
- Multilingual E5: multilingual embedding family: <https://huggingface.co/intfloat/multilingual-e5-large>
- Sentence Transformers semantic search/retrieve-rerank workflow: <https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html>

## 4. Pham vi thuc hien

Trong Phase 12 se lam:

- Mo rong JD parser de nhan heading Anh/Viet, co hoac khong co dau hai cham.
- Mo rong resume parser de nhan heading Anh/Viet, co hoac khong co dau hai cham.
- Ho tro bullet va list format pho bien hon.
- Mo rong taxonomy voi nhom AI, Machine Learning, Computer Vision, eKYC, Biometrics, Model Optimization.
- Them aliases tieng Anh, tieng Viet co dau, tieng Viet khong dau cho skill quan trong.
- Them fallback extract skill tu full raw text dua tren taxonomy aliases.
- Mo rong evidence detector de nhan action verb tieng Viet.
- Mo rong detection cho experience, seniority, domain song ngu.
- Dam bao CLI Phase 10 va API Phase 11 van giu interface cu.
- Them tests unit va regression tests.
- Cap nhat README, dev learning log, refactoring plan sau khi code xong.

## 5. Khong lam trong phase nay

Phase nay khong lam:

- Khong them GPT API.
- Khong dich JD/CV bang GPT.
- Khong them multilingual embedding model vao core scoring.
- Khong download hoac bat buoc chay model local nang.
- Khong sua web PHP TOPCV Lite.
- Khong them PDF/DOCX extraction.
- Khong them OCR.
- Khong thay doi API schema.
- Khong thay doi scoring formula lon neu khong co ly do test ro rang.
- Khong hard-code diem rieng cho `CV_30`, `CV_70`, `CV_85`.

## 6. Thiet ke de xuat

### 6.1 Bilingual section parser

Hien tai `src/jd_parser.py` va `src/resume_parser.py` moi nhan heading co format:

```text
Requirements:
Skills:
Projects:
```

Phase 12 se ho tro them:

```text
Requirements
Yeu cau
Yeu cau cong viec
Ky nang
Ky nang chuyen mon
Kinh nghiem lam viec
Du an
Hoc van
Chung chi
```

Heading can nhan ca dang co dau:

```text
Yêu cầu
Mô tả công việc
Kỹ năng chuyên môn
Kinh nghiệm làm việc
Dự án
Học vấn
Chứng chỉ
```

Va dang khong dau:

```text
Yeu cau
Mo ta cong viec
Ky nang chuyen mon
Kinh nghiem lam viec
Du an
Hoc van
Chung chi
```

De tranh duplicate logic, co the tao helper nho:

```text
src/section_parser.py
```

Helper nay se phu trach:

- normalize heading ve lowercase.
- strip dau hai cham neu co.
- remove bullet/numbering thua.
- so khop heading bang aliases.
- khong coi mot cau dai la heading neu do la noi dung binh thuong.

### 6.2 JD parser song ngu

Mo rong `SECTION_ALIASES` cua JD:

- `requirements`, `required skills`, `must have`, `qualifications`
- `yêu cầu`, `yeu cau`, `yêu cầu công việc`, `yeu cau cong viec`
- `kỹ năng bắt buộc`, `ky nang bat buoc`
- `nice to have`, `preferred`, `preferred skills`
- `ưu tiên`, `uu tien`, `điểm cộng`, `diem cong`, `lợi thế`, `loi the`
- `responsibilities`, `job responsibilities`
- `mô tả công việc`, `mo ta cong viec`, `trách nhiệm`, `trach nhiem`

Mo rong experience detection:

```text
3+ years experience
At least 2 years
Tối thiểu 2 năm kinh nghiệm
Từ 1 năm kinh nghiệm
1+ năm
```

Mo rong seniority:

- `senior`, `middle`, `mid`, `junior`, `fresher`, `intern`
- `trưởng nhóm`, `lead`, `thực tập`, `mới tốt nghiệp`

Mo rong domain detection:

- Backend
- Web Application
- Testing
- Data
- AI/Machine Learning
- Computer Vision
- eKYC/Biometrics
- Mobile AI

### 6.3 Resume parser song ngu

Mo rong `SECTION_ALIASES` cua resume:

- Summary:
  - `summary`, `profile`, `objective`
  - `tóm tắt`, `tom tat`, `mục tiêu nghề nghiệp`, `muc tieu nghe nghiep`
- Skills:
  - `skills`, `technical skills`
  - `kỹ năng`, `ky nang`, `kỹ năng chuyên môn`, `ky nang chuyen mon`, `công nghệ`, `cong nghe`
- Work experience:
  - `work experience`, `experience`, `employment history`
  - `kinh nghiệm`, `kinh nghiem`, `kinh nghiệm làm việc`, `kinh nghiem lam viec`
- Projects:
  - `projects`, `project`
  - `dự án`, `du an`, `dự án tiêu biểu`, `du an tieu bieu`
- Education:
  - `education`
  - `học vấn`, `hoc van`, `trình độ học vấn`, `trinh do hoc van`
- Certifications:
  - `certifications`, `certification`
  - `chứng chỉ`, `chung chi`

Parser can giu output schema cu:

```python
{
    "candidate_name": "",
    "headline": "",
    "summary": "",
    "raw_skills": [],
    "work_experience": [],
    "projects": [],
    "education": [],
    "certifications": [],
}
```

### 6.4 Taxonomy AI, Computer Vision, eKYC

Mo rong `data/taxonomy/skills.json` them cac skill/domain sau:

- Machine Learning
- Deep Learning
- Computer Vision
- Image Processing
- Python
- PyTorch
- TensorFlow
- ONNX
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- OCR
- Face Recognition
- Face Detection
- Face Matching
- Face Alignment
- Facial Landmark Detection
- Liveness Detection
- Anti-Spoofing
- eKYC
- Biometrics
- Model Optimization
- Quantization
- Pruning
- Knowledge Distillation
- Mobile AI
- Android
- iOS
- FAR
- FRR
- AUC

Moi skill quan trong nen co aliases song ngu, vi du:

```json
{
  "Face Recognition": {
    "aliases": [
      "Facial Recognition",
      "Nhan dien khuon mat",
      "Nhận diện khuôn mặt"
    ],
    "category": "Computer Vision",
    "related": ["Face Detection", "Face Matching", "Biometrics", "eKYC"],
    "transferable": []
  }
}
```

Nguyen tac mo rong taxonomy:

- Canonical skill giu bang tieng Anh de output on dinh cho web.
- Alias co the la tieng Anh, tieng Viet co dau, tieng Viet khong dau.
- Skill qua chung nhu `Mobile` phai can than de khong match sai.
- Metric nhu `FAR`, `FRR`, `AUC` duoc xep vao evaluation/biometrics metric.

### 6.5 Full-text skill extraction fallback

Hien tai pipeline chu yeu lay skill tu section `skills` cua CV va `requirements` cua JD. Neu parser khong tach duoc section, skill se rong.

Phase 12 se them fallback:

```python
def extract_taxonomy_skills_from_text(text: str, taxonomy: dict) -> list[str]:
    ...
```

Fallback nay:

- scan raw JD/CV text bang canonical skill va aliases.
- normalize tieng Viet co dau/khong dau khi can.
- tra ve canonical skill.
- dedupe theo thu tu xuat hien.
- uu tien precision hon recall de tranh gan skill sai.

Ung dung:

- JD: neu `must_have_skills` rong hoac it, bo sung skill tim thay trong raw text.
- CV: bo sung `raw_skills` tu full raw text neu section skills rong hoac thieu.
- Evidence: van can text goc de tim cau co bang chung.

### 6.6 Vietnamese evidence detection

Mo rong action verb cho tieng Viet:

```text
xay dung, xây dựng
phat trien, phát triển
trien khai, triển khai
toi uu, tối ưu
huan luyen, huấn luyện
danh gia, đánh giá
tich hop, tích hợp
thiet ke, thiết kế
cai dat, cài đặt
su dung, sử dụng
phan tich, phân tích
kiem thu, kiểm thử
cai thien, cải thiện
```

Evidence level van giu logic hien tai:

- Level 3: skill xuat hien trong work/project sentence co action verb.
- Level 2: skill xuat hien trong work/project sentence nhung chua co action verb.
- Level 1: skill xuat hien trong summary/headline/skills.
- Level 0: khong co evidence.

### 6.7 API va CLI impact

Phase 12 khong thay doi cach goi CLI:

```bash
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

Phase 12 khong thay doi API endpoint:

```http
POST http://127.0.0.1:8000/screening
```

Web PHP khong can doi request schema. Khi web gui JD/CV text nhu cu, Python API se tu parse va rank tot hon.

## 7. Test plan

### 7.1 Automated tests

Them hoac mo rong tests:

- `tests/test_jd_parser.py`
  - heading English khong dau hai cham.
  - heading Viet co dau.
  - heading Viet khong dau.
  - extract experience `năm kinh nghiệm`.
  - detect domain Computer Vision/eKYC.
- `tests/test_resume_parser.py`
  - heading `Kỹ năng`, `Kinh nghiệm làm việc`, `Dự án`.
  - heading khong dau `Ky nang`, `Kinh nghiem lam viec`, `Du an`.
  - project/work bullets tieng Viet.
- `tests/test_skill_taxonomy.py`
  - taxonomy JSON hop le.
  - skill AI/CV/eKYC quan trong ton tai.
  - moi skill co keys `aliases`, `category`, `related`, `transferable`.
- `tests/test_skill_normalizer.py`
  - normalize alias tieng Viet ve canonical English.
  - normalize alias khong dau ve canonical English.
- Test moi du kien `tests/test_skill_extractor.py`
  - extract `Face Recognition` tu `nhận diện khuôn mặt`.
  - extract `Liveness Detection` tu `phát hiện sống`.
  - extract `Anti-Spoofing` tu `chống giả mạo`.
  - khong match false positive voi tu qua chung.
- `tests/test_evidence_detector.py`
  - evidence level 3 voi cau tieng Viet co action verb.
  - evidence level 1 khi skill chi nam trong section skills.
- `tests/test_payload_pipeline.py`
  - API payload voi JD English + CV Vietnamese van co skill/evidence.
  - API payload voi JD Vietnamese + CV English van co skill/evidence.

### 7.2 Regression tests

Tat ca test hien tai phai pass:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
pytest
```

CLI cu phai chay binh thuong:

```powershell
python main.py --jd data/jobs/jd_backend_java.txt --cv-dir data/cvs
```

API cu phai chay binh thuong:

```powershell
uvicorn api:app --host 127.0.0.1 --port 8000
```

### 7.3 Manual benchmark voi JD_1/CV_30/CV_70/CV_85

Dung bo test nguoi dung da them local:

```text
data/jobs/JD_1.txt
data/cvs/CV_30.txt
data/cvs/CV_70.txt
data/cvs/CV_85.txt
```

Ky vong sau Phase 12:

- `JD_1.txt` parse duoc title, requirements, responsibilities, experience/domain neu co.
- `CV_85.txt` extract duoc nhieu skill Computer Vision/eKYC nhat.
- `CV_70.txt` extract duoc mot phan skill lien quan AI/CV.
- `CV_30.txt` extract it hoac khong co skill lien quan neu CV khong phu hop.
- Ranking ky vong: `CV_85` > `CV_70` > `CV_30`.
- Khong ep diem tuyet doi, nhung diem khong nen dong loat 35/100 nhu hien tai.

Neu muon dua bo test nay vao repo lam fixture chinh thuc, can co xac nhan rieng de commit cac file `JD_1/CV_30/CV_70/CV_85`.

## 8. Implementation checklist

1. Tao/bo sung helper normalize heading va strip bullet/list marker.
2. Cap nhat JD parser section aliases Anh/Viet.
3. Cap nhat resume parser section aliases Anh/Viet.
4. Them Unicode/accent normalization helper neu can.
5. Them skill extractor fallback dua tren taxonomy.
6. Mo rong taxonomy AI/CV/eKYC.
7. Mo rong evidence detector voi action verbs tieng Viet.
8. Cap nhat domain/seniority/experience detection song ngu.
9. Ket noi fallback extraction vao file-based pipeline va payload pipeline.
10. Them tests tuong ung.
11. Chay full test suite.
12. Chay manual CLI/API regression.
13. Chay manual benchmark `JD_1` voi `CV_30/CV_70/CV_85`.
14. Cap nhat README.
15. Cap nhat dev learning log.
16. Tao refactoring plan Phase 12.

## 9. Ruit ro va cach giam thieu

### 9.1 False positive khi scan full text

Risk:

- Tu qua chung nhu `mobile`, `model`, `alignment`, `testing` co the match sai.

Giam thieu:

- Chi them alias du ro nghia.
- Can than voi skill metric ngan nhu `AUC`, `FAR`, `FRR`.
- Dung word boundary cho Latin phrase.
- Voi tieng Viet, uu tien phrase dai hon nhu `nhan dien khuon mat` thay vi tu don.

### 9.2 Taxonomy phinh to qua nhanh

Risk:

- Them qua nhieu skill lam normalizer kho kiem soat.

Giam thieu:

- Phase 12 chi them nhom can cho AI/CV/eKYC va cac skill xuat hien trong JD/CV benchmark.
- Giu schema taxonomy cu.
- Khong import toan bo ESCO/O*NET.

### 9.3 Diem tang nhung giai thich van yeu

Risk:

- Skill match duoc nhung evidence_text rong hoac chung chung.

Giam thieu:

- Evidence detector phai doc work/project sentences tieng Viet.
- Review card phai co evidence highlights thuc te tu CV.

### 9.4 API/web bi anh huong

Risk:

- Web PHP dang goi API Phase 11, neu doi schema se gay loi.

Giam thieu:

- Giu nguyen request/response schema.
- Chi cai thien logic ben trong pipeline.
- Regression test API.

## 10. Tieu chi hoan thanh

Phase 12 hoan thanh khi:

- Parser doc duoc heading JD/CV Anh/Viet, co hoac khong co dau hai cham.
- Taxonomy co nhom AI/Computer Vision/eKYC can thiet.
- Normalizer map duoc aliases tieng Viet ve canonical skill tieng Anh.
- Fallback full-text skill extraction hoat dong va co test.
- Evidence detector nhan duoc action verbs tieng Viet.
- Full test suite pass.
- CLI Phase 10 van chay.
- API Phase 11 van chay.
- Manual benchmark `JD_1 + CV_30/CV_70/CV_85` khong con dong loat 35/100 va ranking hop ly hon.
- README, dev learning log, refactoring plan duoc cap nhat.

## 11. Chuan bi cho Phase 13

Sau Phase 12, neu parser/taxonomy/evidence da tot, Phase 13 co the them multilingual embedding local:

- Thu nghiem `BAAI/bge-m3` va `intfloat/multilingual-e5-large`.
- Them config model name va lazy loading.
- So sanh phrase/cau evidence Viet-Anh bang cosine similarity.
- Giu rule-based/taxonomy la backbone de review card van explainable.
- Chi dung embedding de bo sung semantic signal, khong thay the hoan toan rule-based matching.

## 12. Ket qua implementation

Sau khi code Phase 12:

- Parser nhan heading Anh/Viet co hoac khong co dau hai cham.
- Parser co repair mojibake pho bien khi text UTF-8 bi doc sai thanh Windows-1252.
- Taxonomy co them nhom AI, Computer Vision, eKYC, biometrics, model optimization, mobile AI.
- `src/skill_extractor.py` scan skill tu raw text bang canonical skill va aliases.
- CLI pipeline va API payload pipeline deu dung fallback extraction noi bo.
- Evidence detector nhan aliases tieng Viet va action verbs tieng Viet.
- Scorer nhan them domain AI/Machine Learning, Computer Vision, eKYC/Biometrics, Mobile AI.
- Tests duoc mo rong tu 91 len 103 test.

Benchmark thu cong voi `JD_1.txt` va 3 CV local:

```text
1. Le Hoang Nam - 89/100 - Strong Review
2. Tran Quoc Bao - 66/100 - Maybe Review
3. Nguyen Van Minh - 26/100 - Not Enough Evidence
```

Ket qua nay cho thay ranking khong con dong loat 35/100 nhu truoc Phase 12. He thong da doc duoc skill va evidence nen CV dung domain duoc xep cao hon ro rang.
