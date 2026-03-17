import requests
import time
import os
import smtplib

URL = "https://visacatcher.bot/appointments/london/czech%20republic"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL = os.getenv("EMAIL")
EMAIL_PASS = os.getenv("EMAIL_PASS")

last_content = ""


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
    global last_content

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    text = response.text

    if last_content == "":
        last_content = text
        return False

    if text != last_content:
        last_content = text
        return True

    return False


print("🚀 Bot started...")

while True:
    try:
        if check_available():
            print("🔥 CHANGE DETECTED → sending 4 alerts")

            for i in range(4):
                msg = f"🔥 APPOINTMENT AVAILABLE!\n\n{URL}"

                send_telegram(msg)
                send_email(msg)

                print(f"✅ ALERT {i+1}/4 SENT")

                time.sleep(10)  # gap between alerts

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
