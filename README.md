# automated-stock-trader-bot
📈 Automated Stock Trader Bot
=============================

A modular, Python-based trading bot framework that supports:
- ✅ Live & paper trading via Alpaca API
- ✅ Telegram alerts
- ✅ Strategy-driven buy/sell decisions
- ✅ Daily cron-based execution
- ✅ Backtesting engine with PnL tracking

-----------------------------

🧱 Project Structure

.
├── core/                # Brokers, logging, notifier, strategy registry
├── strategies/          # Individual strategy implementations
├── jobs/                # Scheduled runners (buy, sell, backtest)
├── data/                # Ticker CSVs and static data
├── configs/             # JSON configs for strategies
├── logs/                # SQLite trade logs (ignored in Git)
├── backtest_results/    # Backtest output CSVs (ignored in Git)

-----------------------------

⚙️ Setup

# Install dependencies
pip install -r requirements.txt

# Setup environment variables (Alpaca, Telegram)
cp .env.example .env

-----------------------------

📥 Ticker Universe

- Loaded from `data/tickers.csv`
- Dynamically pulled into every strategy
- Source: S&P 500 + Nasdaq 100 (519 deduplicated tickers)

-----------------------------

🚀 Running Jobs

1. Run Buy Logic:
   python -m jobs.run_buy

2. Run Sell Logic:
   python -m jobs.run_exit

3. Run Backtest:
   python -m jobs.backtester --config configs/high_volume_breakout.json

-----------------------------

🔬 Strategies

✅ Included:
- high_volume_breakout.py: Buy on 2x+ volume spike, exit on 5% gain or 3% stop loss

🛠️ To Add:
- Moving average crossover
- RSI swing reversal
- Earnings momentum, etc.

-----------------------------

🛑 Notes

- Trade logs stored in `logs/trades.db`
- Telegram bot used for alerts
- Alpaca API is used for placing and simulating orders
- Add "max_tickers" to config for lightweight development mode

-----------------------------

📦 License

MIT (You’re free to use, adapt, and build your own hedge fund 😉)

-----------------------------

✨ Author

Made with obsession by Sushant Kulkarni
