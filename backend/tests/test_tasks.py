import pytest
from fastapi.testclient import TestClient
from backend.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User
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


#Invalid data handling tests
def test_create_task_with_missing_fields(token):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"description": "Test Description"}  # Missing title
    )
    assert response.status_code == 422  # Expecting validation error

def test_create_task_with_invalid_due_date(token):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test Task", "description": "Test Description", "due_date": "invalid-date"}
    )
    assert response.status_code == 422  # Expecting validation error

def test_create_task_with_long_title(token):
    long_title = "A" * 1000  # Assuming 1000 is longer than the allowed title length
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": long_title, "description": "Test Description"}
    )
    assert response.status_code == 422  # Expecting validation error if length is constrained


def test_create_task_invalid_token():
    # Generate a fake token
    fake_token = "Bearer faketoken123"
    
    response = client.post(
        "/tasks/",
        headers={"Authorization": fake_token},
        json={"title": "Task with Invalid Token", "description": "This should fail"}
    )
    
    assert response.status_code == 401  # Unauthorized
    assert response.json() == {"detail": "Could not validate credentials"}

def test_create_task_expired_token():
    # Assume expired_token is generated to simulate an expired token
    expired_token = "fake.expired.token"
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {expired_token}"},
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_create_task_no_token_provided():
    response = client.post(
        "/tasks/",
        # No Authorization header provided
        json={"title": "Task with No Token", "description": "This should fail too"}
    )
    
    assert response.status_code == 401  # Unauthorized
    assert response.json() == {"detail": "Not authenticated"}


#Boundary tests
def test_pagination_limits(token):
    # Test with negative skip value
    response = client.get(
        "/tasks/?skip=-1&limit=10",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Expecting a validation error

    # Test with a limit of 0
    response = client.get(
        "/tasks/?skip=0&limit=0",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Expecting a validation error

    # Test with an excessively high limit value
    response = client.get(
        "/tasks/?skip=0&limit=10000",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10000  # Ensure it returns within a reasonable limit

# Concurrency tests
import threading

def create_task(token, task_num):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": f"Concurrent Task {task_num}", "description": "Test Description", "status": "pending", "due_date": "2024-08-21"}
    )
    assert response.status_code == 200
    return response.json()["id"]  # Return the task ID for deletion

def delete_task(token, task_id):
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def clear_all_tasks(token):
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    tasks = response.json()
    
    # Delete all existing tasks
    for task in tasks:
        delete_task(token, task["id"])

def test_concurrent_task_creation_and_deletion(token):
    # Clear existing tasks to ensure a clean slate
    clear_all_tasks(token)

    # Create tasks concurrently
    threads = []
    task_ids = []

    for i in range(10):  # Simulate 10 concurrent task creations
        thread = threading.Thread(target=lambda: task_ids.append(create_task(token, i+1)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Verify all tasks were created
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 10  # Ensure at least 10 tasks were created

    # Now, delete tasks concurrently
    threads = []
    for task_id in task_ids:
        thread = threading.Thread(target=delete_task, args=(token, task_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Verify tasks were deleted
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # All tasks should be deleted