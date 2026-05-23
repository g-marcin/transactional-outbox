#!/usr/bin/env python3
"""Outbox statistics functionality."""

import requests


def show_stats(base_url: str = "http://localhost:8000") -> None:
    """Display outbox statistics."""
    try:
        response = requests.get(f"{base_url}/admin/outbox-stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Outbox Statistics:")
            print(f"   PENDING:   {data['pending']:3d}")
            print(f"   PROCESSED: {data['processed']:3d}")
            print(f"   FAILED:    {data['failed']:3d}")
            print(f"   {'─' * 25}")
            print(f"   TOTAL:     {data['total']:3d}\n")
        else:
            print(f"\n✗ Failed: {response.status_code}\n")
    except requests.RequestException as e:
        print(f"\n✗ Error connecting to {base_url}: {e}\n")
