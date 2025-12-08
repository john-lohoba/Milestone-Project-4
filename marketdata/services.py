from django.core.exceptions import ValidationError
from datetime import datetime
import pandas as pd
import requests

COINGECKO_BASE = "https://api.coingecko.com/api/v3"


def get_ohlcv(symbol: str, timeframe: str, start, end) -> pd.DataFrame:
    """
    Fetch OHLCV data from CoinGecko and Converts to DataFrame
    """
    coin_id = symbol_to_coingecko_id(symbol)
    if coin_id is None:
        raise ValidationError(f"Unknown symbol '{symbol}'")
    
    days = (end - start).days

    url = f"{COINGECKO_BASE}/coins/{coin_id}/ohlc"
    params = {"vs_currency": "usd", "days": days}

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if not data or not isinstance(data, list):
        raise ValidationError("CoinGecko returned empty OHLC data.")
    
    # Converts retrieved data into pd DataFrame for Backtesting to use later
    df = pd.DataFrame(
        data,
        columns=["timestamps", "Open", "High", "Low", "Close"]
    )

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)

    # Add dummy data for volume since CoinGecko doesn't by default
    df["Volume"] = 1.0

    df = df.loc[start:end]

    return df

def symbol_to_coingecko_id(symbol: str) -> str | None:
    """
    CoinGecko ID mapper
    """
    symbol = symbol.lower()
    mapping = {
        "btc": "bitcoin",
        "eth": "etherium",
        "sol": "solana",
    }

    return mapping.get(symbol)
