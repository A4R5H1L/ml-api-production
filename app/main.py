"""
Main FastAPI application.

This module initializes the FastAPI application with all middleware,
routers, and configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application.
    """
    # Startup
    logger.info("Starting ML API application...")
    logger.info(f"API Version: {settings.api_version}")
    logger.info(f"Model: {settings.model_name}")
    logger.info(f"Device: {settings.model_device or 'auto-detect'}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down ML API application...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include API routes
app.include_router(router)


@app.get(
    "/",
    summary="Root Endpoint",
    description="Get basic API information",
    tags=["Info"]
)
async def root():
    """
    Root endpoint providing basic API information.
    
    Returns:
        Dictionary with API name, version, and documentation links
    """
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "description": settings.api_description,
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
