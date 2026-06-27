# AWS EC2 Docker Deploy Bundle

Bo file nay dung de deploy ca:

- `Semantic-Skills-based-Resume-Screening-System` (AI FastAPI)
- `topcv-lite` (web PHP)

Theo dung kieu ma code hien tai dang can:

- web goi AI qua FastAPI
- web can doc taxonomy base
- web va AI can dung chung runtime taxonomy (`skills_merged.json`)

## 1. Cau truc clone tren EC2

Tren EC2, ban nen clone dung theo cau truc nay:

```text
/opt/topcv-stack/repos/
|-- semantic_skills_resume/
|   `-- deploy/aws-ec2-docker/
`-- topcv_lite/
```

Vi `docker-compose.yml` trong bo deploy nay dang tham chieu den web repo theo duong dan sibling `../../../topcv_lite`.

## 2. Clone code

```bash
sudo mkdir -p /opt/topcv-stack/repos
sudo chown -R $USER:$USER /opt/topcv-stack
cd /opt/topcv-stack/repos

git clone https://github.com/Zapkadz/Semantic-Skills-based-Resume-Screening-System.git semantic_skills_resume
git clone https://github.com/Zapkadz/topcv-lite.git topcv_lite
```

## 3. Cai Docker tren Ubuntu

```bash
cd /opt/topcv-stack/repos/semantic_skills_resume/deploy/aws-ec2-docker
chmod +x scripts/bootstrap-ubuntu.sh
./scripts/bootstrap-ubuntu.sh
newgrp docker
docker compose version
```

## 4. Khoi tao file local

```bash
chmod +x scripts/check-layout.sh
./scripts/check-layout.sh
chmod +x scripts/init-stack.sh
./scripts/init-stack.sh
```

Sau do sua:

- `.env`
- `config/db.local.php`
- `config/ai.local.php`
- `config/ai_screening.local.php`
- `config/ai_taxonomy.local.php`

### `config/db.local.php`

- `host` phai la `db`
- `base_url` nen de:
  - `http://YOUR_EC2_IP/topcv_lite/`
  - hoac domain cua ban: `https://your-domain/topcv_lite/`

### `config/ai_screening.local.php`

Da dat san:

- `api_url = http://ai-api:8000/screening`
- `health_url = http://ai-api:8000/health`
- `recommend_jobs_api_url = http://ai-api:8000/recommend-jobs`

Dung voi Docker network noi bo.

### `config/ai_taxonomy.local.php`

Da cau hinh san:

- base taxonomy doc tu AI repo
- merged taxonomy doc/ghi tai volume runtime dung chung

Neu admin duyet taxonomy tren web, file `skills_merged.json` se duoc xuat vao:

```text
./volumes/topcv_ai_runtime/taxonomy/skills_merged.json
```

va AI screening se nhin thay file nay thong qua runtime path dung chung.

## 5. Build va chay

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f ai-api
```

## 5.1. Test local tren Windows

Neu test tren may Windows hien tai, web repo dang nam o:

```text
C:\xampp\htdocs\topcv_lite
```

va XAMPP co the dang chiem port `80`, nen co the dung override local:

```powershell
copy docker-compose.local.example.yml docker-compose.local.yml
docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
```

Khi do web se mo tai:

```text
http://localhost:8088/topcv_lite/
```

File `docker-compose.local.yml` da nam trong `.gitignore`, khong commit.

## 6. Import database

Neu file `topcv_lite.sql` trong repo la du lieu ban muon dung:

```bash
chmod +x scripts/import-db.sh
./scripts/import-db.sh
```

Neu ban co file SQL moi hon:

```bash
./scripts/import-db.sh /path/to/your-latest-dump.sql
```

## 7. Copy uploads tu local len server

GitHub khong mang:

- `uploads/`
- `storage/`

Ban can copy du lieu thuc te len cac thu muc nay:

- `./volumes/topcv_uploads/`
- `./volumes/topcv_storage/`

Neu muon giu logo cong ty, CV PDF, avatar, snapshot..., day la buoc bat buoc.

## 8. Warm-up model BGE-M3

Lan dau model se tai ve Hugging Face cache:

```bash
chmod +x scripts/warmup-bge.sh
./scripts/warmup-bge.sh
```

Sau khi tai xong, cache nam trong:

```text
./volumes/hf_cache/
```

## 9. Test nhanh

### AI health

```bash
chmod +x scripts/test-health.sh
./scripts/test-health.sh
```

### Web

Mo:

```text
http://YOUR_EC2_IP/topcv_lite/
```

## 10. Update sau nay

```bash
chmod +x scripts/pull-and-rebuild.sh
./scripts/pull-and-rebuild.sh
```

## 11. Ghi chu quan trong

### Web hien tai dang hardcode `/topcv_lite/`

File [includes/header.php](../../../topcv_lite/includes/header.php) dang hardcode base path `/topcv_lite/`.

Vi vay deploy an toan nhat hien tai la:

- chay app o `http://IP/topcv_lite/`
- khong nen doi sang root `/` ngay neu chua refactor base path

### AI path chung cho taxonomy

Web hien tai can:

- doc base taxonomy
- doc merged taxonomy
- ghi merged taxonomy khi admin duyet

Nen web container dang mount:

- AI repo read-only vao `/opt/semantic_skills_resume`
- runtime volume vao `/var/lib/topcv_ai_runtime`

Day la chu y rat quan trong, khong nen bo di.

### GPT vision va Imagick

Web Dockerfile hien tai da ho tro:

- PHP cURL
- `pdo_mysql`
- `mbstring`
- `gd`

nhung chua cai them `Imagick`.

Dieu nay co nghia la:

- CV import bang GPT vision van co the chay theo duong PDF/file API
- fallback rasterize moi trang PDF thanh image trong `PdfVisionRasterizer` chua duoc bat tren stack nay

Neu sau nay ban muon bat manh hon cho PDF scan kho, minh co the lam them mot phase nho de cai `Imagick` + policy phu hop cho Docker production.

### Secrets

Khong commit cac file sau:

- `.env`
- `config/db.local.php`
- `config/ai.local.php`
- `config/ai_screening.local.php`
- `config/ai_taxonomy.local.php`
