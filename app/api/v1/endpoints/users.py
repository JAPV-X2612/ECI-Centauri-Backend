"""
User CRUD endpoints with improved error handling.

This module provides RESTful API endpoints for user management
with clear error messages and proper HTTP status codes.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.api.v1.dependencies import get_current_user_required
from app.models.user import User
from app.core.exceptions import (
    UserNotFoundException,
    UnauthorizedAccessException,
    EmailAlreadyExistsException
)

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    response_description="Current user information"
)
def get_current_user_info(current_user: User = Depends(get_current_user_required)):
    """
    Get authenticated user's profile information.

    **Returns:**
    - User profile information

    **Errors:**
    - **401 Unauthorized**: Missing or invalid token

    **Requires:**
    Valid JWT token in Authorization header
    """
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    response_description="User information"
)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Get user information by ID.

    **Path Parameters:**
    - **user_id**: User's unique identifier

    **Returns:**
    - User information

    **Errors:**
    - **401 Unauthorized**: Missing or invalid token
    - **403 Forbidden**: Attempting to access another user's data
    - **404 Not Found**: User does not exist
    - **503 Service Unavailable**: Database connection error

    **Note:**
    Users can only access their own profile information.
    """
    # Users can only access their own data
    if current_user.id != user_id:
        raise UnauthorizedAccessException("user profile")

    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundException(user_id=user_id)

    return user


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List all users",
    response_description="List of users"
)
def list_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    List all users with pagination.

    **Query Parameters:**
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 100)

    **Returns:**
    - List of users

    **Errors:**
    - **401 Unauthorized**: Missing or invalid token
    - **503 Service Unavailable**: Database connection error

    **Note:**
    In production, implement role-based access control for this endpoint.
    """
    return UserService.get_users(db, skip=skip, limit=limit)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user information",
    response_description="Updated user information"
)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Update user profile information.

    **Path Parameters:**
    - **user_id**: User's unique identifier

    **Request Body (all optional):**
    - **name**: Updated name
    - **email**: Updated email (must be unique)
    - **password**: Updated password (min 8 characters)

    **Returns:**
    - Updated user information

    **Errors:**
    - **401 Unauthorized**: Missing or invalid token
    - **403 Forbidden**: Attempting to update another user
    - **404 Not Found**: User does not exist
    - **409 Conflict**: Email already registered to another user
    - **503 Service Unavailable**: Database connection error

    **Note:**
    Users can only update their own profile.
    """
    # Users can only update their own data
    if current_user.id != user_id:
        raise UnauthorizedAccessException("user profile")

    return UserService.update_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user account",
    response_description="User successfully deleted"
)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Delete user account permanently.

    **Path Parameters:**
    - **user_id**: User's unique identifier

    **Returns:**
    - No content (204)

    **Errors:**
    - **401 Unauthorized**: Missing or invalid token
    - **403 Forbidden**: Attempting to delete another user
    - **404 Not Found**: User does not exist
    - **503 Service Unavailable**: Database connection error

    **Warning:**
    This action is permanent and cannot be undone.
    Users can only delete their own account.
    """
    # Users can only delete their own account
    if current_user.id != user_id:
        raise UnauthorizedAccessException("user account")

    UserService.delete_user(db, user_id)
    return None
