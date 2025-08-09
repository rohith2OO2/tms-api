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

# Create group and user with specific GID and UID
RUN groupadd -g 1000 celerygroup \
 && useradd -r -u 1000 -g celerygroup celeryuser

# Switch to non-root user
USER celeryuser

# Expose FastAPI port
EXPOSE 8000

# Default command for web service (overridden for celery_worker)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
