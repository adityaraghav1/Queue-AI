from app.services.ai_triage import analyze_ticket


subject = "Charged twice for subscription"

description = (
    "I was charged twice this month and nobody is responding "
    "to my emails. Please help me resolve this issue."
)

try:
    result = analyze_ticket(subject, description)

    print("\nAI Ticket Analysis")
    print("------------------")
    print("Category:", result["category"].value)
    print("Priority:", result["priority"].value)
    print("Sentiment:", result["sentiment"].value)
    print("Suggested Response:", result["suggested_response"])

except Exception as error:
    print("AI triage test failed:", error)