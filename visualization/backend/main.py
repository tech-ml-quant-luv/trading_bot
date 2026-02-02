from fyers_apiv3.FyersWebsocket import data_ws
from datetime import datetime
import signal
import sys

# ----------------------------
# Engine hooks (placeholders)
# ----------------------------

def handle_tick(symbol: str, ltp: float, ts: int):
    """
    Single source of truth for live ticks.
    Later this will:
    - update OHLCV
    - update indicators
    - publish bars to visualization
    """
    exchange_time = datetime.fromtimestamp(ts)
    print(f"[{exchange_time}] {symbol} | LTP: {ltp}")


# ----------------------------
# WebSocket callbacks
# ----------------------------

def on_error(message):
    print("WebSocket Error:", message)


def on_close(message):
    print("WebSocket Closed:", message)


def on_open():
    print("WebSocket Connected")

    symbols = [
        "NSE:ADANIPORTS-EQ",
        "NSE:SBIN-EQ"
    ]

    fyers.subscribe(
        symbols=symbols,
        data_type="SymbolUpdate"
    )

    fyers.keep_running()


def on_message(message):
    """
    Expected message format (Fyers):
    {
        'symbol': 'NSE:SBIN-EQ',
        'ltp': 612.35,
        'timestamp': 1706855402
    }
    """
    try:
        symbol = message.get("symbol")
        ltp = message.get("ltp")
        ts = message.get("timestamp")

        if symbol is None or ltp is None or ts is None:
            return

        handle_tick(symbol, float(ltp), int(ts))

    except Exception as e:
        print("Tick handling error:", e)


# ----------------------------
# Graceful shutdown
# ----------------------------

def shutdown(sig, frame):
    print("Shutting down...")
    fyers.close_connection()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


# ----------------------------
# Entry point
# ----------------------------

def start_fyers_socket(access_token: str):
    global fyers

    fyers = data_ws.FyersDataSocket(
        access_token=access_token,   # "appid:accesstoken"
        log_path="",
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=on_open,
        on_close=on_close,
        on_error=on_error,
        on_message=on_message
    )

    fyers.connect()


if __name__ == "__main__":
    # TEMPORARY (until frontend supplies token)
    ACCESS_TOKEN = "APPID:ACCESS_TOKEN"

    start_fyers_socket(ACCESS_TOKEN)
