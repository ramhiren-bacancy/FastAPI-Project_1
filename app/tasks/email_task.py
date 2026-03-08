from app.core.celery_app import celery_app
from email_service import send_welcome_email
import time


@celery_app.task(name="send_welcome_back_email")
def send_welcome_back_email(email: str, username: str):
    time.sleep(10)
    send_welcome_email(email, username)
    # return "Email sent"