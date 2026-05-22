from datetime import datetime

from db import transaction
from repositories import orders as orders_repo
from repositories import outbox as outbox_repo


def create_order_with_event(item: str, quantity: int) -> dict:
    with transaction() as (_, cursor):
        order_id = orders_repo.insert_order(cursor, item, quantity)
        payload = {
            "order_id": order_id,
            "item": item,
            "quantity": quantity,
            "created_at": datetime.now().isoformat(),
        }
        outbox_id = outbox_repo.insert_event(cursor, "OrderCreated", payload)
    return {
        "order_id": order_id,
        "outbox_id": outbox_id,
        "item": item,
        "quantity": quantity,
    }
