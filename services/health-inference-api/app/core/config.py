"""
Configuration management using Pydantic Settings.
Environment variables override these defaults.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    In K8s, these come from ConfigMaps or Secrets.
    Locally, they come from .env file.
    """
    # Application
    APP_NAME: str = "HealthWatch AI - Inference API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # API
    API_PREFIX: str = "/api/v1"

    # ML Model
    MODEL_PATH: str = "/models"  # K8s volume mount path
    MODEL_NAME: str = "health_risk_model.pkl"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Monitoring
    ENABLE_METRICS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.

    @lru_cache ensures we only load settings once,
    not on every request (performance optimization).
    """
    return Settings()