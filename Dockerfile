FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev
RUN uv pip install --python /app/.venv flet-web

FROM python:3.12-slim-bookworm

ENV TZ=Europe/Kyiv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    FLET_FORCE_WEB_SERVER=true

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && groupadd -g 900 appuser \
    && useradd -u 900 -g appuser -m -s /bin/bash appuser \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder --chown=appuser:appuser /app /app

USER appuser

EXPOSE 8000

CMD ["python", "src/main.py"]
