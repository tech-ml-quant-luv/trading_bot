import time
import pandas as pd
import numpy as np

from create_features import create_features
from fetch_ohlcv_data import fyers_history_to_df

# -------------------------------
# Start total timer
# -------------------------------
t0 = time.perf_counter()

# -------------------------------
# Fetch OHLCV
# -------------------------------
t_fetch_start = time.perf_counter()
df = fyers_history_to_df()
t_fetch_end = time.perf_counter()

# -------------------------------
# Feature engineering
# -------------------------------
t_feat_start = time.perf_counter()
final_df = create_features(df)
t_feat_end = time.perf_counter()

# -------------------------------
# Save (optional)
# -------------------------------
df.to_csv("current_data.csv")

# -------------------------------
# End total timer
# -------------------------------
t1 = time.perf_counter()

# -------------------------------
# Print latency
# -------------------------------
print(f"Fetch latency        : {(t_fetch_end - t_fetch_start)*1000:.2f} ms")
print(f"Feature latency      : {(t_feat_end - t_feat_start)*1000:.2f} ms")
print(f"Total pipeline time  : {(t1 - t0)*1000:.2f} ms")
