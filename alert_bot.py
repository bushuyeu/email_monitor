import os  # For accessing environment variables
import requests  # HTTP client to send request to Telegram API

def alert(message: str) -> None:
    """Send a message to a Telegram chat using the Telegram bot API."""

    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_BOT_TOKEN']}/sendMessage"  # Telegram sendMessage endpoint
    payload = {
        "chat_id": os.environ["TELEGRAM_CHAT_ID"],  # Target chat ID
        "text": message  # Message text to send
    }
    requests.post(url, json=payload)  # Make the POST request to send the message
