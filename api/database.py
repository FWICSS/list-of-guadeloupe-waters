import sqlite3
import uuid
import os
from datetime import date, datetime
from pathlib import Path

DB_PATH = os.getenv("DB_PATH", str(Path(__file__).parent / "api_keys.db"))


def _conn():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                key TEXT PRIMARY KEY,
                email TEXT NOT NULL,
                name TEXT NOT NULL,
                tier TEXT NOT NULL DEFAULT 'free',
                created_at TEXT NOT NULL,
                requests_today INTEGER NOT NULL DEFAULT 0,
                last_reset_date TEXT NOT NULL,
                stripe_customer_id TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS anon_requests (
                ip TEXT PRIMARY KEY,
                requests_today INTEGER NOT NULL DEFAULT 0,
                last_reset_date TEXT NOT NULL
            )
        """)
        conn.commit()


def create_key(email: str, name: str) -> str:
    key = "gw_" + uuid.uuid4().hex
    today = date.today().isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO api_keys (key, email, name, tier, created_at, requests_today, last_reset_date) "
            "VALUES (?, ?, ?, 'free', ?, 0, ?)",
            (key, email, name, datetime.utcnow().isoformat(), today),
        )
        conn.commit()
    return key


def get_key(key: str) -> dict | None:
    with _conn() as conn:
        row = conn.execute("SELECT * FROM api_keys WHERE key = ?", (key,)).fetchone()
        return dict(row) if row else None


def increment_requests(key: str):
    today = date.today().isoformat()
    with _conn() as conn:
        row = conn.execute("SELECT last_reset_date FROM api_keys WHERE key = ?", (key,)).fetchone()
        if row and row["last_reset_date"] != today:
            conn.execute(
                "UPDATE api_keys SET requests_today = 1, last_reset_date = ? WHERE key = ?",
                (today, key),
            )
        else:
            conn.execute(
                "UPDATE api_keys SET requests_today = requests_today + 1 WHERE key = ?",
                (key,),
            )
        conn.commit()


def get_anon_requests(ip: str) -> int:
    today = date.today().isoformat()
    with _conn() as conn:
        row = conn.execute("SELECT * FROM anon_requests WHERE ip = ?", (ip,)).fetchone()
        if not row:
            return 0
        if row["last_reset_date"] != today:
            conn.execute(
                "UPDATE anon_requests SET requests_today = 0, last_reset_date = ? WHERE ip = ?",
                (today, ip),
            )
            conn.commit()
            return 0
        return row["requests_today"]


def increment_anon(ip: str):
    today = date.today().isoformat()
    with _conn() as conn:
        conn.execute(
            "INSERT INTO anon_requests (ip, requests_today, last_reset_date) VALUES (?, 1, ?) "
            "ON CONFLICT(ip) DO UPDATE SET "
            "requests_today = CASE WHEN last_reset_date != ? THEN 1 ELSE requests_today + 1 END, "
            "last_reset_date = ?",
            (ip, today, today, today),
        )
        conn.commit()


def upgrade_to_premium(key: str):
    with _conn() as conn:
        conn.execute("UPDATE api_keys SET tier = 'premium' WHERE key = ?", (key,))
        conn.commit()


def revoke_key(key: str):
    with _conn() as conn:
        conn.execute("DELETE FROM api_keys WHERE key = ?", (key,))
        conn.commit()


def list_keys() -> list[dict]:
    with _conn() as conn:
        rows = conn.execute("SELECT * FROM api_keys ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def reset_daily_counts():
    today = date.today().isoformat()
    with _conn() as conn:
        conn.execute("UPDATE api_keys SET requests_today = 0, last_reset_date = ?", (today,))
        conn.execute("UPDATE anon_requests SET requests_today = 0, last_reset_date = ?", (today,))
        conn.commit()
