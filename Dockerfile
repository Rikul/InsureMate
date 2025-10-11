# syntax=docker/dockerfile:1.6
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install build dependencies and create virtual environment
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && python -m venv /opt/venv \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["flask", "run"]
