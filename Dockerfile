FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libz-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src ./src
COPY scripts ./scripts
COPY README.md ./

# Expose API port
EXPOSE 8000

# Default entrypoint: API
CMD ["uvicorn", "src.adapters.driving.api:app", "--host", "0.0.0.0", "--port", "8000"]

