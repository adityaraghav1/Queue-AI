from unittest.mock import patch

from app.database.models import (
    TicketCategory,
    TicketPriority,
    TicketSentiment,
)


def test_ticket_creation_with_ai(client, customer_token):
    mock_result = {
        "category": TicketCategory.BILLING,
        "priority": TicketPriority.HIGH,
        "sentiment": TicketSentiment.NEGATIVE,
        "suggested_response": "We are sorry about the duplicate charge.",
    }

    with patch(
        "app.routes.tickets.analyze_ticket",
        return_value=mock_result,
    ):
        response = client.post(
            "/tickets",
            headers={"Authorization": f"Bearer {customer_token}"},
            json={
                "subject": "Duplicate subscription charge",
                "description": "I was charged twice for my subscription.",
            },
        )

    assert response.status_code == 201

    data = response.json()
    assert data["category"] == "billing"
    assert data["priority"] == "high"
    assert data["sentiment"] == "negative"
    assert data["suggested_response"] == (
        "We are sorry about the duplicate charge."
    )


def test_ticket_creation_when_ai_fails(client, customer_token):
    with patch(
        "app.routes.tickets.analyze_ticket",
        side_effect=Exception("Simulated AI failure"),
    ):
        response = client.post(
            "/tickets",
            headers={"Authorization": f"Bearer {customer_token}"},
            json={
                "subject": "Unable to access my account",
                "description": "I cannot log into my account.",
            },
        )

    assert response.status_code == 201

    data = response.json()
    assert data["category"] is None
    assert data["priority"] is None
    assert data["sentiment"] is None
    assert data["suggested_response"] is None