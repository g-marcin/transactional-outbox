#!/usr/bin/env python3
"""Show outbox statistics (PENDING, PROCESSED, FAILED counts)."""

from stats import show_stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Show outbox statistics")
    parser.add_argument("--url", "-u", default="http://localhost:8000", help="API URL")

    args = parser.parse_args()
    show_stats(base_url=args.url)
