# 🧠 Future Enhancements: Automated Stock Trader Bot

A high-level roadmap and backlog for scaling, refining, and hardening the automated trading system. Prioritized from critical (P1) to nice-to-have (P3).

---

## ✅ Phase 1: Immediate Enhancements (P1)

### Core Logic & Trading
- [ ] Handle overlapping strategy signals (consolidate per symbol; tag multiple strategies)  
  _Consider specifying whether this logic should be handled in the strategy module itself or consolidated in `run_buy.py` for clarity._
- [ ] Implement sell order error recovery (e.g., wash trade protection, retry logic)  
  _You could break this down into specific error types and recommended handling mechanisms, such as retries or fallback orders._
- [ ] Add trailing stop loss logic (+10%, timeout, dynamic stop)
- [ ] Mark strategy buys in DB with multiple strategy tags
- [ ] Flag weekend/holiday dates to avoid placing orders

### Dev & Infra
- [ ] Support `max_tickers` for faster local dev cycles
- [ ] Exclude `backtest_results/` and `logs/` from Git
- [ ] Add `.env` encryption or Secrets Manager for production

### Testing
- [ ] Add unit tests for `core/` modules
- [ ] Add integration test for buy/sell loop using mocks

---

## 🛠 Phase 2: Strategy & Data Expansion (P2)

### New Strategies
- [ ] RSI Swing Reversal: RSI < 30, bounce confirmation
- [ ] Earnings Momentum: Earnings beat + volume + price spike
- [ ] Moving Average Crossover: e.g., EMA 50/200

### Backtest Engine
- [ ] Walk-forward testing
- [ ] Parameter sweep backtesting (grid search for optimal configs)  
  _It may be helpful to define how these parameters will be configured (e.g., JSON, CLI flags, or UI), especially for automation later._
- [ ] Realistic fills/slippage modeling
- [ ] Export backtest stats to charts (e.g., PnL curves)

### Data Layer
- [ ] Integrate fundamental API (e.g., Polygon, Finnhub)
- [ ] Add sector filters to strategies
- [ ] Tag tickers with ETF/Index membership

### Logging & Monitoring
- [ ] Add nightly report summary via Telegram
- [ ] Store logs in S3 bucket for durability

---

## 🔧 Phase 3: Automation & Ops (P3)

### Infra
- [ ] Auto-deploy AWS Lambda from CLI
- [ ] Daily cron (6 AM ET buy job)
- [ ] 30-minute interval cron for sell job (8 AM - 6 PM ET)
- [ ] Split environments: dev vs prod mode (paper vs live)

### Notification
- [ ] Add Slack/Discord webhook alerts
- [ ] Use Sentry for error logging

### Quality of Life
- [ ] Web dashboard to view current positions, PnL, and logs  
  _You might want to indicate whether this dashboard will be built with a specific framework (e.g., Streamlit, Flask) to guide future planning._
- [ ] Strategy toggling via JSON or UI config
- [ ] Filter trades by sector or theme

---

## 🌟 Experimental Ideas

- [ ] AI model to rank strategy success based on backtests  
  _Consider clarifying whether this model would use statistical evaluation (e.g., Sharpe, win rate) or integrate LLM-based analysis._
- [ ] Adaptive capital allocation per strategy
- [ ] Sentiment analysis filters (optional)
- [ ] Dynamic position sizing based on volatility or Kelly criterion

---

## ⚡ Tracking

- Keep this updated as we build.
- Items may move between phases based on testing, bugs, or new insights.

---

_Last updated: April 2025_
