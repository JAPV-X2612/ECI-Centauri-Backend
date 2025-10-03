"""
API dependencies for authentication and authorization.

This module provides dependency functions for FastAPI endpoints
to handle user authentication via JWT tokens.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.core.security import decode_access_token
from app.services.user_service import UserService
from app.models.user import User
from app.schemas.user import TokenData

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
        HTTPException: If token is invalid or user not found (401 Unauthorized)
    """
    if not token:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        if payload is None:
            raise credentials_exception

        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = UserService.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception

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
        HTTPException: If user is not authenticated (401 Unauthorized)
    """
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
