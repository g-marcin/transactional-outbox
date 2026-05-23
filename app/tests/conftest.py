import os
from pathlib import Path

import psycopg2
import pytest
from testcontainers.postgres import PostgresContainer

INIT_SQL_PATH = Path(__file__).resolve().parent.parent.parent / "init.sql"

_container: PostgresContainer | None = None


def pytest_sessionstart(session):
    """Start a Postgres container and apply init.sql before any tests import app modules."""
    global _container
    _container = PostgresContainer("postgres:15")
    _container.start()

    url = (
        f"postgresql://{_container.username}:{_container.password}"
        f"@{_container.get_container_host_ip()}:{_container.get_exposed_port(5432)}"
        f"/{_container.dbname}"
    )
    os.environ["DATABASE_URL"] = url

    _apply_init_sql(url)


def pytest_sessionfinish(session, exitstatus):
    if _container is not None:
        _container.stop()


def _apply_init_sql(url: str) -> None:
    sql = INIT_SQL_PATH.read_text()
    conn = psycopg2.connect(url)
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


@pytest.fixture(autouse=True)
def reset_db():
    """Truncate both tables between tests so each starts from a clean slate."""
    from db import get_connection

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE orders, outbox RESTART IDENTITY")
        conn.commit()
    finally:
        conn.close()
    yield
