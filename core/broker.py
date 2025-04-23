import alpaca_trade_api as tradeapi
from config.settings import ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL)

def buy_stock(symbol, qty):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        print(f"✅ Order placed: BUY {symbol} x{qty}")
    except Exception as e:
        print(f"❌ Failed to BUY {symbol}: {e}")
        raise  # Let the outer code decide what to do


def sell_stock(symbol: str, qty: int):
    try:
        order = api.submit_order(
            symbol=symbol,
            qty=qty,
            side="sell",
            type="market",
            time_in_force="day"
        )
        print(f"✅ Order placed: SELL {symbol} x{qty}")
        return order
    except Exception as e:
        if "wash trade" in str(e).lower():
            print(f"⚠️ Wash trade detected on SELL {symbol}. Skipping.")
        else:
            print(f"❌ Failed to SELL {symbol}: {e}")
        raise



def get_current_price(symbol):
    return float(api.get_latest_trade(symbol).price)

