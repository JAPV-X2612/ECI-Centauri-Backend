"""
Password management endpoints.

This module handles password change and reset operations.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import (
    PasswordChange,
    PasswordResetRequest,
    PasswordResetConfirm,
    MessageResponse,
    PasswordResetSimple,
)
from app.services.user_service import UserService
from app.api.v1.dependencies import get_current_user_required
from app.models.user import User

router = APIRouter()


@router.post(
    "/change",
    response_model=MessageResponse,
    summary="Change password (authenticated)",
    response_description="Password changed successfully"
)
def change_password(
        password_data: PasswordChange,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_required)
):
    """
    Change password for authenticated user.

    **Request Body:**
    - **current_password**: Current password for verification
    - **new_password**: New password (min 8 characters)

    **Returns:**
    - Success message

    **Errors:**
    - **401 Unauthorized**: Missing/invalid token or wrong current password
    - **503 Service Unavailable**: Database error

    **Requires:**
    Valid JWT token in Authorization header
    """
    UserService.change_password(
        db,
        current_user.id,
        password_data.current_password,
        password_data.new_password
    )

    return {"message": "Password changed successfully"}


@router.post(
    "/reset/request",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Request password reset code",
    response_description="Verification code sent"
)
def request_password_reset(
        request_data: PasswordResetRequest,
        db: Session = Depends(get_db)
):
    """
    Request password reset verification code.

    **Request Body:**
    - **email**: User's email address

    **Returns:**
    - Success message (code sent to email)

    **Errors:**
    - **404 Not Found**: Email not registered
    - **503 Service Unavailable**: Database error

    **Note:**
    - Code expires in 15 minutes
    - For demo purposes, code is returned in response
    - In production, send code via email service
    """
    code = UserService.generate_verification_code(db, request_data.email)

    # TODO: Send code via email service (SendGrid, AWS SES, etc.)
    # For now, return code in response for testing

    return {
        "message": f"Verification code sent to {request_data.email}. Code: {code} (expires in 15 min)"
    }


@router.post(
    "/reset/confirm",
    response_model=MessageResponse,
    summary="Reset password with code",
    response_description="Password reset successfully"
)
def confirm_password_reset(
        reset_data: PasswordResetConfirm,
        db: Session = Depends(get_db)
):
    """
    Reset password using verification code.

    **Request Body:**
    - **email**: User's email address
    - **verification_code**: 6-digit code received
    - **new_password**: New password (min 8 characters)

    **Returns:**
    - Success message

    **Errors:**
    - **401 Unauthorized**: Invalid or expired code
    - **404 Not Found**: Email not registered
    - **503 Service Unavailable**: Database error

    **Note:**
    Code can only be used once and expires in 15 minutes
    """
    UserService.reset_password_with_code(
        db,
        reset_data.email,
        reset_data.verification_code,
        reset_data.new_password
    )

    return {"message": "Password reset successfully"}


@router.post(
    "/reset/simple",
    response_model=MessageResponse,
    summary="Reset password with email only",
    response_description="Password reset successfully"
)
def reset_password_simple(
        reset_data: PasswordResetSimple,
        db: Session = Depends(get_db)
):
    """
    Reset password directly using email (no verification code).

    **Request Body:**
    - **email**: User's email address
    - **new_password**: New password (min 8 characters)

    **Returns:**
    - Success message

    **Errors:**
    - **404 Not Found**: Email not registered
    - **503 Service Unavailable**: Database error

    **Note:**
    This endpoint is for demo purposes. In production, implement
    email verification with codes or magic links.
    """
    UserService.reset_password_simple(
        db,
        reset_data.email,
        reset_data.new_password
    )

    return {"message": "Password reset successfully. You can now sign in with your new password."}
