import datetime

def trigger_long(ltp, ma20, ma50, ma200, rsi, ticker):
    if (ltp >= ma20) and (35 <= rsi <= 55) and (ma50 > ma200):
        print(f"Long entry triggered for {ticker} at {datetime.datetime.now()}")

def trigger_short(ltp, ma20, ma50, ma200, rsi, ticker):
    if (ltp <= ma20) and (60 <= rsi <= 75) and (ma50 < ma200):
        print(f"Short entry triggered for {ticker} at {datetime.datetime.now()}")