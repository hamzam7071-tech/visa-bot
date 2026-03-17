import requests
from bs4 import BeautifulSoup
import time
import os

# =========================
# CONFIG
# =========================

URL = "https://visacatcher.bot/appointments/london/czech%20republic"

CHECK_INTERVAL = 5  # seconds (safe for Railway)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

# =========================
# FUNCTIONS
# =========================

def check_appointments():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        if "Appointments Available!" in soup.text:
            print("✅ AVAILABLE")
            return True
        else:
            print("❌ Not available")
            return False

    except Exception as e:
        print("Error:", e)
        return False


def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })
        print("📨 Telegram sent")
    except Exception as e:
        print("Telegram error:", e)


def send_pushover(msg):
    try:
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER,
            "message": msg,
            "priority": 2,
            "retry": 30,
            "expire": 3600
        })
        print("📱 Pushover sent")
    except Exception as e:
        print("Pushover error:", e)


def send_multiple_alerts(msg):
    for i in range(4):  # 🔥 send 4 times
        print(f"🔔 Alert {i+1}/4")

        send_telegram(msg)
        send_pushover(msg)

        time.sleep(2)  # gap between alerts


# =========================
# MAIN LOOP
# =========================

print("🚀 Bot started...")

while True:
    available = check_appointments()

    if available:
        message = f"🔥 APPOINTMENT AVAILABLE!\n\n{URL}"

        send_multiple_alerts(message)

        # wait longer after detection to avoid spam loop
        time.sleep(30)

    time.sleep(CHECK_INTERVAL)
