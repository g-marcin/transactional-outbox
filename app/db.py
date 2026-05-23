from contextlib import contextmanager

import psycopg2
from config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@contextmanager
def transaction():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
