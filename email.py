import smtplib
from email.mime.text import MIMEText

EMAIL_FROM = "abhisaroj226002@gmail.com"
EMAIL_TO = "chutki144401@gmail.com"
EMAIL_PASSWORD = "tflzjtguabrhtyyp"

def send_email_alert(process_name):
    msg = MIMEText(f"⚠ Alert: {process_name} was detected and terminated!")
    msg["Subject"] = "🚨 Threat Detected!"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    except Exception as e:
        print(f"⚠ Failed to send email: {e}")
