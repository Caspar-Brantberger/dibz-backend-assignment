from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def get_connection(db_path: str) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def get_user_id(connection: sqlite3.Connection, full_name: str) -> int | None:
    row = connection.execute(
        "SELECT id FROM users WHERE full_name = ?",
        (full_name,),
    ).fetchone()
    return None if row is None else int(row["id"])


def update_last_login(connection: sqlite3.Connection, user_id: int, timestamp: str) -> None:
    """TODO: update users.last_login for the given user."""
    raise NotImplementedError


def update_queue_spot(
    connection: sqlite3.Connection,
    user_id: int,
    queue_type: str,
    registration_date: str,
    last_updated: str,
    update_before: str,
    status: str,
    inactive_reason: str | None,
) -> None:
    """TODO: update one queue_spots row for the given user and queue_type."""
    raise NotImplementedError
