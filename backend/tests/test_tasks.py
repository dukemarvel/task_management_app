import pytest
from fastapi.testclient import TestClient
from backend.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Task
from backend.auth import get_password_hash, create_access_token
from backend.dependencies import get_db
import os


# Load environment variables
from dotenv import load_dotenv
load_dotenv()


# Setup the TestClient
client = TestClient(app)

# Setup the test database
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

test_engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def get_test_token():
    db = TestingSessionLocal()
    try:
        test_user = db.query(User).filter(User.email == "testuser1@example.com").first()
        
        if not test_user:
            test_user = User(
                email="testuser1@example.com",
                hashed_password=get_password_hash("testpassword"),
                full_name="Test User"
            )
            db.add(test_user)
            db.commit()
            db.refresh(test_user)

        token = create_access_token(data={"sub": test_user.email})
        
        return token
    
    except Exception as e:
        db.rollback()
        
        raise e
    
    finally:
        db.close()

@pytest.fixture
def token():
    return get_test_token()

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup code before tests
    Base.metadata.create_all(bind=test_engine)  # Create the tables before tests
    
    yield
    # Teardown code after tests
    Base.metadata.drop_all(bind=test_engine)  # Drop all the tables after tests
    

def test_create_task(token):
    print(f"Token-printed: {token}")
    
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "Test Description", "status": "pending", "due_date": "2024-08-21"}
    )
    
    print(f"Response content: {response.json()}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    
def test_read_tasks(token):
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)

def test_read_task(token):
    # First, create a task to be read
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "Test Description", "status": "pending", "due_date": "2024-08-21"}
    )
    task_id = response.json()["id"]
    

    # Now read the task
    response = client.get(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"

def test_update_task(token):
    # First, create a task to be updated
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "Test Description", "status": "pending", "due_date": "2024-08-21"}
    )
    task_id = response.json()["id"]
    

    # Now update the task
    response = client.put(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated Task", "description": "Updated Description", "status": "completed", "due_date": "2024-08-22"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["status"] == "completed"

def test_delete_task(token):
    # First, create a task to be deleted
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "Test Description", "status": "pending", "due_date": "2024-08-21"}
    )
    task_id = response.json()["id"]
    
    # Now delete the task
    response = client.delete(f"/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
