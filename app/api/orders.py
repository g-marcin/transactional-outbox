from db import get_connection
from fastapi import APIRouter, HTTPException, Query
from schemas import OrderListItem, OrderListResponse, OrderRequest, OrderResponse
from services import orders as orders_service

router = APIRouter(tags=["orders"])


@router.post(
    "/order",
    response_model=OrderResponse,
    summary="Create new order",
    responses={
        200: {"description": "Order created successfully with outbox event"},
        422: {"description": "Invalid request (missing/invalid fields)"},
        500: {"description": "Server error during order creation"},
    },
)
def create_order(request: OrderRequest) -> OrderResponse:
    """Create a new order with transactional outbox event.

    The order and outbox event are created atomically within a single
    database transaction to ensure eventual consistency.
    """
    try:
        result = orders_service.create_order_with_event(request.item, request.quantity)
        return OrderResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/orders",
    response_model=OrderListResponse,
    summary="List all orders",
    responses={
        200: {"description": "Orders retrieved successfully"},
        500: {"description": "Server error retrieving orders"},
    },
)
def list_orders(
    limit: int = Query(
        50,
        ge=1,
        le=100,
        description="Number of orders to return (max 100)",
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Number of orders to skip",
    ),
) -> OrderListResponse:
    """Retrieve paginated list of all orders.

    Returns orders sorted by creation time (newest first).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM orders")
            total = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT order_id, item, quantity
                FROM orders
                ORDER BY order_id DESC
                LIMIT %s OFFSET %s
                """,
                (limit, offset),
            )
            items = [
                OrderListItem(order_id=row[0], item=row[1], quantity=row[2])
                for row in cursor.fetchall()
            ]

        return OrderListResponse(
            total=total,
            limit=limit,
            offset=offset,
            items=items,
        )
    finally:
        conn.close()
