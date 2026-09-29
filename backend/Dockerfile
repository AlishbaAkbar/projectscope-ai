# Start from the supported Python slim base image.
FROM python:3.13-slim

# Keep application files and the SQLite data directory under /app.
WORKDIR /app

# Install native build tools and curl for Python dependencies and health checks.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies separately so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the application and database seeding script.
COPY app/ ./app/
COPY seed.py ./

# Create writable SQLite storage, then run the service without root privileges.
RUN mkdir -p /app/data && \
    useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Check that the API health endpoint is responding.
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
