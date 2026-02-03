import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "market_data.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def save_features_df(ticker,df):

    conn = get_connection()
    table_name = f"features_{ticker.lower()}"
    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )
    conn.close()


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candles (
            ticker TEXT,
            timestamp DATETIME,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            PRIMARY KEY (ticker, timestamp)
        )
    """)

    conn.commit()
    conn.close()

