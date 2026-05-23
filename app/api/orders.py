from fastapi import APIRouter, HTTPException
from schemas import OrderRequest, OrderResponse
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
