#!/usr/bin/env python3
"""Seed database via outbox pattern by creating orders through API."""

import random
import time
from dataclasses import dataclass

import requests


@dataclass
class OrderSeed:
    item: str
    quantity: int


ITEMS = [
    "laptop",
    "phone",
    "tablet",
    "monitor",
    "keyboard",
    "mouse",
    "headphones",
    "webcam",
    "charger",
    "usb-cable",
]


def generate_orders(count: int) -> list[OrderSeed]:
    """Generate diverse order data."""
    orders = []
    for _ in range(count):
        orders.append(
            OrderSeed(
                item=random.choice(ITEMS),
                quantity=random.randint(1, 10),
            )
        )
    return orders


def send_order(base_url: str, order: OrderSeed, chaos_rate: float = 0) -> bool:
    """Send order via HTTP, return True if successful.

    Args:
        base_url: API base URL
        order: Order data to send
        chaos_rate: Probability of simulating client-side failure (0-1)
    """
    # Simulate client-side failures (invalid data, network errors, etc.)
    if random.random() < chaos_rate:
        failure_type = random.choice(["invalid_quantity", "timeout", "bad_format"])
        if failure_type == "invalid_quantity":
            payload = {"item": order.item, "quantity": -1}  # Invalid
        elif failure_type == "timeout":
            print(f"✗ {order.item:15} qty={order.quantity:2} TIMEOUT (simulated)")
            return False
        else:
            payload = {"item": order.item}  # Missing quantity
        status_code = 422
    else:
        payload = {"item": order.item, "quantity": order.quantity}
        status_code = None

    try:
        response = requests.post(
            f"{base_url}/order",
            json=payload,
            timeout=5,
        )
        success = response.status_code == 200
        status = "✓" if success else "✗"
        print(f"{status} {order.item:15} qty={order.quantity:2} {response.status_code}")
        return success
    except requests.RequestException as e:
        print(f"✗ {order.item:15} qty={order.quantity:2} ERROR: {e}")
        return False


def seed_orders(
    count: int = 10,
    base_url: str = "http://localhost:8000",
    delay: float = 0.1,
    chaos_rate: float = 0,
) -> None:
    """Seed database with diverse orders.

    Args:
        count: Number of orders to create
        base_url: API base URL
        delay: Delay between requests (seconds)
        chaos_rate: Probability of simulating client-side failure (0-1)
    """
    print(f"\n📦 Seeding {count} orders...\n")

    orders = generate_orders(count)
    success = 0
    failed = 0

    for i, order in enumerate(orders, 1):
        if send_order(base_url, order, chaos_rate=chaos_rate):
            success += 1
        else:
            failed += 1

        if i < len(orders):
            time.sleep(delay)

    print(f"\n📊 Results: {success} succeeded, {failed} failed\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed database via API (outbox pattern)")
    parser.add_argument("--count", "-c", type=int, default=50, help="Number of orders")
    parser.add_argument("--url", "-u", default="http://localhost:8000", help="API URL")
    parser.add_argument("--delay", "-d", type=float, default=0.1, help="Delay between requests")
    parser.add_argument(
        "--chaos",
        type=float,
        default=0,
        help="Client-side failure rate 0-1 (e.g., 0.2 = 1 in 5 requests fail)",
    )

    args = parser.parse_args()
    seed_orders(count=args.count, base_url=args.url, delay=args.delay, chaos_rate=args.chaos)
