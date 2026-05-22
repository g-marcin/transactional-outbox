def insert_order(cursor, item: str, quantity: int) -> int:
    cursor.execute(
        """
        INSERT INTO orders (item, quantity)
        VALUES (%s, %s)
        RETURNING id
        """,
        (item, quantity),
    )
    return cursor.fetchone()[0]
