# ==============================================================================
# Multi-stage Dockerfile for ML API Production
# ==============================================================================
# Build optimizations:
# - Multi-stage build to reduce final image size
# - Wheel compilation in builder stage for faster installs
# - Non-root user for security
# - Minimal runtime dependencies
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Builder - Compile dependencies
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build tools required for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (Docker layer caching optimization)
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ------------------------------------------------------------------------------
# Stage 2: Runtime - Production image
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# Metadata
LABEL maintainer="ML API Team" \
      version="0.1.0" \
      description="Production ML API for image classification"

# Security and performance environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/opt/venv/bin:$PATH" \
    # Application settings
    MODEL_DEVICE=cpu \
    LOG_LEVEL=INFO \
    LOG_FORMAT=json

# Create non-root user for security (best practice)
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser && \
    mkdir -p /app && \
    chown -R appuser:appgroup /app

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code (owned by non-root user)
COPY --chown=appuser:appgroup ./app ./app
COPY --chown=appuser:appgroup ./imagenet_classes.txt ./imagenet_classes.txt

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 8000

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Default command - production server
# Use PORT environment variable from Cloud Run (defaults to 8000 for local)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1
