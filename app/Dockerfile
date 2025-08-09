# Use an official Python runtime as base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# --- Security: Create non-root user and group for Celery & Web ---
RUN addgroup --gid 1000 celerygroup && \
    adduser --uid 1000 --gid 1000 --system --group celeryuser

# Switch to non-root user
USER celeryuser

# Expose FastAPI port
EXPOSE 8000

# Default command for web service (overridden by celery_worker in docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
