import pandas as pd
import numpy as np
from joblib import load
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

# Feature columns (same order as training)
FEATURE_COLUMNS = [
    'hour', 'session_progress', 'is_early_session', 'is_late_session',
    'hl_ratio', 'volume_ma', 'volume_ratio', 'volume_pressure_prev',
    'range_per_volume_prev', 'breakout_volume_ratio', 'rsi_14',
    'macd', 'macd_signal', 'macd_hist', 'macd_norm', 'macd_hist_norm',
    '5ma', '10ma', '50ma', '200ma', '5_10_ma_diff_pct',
    'close_5ma_diff_pct', 'close_10ma_diff_pct', 'golden_cross_pct',
    'close_50ma_diff_pct', 'close_200ma_diff_pct', '5ma_roc', '50ma_roc',
    'gap_pct', 'candle_type', 'candle_type_lag1', 'candle_type_lag2',
    'resistance', 'support', 'resistance_breakout_strength',
    'support_breakdown_strength', 'resistance_breakout_conviction',
    'support_breakdown_conviction', 'resistance_touch_count',
    'support_touch_count'
]

# Model configuration
TIMEFRAME_MINUTES = 5  # Changed from to 5 for your naming convention
CONFIDENCE_THRESHOLD = 0.6

# Cache loaded models to avoid reloading
_model_cache = {}


def load_model(ticker):
    """Load XGBoost model for a ticker (with caching)"""
    if ticker in _model_cache:
        return _model_cache[ticker]
    
    # Updated model path: models/ADANIPORTS_5_XGB.joblib
    model_path = os.path.join(
    MODEL_DIR,
    f"{ticker}_{TIMEFRAME_MINUTES}_XGB.joblib"
)
    if not os.path.exists(model_path):
        print(f"Warning: Model not found at {model_path}")
        return None
    
    try:
        model = load(model_path)
        _model_cache[ticker] = model
        return model
    except Exception as e:
        print(f"Error loading model {model_path}: {str(e)}")
        return None


def get_latest_prediction(ticker, final_df):
    model = load_model(ticker)
    if model is None:
        return None
    
    try:
        # Extract features
        latest_features = final_df[FEATURE_COLUMNS].iloc[-1:].copy()
        
        if latest_features.isnull().any().any():
            print(f"{ticker}: Latest row has NaN values, skipping prediction")
            return None
        
        # Convert to numpy array to bypass feature name validation
        X_array = latest_features.values
        
        # Get prediction
        y_pred_binary = model.predict(X_array)[0]
        y_pred = y_pred_binary * 2 - 1
        
        # Get confidence
        y_pred_proba = model.predict_proba(X_array)[0, 1]
        
        # Generate trade signal
        trade_signal = (y_pred == 1) and (y_pred_proba >= CONFIDENCE_THRESHOLD)
        
        # Add predictions back to final_df
        final_df.loc[latest_features.index, 'ml_prediction'] = y_pred
        final_df.loc[latest_features.index, 'ml_confidence'] = y_pred_proba
        final_df.loc[latest_features.index, 'trade_signal'] = trade_signal
        
        return {
            'timestamp': latest_features.index[0],
            'prediction': y_pred,
            'confidence': y_pred_proba,
            'trade_signal': trade_signal
        }
        
    except Exception as e:
        print(f"{ticker}: Error in prediction - {str(e)}")
        return None

def get_batch_predictions(ticker, final_df):
    """
    Get predictions for all rows (for backtesting)
    
    Parameters:
    -----------
    ticker : str
        Stock ticker name (e.g., "ADANIPORTS")
    final_df : pd.DataFrame
        DataFrame with all features created
    
    Returns:
    --------
    pd.DataFrame : final_df with added columns: ml_prediction, ml_confidence, trade_signal
    """
    
    model = load_model(ticker)
    if model is None:
        return final_df
    
    # Extract all valid features
    X = final_df[FEATURE_COLUMNS].dropna()
    
    if len(X) == 0:
        print(f"{ticker}: No valid samples for prediction")
        return final_df
    
    try:
        # Get predictions
        y_pred_binary = model.predict(X)
        y_pred = y_pred_binary * 2 - 1
        
        # Get probabilities
        y_pred_proba = model.predict_proba(X)[:, 1]
        
        # Add to dataframe
        final_df.loc[X.index, 'ml_prediction'] = y_pred
        final_df.loc[X.index, 'ml_confidence'] = y_pred_proba
        final_df.loc[X.index, 'trade_signal'] = (
            (y_pred == 1) & (y_pred_proba >= CONFIDENCE_THRESHOLD)
        )
        
        print(f"{ticker}: Generated {len(X)} predictions")
        print(f"  - Predicted profitable: {(y_pred == 1).sum()}")
        print(f"  - Predicted losing: {(y_pred == -1).sum()}")
        print(f"  - Trade signals: {final_df['trade_signal'].sum()}")
        
        return final_df
        
    except Exception as e:
        print(f"{ticker}: Error in batch prediction - {str(e)}")
        import traceback
        traceback.print_exc()
        return final_df
