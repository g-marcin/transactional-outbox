from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/process-pending")
def process_pending() -> dict:
    """Manually trigger worker to process pending outbox entries.

    Useful when worker was down and needs to catch up.
    """
    from worker import get_worker

    worker = get_worker()
    if not worker:
        return {"message": "Worker not initialized", "status": "error"}

    worker._process_batch()
    return {"message": "Triggered batch processing", "status": "ok"}


@router.get("/outbox-stats")
def outbox_stats() -> dict:
    """Get outbox statistics by status."""
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
        return {
            "pending": stats.get("PENDING", 0),
            "processed": stats.get("PROCESSED", 0),
            "failed": stats.get("FAILED", 0),
            "total": sum(stats.values()),
        }
    finally:
        conn.close()
