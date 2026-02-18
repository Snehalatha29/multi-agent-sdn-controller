import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "traffic_logs.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS traffic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        INSERT INTO traffic_logs (timestamp, latency, bandwidth, fault, decision)
        VALUES (datetime('now'), ?, ?, ?, ?)
    """, (latency, bandwidth, fault, decision))

    conn.commit()
    conn.close()
