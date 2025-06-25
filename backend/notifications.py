import smtplib
from email.mime.text import MIMEText
from flask import current_app

def send_email(to_email, subject, body):
    if not to_email:
        return

    if current_app.config.get("ENV") == "development":
        print(f"📨 [DEV MODE] Would send to {to_email}:\nSubject: {subject}\n\n{body}")
        return

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = current_app.config["EMAIL_FROM"]
        msg["To"] = to_email

        with smtplib.SMTP(current_app.config["SMTP_SERVER"], current_app.config["SMTP_PORT"]) as server:
            server.starttls()
            server.login(current_app.config["SMTP_USERNAME"], current_app.config["SMTP_PASSWORD"])
            server.send_message(msg)

        print(f"📧 Email sent to {to_email}")

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")