from datetime import datetime
from features.create_features import create_features
from data.fetch_ohlcv_data import fyers_history_to_df
from concurrent.futures import ThreadPoolExecutor
from data.sqlite_store import save_features_df
from engine.inference import get_latest_prediction
from shared_state import update_row

TICKERS = ["ADANIPORTS", "ICICIBANK", "INFY", "RELIANCE", "HINDALCO"]
columns_required = ['support', 'resistance', 'rsi_14', 'atr', '20ma', '50ma', '200ma']


def pipeline_function(ticker):
    # Fetch data for one ticker
    df = fyers_history_to_df(ticker)
    final_df = create_features(df.copy())
    
    # Get ML prediction for latest bar
    prediction = get_latest_prediction(ticker, final_df)
    if prediction:
        print(f"{ticker} | Pred: {prediction['prediction']} | Confidence: {prediction['confidence']:.2%}")
    else:
        print(f"{ticker} | No prediction (model not found or NaN values)")
    
    # Save features with predictions
    save_features_df(ticker, final_df)
    
    # Prepare last row for shared state
    last_row = final_df[columns_required].iloc[-1].to_dict()
    
    # Add predictions to the dict
    if prediction:
        last_row['ml_prediction'] = prediction['prediction']
        last_row['ml_confidence'] = prediction['confidence']
    else:
        last_row['ml_prediction'] = None
        last_row['ml_confidence'] = None
    
    # Add ticker
    last_row['ticker'] = ticker
    
    # Update shared state
    update_row(ticker, last_row)
    print(f"{ticker} | Shared state updated")


def run_pipeline():
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(pipeline_function, TICKERS)