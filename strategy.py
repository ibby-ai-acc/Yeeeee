import os, requests, pandas as pd
from dotenv import load_dotenv
load_dotenv()

BASE = "https://data.alpaca.markets/v2"
HEAD = {
    "APCA-API-KEY-ID":     os.getenv("ALPACA_API_KEY"),
    "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY")
}

WATCHLIST = [
    "AAPL","MSFT","TSLA","NVDA","GOOGL","AMZN","INTC","ORCL",
    "CSCO","TSM","QCOM","PFE","MRK","JNJ","UNH","HD",
    "PG","COST","KO","NKE","ADBE","CRM","HLAL","SPUS","VOO"
]

def _bars(sym, tf="15Min", lim=100):
    r = requests.get(f"{BASE}/stocks/{sym}/bars",
                     headers=HEAD, params={"timeframe": tf, "limit": lim})
    if r.status_code != 200: return None
    df = pd.DataFrame(r.json().get("bars", []))
    if df.empty: return None
    df['t'] = pd.to_datetime(df['t']); df.set_index('t', inplace=True)
    return df

def _ind(df):
    df['EMA9']  = df['c'].ewm(span=9).mean()
    df['EMA21'] = df['c'].ewm(span=21).mean()
    delta = df['c'].diff(); gain = delta.clip(lower=0); loss = -delta.clip(upper=0)
    rs = gain.rolling(14).mean() / loss.rolling(14).mean()
    df['RSI'] = 100 - 100/(1+rs)
    df['Vavg20'] = df['v'].rolling(20).mean()
    return df

def signal_for(sym):
    df = _bars(sym);  # 15-min bars
    if df is None or len(df) < 22: return "hold", sym, 0
    df = _ind(df);    now, prev = df.iloc[-1], df.iloc[-2]
    if (now['EMA9']>now['EMA21'] and prev['EMA9']<=prev['EMA21']
        and 40<now['RSI']<70 and now['v']>1.5*now['Vavg20']):
        return "buy", sym, now['c']
    if (now['EMA9']<now['EMA21'] and prev['EMA9']>=prev['EMA21']
        and now['RSI']>70):
        return "sell", sym, now['c']
    return "hold", sym, now['c']

def find_best_signal():
    for s in WATCHLIST:
        sig, _, p = signal_for(s)
        if sig=="buy": return sig, s, p
    return "hold", None, None
