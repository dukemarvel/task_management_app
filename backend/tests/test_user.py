from fastapi.testclient import TestClient
from backend.main import app
from backend.dependencies import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base
import pytest
import os
from dotenv import load_dotenv

load_dotenv()


database_url = os.getenv("DATABASE_URL")


engine = create_engine(database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup code before tests
    Base.metadata.create_all(bind=engine)  # Create the tables before tests
    yield
    # Teardown code after tests
    Base.metadata.drop_all(bind=engine)  # Drop all the tables after tests

def test_register_user():
    response = client.post("api/v1/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "hashed_password" not in response.json()  # Don't expose hashed password

def test_login_for_access_token():
    # First, register a user
    client.post("api/v1/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    response = client.post("api/v1/login", data={
        "username": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_with_incorrect_password():
    # Register the user first
    client.post("api/v1/register", json={
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    })

    response = client.post("api/v1/login", data={
        "username": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
