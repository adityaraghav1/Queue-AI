import smtplib
from unittest.mock import MagicMock, patch

from app.services.email_service import send_email


@patch("app.services.email_service.settings")
def test_email_disabled(mock_settings):
    mock_settings.email_enabled = False

    result = send_email(
        recipient="customer@example.com",
        subject="Test Email",
        body="This is a test."
    )

    assert result is False


@patch("app.services.email_service.settings")
@patch("app.services.email_service.smtplib.SMTP")
def test_email_sent_successfully(mock_smtp, mock_settings):
    mock_settings.email_enabled = True
    mock_settings.email_host = "smtp.example.com"
    mock_settings.email_port = 587
    mock_settings.email_from = "support@example.com"
    mock_settings.email_use_tls = True
    mock_settings.email_username = ""
    mock_settings.email_password = ""

    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    result = send_email(
        recipient="customer@example.com",
        subject="Ticket Resolved",
        body="Your ticket has been resolved."
    )

    assert result is True

    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        587,
        timeout=10
    )

    mock_server.starttls.assert_called_once()
    mock_server.send_message.assert_called_once()


@patch("app.services.email_service.settings")
@patch("app.services.email_service.smtplib.SMTP")
def test_email_failure(mock_smtp, mock_settings):
    mock_settings.email_enabled = True
    mock_settings.email_host = "smtp.example.com"
    mock_settings.email_port = 587
    mock_settings.email_from = "support@example.com"
    mock_settings.email_use_tls = True
    mock_settings.email_username = ""
    mock_settings.email_password = ""

    mock_smtp.side_effect = smtplib.SMTPException(
        "Simulated SMTP failure"
    )

    result = send_email(
        recipient="customer@example.com",
        subject="Ticket Resolved",
        body="Your ticket has been resolved."
    )

    assert result is False