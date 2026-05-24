#!/bin/bash
set -e

cd /app

# Seed data if requested
if [ "$SEED_DATA" = "true" ]; then
    echo "[ENTRYPOINT] Waiting for API to be ready..."
    sleep 5
    echo "[ENTRYPOINT] Seeding database with $SEED_COUNT orders..."
    cd /scripts
    python -c "
import sys
from seed_orders import seed_orders
seed_orders(count=$SEED_COUNT, delay=0.05, base_url='http://localhost:8000')
    " || echo "[ENTRYPOINT] Seeding failed"
    echo "[ENTRYPOINT] Seeding complete"
fi

# Start the app
exec uvicorn main:app --host 0.0.0.0 --port 8000
