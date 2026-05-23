from __future__ import annotations

import os
import random
import threading
import time

from config import MAX_RETRIES, POLL_INTERVAL_SECONDS
from db import transaction
from publisher import send_to_queue
from repositories import outbox as outbox_repo

_global_worker: OutboxWorker | None = None


class OutboxWorker:
    def __init__(
        self,
        poll_interval: float = POLL_INTERVAL_SECONDS,
        max_retries: int = MAX_RETRIES,
    ):
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("[APP] Background worker started")

    def stop(self) -> None:
        self._stop.set()

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                self._process_batch()
            except Exception as e:
                print(f"[WORKER] Exception in loop: {e}")
            time.sleep(self.poll_interval)

    def _process_batch(self) -> None:
        with transaction() as (_, cursor):
            pending = outbox_repo.fetch_pending(cursor)
            if pending:
                print(f"[WORKER] Found {len(pending)} pending items")
                for row_id, payload in pending:
                    self._dispatch(cursor, row_id, payload)
            else:
                print("[WORKER] Poll: No pending items")

    def _dispatch(self, cursor, row_id: int, payload: dict) -> None:
        # Chaos injection: simulate processing failures
        chaos_rate = float(os.environ.get("WORKER_CHAOS", "0"))
        if random.random() < chaos_rate:
            error_msg = "Simulated broker failure (chaos mode)"
            outbox_repo.mark_failed(cursor, row_id, error_msg, self.max_retries)
            print(f"[WORKER] Chaos: Failed id={row_id} (will retry)")
            return

        try:
            success = send_to_queue(payload)
            if not success:
                raise Exception("Queue returned False")
            outbox_repo.mark_processed(cursor, row_id)
            print(f"[WORKER] Processed outbox id={row_id}")
        except Exception as e:
            outbox_repo.mark_failed(cursor, row_id, str(e), self.max_retries)
            print(f"[WORKER] Error processing id={row_id}: {e}")


def set_worker(worker: OutboxWorker) -> None:
    """Register worker instance for admin access."""
    global _global_worker
    _global_worker = worker


def get_worker() -> OutboxWorker | None:
    """Get registered worker instance."""
    return _global_worker
