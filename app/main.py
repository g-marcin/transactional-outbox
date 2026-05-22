from fastapi import FastAPI

from api import health, orders
from worker import OutboxWorker

app = FastAPI()
app.include_router(orders.router)
app.include_router(health.router)

_worker = OutboxWorker()


@app.on_event("startup")
def startup_event() -> None:
    _worker.start()
