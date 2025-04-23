# strategies/high_volume_breakout.py

import pandas as pd
from core.data_provider import get_daily_data

# ✅ Buy signal strategy logic

def run(config: dict) -> list:
    """
    Run the volume breakout BUY strategy.
    Uses get_daily_data() interface to abstract away the data source (e.g., yfinance, alpaca).
    """
    tickers = config.get("tickers", [])
    volume_multiplier = config.get("volume_multiplier", 2.0)
    period = config.get("period", "6d")
    lookback = config.get("lookback_days", 5)
    signals = []

    # Fetch OHLCV data for each ticker
    data_map = get_daily_data(tickers, start=None, end=None, source=config.get("data_source", "yfinance"))

    for symbol in tickers:
        data = data_map.get(symbol)
        if data is None or data.empty or len(data) <= lookback:
            continue

        recent_volume = data["Volume"].iloc[-1]
        avg_volume = data["Volume"].iloc[-lookback - 1:-1].mean()

        # ✅ Type-safe fallback
        if isinstance(recent_volume, pd.Series):
            recent_volume = recent_volume.iloc[0]
        if isinstance(avg_volume, pd.Series):
            avg_volume = avg_volume.iloc[0]

        # ✅ Convert to float explicitly
        recent_volume = float(recent_volume)
        avg_volume = float(avg_volume)

        if recent_volume >= volume_multiplier * avg_volume:
            signals.append({
                "symbol": symbol,
                "action": "buy",
                "qty": 1
            })

    return signals

# ✅ Buy signal for backtest simulation (on one day of data)
def run_backtest_on_day(data: pd.DataFrame, symbol: str, config: dict) -> dict | None:
    volume_multiplier = config.get("volume_multiplier", 1.0)
    lookback = config.get("lookback_days", 5)

    if data is None or data.empty or len(data) < lookback + 1:
        return None

    recent_volume = data["Volume"].iloc[-1]
    avg_volume = data["Volume"].iloc[:-1].tail(config["lookback_days"]).mean()

    if isinstance(recent_volume, pd.Series):
        recent_volume = recent_volume.iloc[0]
    if isinstance(avg_volume, pd.Series):
        avg_volume = avg_volume.iloc[0]

    recent_volume = float(recent_volume)
    avg_volume = float(avg_volume)

    if recent_volume >= config["volume_multiplier"] * avg_volume:
        return {
            "symbol": symbol,
            "action": "buy",
            "qty": 1
        }

    return None

# ✅ Exit logic (e.g., sell when price drops 3% from peak)
def run_exit(config: dict, holdings: list) -> list:
    """
    Evaluate exit (SELL) signals based on target profit/loss thresholds.
    Still uses yfinance intraday 1-min data for simplicity.
    """
    import yfinance as yf
    exit_signals = []
    profit_target = config.get("profit_pct", 0.05)  # 5% gain
    stop_loss = config.get("loss_pct", 0.03)       # 3% drop

    for position in holdings:
        symbol = position["symbol"]
        entry_price = float(position["price"])
        qty = position["qty"]

        try:
            data = yf.download(symbol, period="1d", interval="1m", auto_adjust=False)
            if data is None or data.empty:
                continue
            val = data["Close"].iloc[-1]
            if isinstance(val, pd.Series):
                val = val.iloc[0]
            current_price = float(val)
            gain = (current_price - entry_price) / entry_price

            if gain >= profit_target or gain <= -stop_loss:
                exit_signals.append({
                    "symbol": symbol,
                    "action": "sell",
                    "qty": qty
                })

        except Exception as e:
            print(f"⚠️ Could not evaluate exit for {symbol}: {e}")

    return exit_signals
