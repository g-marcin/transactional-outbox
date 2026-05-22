import json
from datetime import datetime
from typing import List, Tuple

from enums import OutboxStatus


def insert_event(cursor, aggregate_type: str, payload: dict) -> int:
    cursor.execute(
        """
        INSERT INTO outbox (aggregate_type, payload, status)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (aggregate_type, json.dumps(payload), OutboxStatus.PENDING),
    )
    return cursor.fetchone()[0]


def fetch_pending(cursor) -> List[Tuple[int, dict]]:
    cursor.execute(
        """
        SELECT id, payload FROM outbox
        WHERE status = %s
        ORDER BY created_at
        FOR UPDATE SKIP LOCKED
        """,
        (OutboxStatus.PENDING,),
    )
    return cursor.fetchall()


def mark_processed(cursor, row_id: int) -> None:
    cursor.execute(
        """
        UPDATE outbox
        SET status = %s, processed_at = %s
        WHERE id = %s
        """,
        (OutboxStatus.PROCESSED, datetime.now(), row_id),
    )


def mark_failed(cursor, row_id: int, error: str, max_retries: int) -> None:
    cursor.execute("SELECT retry_count FROM outbox WHERE id = %s", (row_id,))
    retry_count = cursor.fetchone()[0] + 1
    new_status = (
        OutboxStatus.FAILED if retry_count >= max_retries else OutboxStatus.PENDING
    )
    cursor.execute(
        """
        UPDATE outbox
        SET retry_count = %s, status = %s, error_message = %s
        WHERE id = %s
        """,
        (retry_count, new_status, error, row_id),
    )
