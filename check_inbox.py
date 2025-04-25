import os  # To load credentials from environment
import imaplib  # For IMAP email access
import email  # To parse email messages
import logging  # To record logs
from datetime import datetime, timedelta  # For checking time window
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Logger for this module

IMAP_SERVER = "mail.mxlogin.com"  # MXroute IMAP server

def check_inbox() -> None:
    """Check monitor@bushuyeu.com inbox for a recent test email."""

    try:
        with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:  # Connect securely to IMAP server
            imap.login(os.environ["MONITOR_EMAIL"], os.environ["MONITOR_PASSWORD"])  # Login to mailbox
            imap.select("INBOX")  # Select inbox folder

            # Create IMAP search criteria: recent email with specific subject
            since = (datetime.utcnow() - timedelta(hours=1)).strftime("%d-%b-%Y")  # Search within the past hour
            result, data = imap.search(None, f'(SINCE "{since}" SUBJECT "Email Monitor Test")')  # Perform search

            if data[0]:  # If messages are found
                logger.info("📬 Test email found in monitor inbox.")  # Log success
            else:
                raise Exception("🚫 No recent test email found.")  # Raise error if not found

    except Exception:
        logger.exception("❌ Failed inbox check")  # Log the failure
        from alert_bot import alert  # Import alert function
        alert("❌ Email not received in monitor@bushuyeu.com")  # Notify via Telegram

if __name__ == "__main__":
    check_inbox()  # Run function if executed directly
