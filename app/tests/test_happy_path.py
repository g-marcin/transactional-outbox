from db import get_connection
from enums import OutboxStatus
from services.orders import create_order_with_event
from worker import OutboxWorker


def _fetch_outbox(row_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT status, retry_count, processed_at FROM outbox WHERE id = %s",
                (row_id,),
            )
            return cursor.fetchone()
    finally:
        conn.close()


def _count(table: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            return cursor.fetchone()[0]
    finally:
        conn.close()


def test_order_and_outbox_inserted_then_worker_marks_processed():
    result = create_order_with_event("laptop", 1)

    assert _count("orders") == 1
    status, retry_count, processed_at = _fetch_outbox(result["outbox_id"])
    assert status == OutboxStatus.PENDING
    assert retry_count == 0
    assert processed_at is None

    OutboxWorker()._process_batch()

    status, retry_count, processed_at = _fetch_outbox(result["outbox_id"])
    assert status == OutboxStatus.PROCESSED
    assert retry_count == 0
    assert processed_at is not None
