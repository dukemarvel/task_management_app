from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

load_dotenv()

# Load the database URL from environment variables
database_url = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(database_url)

# Check if the database exists, and create it if it doesn't
if not database_exists(engine.url):
    create_database(engine.url)
    print(f"Database '{engine.url.database}' created.")

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative class definitions
Base = declarative_base()
