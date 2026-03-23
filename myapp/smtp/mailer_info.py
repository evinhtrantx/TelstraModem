"""SMTP constants container."""

import os
import smtplib
import ssl
from email.message import EmailMessage


class mailerInfo:
    """Container for SMTP configuration constants."""
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SENDER_NAME: str = ""
    SENDER_EMAIL: str = ""

    def get_email_password(self) -> str:
        """Private: retrieve the email password from the environment.

        Reads `MODEM_EMAIL_PWD` and returns it as text. Returns empty
        string when the variable is not set.
        """
        return os.environ.get("MODEM_EMAIL_PWD", "")


    def send_email(self, to_address: str, subject: str, message: str) -> None:
        """Send a plain-text email via SMTP over SSL.

        - Connects to `SMTP_HOST` (falls back to Gmail) on port 465 using
          SSL and logs in with `SMTP_USER` and the password returned by
          `get_emai_password()`.
        - Sends a simple plain-text email with the provided subject and
          message body to `to_address`.
        """
        host = self.SMTP_HOST or "smtp.gmail.com"
        port = 465

        username = self.SMTP_USER
        password = self.get_emai_password()

        if not username or not password:
            raise ValueError("SMTP_USER and MODEM_EMAIL_PWD must be set")

        sender = self.SENDER_EMAIL or username

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = to_address
        msg.set_content(message)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.send_message(msg)
