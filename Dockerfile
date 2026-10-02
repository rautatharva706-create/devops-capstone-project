# ==========================================================
# Stage 1: Build & Dependency Installation
# ==========================================================
FROM python:3.9-slim AS builder

WORKDIR /app

# Install system dependencies needed for compiling python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependencies file to leverage Docker layer caching
COPY requirements.txt .

# Compile wheels for dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ==========================================================
# Stage 2: Final Secure Runner Image
# ==========================================================
FROM python:3.9-slim AS runner

WORKDIR /app

# Create a non-root system user for security isolation
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

# Copy installed dependencies from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY requirements.txt .

# Ensure appuser's local bin is in PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy all application files to the container
COPY . .

# Change ownership of working directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user context
USER appuser

# Expose microservice listening port
EXPOSE 8080

# Environment variables for Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Start the application using Gunicorn for production scalability
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
