"""
Custom exception classes for domain-specific errors.
"""
from typing import Optional


class HealthWatchException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class ModelLoadError(HealthWatchException):
    """Raised when ML model fails to load."""

    pass


class PredictionError(HealthWatchException):
    """Raised when prediction fails."""

    pass


class InvalidInputError(HealthWatchException):
    """Raised when input validation fails."""

    pass
