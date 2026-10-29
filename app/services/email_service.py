import logging
import smtplib
from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger(__name__)


def send_email(
    recipient: str,
    subject: str,
    body: str
) -> bool:
    """
    Send an email using the configured SMTP server.

    Returns True if the email is sent successfully,
    or False if sending is disabled or fails.
    """

    if not settings.email_enabled:
        logger.info("Email sending is disabled.")
        return False

    if not settings.email_host or not settings.email_from:
        logger.error("Email configuration is incomplete.")
        return False

    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(
            settings.email_host,
            settings.email_port,
            timeout=10
        ) as server:

            if settings.email_use_tls:
                server.starttls()

            if settings.email_username and settings.email_password:
                server.login(
                    settings.email_username,
                    settings.email_password
                )

            server.send_message(message)

        logger.info("Email sent successfully.")
        return True

    except (OSError, smtplib.SMTPException):
        logger.exception("Failed to send email.")
        return False