# jobs/backtester.py

from core.strategy_registry import STRATEGY_REGISTRY
from core.data_provider import get_daily_data
from core.ticker_loader import load_tickers
import pandas as pd
import datetime
import csv
import os
import argparse
import json

def load_config(config_path):
    with open(config_path, "r") as f:
        return json.load(f)

def simulate_exit(entry_price, data, profit_pct, loss_pct):
    # Clean up column names
    data.columns = [str(col).strip() for col in data.columns]

    required_cols = {"High", "Low", "Close"}
    if not required_cols.issubset(set(data.columns)):
        print(f"❌ Missing columns: {required_cols - set(data.columns)}")
        return (None, entry_price, "hold")

    target_price = entry_price * (1 + profit_pct)
    stop_price = entry_price * (1 - loss_pct)

    for idx in data.index:
        try:
            high = float(data.loc[idx, "High"])
            low = float(data.loc[idx, "Low"])
        except Exception as e:
            print(f"⚠️ Data error on {idx}: {e}")
            continue

        if high >= target_price:
            return (idx, target_price, "win")
        if low <= stop_price:
            return (idx, stop_price, "loss")

    try:
        exit_price = float(data["Close"].iloc[-1])
        return (data.index[-1], exit_price, "hold")
    except Exception as e:
        print(f"⚠️ Final row error: {e}")
        return (None, entry_price, "hold")

def run_backtest(config):
    strategy_name = config["strategy"]
    tickers = tickers = config.get("tickers", load_tickers())
    start_date = config["start_date"]
    end_date = config["end_date"]

    max_tickers = config.get("max_tickers")
    if max_tickers:
        tickers = tickers[:max_tickers]

    strategy = STRATEGY_REGISTRY.get(strategy_name)
    strategy_module = __import__(strategy.__module__, fromlist=["run_backtest_on_day"])

    if not hasattr(strategy_module, "run_backtest_on_day"):
        raise Exception("Selected strategy does not support backtesting.")

    backtest_fn = getattr(strategy_module, "run_backtest_on_day")
    results = []

    # Fetch all data up front for all tickers using unified interface
    data_map = get_daily_data(tickers, start=start_date, end=end_date, source=config.get("data_source", "yfinance"))

    for symbol in tickers:
        print(f"🔍 Backtesting {symbol}...")
        data = data_map.get(symbol)

        if data is None or data.empty:
            print(f"❌ No data found for {symbol}. Skipping.")
            continue

        data = data.dropna()

        # Step 3: Flatten MultiIndex columns like ('High', 'AAPL') → 'High'
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Normalize column names
        data.columns = [str(col).strip() for col in data.columns]

        # Ensure required OHLC columns
        required_cols = {"High", "Low", "Close"}
        if not required_cols.issubset(data.columns):
            print(f"❌ Missing expected OHLC columns in {symbol}. Skipping.")
            continue

        for i in range(config["lookback_days"], len(data) - 1):
            window = data.iloc[i - config["lookback_days"]:i + 1]
            result = backtest_fn(window, symbol, config)

            if result:
                entry_date = window.index[-1]
                entry_price = window.iloc[-1]['Close']
                future_data = data.iloc[i+1:i+15]

                exit_date, exit_price, outcome = simulate_exit(
                    entry_price,
                    future_data,
                    config['profit_pct'],
                    config['loss_pct']
                )

                holding_days = (exit_date - entry_date).days if exit_date else 0
                gain_pct = ((exit_price - entry_price) / entry_price) * 100

                results.append({
                    "date": entry_date.strftime("%Y-%m-%d"),
                    "symbol": symbol,
                    "entry_price": round(entry_price, 2),
                    "exit_price": round(exit_price, 2),
                    "gain_pct": round(gain_pct, 2),
                    "holding_days": holding_days,
                    "outcome": outcome
                })

    if not results:
        print("⚠️ No valid backtest results to write.")
        return

    os.makedirs("backtest_results", exist_ok=True)
    results_file = os.path.join("backtest_results", f"{strategy_name}.csv")
    with open(results_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    print("\n📈 Backtest Results Summary:")
    df = pd.DataFrame(results)

    if df.empty:
        print("No trades were triggered in the backtest.")
        return

    df["gain_pct"] = pd.to_numeric(df["gain_pct"], errors="coerce")
    df = df.dropna(subset=["gain_pct"])

    total = len(df)
    wins = df[df["outcome"] == "win"]
    losses = df[df["outcome"] == "loss"]
    win_rate = len(wins) / total * 100 if total > 0 else 0
    avg_gain = df["gain_pct"].mean() if total > 0 else 0
    max_drawdown = df["gain_pct"].min() if total > 0 else 0

    print(f"Total trades: {total}")
    print(f"Win rate: {win_rate:.2f}%")
    print(f"Avg return: {avg_gain:.2f}%")
    print(f"Max drawdown: {max_drawdown:.2f}%")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config JSON file")
    args = parser.parse_args()

    config = load_config(args.config)
    run_backtest(config)
