from alpaca_client import place_order
from telegram_alerts import send_telegram_message

def execute_trade(sym, qty, side):
    r = place_order(sym, qty, side)
    if 'id' in r:
        send_telegram_message(f"{side.upper()} {sym} qty {qty} OK")
    else:
        send_telegram_message(f"ORDER FAIL {sym}: {r}")
