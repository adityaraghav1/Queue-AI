from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketSentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class TicketCategory(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    DELIVERY = "delivery"
    GENERAL = "general"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.CUSTOMER,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    tickets: Mapped[list["Ticket"]] = relationship(
        "Ticket",
        back_populates="customer"
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    subject: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    category: Mapped[TicketCategory | None] = mapped_column(
        SqlEnum(TicketCategory),
        nullable=True
    )

    priority: Mapped[TicketPriority | None] = mapped_column(
        SqlEnum(TicketPriority),
        nullable=True
    )

    sentiment: Mapped[TicketSentiment | None] = mapped_column(
        SqlEnum(TicketSentiment),
        nullable=True
    )

    suggested_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    final_response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[TicketStatus] = mapped_column(
        SqlEnum(TicketStatus),
        default=TicketStatus.OPEN,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    customer: Mapped["User"] = relationship(
        "User",
        back_populates="tickets"
    )