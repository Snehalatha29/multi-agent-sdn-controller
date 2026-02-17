import sqlite3
from datetime import datetime

DB_PATH = "database/traffic_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        timestamp TEXT,
        latency INTEGER,
        bandwidth INTEGER,
        fault TEXT,
        decision TEXT
    )
    """)

    conn.commit()
    conn.close()


def log_decision(latency, bandwidth, fault, decision):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT INTO logs VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%H:%M:%S"),
        latency,
        bandwidth,
        fault,
        decision
    ))

    conn.commit()
    conn.close()
