# jobs/run_buy.py

from core.strategy_registry import STRATEGY_REGISTRY
from core.broker import buy_stock, get_current_price
from core.notifier import send_telegram
from core.sqlite_logger import init_db, log_trade
from core.ticker_loader import load_tickers

# ✅ Default configuration per strategy
# These can be overridden via CLI args or scheduler-based configuration
DEFAULT_CONFIGS = {
    "volume_breakout": {
        "tickers": load_tickers(),
        "volume_multiplier": 0.5,
        "lookback_days": 5,
        "period": "6d"
    }
}

def run_all_strategies():
    """
    Executes all registered BUY strategies:
    - Initializes local DB
    - Runs strategy and gets buy signals
    - Places orders, logs trades, and sends notifications
    """
    init_db()

    for strategy_name, strategy_fn in STRATEGY_REGISTRY.items():
        config = DEFAULT_CONFIGS.get(strategy_name, {})
        print(f"▶️ Running strategy: {strategy_name}")

        try:
            # 🔍 Run strategy to fetch buy signals
            signals = strategy_fn(config)
            if not signals:
                print(f"🔕 No signals for {strategy_name}")
                continue

            for signal in signals:
                symbol = signal["symbol"]
                qty = signal.get("qty", 1)
                action = signal.get("action", "buy")

                # 💰 Fetch market price and place buy order
                price = get_current_price(symbol)
                buy_stock(symbol, qty)

                # 📣 Alert and log the trade
                send_telegram(f"✅ {action.upper()} {symbol} x{qty} @ ${price:.2f}")
                log_trade(
                    symbol=symbol,
                    action=action,
                    qty=qty,
                    price=price,
                    strategy=strategy_name,
                    env="paper",  # Change to "live" for live orders
                    status="executed"
                )

        except Exception as e:
            print(f"❌ Error in strategy '{strategy_name}': {e}")
            send_telegram(f"⚠️ Strategy error in {strategy_name}: {e}")


if __name__ == "__main__":
    run_all_strategies()
