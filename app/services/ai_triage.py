import json

from groq import Groq

from app.core.config import settings
from app.database.models import TicketCategory, TicketPriority, TicketSentiment


client = Groq(api_key=settings.groq_api_key)


def analyze_ticket(subject: str, description: str) -> dict:
    prompt = f"""
    You are an AI customer support ticket triage assistant.

    Analyze the ticket below.

    Subject: {subject}
    Description: {description}

    Return ONLY a valid JSON object with these four fields:
    {{
        "category": "billing, technical, account, delivery, or general",
        "priority": "low, medium, high, or urgent",
        "sentiment": "positive, neutral, or negative",
        "suggested_response": "A short, polite response to the customer"
    }}

    Do not include Markdown or any text outside the JSON object.
    """

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Classify customer support tickets and return valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    result = json.loads(completion.choices[0].message.content)

    category = TicketCategory(result["category"])
    priority = TicketPriority(result["priority"])
    sentiment = TicketSentiment(result["sentiment"])

    return {
        "category": category,
        "priority": priority,
        "sentiment": sentiment,
        "suggested_response": result["suggested_response"]
    }