import os

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/outbox_demo",
)

POLL_INTERVAL_SECONDS = 2
MAX_RETRIES = 3
QUEUE_LATENCY_SECONDS = 0.5
