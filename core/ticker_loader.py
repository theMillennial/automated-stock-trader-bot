import pandas as pd

def load_tickers(index_filter=None):
    df = pd.read_csv("data/tickers.csv")
    
    if index_filter:
        df = df[df["index"].str.contains(index_filter)]
    
    return df["symbol"].tolist()
