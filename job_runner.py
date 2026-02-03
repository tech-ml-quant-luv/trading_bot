from datetime import datetime
from features.create_features import create_features
from data.fetch_ohlcv_data import fyers_history_to_df
from concurrent.futures import ThreadPoolExecutor
from data.sqlite_store import save_features_df

TICKERS = ["ADANIPORTS", "ICICIBANK", "INFY", "RELIANCE"]

def pipeline_function(ticker):
    start_time = datetime.now()
    print(f"{ticker}, Job started at {start_time}")

    #Fetch data for one ticker
    df = fyers_history_to_df(ticker)
    final_df = create_features(df)

    print(f"{ticker} Latest Row: {final_df.tail(1)}")

    save_features_df(ticker, final_df)

    print(f"Job completed at {datetime.now()}")

def run_pipeline():
    with ThreadPoolExecutor(max_workers=4) as executer:
        executer.map(pipeline_function, TICKERS)


   
