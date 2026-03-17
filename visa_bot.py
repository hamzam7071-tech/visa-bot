def send_email(msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(EMAIL, EMAIL_PASS)

        message = f"Subject: Visa Alert\n\n{msg}"
        server.sendmail(EMAIL, EMAIL, message)

        server.quit()

        print("📧 Email sent")

    except Exception as e:
        print("❌ Email error:", e)
