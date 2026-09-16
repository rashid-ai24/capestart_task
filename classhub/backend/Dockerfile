# ============================================
# ClassHub Backend Dockerfile
# Multi-stage build for Django Application
# ============================================

# ============================================
# Stage 1: Base Python Image
# ============================================
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# ============================================
# Stage 2: Development Image
# ============================================
FROM base AS development

# Install development dependencies
COPY requirements/ .
RUN pip install -r development.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ============================================
# Stage 3: Production Dependencies
# ============================================
FROM base AS production-deps

# Install production dependencies
COPY requirements/ .
RUN pip install -r production.txt

# ============================================
# Stage 4: Production Image
# ============================================
FROM production-deps AS production

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/media /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run with gunicorn
CMD ["gunicorn", "config.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--threads", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
