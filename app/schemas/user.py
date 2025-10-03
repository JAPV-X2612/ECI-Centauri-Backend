"""
Pydantic schemas for user data validation.

This module defines request/response models for user-related endpoints,
ensuring data validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base user schema with common attributes.

    Attributes:
        email: User's email address
        name: User's full name
    """
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """
    Schema for user creation request.

    Attributes:
        password: Plain text password (will be hashed)
    """
    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """
    Schema for user update request.

    All fields are optional to allow partial updates.

    Attributes:
        name: Optional updated name
        email: Optional updated email
        password: Optional updated password
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """
    Schema for user response (excludes password).

    Attributes:
        id: User's unique identifier
        created_at: Timestamp of user creation
        updated_at: Timestamp of last update
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Attributes:
        email: User's email address
        password: User's plain text password
    """
    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Schema for JWT token response.

    Attributes:
        access_token: JWT access token
        token_type: Type of token (always "bearer")
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for decoded token data.

    Attributes:
        email: User's email extracted from token
    """
    email: Optional[str] = None
