import time, math
from alpaca_client import get_account, get_positions
from strategy import find_best_signal
from execution import execute_trade
from position_manager import PositionManager
from trade_logger import log_trade
from telegram_alerts import send_telegram_message

RISK_PCT   = 0.02     # 2 % per trade
TRAIL_PCT  = 1.5      # trailing stop %
POLL_SEC   = 60       # check every 60 s

pm   = PositionManager(TRAIL_PCT)
pos  = {"sym":None,"qty":0,"entry":0}

def size(cash, price): return max(1, math.floor((cash*RISK_PCT)/price))

def step():
    global pos
    if pos["sym"] is None:                     # hunt
        sig,sym,price = find_best_signal()
        if sig=="buy":
            cash = float(get_account()['cash'])
            q=size(cash,price)
            execute_trade(sym,q,"buy")
            pm.open(price)
            pos={"sym":sym,"qty":q,"entry":price}
            log_trade("BUY",sym,q,price)
    else:                                      # manage
        for p in get_positions():
            if p['symbol']==pos["sym"]:
                cur=float(p['current_price'])
                if pm.check(cur):              # trailing stop hit
                    execute_trade(pos["sym"],pos["qty"],"sell")
                    log_trade("SELL",pos['sym'],pos['qty'],cur)
                    send_telegram_message(f"Exit {pos['sym']} @ {cur:.2f}")
                    pm.reset(); pos={"sym":None,"qty":0,"entry":0}
                break

if __name__=="__main__":
    send_telegram_message("🚀 Demo bot ONLINE (paper).")
    while True:
        try: step()
        except Exception as e:
            send_telegram_message(f"Error: {e}")
        time.sleep(POLL_SEC)
