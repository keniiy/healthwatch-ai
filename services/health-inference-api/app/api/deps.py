"""
Dependency injection for FastAPI routes.
This is how you provide instances to your route handlers.
"""

from app.domain.services.risk_scorer import RiskScoringService
from app.infrastructure.ml.model_loader import ModelLoader


def get_risk_scoring_service() -> RiskScoringService:
    """
    Dependency provider for risk scoring service.

    FastAPI calls this function to get a service instance
    for each request.
    """
    return RiskScoringService()


def get_model_loader() -> ModelLoader:
    """Dependency provider for model loader."""
    return ModelLoader()
