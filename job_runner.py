from datetime import datetime
from features.create_features import create_features
from data.fetch_ohlcv_data import fyers_history_to_df
from concurrent.futures import ThreadPoolExecutor
from data.sqlite_store import save_features_df
from engine.inference import get_latest_prediction

TICKERS = ["ADANIPORTS", "ICICIBANK", "INFY", "RELIANCE", "HINDALCO"]


def pipeline_function(ticker):
    start_time = datetime.now()
    print(f"{ticker}, Job started at {start_time}")

    # Fetch data for one ticker
    df = fyers_history_to_df(ticker)
    final_df = create_features(df)
    
    # Get ML prediction for latest bar
    prediction = get_latest_prediction(ticker, final_df)
    
    if prediction and prediction['trade_signal']:
        print(f"🟢 {ticker} | TRADE SIGNAL | Confidence: {prediction['confidence']:.2%}")
    
    # Save features with predictions
    save_features_df(ticker, final_df)

    print(f"{ticker}, Job completed at {datetime.now()}")


def run_pipeline():
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(pipeline_function, TICKERS)