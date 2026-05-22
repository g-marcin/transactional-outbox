import time

from config import QUEUE_LATENCY_SECONDS


def send_to_queue(payload: dict) -> bool:
    print(f"[QUEUE] Receiving payload: {payload}")
    time.sleep(QUEUE_LATENCY_SECONDS)
    print("[QUEUE] Acknowledged safely")
    return True
