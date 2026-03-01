# services/email_service.py
import smtplib
from email.message import EmailMessage
from emailConfig import EMAIL_ADDRESS, EMAIL_PASSWORD


def send_welcome_email(email: str, username: str):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be configured")
    msg = EmailMessage()
    msg["Subject"] = "Welcome to Our Platform 🎉"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    msg.set_content(
        f"""
        Hi {username},

        Welcome to our platform!
        Your account has been created successfully.

        Regards,
        FastAPI Team
        """
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(str(EMAIL_ADDRESS), str(EMAIL_PASSWORD))
        smtp.send_message(msg)

def send_otp_email(email: str, otp: str):
    from email.message import EmailMessage
    import smtplib
    from emailConfig import EMAIL_ADDRESS, EMAIL_PASSWORD

    msg = EmailMessage()
    msg["Subject"] = "Your OTP Code 🔐"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = email

    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)