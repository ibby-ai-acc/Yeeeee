import os, requests
from dotenv import load_dotenv
load_dotenv()

BOT  = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(msg):
    if not BOT or not CHAT: return
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    requests.post(url, json={"chat_id": CHAT, "text": msg})
