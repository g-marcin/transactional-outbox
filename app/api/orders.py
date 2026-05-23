from fastapi import APIRouter, HTTPException
from schemas import OrderRequest, OrderResponse
from services import orders as orders_service

router = APIRouter()


@router.post("/order", response_model=OrderResponse)
def create_order(request: OrderRequest) -> OrderResponse:
    try:
        result = orders_service.create_order_with_event(request.item, request.quantity)
        return OrderResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
