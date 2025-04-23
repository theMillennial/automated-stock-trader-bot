# jobs/run_exit.py

from core.strategy_registry import STRATEGY_REGISTRY
from core.broker import sell_stock, get_current_price
from core.notifier import send_telegram
from core.sqlite_logger import init_db, log_trade
from core.position_tracker import get_open_positions_by_strategy
from core.ticker_loader import load_tickers

# ✅ Default config for exit logic per strategy
# Can be overridden via external JSON in the future
DEFAULT_EXIT_CONFIGS = {
    "volume_breakout": {
        "profit_pct": 0.0001,  # Tiny threshold for testing exits
        "loss_pct": 0.0001,
        "tickers": load_tickers()
    }
}

def run_all_exits():
    """
    Scans all registered exit strategies and executes sell signals:
    - Loads current open positions
    - Checks exit conditions for each strategy
    - Sells matching symbols and logs actions
    """
    init_db()

    for strategy_name, strategy_fn in STRATEGY_REGISTRY.items():
        if not hasattr(strategy_fn, "__module__"):
            continue

        # 🔍 Dynamically import the strategy's exit function
        strategy_module = __import__(strategy_fn.__module__, fromlist=["run_exit"])
        if not hasattr(strategy_module, "run_exit"):
            print(f"⚠️ No run_exit() for {strategy_name}")
            continue

        exit_fn = getattr(strategy_module, "run_exit")
        config = DEFAULT_EXIT_CONFIGS.get(strategy_name, {})
        holdings = get_open_positions_by_strategy(strategy_name)

        try:
            # 📭 Scan for sell signals
            exit_signals = exit_fn(config, holdings)
            if not exit_signals:
                print(f"📭 No exit signals for {strategy_name}")
                continue

            for signal in exit_signals:
                symbol = signal["symbol"]
                qty = signal.get("qty", 1)
                action = signal.get("action", "sell")

                # 💰 Execute trade
                price = get_current_price(symbol)
                sell_stock(symbol, qty)

                # 📝 Log and notify
                send_telegram(f"🚪 {action.upper()} {symbol} x{qty} @ ${price:.2f}")
                log_trade(
                    symbol=symbol,
                    action=action,
                    qty=qty,
                    price=price,
                    strategy=strategy_name,
                    env="paper",
                    status="closed"
                )

        except Exception as e:
            print(f"❌ Error running exit for {strategy_name}: {e}")
            send_telegram(f"⚠️ Exit error in {strategy_name}: {e}")


if __name__ == "__main__":
    run_all_exits()