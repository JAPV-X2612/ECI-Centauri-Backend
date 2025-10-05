"""
Pydantic schemas for user data validation.

This module defines request/response models for user-related endpoints,
ensuring data validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """
    Base user schema with common attributes.

    Attributes:
        email: User's email address
        name: User's full name
        photo_url: Optional profile photo (URL or base64)
        role: Optional user role
    """
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    photo_url: Optional[str] = None
    role: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """
    Schema for user creation request.

    Attributes:
        password: Plain text password (will be hashed)
    """
    password: str = Field(..., min_length=8, max_length=100)

    @validator('photo_url')
    def validate_photo(cls, v):
        """Validate photo URL or base64 string."""
        if v is not None and len(v) > 0:
            if not (v.startswith('http://') or v.startswith('https://') or v.startswith('data:image/')):
                raise ValueError('photo_url must be a valid URL or base64 encoded image')
        return v


class UserUpdate(BaseModel):
    """
    Schema for user update request.

    All fields are optional to allow partial updates.

    Attributes:
        name: Optional updated name
        email: Optional updated email
        password: Optional updated password
        photo_url: Optional updated photo
        role: Optional updated role
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    photo_url: Optional[str] = None
    role: Optional[str] = Field(None, max_length=50)

    @validator('photo_url')
    def validate_photo(cls, v):
        """Validate photo URL or base64 string."""
        if v is not None and len(v) > 0:
            if not (v.startswith('http://') or v.startswith('https://') or v.startswith('data:image/')):
                raise ValueError('photo_url must be a valid URL or base64 encoded image')
        return v


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


class PasswordChange(BaseModel):
    """
    Schema for password change request (authenticated user).

    Attributes:
        current_password: User's current password for verification
        new_password: New password to set
    """
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=100)


class PasswordResetRequest(BaseModel):
    """
    Schema for password reset request (generates verification code).

    Attributes:
        email: User's email address
    """
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """
    Schema for password reset confirmation with code.

    Attributes:
        email: User's email address
        verification_code: 6-digit code sent to email
        new_password: New password to set
    """
    email: EmailStr
    verification_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=100)


class MessageResponse(BaseModel):
    """
    Schema for simple message responses.

    Attributes:
        message: Response message
    """
    message: str


class PasswordResetSimple(BaseModel):
    """
    Schema for simplified password reset (no verification code).

    Attributes:
        email: User's email address
        new_password: New password to set
    """
    email: EmailStr
    new_password: str = Field(..., min_length=8, max_length=100)
