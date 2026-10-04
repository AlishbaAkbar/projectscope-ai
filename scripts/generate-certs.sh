#!/bin/bash
# ============================================
# Generate self-signed TLS certificates (DEV ONLY)
# ============================================

set -e

CERT_DIR="./nginx/certs"
DOMAIN="${DOMAIN:-localhost}"

mkdir -p "${CERT_DIR}"

echo "🔐 Generating self-signed certificate for ${DOMAIN}..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "${CERT_DIR}/privkey.pem" \
    -out "${CERT_DIR}/fullchain.pem" \
    -subj "/C=PK/ST=Punjab/L=Lahore/O=ProjectScope/CN=${DOMAIN}" \
    -addext "subjectAltName=DNS:${DOMAIN},DNS:www.${DOMAIN},DNS:localhost"

echo "✅ Certificate generated:"
echo "   - ${CERT_DIR}/privkey.pem"
echo "   - ${CERT_DIR}/fullchain.pem"