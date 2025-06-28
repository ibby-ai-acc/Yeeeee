from datetime import datetime
def log_trade(action,sym,qty,price):
    with open("trade_log.csv","a") as f:
        f.write(f"{datetime.now()},{action},{sym},{qty},{price}\n")
