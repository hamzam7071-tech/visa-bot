import requests
import time
import os
import smtplib

URL = "https://visacatcher.bot/appointments/london/czech%20republic"

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
    return "Appointments Available!" in response.text


last_status = False

print("🚀 Bot started...")

while True:
    try:
        current = check_available()

        if not last_status and current:
            msg = f"🔥 APPOINTMENT AVAILABLE!\n\nBook now:\n{URL}"

            send_telegram(msg)
            send_email(msg)

            print("✅ ALERT SENT")

        last_status = current

    except Exception as e:
        print("Error:", e)

    time.sleep(5)  # check every 5 seconds
