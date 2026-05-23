from api import health, orders
from fastapi import FastAPI
from worker import OutboxWorker

# __CLIENT__
app = FastAPI()
app.include_router(orders.router)
app.include_router(health.router)

# __OUTBOX_POLLING__
_worker = OutboxWorker()


# FastAPI lifespan hook
@app.on_event("startup")
def startup_event() -> None:
    _worker.start()
