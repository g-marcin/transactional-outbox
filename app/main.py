from api import admin, health, orders
from fastapi import FastAPI

# __CLIENT__
app = FastAPI(
    title="Transactional Outbox API",
    description="Event-driven architecture using transactional outbox pattern",
    version="1.0.0",
    docs_url="/doc",
    redoc_url="/redoc",
)
app.include_router(orders.router)
app.include_router(health.router)
app.include_router(admin.router)
