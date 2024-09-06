import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import User, Task
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup the test database
SQLALCHEMY_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Setup: Create the tables before tests
    Base.metadata.create_all(bind=test_engine)
    yield
    # Teardown: Drop all the tables after tests
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db():
    # Setup a session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_user(db):
    # Test the creation of a User
    new_user = User(
        email="testuser@example.com",
        hashed_password="hashedpassword",
        full_name="Test User"
    )
    db.add(new_user)
    db.commit()

    user_in_db = db.query(User).filter(User.email == "testuser@example.com").first()
    assert user_in_db is not None
    assert user_in_db.email == "testuser@example.com"
    assert user_in_db.full_name == "Test User"

def test_create_task(db):
    # Test the creation of a Task
    new_user = User(
        email="taskuser@example.com",
        hashed_password="hashedpassword",
        full_name="Task User"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_task = Task(
        title="Test Task",
        description="Test Description",
        owner_id=new_user.id,
        status="pending",
        due_date="2024-08-21"
    )
    db.add(new_task)
    db.commit()

    task_in_db = db.query(Task).filter(Task.title == "Test Task").first()
    assert task_in_db is not None
    assert task_in_db.title == "Test Task"
    assert task_in_db.owner_id == new_user.id

def test_relationship_between_user_and_task(db):
    # Test the relationship between User and Task
    user = db.query(User).filter(User.email == "taskuser@example.com").first()
    task = db.query(Task).filter(Task.title == "Test Task").first()

    assert task in user.tasks
    assert task.owner == user

def test_delete_user_and_cascade_tasks(db):
    # Test the deletion of a User and cascading delete of associated tasks
    user = db.query(User).filter(User.email == "taskuser@example.com").first()
    db.delete(user)
    db.commit()

    task_in_db = db.query(Task).filter(Task.owner_id == user.id).first()
    assert task_in_db is None
