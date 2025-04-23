# core/data_provider.py

from typing import List, Literal
import pandas as pd
import os

# Define valid data source types
DataSourceType = Literal["yfinance", "alpaca"]

# Get default source from environment variable or fallback to 'yfinance'
DEFAULT_SOURCE_RAW = os.getenv("DATA_SOURCE", "yfinance")

# ---------- YFINANCE IMPLEMENTATION ----------
def get_data_yfinance(symbols: List[str], start: str, end: str) -> dict:
    """
    Fetch daily OHLCV data from Yahoo Finance for given symbols and date range.
    """
    import yfinance as yf
    result = {}
    for symbol in symbols:
        df = yf.download(symbol, start=start, end=end, interval="1d", auto_adjust=False)
        if not df.empty:
            df["Symbol"] = symbol  # Add symbol column for identification
            result[symbol] = df
    return result

# ---------- ALPACA IMPLEMENTATION ----------
def get_data_alpaca(symbols: List[str], start: str, end: str) -> dict:
    """
    Fetch daily OHLCV data from Alpaca API for given symbols and date range.
    Requires proper API credentials to be configured.
    """
    from alpaca.data.historical import StockHistoricalDataClient
    from alpaca.data.requests import StockBarsRequest
    from alpaca.data.timeframe import TimeFrame
    import datetime

    client = StockHistoricalDataClient()
    request_params = StockBarsRequest(
        symbol_or_symbols=symbols,
        timeframe=TimeFrame.Day,
        start=datetime.datetime.fromisoformat(start),
        end=datetime.datetime.fromisoformat(end)
    )
    bars = client.get_stock_bars(request_params).df

    result = {}
    for symbol in symbols:
        symbol_df = bars[bars["symbol"] == symbol].copy()
        if not symbol_df.empty:
            symbol_df["Symbol"] = symbol  # Add symbol column for identification
            result[symbol] = symbol_df
    return result

# ---------- PUBLIC INTERFACE FUNCTION ----------
def get_daily_data(
    symbols: List[str],
    start: str,
    end: str,
    source: DataSourceType = DEFAULT_SOURCE_RAW
) -> dict[str, pd.DataFrame]:
    """
    Unified interface to fetch daily stock data.
    Selects data provider based on `source` parameter.
    """
    if source == "yfinance":
        return get_data_yfinance(symbols, start, end)
    elif source == "alpaca":
        return get_data_alpaca(symbols, start, end)
    else:
        raise ValueError(f"Unknown data source: {source}")