# ===========================================
# Stage 1: Builder
# Purpose: Install and compile dependencies
# ===========================================
FROM python:3.11-slim AS builder

# Install system dependencies needed for building python packages
# -build-essential: Gcc compiler for C extensions (numpy, pandas, etc.
# -libpq-dev: PostgreSQL client libraries for psycopg2
# -curl: for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
# Why Poetry in Docker? Dependency resolution and lock file guarantees exact versions
RUN pip install --no-cache-dir poetry==1.8.3

WORKDIR /app

# Copy dependency files FIRST(layer caching optimization)
# If these files don't change, Docker reuses this layer (saves 2-3 minutes
COPY  pyproject.toml poetry.lock ./

# Configure Poetry for Docker environment
# - virtualenvs.create false: Don't create venv (container Is the venv)
# - no-interaction: Disable prompts for input
# - no-ansi: Clean logs in CI/CD
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --no-root
# --no-root: Don't install the current package (we'll do it in the next stage)

# ===========================================
# Stage 2: Runtime
# Purpose: Minimal production image
# ===========================================
FROM python:3.11-slim AS runtime

# Install runtime system dependencies (no build tools)
# - libpq5: PostgreSQL client library (runtime, not dev version)
# - curl: For health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
# Why? Containers is compromised, attacker has limited privileges
# If container is compromised, attacker has limited privileges
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy installed Python packages from builder stage
# This is the magic: we built in stage 1, now we just copy the result
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python#.11/site-packages
COPY --from=builder /usr/local /usr/local

# Copy application code
# .dockerignore prevents. copying .venv/, __pycache__?, etc.
COPY --chown=appuser:appuser app/ ./app/

# Create directory for model storage (K8s will mount volume here)
RUN mkdir -p /models && chown appuser:appuser /models

# Switch to non-root user
USER appuser

# Expose port (documentation only, doesn't actually publish)
EXPOSE 8000

# Health check for Docker (K8s has its own health checks, but good practice)
# This runs every 30 seconds to verify container is healthy
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Environment variables (can be overridden by K8s)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    PATH="/usr/local/bin:${PATH}"

# Command variables (can be overridden by K8s)
# --host 0.0.0.0: Listen on all interfaces (required in containers)
# --port 8000: Match EXPOSE and ENV
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]