import datetime
import sqlite3
import os

# Absolute path to database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'execution', 'trading_bot.db')

def log_trigger(ticker, signal_type, ltp, support, resistance, ma20, ma50, ma200, rsi, ml_prediction, ml_confidence, trigger_reason):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO orders_log 
        (timestamp, ticker, signal_type, ltp, support, resistance, ma20, ma50, ma200, rsi, ml_prediction, ml_confidence, trigger_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (datetime.datetime.now(), ticker, signal_type, ltp, support, resistance, ma20, ma50, ma200, rsi, ml_prediction, ml_confidence, trigger_reason))
    conn.commit()
    conn.close()

def trigger_long(ltp, ma20, ma50, ma200, rsi, ticker, support, resistance, ml_prediction, ml_confidence):
    if (ltp >= ma20):
        print(f"Long entry triggered for {ticker} at {datetime.datetime.now()}")
        log_trigger(ticker, 'LONG', ltp, support, resistance, ma20, ma50, ma200, rsi, ml_prediction, ml_confidence, 'ltp<=support & conditions met')

def trigger_short(ltp, ma20, ma50, ma200, rsi, ticker, support, resistance, ml_prediction, ml_confidence):
    if (ltp <= ma20):
        print(f"Short entry triggered for {ticker} at {datetime.datetime.now()}")
        log_trigger(ticker, 'SHORT', ltp, support, resistance, ma20, ma50, ma200, rsi, ml_prediction, ml_confidence, 'ltp>=resistance & conditions met')