import os, requests
from dotenv import load_dotenv

load_dotenv()

# auto-switches to live if you set ALPACA_BASE_URL in .env
BASE_URL = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
HEADERS  = {
    "APCA-API-KEY-ID":     os.getenv("ALPACA_API_KEY"),
    "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")
}

def _get(path, **p):
    return requests.get(f"{BASE_URL}{path}", headers=HEADERS, params=p).json()

def _post(path, payload):
    return requests.post(f"{BASE_URL}{path}", headers=HEADERS, json=payload).json()

# ── public helpers ───────────────────────────────────────────
get_account   = lambda: _get("/v2/account")
get_positions = lambda: _get("/v2/positions")

def place_order(sym, qty, side, tif="day"):
    body = {"symbol": sym, "qty": qty, "side": side,
            "type": "market", "time_in_force": tif}
    return _post("/v2/orders", body)
