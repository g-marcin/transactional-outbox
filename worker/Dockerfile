FROM python:3.11-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
WORKDIR /app

CMD ["sh", "-c", "python -u worker_standalone.py 2>&1"]
