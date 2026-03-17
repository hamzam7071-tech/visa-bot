import requests
import time
import os
import smtplib

URL = "https://visacatcher.bot/appointments/london/czech%20republic"

# 🔔 ENV VARIABLES (Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")

last_content = ""
alert_count = 0


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
    global last_content

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    text = response.text

    # First run → store baseline
    if last_content == "":
        last_content = text
        print("Initialized baseline")
        return False

    # Detect change
    if text != last_content:
        last_content = text
        print("Change detected!")
        return True

    return False


print("🚀 Bot started...")

while True:
    try:
        current = check_available()

        if current:
            if alert_count < 4:
                msg = f"🔥 APPOINTMENT CHANGE DETECTED!\n\nCheck now:\n{URL}"

                send_telegram(msg)
                send_email(msg)

                alert_count += 1
                print(f"✅ ALERT SENT ({alert_count}/4)")

                time.sleep(10)  # spacing alerts
                continue

        else:
            # reset when no change
            alert_count = 0

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
