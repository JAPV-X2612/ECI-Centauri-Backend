"""
User CRUD endpoints.

This module provides RESTful API endpoints for user management
including read, update, and delete operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.api.v1.dependencies import get_current_user_required
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user_required)):
    """
    Get current authenticated user's information.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        UserResponse: Current user information

    Requires:
        Valid JWT token in Authorization header
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Get user by ID (admin or own profile).

    Args:
        user_id: User's unique identifier
        db: Database session
        current_user: Authenticated user

    Returns:
        UserResponse: User information

    Raises:
        HTTPException: 403 if trying to access another user's data
        HTTPException: 404 if user not found

    Requires:
        Valid JWT token
    """
    # Users can only access their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )

    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.get("/", response_model=List[UserResponse])
def list_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    List all users with pagination.

    Args:
        skip: Number of records to skip (default: 0)
        limit: Maximum number of records to return (default: 100)
        db: Database session
        current_user: Authenticated user

    Returns:
        List[UserResponse]: List of users

    Requires:
        Valid JWT token

    Note:
        For production, implement role-based access control
    """
    return UserService.get_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Update user information.

    Args:
        user_id: User's unique identifier
        user_data: Updated user data
        db: Database session
        current_user: Authenticated user

    Returns:
        UserResponse: Updated user information

    Raises:
        HTTPException: 403 if trying to update another user
        HTTPException: 404 if user not found
        HTTPException: 409 if email already exists

    Requires:
        Valid JWT token
    """
    # Users can only update their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    return UserService.update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Delete user account.

    Args:
        user_id: User's unique identifier
        db: Database session
        current_user: Authenticated user

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 403 if trying to delete another user
        HTTPException: 404 if user not found

    Requires:
        Valid JWT token
    """
    # Users can only delete their own account
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    UserService.delete_user(db, user_id)
    return None
