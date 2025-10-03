"""
User database model.

This module defines the User table structure in PostgreSQL
using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model representing users table in database.

    Attributes:
        id: Primary key, auto-incremented user ID
        name: User's full name
        email: User's email address (unique)
        hashed_password: Bcrypt hashed password
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
