from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage


def send_alert(msg: str) -> None:
    """Send an alert via stdout or email.

    If the ``ALERT_EMAIL`` environment variable is set, an email is attempted
    via localhost SMTP. Otherwise the message is printed to stdout.
    """
    email = os.getenv("ALERT_EMAIL")
    if email:  # pragma: no cover - requires SMTP
        message = EmailMessage()
        message.set_content(msg)
        message["Subject"] = "COCE alert"
        message["From"] = email
        message["To"] = email
        try:
            with smtplib.SMTP("localhost") as smtp:  # pragma: no cover - local smtp
                smtp.send_message(message)  # pragma: no cover - local smtp
        except Exception as exc:  # pragma: no cover - depends on local smtp
            print(f"ALERT FAILED: {exc} | {msg}")
    else:
        print(f"ALERT: {msg}")
