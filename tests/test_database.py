from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.models import Ticket, User, UserRole


TEST_DATABASE_URL = "sqlite:///./test_queueai.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def test_create_user_and_ticket():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        user = User(
            name="Aditya",
            email="aditya@example.com",
            password_hash="fake_hashed_password",
            role=UserRole.CUSTOMER
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        ticket = Ticket(
            customer_id=user.id,
            subject="Payment issue",
            description="My payment was deducted twice from my account."
        )

        db.add(ticket)
        db.commit()
        db.refresh(ticket)

        assert user.id is not None
        assert ticket.id is not None
        assert ticket.customer_id == user.id
        assert ticket.status.value == "open"

    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)