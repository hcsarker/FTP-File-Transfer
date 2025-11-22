# Production Dockerfile for FTP File Transfer app
# Using slim Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system deps (if needed later add: build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create runtime dirs (ensure exist even if host volumes mounted)
RUN mkdir -p uploads_connection_oriented uploads_connectionless temp

# Expose web port (default 5000) - can be overridden at runtime
ENV WEB_PORT=5000 \
    CO_PORT=2121 \
    CL_PORT=2021 \
    FLASK_DEBUG=0
EXPOSE 5000

# Use gunicorn for production serving (adjust workers as needed)
# Binding to 0.0.0.0:$WEB_PORT so container accessible externally
CMD exec gunicorn --bind 0.0.0.0:${WEB_PORT} --workers 3 --threads 4 --timeout 120 app:app
