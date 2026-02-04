import json
from pathlib import Path
from fyers_apiv3.FyersWebsocket import data_ws
from shared_state import get_row
from engine.trigger import trigger_long, trigger_short


TOKEN_PATH = Path(__file__).resolve().parent.parent / "assets" / "fyers_token.json"

client_id = "ALT6RUE1IF-100"
secret_key = "0UT0LW5PE4"
redirect_uri = "https://luvratan.tech/"


def get_access_token():
    with open(TOKEN_PATH, "r") as f:
        token_data = json.load(f)
    return token_data["access_token"]


def onmessage(message):
    """Handle incoming messages from WebSocket."""
    
    # Handle system messages (authentication, subscription, etc.)
    if 'symbol' not in message:
        print(f"System message: {message.get('message', 'Unknown')}")
        return
    
    full_symbol = message['symbol']
    ticker = full_symbol.split(':')[1].split('-')[0]  # Extract middle part
    row = get_row(ticker)
    
    # Handle cold start - database empty
    if row is None:
        print(f"No data available for {ticker} yet. Skipping...")
        return
    
    ltp = message['ltp']
    support = row['support']
    resistance = row['resistance']
    ma20 = row["20ma"]
    ma50 = row["50ma"]
    ma200 = row["200ma"]
    rsi = row["rsi_14"]
    
    if ltp <= support:
        trigger_long(ltp, ma20, ma50, ma200, rsi, ticker)
    elif ltp >= resistance:
        trigger_short(ltp, ma20, ma50, ma200, rsi, ticker)
    else:
        print("No Trigger yet")
    
    print(f"{ticker} | {row['ml_prediction']} | {row['ml_confidence']:.2%} | {ltp} | {support} | {resistance}")


def onerror(message):
    """Handle WebSocket errors."""
    print("Error:", message)


def onclose(message):
    """Handle WebSocket connection close events."""
    print("Connection closed:", message)


def onopen():
    """Subscribe to symbols upon WebSocket connection."""
    data_type = "SymbolUpdate"
    symbols = [
        'NSE:ADANIPORTS-EQ',
        'NSE:INFY-EQ',
        'NSE:ICICIBANK-EQ',
        'NSE:RELIANCE-EQ',
        'NSE:HINDALCO-EQ'
    ]
    fyers.subscribe(symbols=symbols, data_type=data_type)
    fyers.keep_running()


def start_live_data_stream():
    """Main function to start the WebSocket connection."""
    global fyers
    
    access_token = get_access_token()
    
    fyers = data_ws.FyersDataSocket(
        access_token=access_token,
        log_path="",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=onopen,
        on_close=onclose,
        on_error=onerror,
        on_message=onmessage
    )
    
    # This blocks and keeps running
    fyers.connect()


# Remove the direct execution
# fyers.connect()  # DELETE THIS LINE