"""
Application configuration settings.

This module loads environment variables and provides centralized configuration
for the FastAPI application including database, security, and API settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: PostgreSQL connection string
        SECRET_KEY: Secret key for JWT token generation
        ALGORITHM: Algorithm used for JWT encoding
        ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes
        API_V1_PREFIX: API version 1 route prefix
        PROJECT_NAME: Application name
    """

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Exoplanet Detection API"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
