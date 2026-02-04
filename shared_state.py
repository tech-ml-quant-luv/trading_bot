import threading
import sqlite3
import pandas as pd

# Database path
DB_PATH = "data/market_data.db"

# Stock symbols
SYMBOLS = ['ADANIPORTS', 'ICICIBANK', 'RELIANCE', 'INFY', 'HINDALCO']
columns_required = ['support', 'resistance', 'rsi_14', 'atr', '20ma', '50ma', '200ma', 'ml_prediction', 'ml_confidence']

# Shared state - stores last row for each stock as dict
latest_rows = {}

# Lock for thread safety
lock = threading.Lock()


def load_last_rows():
    """Load last row from each table on startup as dict."""
    conn = sqlite3.connect(DB_PATH)
    
    for symbol in SYMBOLS:
        table_name = f"features_{symbol.lower()}"
        query = f"SELECT * FROM {table_name} ORDER BY datetime DESC LIMIT 1"
        df = pd.read_sql(query, conn)
        
        if not df.empty:
            latest_rows[symbol] = df.iloc[0].to_dict()
        else:
            latest_rows[symbol] = None
    
    conn.close()
    print("Loaded last rows from database")


def get_row(symbol):
    """Get last row for a symbol as dict."""
    with lock:
        return latest_rows.get(symbol)


def get_all_rows():
    """Get all last rows as dict."""
    with lock:
        return latest_rows.copy()


def update_row(symbol, row_dict):
    """Update last row for a symbol. Only accepts dict."""
    with lock:
        latest_rows[symbol] = row_dict


# Load data when module is imported
# load_last_rows()