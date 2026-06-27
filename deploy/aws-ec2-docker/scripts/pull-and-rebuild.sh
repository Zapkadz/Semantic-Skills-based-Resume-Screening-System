#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
AI_REPO_DIR="$(cd "${DEPLOY_DIR}/../.." && pwd)"
WEB_REPO_DIR="$(cd "${DEPLOY_DIR}/../../../topcv_lite" && pwd)"

git -C "${AI_REPO_DIR}" pull
git -C "${WEB_REPO_DIR}" pull

cd "${DEPLOY_DIR}"
docker compose up -d --build

echo "Pulled both repos and rebuilt the stack."
