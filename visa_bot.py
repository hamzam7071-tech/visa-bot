import smtplib

EMAIL = "hamzam7072@gmail.com"
EMAIL_PASS = "qliymwchabehihxu"

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, EMAIL_PASS)

    message = "Subject: Test Email\n\nEmail is working!"
    server.sendmail(EMAIL, EMAIL, message)

    server.quit()

    print("✅ Email sent successfully")

except Exception as e:
    print("❌ Error:", e)
