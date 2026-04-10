from __future__ import annotations

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "app.db"

SCHEMA = """
DROP TABLE IF EXISTS queue_spots;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    platform_username TEXT NOT NULL UNIQUE,
    last_login TEXT
);

CREATE TABLE queue_spots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    queue_type TEXT NOT NULL,
    registration_date TEXT,
    last_updated TEXT,
    update_before TEXT,
    status TEXT NOT NULL,
    inactive_reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, queue_type)
);
"""

USERS = [
    ("Maxim Eyd", "maxim@example.com", "maxim@example.com", "2026-03-01T09:00:00+00:00"),
    ("Anna Berg", "anna@example.com", "anna@example.com", "2026-04-06T06:45:00+00:00"),
    ("Johan Nilsson", "johan@example.com", "johan@example.com", None),
]

QUEUE_SPOTS = [
    # Maxim: intentionally stale / partly wrong values so candidate updates these.
    (1, "Regular", "2021-08-14", "2026-03-01", "2026-04-01", "active", None),
    (1, "Parking", "2022-02-01", "2026-03-10", "2026-04-10", "inactive", "Old incorrect value"),
    (1, "Student", "2023-09-15", "2025-09-15", "2025-10-15", "active", None),
    # Other users: should remain untouched.
    (2, "Regular", "2020-01-20", "2026-04-04", "2026-05-04", "active", None),
    (2, "Parking", "2024-02-14", "2026-03-30", "2026-04-30", "active", None),
    (3, "Regular", "2019-11-09", "2026-02-11", "2026-03-11", "inactive", "User requested pause"),
]


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.executescript(SCHEMA)
        connection.executemany(
            "INSERT INTO users (full_name, email, platform_username, last_login) VALUES (?, ?, ?, ?)",
            USERS,
        )
        connection.executemany(
            """
            INSERT INTO queue_spots (
                user_id, queue_type, registration_date, last_updated, update_before, status, inactive_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            QUEUE_SPOTS,
        )
        connection.commit()
    finally:
        connection.close()

    print(f"Database reset: {DB_PATH}")


if __name__ == "__main__":
    main()
