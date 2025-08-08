# Use an official Python runtime as base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY ./app ./app

# Expose the port FastAPI runs on
EXPOSE 8000

# Run uvicorn as default command with reload during development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
