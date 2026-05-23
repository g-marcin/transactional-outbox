#!/bin/bash
set -e

cd /app

# Start the app
uvicorn main:app --host 0.0.0.0 --port 8000 &
APP_PID=$!

# Wait for app to be ready
sleep 3

# Seed data if requested
if [ "$SEED_DATA" = "true" ]; then
    echo "[ENTRYPOINT] Seeding database with $SEED_COUNT orders..."
    cd /scripts
    python -c "
import sys
from seed_orders import seed_orders
seed_orders(count=$SEED_COUNT, delay=0.05, base_url='http://localhost:8000')
    " || echo "[ENTRYPOINT] Seeding failed"
    echo "[ENTRYPOINT] Seeding complete"
fi

# Keep app running
wait $APP_PID
