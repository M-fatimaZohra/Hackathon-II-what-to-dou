#!/usr/bin/env python3
"""
Database initialization script for the Todo API.
This script creates all required database tables.
"""

from sqlmodel import SQLModel
from db import engine

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()