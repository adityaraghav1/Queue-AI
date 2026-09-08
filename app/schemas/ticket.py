from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.database.models import (
    TicketCategory,
    TicketPriority,
    TicketSentiment,
    TicketStatus,
)


class TicketCreate(BaseModel):
    subject: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)


class TicketResponse(BaseModel):
    id: int
    customer_id: int
    subject: str
    description: str

    category: TicketCategory | None
    priority: TicketPriority | None
    sentiment: TicketSentiment | None

    suggested_response: str | None
    final_response: str | None

    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)