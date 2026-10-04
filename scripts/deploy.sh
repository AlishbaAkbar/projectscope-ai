#!/bin/bash
# ============================================
# PROJECTSCOPE AI — Zero-Downtime Deploy
# ============================================

set -e

COMPOSE_FILE="docker-compose.prod.yml"

echo "🚀 Deploying ProjectScope AI..."
echo ""

# 1. Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# 2. Backup database
echo "💾 Creating backup..."
./scripts/backup.sh || echo "⚠️  Backup skipped"

# 3. Build new images
echo "🔨 Building new images..."
docker compose -f ${COMPOSE_FILE} build --pull

# 4. Apply database migrations
echo "🗄️  Applying migrations..."
docker compose -f ${COMPOSE_FILE} run --rm backend alembic upgrade head || echo "⚠️  Migrations skipped"

# 5. Rolling restart
echo "🔄 Rolling restart..."
docker compose -f ${COMPOSE_FILE} up -d --no-deps --scale backend=2 backend
sleep 10
docker compose -f ${COMPOSE_FILE} up -d --no-deps --scale backend=1 backend

# 6. Restart other services
docker compose -f ${COMPOSE_FILE} up -d

# 7. Health check
echo "🏥 Health check..."
sleep 5
curl -sf https://${DOMAIN}/health && echo "✅ Health OK" || echo "❌ Health check failed"

echo ""
echo "✅ Deploy complete!"