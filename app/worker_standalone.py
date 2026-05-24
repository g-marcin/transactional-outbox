"""Standalone worker process for outbox polling."""

import signal
import sys
import time

from .config import MAX_RETRIES, POLL_INTERVAL_SECONDS
from .worker import OutboxWorker


def main():
    print("[WORKER] Starting standalone outbox worker", flush=True)
    sys.stdout.flush()

    worker = OutboxWorker(
        poll_interval=POLL_INTERVAL_SECONDS,
        max_retries=MAX_RETRIES,
    )

    def signal_handler(signum, frame):
        print("[WORKER] Received shutdown signal", flush=True)
        worker.stop()
        sys.exit(0)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    worker.start()
    print("[WORKER] Worker started, keeping process alive", flush=True)
    sys.stdout.flush()

    # Keep main thread alive
    try:
        counter = 0
        while True:
            time.sleep(5)
            counter += 1
            print(f"[WORKER] Main loop heartbeat #{counter}", flush=True)
    except KeyboardInterrupt:
        print("[WORKER] Interrupted", flush=True)
        worker.stop()


if __name__ == "__main__":
    main()
