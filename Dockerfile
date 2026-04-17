FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV TZ=Europe/Kyiv

COPY pyproject.toml .
COPY .python-version .
COPY uv.lock .

RUN uv pip install --system --no-cache -r pyproject.toml flet-cli flet-web flet-desktop

COPY . .

EXPOSE 8080

CMD ["flet", "run", "--web", "--host", "0.0.0.0", "--port", "8080"]
