from strategies.high_volume_breakout import run, run_backtest_on_day, run_exit

STRATEGY_REGISTRY = {
    "volume_breakout": run
}