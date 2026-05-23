#!/usr/bin/env python3
"""Manually kick worker to process pending outbox entries."""

import requests


def kick_worker(base_url: str = "http://localhost:8000") -> None:
    """Trigger worker to process pending outbox entries immediately.

    Use when worker was down and needs to catch up on pending entries.
    """
    try:
        response = requests.post(f"{base_url}/admin/process-pending", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ {data['message']}\n")
        else:
            print(f"\n✗ Failed: {response.status_code}\n{response.text}\n")
    except requests.RequestException as e:
        print(f"\n✗ Error connecting to {base_url}: {e}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Kick worker to process pending outbox entries")
    parser.add_argument("--url", "-u", default="http://localhost:8000", help="API URL")

    args = parser.parse_args()
    kick_worker(base_url=args.url)
