from django.core.exceptions import ValidationError
import pandas as pd
import requests
from tbo.settings import COINGECKO_API_KEY


SYMBOL_MAP = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "SOL": "solana",
}

AVAILABLE_DAYS = [1, 7, 14, 30, 90, 180, 365 ]

def get_ohlcv(symbol: str, days: int=365):
    """
    Fetches OHLC data from CoinGecko's api.
    Data is returned in json and then converted to pd dataframe format.
    """

    # Checks if api endpoint parameters are allowed, if not validation error raised.
    symbol = symbol.upper()
    if symbol not in SYMBOL_MAP:
        raise ValidationError(f"Unsupported symbol {symbol}")
    
    coin_id = SYMBOL_MAP[symbol]

    # Number of days is set to 365 as default for now
    days_selected = 365
    if days_selected not in AVAILABLE_DAYS:
        raise ValidationError(f"Unsupported number of days. Selected: {days_selected}")
    
    days = days_selected
    
    # Dynamic url for api calls
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc?vs_currency=usd&days={days}"

    headers = {"x-cg-demo-api-key": COINGECKO_API_KEY}

    response = requests.get(url, headers=headers)
    print(response.status_code)

    # Converts response into ohlc dataframe format
    data = response.json()
    df = pd.DataFrame(data, columns=["timestamp", "Open", "High", "Low", "Close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    print(df)

    return df