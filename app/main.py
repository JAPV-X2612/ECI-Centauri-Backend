"""
Main FastAPI application entry point.

This module initializes the FastAPI application, configures CORS,
includes routers, and creates database tables on startup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database import engine, Base
from app.api.v1.endpoints import auth, users

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for exoplanet detection with user authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix=f"{settings.API_V1_PREFIX}/users",
    tags=["Users"]
)


@app.get("/")
def root():
    """
    Root endpoint for API health check.

    Returns:
        dict: Welcome message and API status
    """
    return {
        "message": "Exoplanet Detection API",
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: API health status
    """
    return {"status": "healthy"}
