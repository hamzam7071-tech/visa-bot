import requests
import time
import os
import smtplib

URL = "https://visacatcher.bot/appointments/london/netherlands"

# 🔔 ENV VARIABLES (set in Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)


def send_email(msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, EMAIL_PASS)

        message = f"Subject: Visa Appointment Alert\n\n{msg}"
        server.sendmail(EMAIL, EMAIL, message)

        server.quit()
    except Exception as e:
        print("Email error:", e)


def check_available():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)

    text = response.text.lower()

    # 🔍 Better detection (adjust if needed)
    if "no appointments" in text:
        return False
    else:
        return True


alert_count = 0

print("🚀 Bot started...")

while True:
    try:
        current = check_available()

        if current:
            if alert_count < 4:
                msg = f"🔥 APPOINTMENT AVAILABLE!\n\nBook now:\n{URL}"

                send_telegram(msg)
                send_email(msg)

                alert_count += 1
                print(f"✅ ALERT SENT ({alert_count}/4)")

                time.sleep(10)  # wait between alerts
                continue

        else:
            # reset when not available again
            alert_count = 0

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
