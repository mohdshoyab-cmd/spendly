import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'expense_tracker.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            description TEXT,
            date        TEXT    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    from werkzeug.security import generate_password_hash

    conn = get_db()

    if conn.execute("SELECT id FROM users WHERE email = 'demo@spendly.com'").fetchone():
        conn.close()
        return

    conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("password123"))
    )
    user_id = conn.execute(
        "SELECT id FROM users WHERE email = 'demo@spendly.com'"
    ).fetchone()["id"]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        [
            (user_id, 4500.00, "Bills",     "Electricity bill",    "2026-03-01"),
            (user_id, 1200.00, "Bills",     "Internet bill",       "2026-03-20"),
            (user_id, 3200.00, "Food",      "Groceries",           "2026-03-05"),
            (user_id,  900.00, "Food",      "Restaurant dinner",   "2026-03-18"),
            (user_id, 2050.00, "Health",    "Doctor visit",        "2026-03-10"),
            (user_id, 1800.00, "Transport", "Monthly metro pass",  "2026-03-15"),
        ]
    )
    conn.commit()
    conn.close()
