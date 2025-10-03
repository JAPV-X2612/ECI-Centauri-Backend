"""
Custom exception classes for the application.

This module defines custom exceptions with clear error messages
and appropriate HTTP status codes for different error scenarios.
"""

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """
    Exception raised when a user is not found in the database.

    Attributes:
        status_code: HTTP 404 Not Found
        detail: Error message indicating user was not found
    """

    def __init__(self, user_id: int = None, email: str = None):
        identifier = f"ID {user_id}" if user_id else f"email '{email}'"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {identifier} not found"
        )


class EmailAlreadyExistsException(HTTPException):
    """
    Exception raised when attempting to register with an existing email.

    Attributes:
        status_code: HTTP 409 Conflict
        detail: Error message indicating email is already registered
    """

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{email}' is already registered"
        )


class InvalidCredentialsException(HTTPException):
    """
    Exception raised when login credentials are invalid.

    Attributes:
        status_code: HTTP 401 Unauthorized
        detail: Error message for invalid credentials
        headers: WWW-Authenticate header for bearer token
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )


class UnauthorizedAccessException(HTTPException):
    """
    Exception raised when user tries to access unauthorized resources.

    Attributes:
        status_code: HTTP 403 Forbidden
        detail: Error message for forbidden access
    """

    def __init__(self, resource: str = "resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You are not authorized to access this {resource}"
        )


class InvalidTokenException(HTTPException):
    """
    Exception raised when JWT token is invalid or expired.

    Attributes:
        status_code: HTTP 401 Unauthorized
        detail: Error message for invalid token
        headers: WWW-Authenticate header
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )


class DatabaseConnectionException(HTTPException):
    """
    Exception raised when database connection fails.

    Attributes:
        status_code: HTTP 503 Service Unavailable
        detail: Error message for database issues
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed. Please try again later"
        )
