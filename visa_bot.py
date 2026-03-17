import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://visacatcher.bot/appointments/london/netherlands"

# 🔔 Get from Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def check_available():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    return "Appointments Available!" in response.text


last_status = False

print("🚀 Bot started...")

while True:
    try:
        current = check_available()

        if not last_status and current:
            msg = "🔥 APPOINTMENT AVAILABLE!\n\n" + URL
            send_telegram(msg)
            print("✅ ALERT SENT")

        last_status = current

    except Exception as e:
        print("Error:", e)

    time.sleep(5)  # check every 5 seconds
