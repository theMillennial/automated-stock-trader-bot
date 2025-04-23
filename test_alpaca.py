from core.broker import api, get_current_price

# Check account info
account = api.get_account()
print(f"✅ Alpaca account status: {account.status}")
print(f"💰 Buying power: ${account.buying_power}")
print(f"🧾 Account equity: ${account.equity}")

# Get current price of a stock
symbol = "AAPL"
price = get_current_price(symbol)
print(f"📈 Last trade price for {symbol}: ${price}")
