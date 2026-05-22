import worker as worker_module
from db import get_connection
from enums import OutboxStatus
from services.orders import create_order_with_event
from worker import OutboxWorker


def _fetch_status(row_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT status, retry_count, error_message FROM outbox WHERE id = %s",
                (row_id,),
            )
            return cursor.fetchone()
    finally:
        conn.close()


def test_worker_retries_then_marks_failed_after_max_retries(monkeypatch):
    def always_fail(payload):
        raise RuntimeError("broker down")

    monkeypatch.setattr(worker_module, "send_to_queue", always_fail)

    outbox_id = create_order_with_event("laptop", 1)["outbox_id"]
    worker = OutboxWorker(max_retries=3)

    worker._process_batch()
    status, retry, err = _fetch_status(outbox_id)
    assert status == OutboxStatus.PENDING
    assert retry == 1
    assert "broker down" in err

    worker._process_batch()
    status, retry, _ = _fetch_status(outbox_id)
    assert status == OutboxStatus.PENDING
    assert retry == 2

    worker._process_batch()
    status, retry, _ = _fetch_status(outbox_id)
    assert status == OutboxStatus.FAILED
    assert retry == 3
