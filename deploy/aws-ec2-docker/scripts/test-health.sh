#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${DEPLOY_DIR}"

echo "== docker compose ps =="
docker compose ps

echo
echo "== AI health =="
curl -fsS http://127.0.0.1:8000/health
echo

echo
echo "== Web root =="
curl -I http://127.0.0.1/
