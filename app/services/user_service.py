"""
User service containing business logic for user operations.

This module handles all user-related operations including CRUD operations,
authentication, and password management with improved error handling.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.models.user import User
from app.models.verification_code import VerificationCode
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import (
    UserNotFoundException,
    EmailAlreadyExistsException,
    DatabaseConnectionException,
    InvalidCredentialsException,
)
from datetime import datetime, timedelta
import random


class UserService:
    """Service class for user-related business logic."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            db: Database session
            user_id: User's unique identifier

        Returns:
            Optional[User]: User object if found, None otherwise

        Raises:
            DatabaseConnectionException: If database query fails
        """
        try:
            return db.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError:
            raise DatabaseConnectionException()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            db: Database session
            email: User's email address

        Returns:
            Optional[User]: User object if found, None otherwise

        Raises:
            DatabaseConnectionException: If database query fails
        """
        try:
            return db.query(User).filter(User.email == email).first()
        except SQLAlchemyError:
            raise DatabaseConnectionException()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Retrieve a list of users with pagination.

        Args:
            db: Database session
            skip: Number of records to skip (default: 0)
            limit: Maximum number of records to return (default: 100)

        Returns:
            List[User]: List of user objects

        Raises:
            DatabaseConnectionException: If database query fails
        """
        try:
            return db.query(User).offset(skip).limit(limit).all()
        except SQLAlchemyError:
            raise DatabaseConnectionException()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            User: Newly created user object

        Raises:
            EmailAlreadyExistsException: If email already exists
            DatabaseConnectionException: If database operation fails
        """
        try:
            # Check if user already exists
            existing_user = UserService.get_user_by_email(db, user_data.email)
            if existing_user:
                raise EmailAlreadyExistsException(user_data.email)

            # Hash password and create user
            hashed_password = get_password_hash(user_data.password)
            db_user = User(
                name=user_data.name,
                email=user_data.email,
                hashed_password=hashed_password,
                photo_url=user_data.photo_url,
                role=user_data.role,
            )

            db.add(db_user)
            db.commit()
            db.refresh(db_user)

            return db_user
        except EmailAlreadyExistsException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """
        Update an existing user's information.

        Args:
            db: Database session
            user_id: User's unique identifier
            user_data: Updated user data

        Returns:
            User: Updated user object

        Raises:
            UserNotFoundException: If user not found
            EmailAlreadyExistsException: If email already exists
            DatabaseConnectionException: If database operation fails
        """
        try:
            db_user = UserService.get_user_by_id(db, user_id)
            if not db_user:
                raise UserNotFoundException(user_id=user_id)

            # Check email uniqueness if email is being updated
            if user_data.email and user_data.email != db_user.email:
                existing_user = UserService.get_user_by_email(db, user_data.email)
                if existing_user:
                    raise EmailAlreadyExistsException(user_data.email)
                db_user.email = user_data.email

            # Update fields if provided
            if user_data.name:
                db_user.name = user_data.name

            if user_data.password:
                db_user.hashed_password = get_password_hash(user_data.password)

            if user_data.photo_url is not None:
                db_user.photo_url = user_data.photo_url

            if user_data.role is not None:
                db_user.role = user_data.role

            db.commit()
            db.refresh(db_user)

            return db_user
        except (UserNotFoundException, EmailAlreadyExistsException):
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete a user from the database.

        Args:
            db: Database session
            user_id: User's unique identifier

        Returns:
            bool: True if deletion successful

        Raises:
            UserNotFoundException: If user not found
            DatabaseConnectionException: If database operation fails
        """
        try:
            db_user = UserService.get_user_by_id(db, user_id)
            if not db_user:
                raise UserNotFoundException(user_id=user_id)

            db.delete(db_user)
            db.commit()

            return True
        except UserNotFoundException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            db: Database session
            email: User's email address
            password: User's plain text password

        Returns:
            Optional[User]: User object if authentication successful, None otherwise

        Raises:
            DatabaseConnectionException: If database query fails
        """
        try:
            user = UserService.get_user_by_email(db, email)
            if not user:
                return None

            if not verify_password(password, user.hashed_password):
                return None

            return user
        except DatabaseConnectionException:
            raise

    @staticmethod
    def change_password(db: Session, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change user password (requires current password).

        Args:
            db: Database session
            user_id: User's unique identifier
            current_password: Current password for verification
            new_password: New password to set

        Returns:
            bool: True if password changed successfully

        Raises:
            UserNotFoundException: If user not found
            InvalidCredentialsException: If current password is incorrect
            DatabaseConnectionException: If database operation fails
        """
        try:
            db_user = UserService.get_user_by_id(db, user_id)
            if not db_user:
                raise UserNotFoundException(user_id=user_id)

            # Verify current password
            if not verify_password(current_password, db_user.hashed_password):
                raise InvalidCredentialsException()

            # Set new password
            db_user.hashed_password = get_password_hash(new_password)

            db.commit()
            db.refresh(db_user)

            return True
        except (UserNotFoundException, InvalidCredentialsException):
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()

    @staticmethod
    def generate_verification_code(db: Session, email: str) -> str:
        """
        Generate and store verification code for password reset.

        Args:
            db: Database session
            email: User's email address

        Returns:
            str: 6-digit verification code

        Raises:
            UserNotFoundException: If user not found
            DatabaseConnectionException: If database operation fails
        """
        try:
            # Verify user exists
            user = UserService.get_user_by_email(db, email)
            if not user:
                raise UserNotFoundException(email=email)

            # Generate 6-digit code
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

            # Create verification code (expires in 15 minutes)
            verification_code = VerificationCode(
                email=email,
                code=code,
                expires_at=datetime.utcnow() + timedelta(minutes=15)
            )

            db.add(verification_code)
            db.commit()

            return code
        except UserNotFoundException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()

    @staticmethod
    def reset_password_with_code(db: Session, email: str, code: str, new_password: str) -> bool:
        """
        Reset password using verification code.

        Args:
            db: Database session
            email: User's email address
            code: 6-digit verification code
            new_password: New password to set

        Returns:
            bool: True if password reset successfully

        Raises:
            UserNotFoundException: If user not found
            InvalidCredentialsException: If code is invalid or expired
            DatabaseConnectionException: If database operation fails
        """
        try:
            # Verify user exists
            user = UserService.get_user_by_email(db, email)
            if not user:
                raise UserNotFoundException(email=email)

            # Find valid verification code
            verification = db.query(VerificationCode).filter(
                VerificationCode.email == email,
                VerificationCode.code == code,
                VerificationCode.is_used == False,
                VerificationCode.expires_at > datetime.utcnow()
            ).first()

            if not verification:
                raise InvalidCredentialsException()

            # Mark code as used
            verification.is_used = True

            # Update password
            user.hashed_password = get_password_hash(new_password)

            db.commit()

            return True
        except (UserNotFoundException, InvalidCredentialsException):
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()


    @staticmethod
    def reset_password_simple(db: Session, email: str, new_password: str) -> bool:
        """
        Reset password directly with email (no verification code required).

        Args:
            db: Database session
            email: User's email address
            new_password: New password to set

        Returns:
            bool: True if password reset successfully

        Raises:
            UserNotFoundException: If user not found
            DatabaseConnectionException: If database operation fails
        """
        try:
            # Verify user exists
            user = UserService.get_user_by_email(db, email)
            if not user:
                raise UserNotFoundException(email=email)

            # Update password directly
            user.hashed_password = get_password_hash(new_password)

            db.commit()
            db.refresh(user)

            return True
        except UserNotFoundException:
            raise
        except SQLAlchemyError:
            db.rollback()
            raise DatabaseConnectionException()
