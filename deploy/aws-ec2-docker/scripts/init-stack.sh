#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

mkdir -p "${DEPLOY_DIR}/config"
mkdir -p "${DEPLOY_DIR}/volumes/mysql"
mkdir -p "${DEPLOY_DIR}/volumes/hf_cache"
mkdir -p "${DEPLOY_DIR}/volumes/topcv_ai_runtime/taxonomy"
mkdir -p "${DEPLOY_DIR}/volumes/topcv_uploads"
mkdir -p "${DEPLOY_DIR}/volumes/topcv_storage"

copy_if_missing() {
  local source_path="$1"
  local target_path="$2"
  if [ ! -f "${target_path}" ]; then
    cp "${source_path}" "${target_path}"
    echo "Created ${target_path}"
  else
    echo "Keep existing ${target_path}"
  fi
}

copy_if_missing "${DEPLOY_DIR}/.env.example" "${DEPLOY_DIR}/.env"
copy_if_missing "${DEPLOY_DIR}/config/db.local.example.php" "${DEPLOY_DIR}/config/db.local.php"
copy_if_missing "${DEPLOY_DIR}/config/ai.local.example.php" "${DEPLOY_DIR}/config/ai.local.php"
copy_if_missing "${DEPLOY_DIR}/config/ai_screening.local.example.php" "${DEPLOY_DIR}/config/ai_screening.local.php"
copy_if_missing "${DEPLOY_DIR}/config/ai_taxonomy.local.example.php" "${DEPLOY_DIR}/config/ai_taxonomy.local.php"

echo
echo "Next:"
echo "1. Edit ${DEPLOY_DIR}/.env"
echo "2. Edit ${DEPLOY_DIR}/config/*.php"
echo "3. Run: docker compose up -d --build"
