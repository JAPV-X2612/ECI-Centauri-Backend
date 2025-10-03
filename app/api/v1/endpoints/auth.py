"""
Authentication endpoints for user registration and login.

This module handles user authentication operations including
registration, login, and token generation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.user_service import UserService
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user_data: User registration data (name, email, password)
        db: Database session

    Returns:
        UserResponse: Created user information (without password)

    Raises:
        HTTPException: 409 if email already exists
    """
    return UserService.create_user(db, user_data)


@router.post("/login", response_model=Token)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    Authenticate user and generate JWT access token.

    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session

    Returns:
        Token: JWT access token and token type

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Authenticate user (username field contains email)
    user = UserService.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
