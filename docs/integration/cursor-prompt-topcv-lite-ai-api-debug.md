# Prompt cho Cursor: Debug luồng TOPCV Lite gọi Python AI API

Bạn đang code web PHP `topcv_lite`. Mục tiêu là kiểm tra chính xác web đang gửi payload gì sang Python AI API và API trả về gì khi employer bấm "Chạy AI gợi ý xếp hạng".

## Bối cảnh kỹ thuật

- Python AI project nằm tại `C:\SEMANTIC_SKILLS_RESUME`.
- Web PHP nằm tại `C:\xampp\htdocs\topcv_lite`.
- Web hiện đang dùng `driver => api`, gọi `http://127.0.0.1:8000/screening`.
- Python API muốn chạy đúng Phase 17 + BGE-M3 phải được restart bằng env:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
$env:SEMANTIC_EMBEDDING_ENABLED='1'
$env:SEMANTIC_EMBEDDING_MODEL='BAAI/bge-m3'
$env:SEMANTIC_EMBEDDING_THRESHOLD='0.72'
$env:SEMANTIC_EMBEDDING_LOCAL_ONLY='1'
$env:HF_HUB_OFFLINE='1'
uvicorn api:app --host 127.0.0.1 --port 8000
```

Sau khi restart, kiểm tra:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health | ConvertTo-Json -Depth 10
```

Kỳ vọng `phase` là `Phase 17 - Taxonomy-independent Open-set Screening Core` và `embedding_enabled` là `true`.

## Việc cần làm trong web PHP

Hãy thêm chế độ debug cục bộ cho AI screening API, chỉ bật bằng config local, không bật mặc định.

### 1. Thêm config debug

Trong `config/ai_screening.local.php`, hỗ trợ các key:

```php
'debug_api_payload' => true,
'debug_api_dir' => 'C:\\topcv_ai_runtime\\api-debug',
```

Không commit file local nếu đang bị gitignore.

### 2. Ghi request/response JSON khi gọi API

Trong `includes/ai_screening_api.php`, tại `ai_screening_call_api(array $payload)`:

- Nếu `debug_api_payload` bật:
  - Tạo folder debug nếu chưa có.
  - Ghi request JSON vào file:
    `C:\topcv_ai_runtime\api-debug\{timestamp}-job-{job_id}-request.json`
  - Sau khi nhận response, ghi response body vào:
    `C:\topcv_ai_runtime\api-debug\{timestamp}-job-{job_id}-response.json`
  - Ghi log vào `storage/logs/ai_screening.log` với đường dẫn 2 file trên.
- Không echo payload ra màn hình web vì có dữ liệu CV/email/sđt.
- Không làm thay đổi flow lưu DB hiện tại.
- Nếu ghi file debug lỗi thì chỉ log lỗi, không làm hỏng chức năng chạy AI.

### 3. Log thêm metadata ngắn

Sau khi decode response thành công, log thêm:

- `job_id`
- `candidate_count`
- `response_job_title`
- `response_open_set_count`
- `response_embedding_enabled` từ `job.screening_confidence.embedding_enabled`
- top candidate: `application_id`, `candidate_name`, `final_score`, `recommendation`

Mục tiêu là nhìn log có thể biết web đã gọi đúng API Phase 17/BGE chưa.

### 4. Kiểm tra payload web gửi JD có sạch chưa

Payload từ web có thể chứa HTML từ editor trong `jobs.requirements` và `jobs.description`.

Không cần tự parse AI ở PHP, nhưng hãy kiểm tra debug request:

- `job.requirements` hiện có HTML không?
- `job.description` hiện có HTML không?
- `candidates[0].cv_text` có đủ nội dung CV không?
- `candidates[0].application_id` có đúng với ứng viên trên màn hình không?

Python Phase 17 đã có xử lý HTML, nhưng debug request vẫn cần giữ nguyên để đối chiếu.

### 5. Cách test sau khi code

1. Restart Python API bằng lệnh env BGE-M3 ở trên.
2. Mở `http://localhost/topcv_lite/employer/job_candidates.php?job_id=18`.
3. Bấm "Chạy AI gợi ý xếp hạng".
4. Mở `storage/logs/ai_screening.log`.
5. Mở 2 file debug request/response mới nhất trong `C:\topcv_ai_runtime\api-debug`.

Gửi lại cho Codex:

- 10 dòng log mới nhất của `storage/logs/ai_screening.log`.
- File `*-request.json`.
- File `*-response.json`.
- Dòng DB mới nhất trong `ai_screening_results.raw_result_json` của `job_id=18`.

## Tiêu chí đúng

Với hồ sơ Phan Thanh Kiệt giống David Chen và JD IT Security:

- Response phải có `job.open_set_requirements` nhiều hơn 1 item, ví dụ `Linux`, `Qualys`, `vulnerability management`, `access control`, `ISO 27001`, `Security+`.
- `job.screening_confidence.embedding_enabled` phải là `true`.
- Candidate không được chỉ match mỗi `3 năm`.
- Score kỳ vọng sau Phase 17 + BGE-M3 khoảng `72 - Review` nếu CV/JD giống dữ liệu test.

