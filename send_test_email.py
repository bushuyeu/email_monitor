import os  # Access environment variables
import smtplib  # SMTP client to send email
from email.message import EmailMessage  # Used to create the email message
import logging  # Logging for observability

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Logger for this module

SMTP_SERVER = "mail.mxlogin.com"  # MXroute SMTP hostname
SMTP_PORT = 587  # Port used for TLS

def send_test_email() -> None:
    """Send a test email from p@bushuyeu.com to monitor@bushuyeu.com using MXroute SMTP."""

    msg = EmailMessage()  # Create a new email message object
    msg["Subject"] = "Email Monitor Test"  # Subject line for the test email
    msg["From"] = "p@bushuyeu.com"  # Fixed sender address
    msg["To"] = "monitor@bushuyeu.com"  # Fixed recipient address
    msg.set_content("✅ MXroute monitoring script test email.")  # Email body

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  # Connect to the SMTP server
            server.starttls()  # Start TLS encryption
            server.login(os.environ["MXROUTE_EMAIL"], os.environ["MXROUTE_PASSWORD"])  # Login with env credentials
            server.send_message(msg)  # Send the constructed message
            logger.info("✅ Test email sent from p@bushuyeu.com to monitor@bushuyeu.com")  # Log success
    except Exception:
        logger.exception("❌ Failed to send test email")  # Log the exception
        from alert_bot import alert  # Import alert function
        alert("❌ Failed to send test email from MXroute")  # Notify via Telegram

if __name__ == "__main__":
    send_test_email()  # Run the function if script is executed directly
