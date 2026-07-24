"""
Database configuration and session management.

This module sets up the SQLAlchemy engine, session factory, and base class
for database models. It handles connection to PostgreSQL database.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create SQLAlchemy engine
# Pool kept small and connections pre-pinged/recycled since serverless platforms
# (e.g. Vercel) spin up fresh processes per invocation and can otherwise exhaust
# the database's max connection limit or hand back stale connections.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=1,
    max_overflow=2,
    pool_recycle=300,
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.

    Yields:
        Session: SQLAlchemy database session

    Note:
        Automatically closes the session after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
