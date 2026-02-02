# print(final_df.tail(1))
# final_df.to_csv("current_data.csv")


from datetime import datetime
from create_features import create_features
from fetch_ohlcv_data import fyers_history_to_df

def run_pipeline():
    start_time = datetime.now()
    print(f"Job started at {start_time}")

    df = fyers_history_to_df()
    final_df = create_features(df)

    print(final_df.tail(1))
    final_df.to_csv("current_data.csv", index=False)

    print(f"Job completed at {datetime.now()}")
