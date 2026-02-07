#!/usr/bin/env python3
"""
Database initialization script for the Todo API.
This script creates all required database tables.
"""

from sqlmodel import SQLModel
# Import the database engine and models using relative imports that work from the project root
from src.database.db import engine
# Need to import all models to register them in SQLModel metadata
from src.schema.models import Task, Conversation, Message

def create_tables():
    """Create all database tables."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Creating database tables...")

    # Verify which tables are registered in metadata
    registered_tables = list(SQLModel.metadata.tables.keys())
    logger.info(f"Registered tables in metadata: {registered_tables}")

    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()