"""
API dependencies for authentication and authorization.

This module provides dependency functions with improved error handling
for FastAPI endpoints.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.user import TokenData
from app.core.exceptions import InvalidTokenException


# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Optional[User]:
    """
    Get current authenticated user from JWT token.

    Args:
        db: Database session
        token: JWT access token from Authorization header

    Returns:
        Optional[User]: Authenticated user object if token valid, None otherwise

    Raises:
        InvalidTokenException: If token is invalid or user not found
    """
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        if payload is None:
            raise InvalidTokenException()

        email: str = payload.get("sub")
        if email is None:
            raise InvalidTokenException()

        token_data = TokenData(email=email)
    except JWTError:
        raise InvalidTokenException()

    user = UserService.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise InvalidTokenException()

    return user


def get_current_user_required(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require authenticated user (raises exception if not authenticated).

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        User: Authenticated user object

    Raises:
        InvalidTokenException: If user is not authenticated
    """
    if current_user is None:
        raise InvalidTokenException()
    return current_user
