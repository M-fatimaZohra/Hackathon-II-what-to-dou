from sqlmodel import create_engine
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration - prioritize NEON_DATABASE_URL, fall back to DATABASE_URL, then SQLite
DATABASE_URL = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with connection pooling for PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    # PostgreSQL connection with optimized settings for production use
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set to True for debugging
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before using them
        pool_recycle=300,    # Recycle connections after 5 minutes
    )
else:
    # Fallback for SQLite
    engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    from sqlmodel import Session
    with Session(engine) as session:
        yield session