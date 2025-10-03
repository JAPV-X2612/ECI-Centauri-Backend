"""
Authentication endpoints for user registration and login.

This module handles user authentication operations with improved
error handling and clear error messages.
"""

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings
from app.core.exceptions import (
    InvalidCredentialsException,
    EmailAlreadyExistsException
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="User successfully created"
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.

    **Request Body:**
    - **name**: Full name (required)
    - **email**: Valid email address (required, unique)
    - **password**: Password with minimum 8 characters (required)

    **Returns:**
    - User information without password

    **Errors:**
    - **409 Conflict**: Email already registered
    - **503 Service Unavailable**: Database connection error
    """
    try:
        return UserService.create_user(db, user_data)
    except EmailAlreadyExistsException:
        raise


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get access token",
    response_description="JWT access token"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and generate JWT access token.

    **Request Body (form-data):**
    - **username**: User's email address
    - **password**: User's password

    **Returns:**
    - JWT access token valid for 30 minutes
    - Token type (bearer)

    **Errors:**
    - **401 Unauthorized**: Invalid email or password
    - **503 Service Unavailable**: Database connection error

    **Usage:**
    Include the token in subsequent requests:
    Authorization: Bearer <access_token>
    """
    # Authenticate user (username field contains email)
    user = UserService.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise InvalidCredentialsException()

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
