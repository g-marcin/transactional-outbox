import threading
import time
from typing import Optional

from config import MAX_RETRIES, POLL_INTERVAL_SECONDS
from db import transaction
from publisher import send_to_queue
from repositories import outbox as outbox_repo


class OutboxWorker:
    def __init__(
        self,
        poll_interval: float = POLL_INTERVAL_SECONDS,
        max_retries: int = MAX_RETRIES,
    ):
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None

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
            for row_id, payload in outbox_repo.fetch_pending(cursor):
                self._dispatch(cursor, row_id, payload)

    def _dispatch(self, cursor, row_id: int, payload: dict) -> None:
        try:
            success = send_to_queue(payload)
            if not success:
                raise Exception("Queue returned False")
            outbox_repo.mark_processed(cursor, row_id)
            print(f"[WORKER] Processed outbox id={row_id}")
        except Exception as e:
            outbox_repo.mark_failed(cursor, row_id, str(e), self.max_retries)
            print(f"[WORKER] Error processing id={row_id}: {e}")
