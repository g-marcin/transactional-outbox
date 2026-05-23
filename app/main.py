from api import admin, health, orders
from fastapi import FastAPI
from worker import OutboxWorker, set_worker

# __CLIENT__
app = FastAPI()
app.include_router(orders.router)
app.include_router(health.router)
app.include_router(admin.router)

# __OUTBOX_POLLING__
_worker = OutboxWorker()
set_worker(_worker)


# FastAPI lifespan hook
@app.on_event("startup")
def startup_event() -> None:
    _worker.start()
