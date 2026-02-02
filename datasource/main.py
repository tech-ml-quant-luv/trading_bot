import pandas as pd
import numpy as np

from create_features import create_features
from fetch_ohlcv_data import fyers_history_to_df

df = fyers_history_to_df()
final_df = create_features(df)

df.to_csv("current_data.csv")