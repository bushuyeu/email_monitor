# 📧 Email Health Monitor Bot

This project monitors the health and availability of an email account by periodically sending test emails and checking the inbox for their arrival.

If the monitored email account is unreachable or test emails fail to be sent or received, an alert is automatically sent via a Telegram bot to a configured chat.

---

## ✨ Features

- ✅ Periodically sends test emails to verify email service health
- ✅ Checks inbox for test emails to confirm delivery
- ✅ Sends instant Telegram alerts if email sending or receiving fails
- ✅ Lightweight and easy to deploy via crontab on a VM
- ✅ Environment-variable based configuration for easy security management

---

## 🛠 Project Structure

```
email_health_monitor/
├── requirements.txt    # Required libraries
├── send_test_email.py  # Script to send test emails
├── check_inbox.py      # Script to check inbox for test emails
├── cleanup_inbox.py    # Script to clean up old test emails
├── alert_bot.py        # Script to send Telegram alerts
├── .env                # Environment variables (NEVER commit this file)
└── README.md           # Project documentation
```

---

## ⚙️ Requirements

- Python 3.10 or higher
- `requests` library
- `python-dotenv` for environment management

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 .env Configuration

Create a `.env` file in the `email_health_monitor/` folder with the following keys:

```dotenv
# MXRoute email account credentials used to send test emails
MXROUTE_EMAIL=your_mxroute_email@example.com
MXROUTE_PASSWORD=your_mxroute_password

# Email account credentials to monitor (inbox to check)
MONITOR_EMAIL=your_monitor_email@example.com
MONITOR_PASSWORD=your_monitor_email_password

# Telegram bot token used to send you alert messages
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Your Telegram user or group chat ID to receive alerts
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

> **Important:** Make sure this `.env` file is added to `.gitignore` and never committed to GitHub.

---

## 🚀 How to Run Manually

Activate your virtual environment (if using one):

```bash
source venv/bin/activate
```

Send a test email:

```bash
python send_test_email.py
```

Check inbox for test email:

```bash
python check_inbox.py
```

Cleanup old test emails:

```bash
python cleanup_inbox.py
```

✅ If the email service is healthy, you’ll see confirmation messages.

❌ If sending or receiving fails, you’ll receive a Telegram alert.

---

## 🕒 Cronjob Setup (Recommended)

To automatically monitor every 30 minutes and clean up inbox weekly:

1. Edit your crontab:

```bash
crontab -e
```

2. Add the following lines:

```bash
*/30 * * * * cd /home/ubuntu/email_health_monitor && source venv/bin/activate && python send_test_email.py && python check_inbox.py >> monitor_email.log 2>&1
0 3 * * 0 cd /home/ubuntu/email_health_monitor && source venv/bin/activate && python cleanup_inbox.py >> cleanup_email.log 2>&1
```

✅ This ensures health checks run automatically every 30 minutes and inbox cleanup runs weekly at 3 AM on Sundays. Logs are saved to `monitor_email.log` and `cleanup_email.log`.

---

## 📜 License

This project is for personal monitoring use. No warranties implied.

---

## ✨ Credits

Built by [@bushuyeu](https://github.com/bushuyeu) with ❤️ to keep email services reliable and monitored.
