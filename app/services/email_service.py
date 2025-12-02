# app/services/email_service.py

# ... existing imports ...
from datetime import datetime
from email.message import EmailMessage
import smtplib
from app.core.config import get_settings

settings = get_settings()

class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, body: str):
        # NOTE: This implementation is SYNCHRONOUS and will block the API thread. 
        # For production, this logic should be wrapped in an async function (aiosmtplib)
        # OR better, offloaded to a Celery/Redis Queue worker.
        try:
            msg = EmailMessage()
            # ... existing email setup ...
            msg["From"] = settings.EMAILS_FROM_EMAIL # Use the new config key
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.set_content(body, subtype='html') # Change to html for better formatting

            # Use SMTP credentials from the updated config
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            print(f"Email sent successfully to {to_email}")

        except Exception as e:
            # We raise the exception so the caller (AuthService) can handle it,
            # or the background task can retry it.
            print(f"Email send failed to {to_email}: {str(e)}")
            raise

    @staticmethod
    def send_otp_email(email: str, otp: str, expiry_minutes: int): # Added expiry time
        subject = "StockPulse: Email Verification Code"
        body = f"""
        <html>
            <body>
                <h1>Your Verification Code is: <b>{otp}</b></h1>
                <p>This code is valid for **{expiry_minutes} minutes**.</p>
                <p>Do not share this code with anyone.</p>
            </body>
        </html>
        """
        EmailService.send_email(email, subject, body)

    @staticmethod
    def send_welcome_email(email: str, username: str): # Added username
        subject = "Welcome to StockPulse 🎉"
        body = f"""
        <html>
            <body>
                <h1>Hello {username},</h1>
                <p>Your account is successfully verified. Welcome to StockPulse!</p>
                <p>Happy trading 🚀</p>
            </body>
        </html>
        """
        EmailService.send_email(email, subject, body)