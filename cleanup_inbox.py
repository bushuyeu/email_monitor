import os  # Access environment variables to fetch credentials
import imaplib  # Interact with IMAP server for mailbox operations
import logging  # Use logging for tracking operations and errors
from datetime import datetime, timedelta  # Handle time-based retention logic

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Create logger specific to this script

# Constants
IMAP_SERVER = "mail.mxlogin.com"  # MXroute IMAP server address
RETENTION_DAYS = 7  # Days after which emails should be deleted

def cleanup_old_emails() -> None:
    """Delete 'Email Monitor Test' emails older than RETENTION_DAYS from the monitor@bushuyeu.com inbox."""
    try:
        # Connect securely to the IMAP server
        with imaplib.IMAP4_SSL(IMAP_SERVER) as imap:
            # Log into the monitor email account
            imap.login(os.environ["MONITOR_EMAIL"], os.environ["MONITOR_PASSWORD"])

            # Select the inbox
            imap.select("INBOX")

            # Calculate the date before which emails should be deleted
            cutoff_date = (datetime.utcnow() - timedelta(days=RETENTION_DAYS)).strftime("%d-%b-%Y")

            # Search for emails with the specific subject older than the cutoff date
            status, data = imap.search(None, f'(BEFORE "{cutoff_date}" SUBJECT "Email Monitor Test")')

            # Get list of email IDs from the search results
            email_ids = data[0].split()

            # If no old emails found, log and exit
            if not email_ids:
                logger.info("🧼 No old test emails to clean up.")
                return

            # Mark the matching emails for deletion
            for email_id in email_ids:
                imap.store(email_id, '+FLAGS', '\Deleted')

            # Permanently delete the marked emails
            imap.expunge()

            # Log the successful cleanup
            logger.info(f"🧹 Deleted {len(email_ids)} old test email(s).")

    except Exception:
        # Log and alert on failure
        logger.exception("❌ Cleanup process failed.")
        from alert_bot import alert  # Import inside function to avoid circular import
        alert("❌ Cleanup failed: Could not remove old test emails from monitor@bushuyeu.com")

# Entry point to run cleanup if script is executed directly
if __name__ == "__main__":
    cleanup_old_emails()
