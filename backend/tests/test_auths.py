import pytest
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.auth import create_access_token, get_current_user, verify_password, get_password_hash
from backend.models import User
from backend.database import Base
from backend.dependencies import get_db
from fastapi.testclient import TestClient
from backend.main import app
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))

@pytest.fixture(scope="module")
def db():
    # Setup in-memory SQLite database for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=test_engine)

def test_create_access_token():
    data = {"sub": "testuser@example.com"}
    token = create_access_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    assert token is not None
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "testuser@example.com"
    
    expire = payload.get("exp")
    assert expire is not None
    assert expire > datetime.utcnow().timestamp()

def test_verify_password():
    hashed_password = get_password_hash("testpassword")
    assert verify_password("testpassword", hashed_password)

def test_get_current_user(db: Session):
    test_user = User(email="testuser@example.com", hashed_password=get_password_hash("testpassword"))
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    data = {"sub": test_user.email}
    token = create_access_token(data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    
    user = get_current_user(token=token, db=db)
    assert user.email == test_user.email

def test_invalid_token(db: Session):
    invalid_token = "invalidtoken"
    
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=invalid_token, db=db)
        
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"
