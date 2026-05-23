import pytest
from db import get_connection
from repositories import outbox as outbox_repo
from services.orders import create_order_with_event


def _count(table: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row = cursor.fetchone()
            return int(row[0])
    finally:
        conn.close()


def test_outbox_insert_failure_rolls_back_the_order(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("simulated outbox insert failure")

    monkeypatch.setattr(outbox_repo, "insert_event", boom)

    with pytest.raises(RuntimeError, match="simulated outbox insert failure"):
        create_order_with_event("laptop", 1)

    # The outbox pattern's atomicity guarantee: if event insert fails,
    # the order insert must roll back too — both rows or neither.
    assert _count("orders") == 0
    assert _count("outbox") == 0
