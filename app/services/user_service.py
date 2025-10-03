"""
User service containing business logic for user operations.

This module handles all user-related operations including CRUD operations,
authentication, and password management with improved error handling.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import (
    UserNotFoundException,
    EmailAlreadyExistsException,
    DatabaseConnectionException
)


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
                hashed_password=hashed_password
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
