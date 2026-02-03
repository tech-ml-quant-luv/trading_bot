import pandas as pd
import numpy as np
import time
from fyers_apiv3 import fyersModel
from datetime import datetime, timedelta

RESOLUTION = 5
LOOKBACK_PERIOD = 5
client_id="ALT6RUE1IF-100"
secret_key="0UT0LW5PE4"
redirect_uri="https://luvratan.tech/"


def create_data_range(lookback_period):
    lookback_seconds = lookback_period * 24* 60* 60 #Since fyers api give timestamp in seconds
    range_to = int(time.time()) 
    range_from = range_to - lookback_seconds
    ranges = {
        "range_from":range_from,
        "range_to": range_to
    }
    return ranges

def fetch_data(ticker):
    # access_token = input("Enter access token")
    access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOlsiZDoxIiwiZDoyIiwieDowIiwieDoxIl0sImF0X2hhc2giOiJnQUFBQUFCcGdZQkpIWUtIZnpEdUllMW9wMkF3NUJZOE53Y2FITzdWYVVlSjVxRFJGc3lOaTVqZDZWXzNZc0NTNWw5dmF2WmRGelBPenoyeV9fcHBHR2lybEF6SnVON2ZCWW1wX2NSVXIwNmRmSHQ4WU9RczRnVT0iLCJkaXNwbGF5X25hbWUiOiIiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIyMDc4NGJkZTQ4NDliZTdjNmYxZmI4MGM3OWNiNDNmNzJmZTQxMmMyYzA0ZmNjNTUxMWVhZjBlZiIsImlzRGRwaUVuYWJsZWQiOiJOIiwiaXNNdGZFbmFibGVkIjoiTiIsImZ5X2lkIjoiWEwwMDcyMSIsImFwcFR5cGUiOjEwMCwiZXhwIjoxNzcwMTY1MDAwLCJpYXQiOjE3NzAwOTQ2NjUsImlzcyI6ImFwaS5meWVycy5pbiIsIm5iZiI6MTc3MDA5NDY2NSwic3ViIjoiYWNjZXNzX3Rva2VuIn0.GT2ZY46axzp0mSX-bYfcp--UOtapgNzek8mMWjlve0c"
    
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
    ranges = create_data_range(LOOKBACK_PERIOD)
    data = {
    "symbol": f"NSE:{ticker}-EQ",
    "resolution": RESOLUTION,
    "date_format": "0",
    "range_from": ranges["range_from"],
    "range_to": ranges["range_to"],
    "cont_flag": "1"
    }
    response = fyers.history(data=data)
    return response


def fyers_history_to_df(ticker) -> pd.DataFrame:
    """
    Convert FYERS history API response to a pandas DataFrame.
    Shifts intraday candle timestamps forward by 15 minutes.
    """
    response = fetch_data(ticker)

    if response.get("s") != "ok":
        raise ValueError(f"FYERS API error: {response}")
    print(response["candles"])
    df = pd.DataFrame(
        response["candles"],
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )

    # Convert UNIX epoch → timezone-aware datetime (IST)
    df["datetime"] = (
        pd.to_datetime(df["timestamp"], unit="s", utc=True)
        .dt.tz_convert("Asia/Kolkata")
    )

    # Shift candle time forward by n minutes
    # df["datetime"] = df["datetime"] + pd.Timedelta(minutes=resolution)

    # Sort by adjusted time
    df = df.sort_values("datetime")

    # Drop raw timestamp if not needed
    df = df.drop(columns=["timestamp"])
    df = df.set_index("datetime")

    return df
