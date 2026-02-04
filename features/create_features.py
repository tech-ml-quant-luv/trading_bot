import pandas as pd
import numpy as np

def create_features(df):
    df = df.copy()

    #Calculate Support and resistance

    df["resistance"] = df["close"].shift().rolling(10).max() 
    df["support"]    = df["close"].shift().rolling(10).min() 



    # Calculate True Range 
    # df['prev_close'] = df['close'].shift(1)
    # df['tr'] = df[['high', 'low', 'prev_close']].apply(
    #     lambda x: max(x['high'] - x['low'], 
    #                 abs(x['high'] - x['prev_close']), 
    #                 abs(x['low'] - x['prev_close'])), axis=1
    # )
    df['prev_close'] = df['close'].shift(1)
    high_low = df['high'] - df['low']
    high_pc  = (df['high'] - df['prev_close']).abs()
    low_pc   = (df['low'] - df['prev_close']).abs()

    df['tr'] = np.maximum.reduce([high_low, high_pc, low_pc])
    df['atr'] = df['tr'].shift().rolling(14).mean()



    # Session Progress and Position-Based Features
    df["hour"] = df.index.hour
    # First, let's define market hours in minutes
    market_open_minutes = 9 * 60 + 15  # 9:15 AM = 555 minutes from midnight
    market_close_minutes = 15 * 60 + 30  # 3:30 PM = 930 minutes from midnight
    total_trading_minutes = market_close_minutes - market_open_minutes  # 375 minutes (6h 15min)

    # Get current time in minutes from midnight
    df['current_minutes'] = df['hour'] * 60 + pd.to_datetime(df.index).minute

    # Calculate session progress (0 at open, 1 at close)
    df['session_progress'] = (df['current_minutes'] - market_open_minutes) / total_trading_minutes

    # Create binary flags for early and late sessions
    df['is_early_session'] = (df['session_progress'] < 0.33).astype(int)  # First ~2 hours
    df['is_late_session'] = (df['session_progress'] > 0.67).astype(int)   # Last ~2 hours

    # Optional: You can drop the intermediate 'current_minutes' column if you don't need it
    # df = df.drop('current_minutes', axis=1)


    df['hl_ratio'] = (
        (df['high'].shift(1) - df['low'].shift(1)) / df['close'].shift(1)
    )   #This comes from previous candle


    df['open_to_support_dist'] = (df['open'] - df['support']) / df['open']


    df = df.copy()
    lookback = 20 

    df["volume_ma"] = df["volume"].shift().rolling(window=lookback).mean()
    df["volume_ratio"] = df["volume"].shift() / df["volume_ma"]



    #Calcualate RSI

    def calculate_rsi(data, period=14):
        delta = data.diff().shift(1)  # ✓ Shift after diff
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    df["rsi_14"] = calculate_rsi(df["close"], period=14)




    #Calculate MACD

    def calculate_macd(data, fast=12, slow=26, signal=9):
        shifted_data = data.shift(1)
        ema_fast = shifted_data.ewm(span=fast, adjust=False).mean()
        ema_slow = shifted_data.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        macd_histogram = macd_line - signal_line
        return macd_line, signal_line, macd_histogram

    df["macd"], df["macd_signal"], df["macd_hist"] = calculate_macd(df["close"])

    # Normalize by PREVIOUS close (not current)
    df["macd_norm"] = df["macd"] / df["close"].shift(1)
    df["macd_hist_norm"] = df["macd_hist"] / df["close"].shift(1)



    # Moving averages (just for calculation, not direct features)
    df["5ma"] = df["close"].shift().rolling(5).mean()
    df["10ma"] = df["close"].shift().rolling(10).mean()
    df["20ma"] = df["close"].shift().rolling(20).mean()
    df["50ma"] = df["close"].shift().rolling(50).mean()
    df["200ma"] = df["close"].shift().rolling(200).mean()  # Fixed: was 100

    # RELATIVE features (normalized by price)
    df["5_10_ma_diff_pct"] = (df["5ma"] - df["10ma"]) / df["close"].shift()
    df["close_5ma_diff_pct"] = (df["close"].shift() - df["5ma"]) / df["close"].shift()
    df["close_10ma_diff_pct"] = (df["close"].shift() - df["10ma"]) / df["close"].shift()
    df["golden_cross_pct"] = (df["50ma"] - df["200ma"]) / df["close"].shift()

    # Additional useful MA features
    df["close_50ma_diff_pct"] = (df["close"].shift() - df["50ma"]) / df["close"].shift()
    df["close_200ma_diff_pct"] = (df["close"].shift() - df["200ma"]) / df["close"].shift()

    # Slope/momentum of MAs (rate of change)
    df["5ma_roc"] = df["5ma"].pct_change(periods=5)
    df["50ma_roc"] = df["50ma"].pct_change(periods=10)


    #Pressure Features

    df["volume_pressure_prev"] = (
        df["close"].shift(1) - df["open"].shift(1)
    ) / df["volume"].shift(1)
    df["range_per_volume_prev"] = (
        df["high"].shift(1) - df["low"].shift(1)
    ) / df["volume"].shift(1)

    #Gap Features


    df["gap_pct"] = (
        df["open"] - df["close"].shift(1)
    ) / df["close"].shift(1)


    #Candle type

    df["candle_type"] = (df["close"].shift() - df["open"].shift())/(df["high"].shift()-df["low"].shift())   
    df["candle_type_lag1"] = df["candle_type"].shift(1)  # Previous candle
    df["candle_type_lag2"] = df["candle_type"].shift(2)  # 2 candles ago


    #Position of the price

    # Open's position relative to S/R levels
    df['open_above_resistance'] = (
        ((df['open'] - df['resistance']) / df['atr']).shift(1)
    )
    df['open_below_support'] = (
        ((df['support'] - df['open']) / df['atr']).shift(1)
    )

    # Or combined - where is open in the S/R range?
    df['open_sr_position'] = (
        ((df['open'] - df['support']) / (df['resistance'] - df['support']))
    ).shift(1)  # 0 = at support, 1 = at resistance, >1 = above, <0 = below

    # S/R range width (how wide is the channel?)
    df['sr_range_atr'] = (
        ((df['resistance'] - df['support']) / df['atr']).shift(1)
    )




    #Breakout Features

    # Strength
    df['resistance_breakout_strength'] = (
        ((df['close'] - df['resistance']) / df['atr']).clip(lower=0).shift(1)
    )
    df['support_breakdown_strength'] = (
        ((df['support'] - df['close']) / df['atr']).clip(lower=0).shift(1)
    )
    # Conviction
    rng = (df['high'] - df['low']).replace(0, np.nan)
    df['resistance_breakout_conviction'] = (
        ((df['close'] - df['resistance']) / rng).clip(-1, 1).shift(1)
    )
    df['support_breakdown_conviction'] = (
        ((df['support'] - df['close']) / rng).clip(-1, 1).shift(1)
    )
    # Volume
    df['breakout_volume_ratio'] = (
        df['volume'] / df['volume'].rolling(20).mean()
    ).shift(1)
    # Pressure / velocity
    df['resistance_touch_count'] = (
        (df['high'].shift(1) >= df['resistance'].shift(1))
        .rolling(10).sum()
    )
    df['support_touch_count'] = (
        (df['low'].shift(1) <= df['support'].shift(1))
        .rolling(10).sum()
    )

    return df
