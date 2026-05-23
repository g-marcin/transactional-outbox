FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /

COPY app/requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

COPY app /app
COPY scripts /scripts

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
