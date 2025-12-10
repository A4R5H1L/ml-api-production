"""
Application configuration using Pydantic Settings.

This module manages all application configuration through environment variables
and provides sensible defaults for development and production environments.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables.
    For example, set API_TITLE="My API" to change the API title.
    """
    
    # API Metadata
    api_title: str = "ML Image Classification API"
    api_version: str = "0.1.0"
    api_description: str = "Production-ready ML API for image classification using ResNet-18"
    
    # Server Settings
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ML Model Settings
    model_name: str = "resnet18"  # Options: resnet18, resnet50, resnet101, efficientnet_b2
    model_device: Optional[str] = None  # None = auto-detect (CUDA if available)
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # 'json' or 'text'
    
    # CORS Settings
    cors_origins: list[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
