FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv pip install --system -r pyproject.toml flet-cli flet-web flet-desktop

COPY . .

EXPOSE 8080

CMD ["flet", "run", "--web", "--host", "0.0.0.0", "--port", "8080"]