import requests
import time
import os
import smtplib

URL = "https://visacatcher.bot/appointments/london/netherlands"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")

COUNT_FILE = "alert_count.txt"


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

        message = f"Subject: Visa Alert\n\n{msg}"
        server.sendmail(EMAIL, EMAIL, message)

        server.quit()
    except Exception as e:
        print("Email error:", e)


def check_available():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    return "Appointments Available!" in response.text


def get_count():
    if not os.path.exists(COUNT_FILE):
        return 0
    with open(COUNT_FILE, "r") as f:
        return int(f.read())


def save_count(count):
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))


print("🚀 Bot started...")

while True:
    try:
        current = check_available()
        alert_count = get_count()

        if current:
            if alert_count < 4:
                msg = f"🔥 APPOINTMENT AVAILABLE!\n\n{URL}"

                send_telegram(msg)
                send_email(msg)

                alert_count += 1
                save_count(alert_count)

                print(f"✅ ALERT SENT ({alert_count}/4)")
        else:
            # reset when not available
            save_count(0)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
