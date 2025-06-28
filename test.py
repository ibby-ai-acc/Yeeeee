"""
test.py  –  End-to-end diagnostic for the Halal Trading Bot
-----------------------------------------------------------
 • Strategy sanity  • Alpaca connectivity  • Telegram ping
 • Trade-log write  • Trailing-stop trigger
"""

from strategy        import find_best_signal, signal_for
from alpaca_client   import get_account
from telegram_alerts import send_telegram_message
from trade_logger    import log_trade
from position_manager import PositionManager


def test_strategy():
    sig, sym, price = find_best_signal()
    print(f"[STRATEGY] best_signal -> {sig} {sym} @ {price}")
    # also test one explicit ticker
    s2, _, p2 = signal_for("AAPL")
    print(f"[STRATEGY] AAPL signal  -> {s2} @ {p2}")


def test_alpaca():
    acct = get_account()
    print(f"[ALPACA] account status: {acct.get('status')}, "
          f"cash: ${acct.get('cash')}")


def test_telegram():
    print("[TELEGRAM] sending test message…")
    send_telegram_message("✅ Telegram integration OK (Bot self-test)")


def test_logger():
    print("[LOGGER] writing dummy trade line…")
    log_trade("TEST", "DUMMY", 1, 123.45)


def test_trailing_stop():
    pm = PositionManager(trail_pct=1.5)
    pm.open(100.0)
    prices = [100.8, 101.5, 102.0, 101.0, 100.2, 99.0]
    for p in prices:
        exit_now = pm.check(p)
        print(f"[TRAIL] price {p:.2f}  exit? {exit_now}")
        if exit_now:
            break


if __name__ == "__main__":
    print("── Running bot diagnostics ──")
    test_strategy()
    test_alpaca()
    test_telegram()
    test_logger()
    test_trailing_stop()
    print("── All tests executed ──")
