"""
Verification code model for password reset.

This module defines the VerificationCode table for storing
temporary password reset codes.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class VerificationCode(Base):
    """
    Verification code model for password reset.

    Attributes:
        id: Primary key
        email: User's email address
        code: 6-digit verification code
        is_used: Whether code has been used
        created_at: When code was created
        expires_at: When code expires (15 minutes)
    """

    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    code = Column(String(6), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
