import sqlite3
from datetime import datetime
import os

DB_FILE = "logs/trades.db"
os.makedirs("logs", exist_ok=True)

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                action TEXT,
                qty INTEGER,
                price REAL,
                strategy TEXT,
                env TEXT,
                status TEXT,
                notes TEXT
            )
        """)
        conn.commit()

def log_trade(symbol, action, qty, price, strategy="volume_breakout", env="paper", status="executed", notes=None):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trades (timestamp, symbol, action, qty, price, strategy, env, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, symbol, action, qty, price, strategy, env, status, notes))
        conn.commit()

    print(f"📝 Logged trade: {action.upper()} {symbol} x{qty} @ ${price} [{strategy} | {env}]")
