from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read environment variables
DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")  # Default to localhost if not set
DB_PORT = os.getenv("MYSQL_PORT", "3306")       # Default to 3306 if not set
DB_NAME = os.getenv("MYSQL_DB")

# Construct the database URL
MYSQL_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Optional: print connection string for debugging (REMOVE IN PRODUCTION)
print(f"Connecting to DB using: {MYSQL_URL}")

# Create engine and session
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()