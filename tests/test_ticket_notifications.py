from unittest.mock import patch

from app.database.models import Ticket


def create_test_ticket(client, customer_token):
    response = client.post(
        "/tickets",
        headers={
            "Authorization": f"Bearer {customer_token}"
        },
        json={
            "subject": "Test notification ticket",
            "description": "Testing ticket resolution email."
        }
    )

    assert response.status_code == 201, response.text
    return response.json()


@patch("app.routes.tickets.send_email")
def test_ticket_resolution_sends_email(
    mock_send_email,
    client,
    customer_token,
    admin_token,
    db_session
):
    mock_send_email.return_value = True

    ticket_data = create_test_ticket(client, customer_token)
    ticket_id = ticket_data["id"]

    response = client.patch(
        f"/tickets/{ticket_id}/response",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "final_response": "Your issue has been resolved."
        }
    )

    assert response.status_code == 200, response.text

    mock_send_email.assert_called_once()

    email_arguments = mock_send_email.call_args.kwargs

    assert email_arguments["recipient"] == "testcustomer@example.com"
    assert "resolved" in email_arguments["subject"].lower()
    assert "Your issue has been resolved." in email_arguments["body"]


@patch("app.routes.tickets.send_email")
def test_ticket_resolution_succeeds_when_email_fails(
    mock_send_email,
    client,
    customer_token,
    admin_token
):
    mock_send_email.return_value = False

    ticket_data = create_test_ticket(client, customer_token)
    ticket_id = ticket_data["id"]

    response = client.patch(
        f"/tickets/{ticket_id}/response",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "final_response": "Your issue has been resolved."
        }
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "resolved"
    mock_send_email.assert_called_once()
