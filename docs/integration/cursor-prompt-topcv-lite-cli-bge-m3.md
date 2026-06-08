# Cursor Prompt - Fix TOPCV Lite CLI Integration with BGE-M3

Copy prompt duoi day vao Cursor trong project PHP:

```text
Ban dang lam trong project PHP TOPCV Lite tai:

C:\xampp\htdocs\topcv_lite

Ben ngoai project PHP da co AI Python project tai:

C:\SEMANTIC_SKILLS_RESUME

Trong task nay CHUA chuyen sang API. Muc tieu la kiem tra web hien dang goi Python CLI theo kieu nao, sau do sua CLI command cho hoan chinh de chay local multilingual embedding BGE-M3.

Khong sua code AI Python trong task nay.
Khong copy AI project vao topcv_lite.
Khong tich hop FastAPI trong task nay.
Chi sua phan PHP dang goi CLI.

## 1. Viec can lam dau tien: tim web dang goi CLI o dau

Trong Cursor, search toan project cac keyword sau:

```text
SEMANTIC_SKILLS_RESUME
python.exe
python
main.py
--jd
--cv-dir
--output-json
ranking_results.json
exec(
shell_exec(
proc_open(
passthru(
popen(
ai_screening
run_ai
```

Neu dung terminal PowerShell trong `C:\xampp\htdocs\topcv_lite`, co the chay:

```powershell
Get-ChildItem -Recurse -Include *.php |
  Select-String -Pattern 'SEMANTIC_SKILLS_RESUME','python.exe','main.py','--jd','--cv-dir','--output-json','ranking_results.json','exec\(','shell_exec\(','proc_open\(','passthru\(','popen\(','ai_screening','run_ai'
```

Can xac dinh ro:

- File PHP nao dang chay CLI.
- Web dang dung `exec`, `shell_exec`, `proc_open`, hay batch script.
- Web dang tao file JD o dau.
- Web dang tao folder CV o dau.
- Web dang doc file `ranking_results.json` o dau.
- Web dang map ket qua ve `application_id` bang cach nao.

Neu phat hien web da goi `http://127.0.0.1:8000/screening` bang cURL thi do la API, khong phai CLI. Trong task nay hay bao lai, dung tiep API de lam sau.

## 2. CLI command chuan can dat duoc

Command PHP cuoi cung phai tuong duong voi lenh PowerShell nay:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
$env:HF_HUB_OFFLINE='1'
$env:PYTHONIOENCODING='utf-8'

C:\SEMANTIC_SKILLS_RESUME\.venv\Scripts\python.exe C:\SEMANTIC_SKILLS_RESUME\main.py `
  --jd C:\topcv_ai_runtime\job-10\run-test\jd.txt `
  --cv-dir C:\topcv_ai_runtime\job-10\run-test\cvs `
  --taxonomy C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json `
  --output-json C:\topcv_ai_runtime\job-10\run-test\ranking_results.json `
  --enable-embedding `
  --embedding-model BAAI/bge-m3 `
  --embedding-local-only
```

Bat buoc them cac flag moi:

```text
--enable-embedding
--embedding-model BAAI/bge-m3
--embedding-local-only
```

Bat buoc truyen taxonomy bang duong dan tuyet doi:

```text
--taxonomy C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json
```

Ly do: PHP web dang chay trong `C:\xampp\htdocs\topcv_lite`, neu dung relative path `data/taxonomy/skills.json` thi co the bi doc sai thu muc.

## 3. Runtime folder de xuat

Nen luu file tam ngoai web public:

```text
C:\topcv_ai_runtime\
`-- job-{job_id}\
    `-- run-{yyyymmdd-His}\
        |-- jd.txt
        |-- cvs\
        |   |-- application-{application_id}__candidate-{candidate_id}.txt
        |   `-- application-{application_id}__candidate-{candidate_id}.txt
        |-- ranking_results.json
        `-- cli.log
```

Neu hien tai web da co folder runtime khac thi co the giu, nhung phai dam bao:

- Khong nam trong public web neu co the.
- File `.txt` ghi UTF-8.
- Path la absolute path.
- Ten file CV co `application_id` de map nguoc ket qua.

## 4. Format JD text web nen tao

Tu database job, build `jd.txt` dang:

```text
{job_title}

Requirements:
- {requirement_1}
- {requirement_2}
- {experience_requirement}

Nice to have:
- {nice_to_have_1}
- {nice_to_have_2}

Responsibilities:
- {responsibility_1}
- {responsibility_2}
```

Neu database chi co mot field mo ta lon, tao toi thieu:

```text
{job_title}

Requirements:
- {job_description}
```

Khong hard-code JD demo.

## 5. Format CV text web nen tao

Moi ung vien phai co mot file `.txt` trong folder `cvs`.

Ten file de map:

```text
application-{application_id}__candidate-{candidate_id}.txt
```

Noi dung khuyen nghi:

```text
{candidate_name}
{headline_or_position}

Summary:
{summary}

Skills:
- {skill_1}
- {skill_2}

Work Experience:
{title} - {company}
{start_date} - {end_date}
- {description}

Projects:
{project_name}
- {description}

Education:
{education}
```

Neu web chi co CV PDF/DOCX upload ma chua extract text, CLI AI se khong doc truc tiep PDF/DOCX trong flow nay. Can co text da extract hoac CV online structured. Neu chua co text, bo qua candidate do va hien/log ly do ro rang.

## 6. PHP CLI helper mau

Co the tao/sua helper vi du:

```php
<?php

function quote_windows_arg(string $value): string
{
    return '"' . str_replace('"', '""', $value) . '"';
}

function run_ai_screening_cli(string $jdPath, string $cvDir, string $outputJson): array
{
    $aiRoot = 'C:\\SEMANTIC_SKILLS_RESUME';
    $python = $aiRoot . '\\.venv\\Scripts\\python.exe';
    $main = $aiRoot . '\\main.py';
    $taxonomy = $aiRoot . '\\data\\taxonomy\\skills.json';

    putenv('HF_HUB_OFFLINE=1');
    putenv('PYTHONIOENCODING=utf-8');

    $cmd = quote_windows_arg($python)
        . ' ' . quote_windows_arg($main)
        . ' --jd ' . quote_windows_arg($jdPath)
        . ' --cv-dir ' . quote_windows_arg($cvDir)
        . ' --taxonomy ' . quote_windows_arg($taxonomy)
        . ' --output-json ' . quote_windows_arg($outputJson)
        . ' --enable-embedding'
        . ' --embedding-model BAAI/bge-m3'
        . ' --embedding-local-only';

    $outputLines = [];
    $exitCode = 0;
    exec($cmd . ' 2>&1', $outputLines, $exitCode);

    if ($exitCode !== 0) {
        throw new RuntimeException(
            "AI CLI failed with exit code {$exitCode}:\n" . implode("\n", $outputLines)
        );
    }

    if (!is_file($outputJson)) {
        throw new RuntimeException("AI CLI did not create output JSON: {$outputJson}");
    }

    $json = file_get_contents($outputJson);
    $result = json_decode($json, true);

    if (!is_array($result)) {
        throw new RuntimeException("AI CLI output JSON is invalid: " . json_last_error_msg());
    }

    return $result;
}
```

Neu project hien tai dang dung `proc_open`, co the giu `proc_open`, nhung van phai:

- Set env `HF_HUB_OFFLINE=1`.
- Set env `PYTHONIOENCODING=utf-8`.
- Set cwd nen la `C:\SEMANTIC_SKILLS_RESUME`.
- Them cac flags embedding nhu tren.
- Log stdout/stderr khi loi.

## 7. Xu ly thoi gian chay

BGE-M3 la model lon. Goi bang CLI nghia la moi request web co the load model lai.

Can dam bao PHP khong timeout qua som:

```php
set_time_limit(180);
```

Neu web co config timeout rieng cua Apache/PHP, kiem tra them.

Voi demo, CLI chap nhan cham hon API. Sau nay khi chuyen API, model se load mot lan va goi nhanh hon.

## 8. Luu ket qua vao DB

Sau khi CLI tra ve `$result`, can doc:

```php
$result['candidates']
```

Moi candidate co cac field quan trong:

```text
rank
candidate_name
final_score
recommendation
source_file
source_path
review_card
scores
matched_skills
missing_skills
```

Dung `source_file` de lay `application_id`:

```text
application-123__candidate-456.txt
```

Regex goi y:

```php
if (preg_match('/application-(\d+)__candidate-(\d+)\.txt$/', $sourceFile, $m)) {
    $applicationId = (int) $m[1];
    $candidateId = (int) $m[2];
}
```

Sau do luu:

- ai_rank = rank
- ai_score = final_score
- ai_recommendation = recommendation
- ai_review_json = json_encode(review_card, JSON_UNESCAPED_UNICODE)
- ai_screened_at = current datetime

Neu chua muon sua bang applications, tao bang rieng `ai_screening_results`.

## 9. Test CLI doc lap truoc khi test web

Truoc khi bam tren web, hay lay runtime folder ma web tao ra va chay command bang PowerShell:

```powershell
cd C:\SEMANTIC_SKILLS_RESUME
.\.venv\Scripts\Activate.ps1
$env:HF_HUB_OFFLINE='1'
$env:PYTHONIOENCODING='utf-8'

python main.py `
  --jd C:\topcv_ai_runtime\job-10\run-test\jd.txt `
  --cv-dir C:\topcv_ai_runtime\job-10\run-test\cvs `
  --taxonomy C:\SEMANTIC_SKILLS_RESUME\data\taxonomy\skills.json `
  --output-json C:\topcv_ai_runtime\job-10\run-test\ranking_results.json `
  --enable-embedding `
  --embedding-model BAAI/bge-m3 `
  --embedding-local-only
```

Kiem tra output:

```powershell
$result = Get-Content C:\topcv_ai_runtime\job-10\run-test\ranking_results.json -Raw | ConvertFrom-Json
$result.candidates | Select-Object rank,candidate_name,final_score,recommendation,source_file
```

Neu lenh nay fail thi sua runtime file/command truoc, chua test web.

## 10. Test tu web

Sau khi CLI doc lap pass:

1. Vao `http://localhost/topcv_lite/employer/job_candidates.php?job_id=...`
2. Bam nut chay AI ranking.
3. Kiem tra co tao runtime folder khong.
4. Kiem tra co `jd.txt`, folder `cvs`, va `ranking_results.json` khong.
5. Kiem tra DB da luu `ai_rank`, `ai_score`, `ai_recommendation` chua.
6. Kiem tra table ung vien co hien ket qua chua.

Neu loi, UI chi hien message than thien. Loi ky thuat ghi vao log:

```text
AI CLI failed. Please try again later.
```

Log ky thuat nen co:

- command da chay
- exit code
- stdout/stderr
- output json path
- job_id
- runtime folder

## 11. Acceptance criteria

Hoan thanh khi:

- Cursor tim duoc file PHP hien dang goi CLI.
- CLI command da co:
  - `--taxonomy` absolute path.
  - `--enable-embedding`.
  - `--embedding-model BAAI/bge-m3`.
  - `--embedding-local-only`.
- PHP set:
  - `HF_HUB_OFFLINE=1`.
  - `PYTHONIOENCODING=utf-8`.
- JD/CV temp files ghi UTF-8.
- Output JSON duoc tao.
- Web doc JSON va map dung `application_id`.
- UI hien rank/score/recommendation.
- Loi CLI duoc log ro, khong expose stack trace ra UI.

Sau khi task CLI nay pass, moi chuyen sang task API rieng.
```

