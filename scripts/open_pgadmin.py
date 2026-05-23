#!/usr/bin/env python3
"""Open pgAdmin in browser with credentials ready."""

import webbrowser
import time


def open_pgadmin(port: int = 5050) -> None:
    """Open pgAdmin and display credentials."""
    url = f"http://localhost:{port}"

    print("\n" + "=" * 50)
    print("📊 pgAdmin Access")
    print("=" * 50)
    print(f"URL:      {url}")
    print(f"Email:    admin@example.com")
    print(f"Password: admin")
    print("=" * 50)
    print("\nOpening browser...\n")

    webbrowser.open(url)
    time.sleep(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Open pgAdmin in browser")
    parser.add_argument("--port", "-p", type=int, default=5050, help="pgAdmin port")

    args = parser.parse_args()
    open_pgadmin(port=args.port)
