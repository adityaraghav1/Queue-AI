import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db
from app.database import models
from app.database.models import User, UserRole
from app.core.security import hash_password


# Separate SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test_queueai.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture
def db_session():
    # Create fresh tables before each test
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def client(db_session):
    # Override the application's database dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Restore the original dependencies
    app.dependency_overrides.clear()


@pytest.fixture
def customer_token(client, db_session):
    # Create a test customer
    customer = User(
        name="Test Customer",
        email="testcustomer@example.com",
        password_hash=hash_password("testpassword123"),
        role=UserRole.CUSTOMER
    )

    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    # Log in to obtain a JWT token
    response = client.post(
        "/auth/login",
        json={
            "email": "testcustomer@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200, response.text

    return response.json()["access_token"]