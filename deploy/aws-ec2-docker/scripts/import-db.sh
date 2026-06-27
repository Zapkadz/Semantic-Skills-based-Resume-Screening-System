#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DEFAULT_SQL="${DEPLOY_DIR}/../../../topcv_lite/topcv_lite.sql"
SQL_PATH="${1:-${DEFAULT_SQL}}"

if [ ! -f "${SQL_PATH}" ]; then
  echo "SQL file not found: ${SQL_PATH}" >&2
  exit 1
fi

cd "${DEPLOY_DIR}"

set -a
source ./.env
set +a

docker compose exec -T db sh -c \
  'mariadb -uroot -p"$MARIADB_ROOT_PASSWORD" "$MARIADB_DATABASE"' < "${SQL_PATH}"

echo "Imported database from ${SQL_PATH}"
