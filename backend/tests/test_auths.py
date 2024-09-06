import pytest
from datetime import timedelta, datetime
from jose import jwt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.auth import create_access_token, get_current_user, verify_password, get_password_hash, pwd_context
from backend.models import User
from backend.database import Base
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

@pytest.fixture(scope="module")
def db():
    
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

# Test password hash
def test_verify_password():
    hashed_password = get_password_hash("testpassword")
    assert verify_password("testpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

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


# Test deprecated password scheme
def test_deprecated_password_scheme():
    # This checks if 'auto' in schemes works for deprecated passwords
    old_hash = pwd_context.hash("oldpassword")
    assert verify_password("oldpassword", old_hash)


# Test edge cases
def test_edge_cases():
    # Test with no password
    with pytest.raises(ValueError):
        get_password_hash("")
    
    # Test token without 'sub'
    token = create_access_token({})
    with pytest.raises(HTTPException):
        get_current_user(token=token, db=db)