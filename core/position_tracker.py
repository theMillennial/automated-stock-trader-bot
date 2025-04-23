# core/position_tracker.py

import sqlite3

def get_open_positions_by_strategy(strategy_name: str, db_path="logs/trades.db") -> list:
    """
    Returns open positions for a given strategy.
    An open position is any BUY trade that doesn't have a matching SELL or is not marked as closed.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all buys that have not been closed by a corresponding sell or marked closed
    cursor.execute("""
        SELECT symbol, qty, price, timestamp
        FROM trades
        WHERE action = 'buy'
        AND strategy = ?
        AND env = 'paper'
        AND status != 'closed'
    """, (strategy_name,))

    rows = cursor.fetchall()
    conn.close()

    holdings = []
    for row in rows:
        holdings.append({
            "symbol": row[0],
            "qty": row[1],
            "price": row[2],
            "timestamp": row[3]
        })

    return holdings
