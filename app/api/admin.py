from fastapi import APIRouter
from schemas import AdminResponse, OutboxStats
from worker import get_worker

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/process-pending",
    response_model=AdminResponse,
    summary="Trigger worker to process pending entries",
)
def process_pending() -> AdminResponse:
    """Manually trigger worker to process pending outbox entries.

    Useful when worker was down and needs to catch up on processing.
    """
    worker = get_worker()
    if not worker:
        return AdminResponse(message="Worker not initialized", status="error")

    worker._process_batch()
    return AdminResponse(message="Triggered batch processing", status="ok")


@router.get(
    "/outbox-stats",
    response_model=OutboxStats,
    summary="Get outbox event statistics",
)
def outbox_stats() -> OutboxStats:
    """Retrieve current outbox statistics.

    Returns counts of pending, processed, and failed outbox entries.
    """
    from db import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT status, COUNT(*) as count
                FROM outbox
                GROUP BY status
                ORDER BY status
                """
            )
            stats = {row[0]: row[1] for row in cursor.fetchall()}
        return OutboxStats(
            pending=stats.get("PENDING", 0),
            processed=stats.get("PROCESSED", 0),
            failed=stats.get("FAILED", 0),
            total=sum(stats.values()),
        )
    finally:
        conn.close()
