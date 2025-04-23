# main.py

import sys
from jobs.run_buy import run_all_strategies as run_buy
from jobs.run_exit import run_all_exits as run_sell

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "buy"

    if mode == "buy":
        print("🔄 Running BUY logic...")
        run_buy()
    elif mode == "sell":
        print("🔄 Running SELL logic...")
        run_sell()
    else:
        print(f"❌ Unknown mode '{mode}'. Use 'buy' or 'sell'.")
