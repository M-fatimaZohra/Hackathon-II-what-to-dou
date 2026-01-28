#!/usr/bin/env python3
"""
Database initialization script for the Todo API.
This script creates all required database tables.
"""

from sqlmodel import SQLModel
from db import engine

def create_tables():
    """Create all database tables."""
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()