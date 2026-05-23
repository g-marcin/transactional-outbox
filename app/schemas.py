from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    """Request to create an order."""

    item: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Order quantity", gt=0)


class OrderResponse(BaseModel):
    """Order creation response with outbox event."""

    order_id: int = Field(..., description="Created order ID")
    outbox_id: int = Field(..., description="Outbox event ID")
    item: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Ordered quantity")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")


class AdminResponse(BaseModel):
    """Admin operation response."""

    message: str = Field(..., description="Operation result message")
    status: str = Field(..., description="Operation status (ok/error)")


class OutboxStats(BaseModel):
    """Outbox statistics."""

    pending: int = Field(..., description="Number of pending outbox entries")
    processed: int = Field(..., description="Number of processed outbox entries")
    failed: int = Field(..., description="Number of failed outbox entries")
    total: int = Field(..., description="Total number of outbox entries")
