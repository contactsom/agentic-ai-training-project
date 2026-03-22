import sqlite3
from cease_desist_processor.config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cease_requests (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name    TEXT NOT NULL,
            received_date TEXT NOT NULL,
            details     TEXT,
            stored_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def store_cease_request(doc_name: str, received_date: str, details: str) -> str:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO cease_requests (doc_name, received_date, details) VALUES (?, ?, ?)",
        (doc_name, received_date, details),
    )
    conn.commit()
    conn.close()
    return f"Stored cease request for '{doc_name}' in database."
