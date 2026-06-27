#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
AI_REPO_DIR="$(cd "${DEPLOY_DIR}/../.." && pwd)"
WEB_REPO_DIR="$(cd "${DEPLOY_DIR}/../../../topcv_lite" 2>/dev/null && pwd || true)"

fail=0

check_file() {
  local path="$1"
  if [ ! -f "${path}" ]; then
    echo "Missing file: ${path}"
    fail=1
  else
    echo "OK file: ${path}"
  fi
}

check_dir() {
  local path="$1"
  if [ ! -d "${path}" ]; then
    echo "Missing dir: ${path}"
    fail=1
  else
    echo "OK dir: ${path}"
  fi
}

echo "Checking expected stack layout..."
check_dir "${AI_REPO_DIR}"
check_dir "${WEB_REPO_DIR}"

check_file "${AI_REPO_DIR}/api.py"
check_file "${AI_REPO_DIR}/requirements.txt"
check_file "${AI_REPO_DIR}/data/taxonomy/skills.json"

check_file "${WEB_REPO_DIR}/composer.json"
check_file "${WEB_REPO_DIR}/topcv_lite.sql"
check_file "${WEB_REPO_DIR}/includes/ai_screening_config.php"

check_file "${DEPLOY_DIR}/docker-compose.yml"
check_file "${DEPLOY_DIR}/ai/Dockerfile"
check_file "${DEPLOY_DIR}/web/Dockerfile"

if [ "${fail}" -ne 0 ]; then
  echo
  echo "Layout check failed. Re-check clone paths."
  exit 1
fi

echo
echo "Layout check passed."
