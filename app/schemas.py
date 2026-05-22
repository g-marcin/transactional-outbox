from pydantic import BaseModel


class OrderRequest(BaseModel):
    item: str
    quantity: int


class OrderResponse(BaseModel):
    order_id: int
    outbox_id: int
    item: str
    quantity: int
