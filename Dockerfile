# =============================================================================
# SalaryAxis — Multi-stage Dockerfile
# =============================================================================
# Stage 1 (frontend-builder) : Node 20 builds React with Vite → /app/static
# Stage 2 (runtime)          : Python 3.12 slim + Gunicorn serves everything
#
# Build:  docker build -t salaryaxis .
# Run:    docker run -p 8000:8000 salaryaxis
# =============================================================================

# ── Stage 1: React build ──────────────────────────────────────────────────────
FROM node:20-slim AS frontend-builder

WORKDIR /build

# Layer-cache: install deps before copying source
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --prefer-offline --no-audit

# Copy full frontend source
COPY frontend/ ./

# Vite builds to ../static relative to frontend/ → /static at project root.
# We override outDir here to put the output exactly where we want it.
RUN npm run build -- --outDir /app/static && \
    echo "✓ Frontend built: $(ls /app/static | wc -l) files"


# ── Stage 2: Python runtime ───────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# System deps (minimal — curl for healthcheck only)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Python deps — install before copying application source (better layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn==22.0.0

# Copy application source
COPY --chown=appuser:appuser . .

# Copy built React SPA from Stage 1 into Flask's static folder
COPY --from=frontend-builder /app/static /app/static

# Writable output dir for pipeline CSVs and ONS cache
RUN mkdir -p /app/output /app/output/.cache && \
    chown -R appuser:appuser /app/output

USER appuser

EXPOSE 8000

# Healthcheck: Flask /api/v1/health (90s start-period for DataService cold-start)
HEALTHCHECK --interval=30s --timeout=10s --start-period=90s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:app"]
