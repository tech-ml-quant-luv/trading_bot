import sqlite3

def create_orders_log_table():
    conn = sqlite3.connect('trading_bot.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            ticker VARCHAR(20),
            signal_type VARCHAR(10),
            ltp FLOAT,
            support FLOAT,
            resistance FLOAT,
            ma20 FLOAT,
            ma50 FLOAT,
            ma200 FLOAT,
            rsi FLOAT,
            ml_prediction VARCHAR(10),
            ml_confidence FLOAT,
            trigger_reason VARCHAR(50)
        )
    """)
    conn.commit()
    conn.close()

# Call this on startup
create_orders_log_table()