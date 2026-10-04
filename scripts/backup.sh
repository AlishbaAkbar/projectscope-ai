#!/bin/bash
# ============================================
# PROJECTSCOPE AI — Database Backup
# ============================================

set -e

# Config
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/projectscope_${TIMESTAMP}.sql.gz"

# Load env
if [ -f .env.prod ]; then
    export $(cat .env.prod | grep -v '^#' | xargs)
fi

# Create backup dir
mkdir -p "${BACKUP_DIR}"

echo "🔄 Starting database backup..."
echo "   Target: ${BACKUP_FILE}"

# Backup
docker compose -f docker-compose.prod.yml exec -T postgres \
    pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" \
    | gzip > "${BACKUP_FILE}"

# Verify
if [ -f "${BACKUP_FILE}" ]; then
    SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
    echo "✅ Backup complete: ${SIZE}"
else
    echo "❌ Backup failed!"
    exit 1
fi

# Cleanup old backups
echo "🧹 Cleaning backups older than ${RETENTION_DAYS} days..."
find "${BACKUP_DIR}" -name "projectscope_*.sql.gz" -mtime +${RETENTION_DAYS} -delete
echo "✅ Cleanup complete"

echo ""
echo "📊 Backups in ${BACKUP_DIR}:"
ls -lh "${BACKUP_DIR}" | tail -5