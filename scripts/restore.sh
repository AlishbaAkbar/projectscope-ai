#!/usr/bin/env bash
# Restore database from a backup file
# Usage: ./scripts/restore.sh ./backups/projectscope_20261003_120000.sql.gz

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: $0 <backup-file.sql.gz>"
    exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "🔄 Restoring database from $BACKUP_FILE..."

gunzip -c "$BACKUP_FILE" | docker compose -f docker-compose.prod.yml --env-file .env.prod exec -T postgres \
    psql -U "${POSTGRES_USER:-projectscope}" -d "${POSTGRES_DB:-projectscope}"

echo "✅ Restore complete."