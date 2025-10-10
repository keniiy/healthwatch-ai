"""
Prediction endpoints for ML inference.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.prediction import HealthMetricsRequest, RiskAssessmentResponse
from app.domain.services.risk_scorer import RiskScoringService
from app.domain.models.prediction import HealthMetrics
from app.api.deps import get_risk_scoring_service
from app.core.exceptions import HealthWatchException
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/predict",
    response_model=RiskAssessmentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Predictions"],
    summary="Predict health risk",
    response_description="Risk assessment based on patient metrics",
)
async def predict_health_risk(
    request: HealthMetricsRequest,
    risk_service: RiskScoringService = Depends(get_risk_scoring_service),
):
    """
    Predict health risk based on patient metrics.

    **Request Body:**
    - age: Patient age (0-120 years)
    - bmi: Body Mass Index (10-60)
    - blood_pressure: Systolic BP (60-250 mmHg)

    **Returns:**
    - risk_score: Numerical score 0-1
    - risk_level: Category (low/medium/high/critical)
    - confidence: Model confidence
    - contributing_factors: List of risk factors
    """
    try:
        # Convert DTO to domain model
        health_metrics = HealthMetrics(
            age=request.age,
            bmi=request.bmi,
            blood_pressure_systolic=request.blood_pressure,
        )

        # Business logic (domain layer)
        risk_assessment = risk_service.calculate_risk(health_metrics)

        # Convert domain model to DTO
        return RiskAssessmentResponse(
            risk_score=risk_assessment.risk_score,
            risk_level=risk_assessment.risk_level.value,
            confidence=risk_assessment.confidence,
            contributing_factors=risk_assessment.contributing_factors,
        )

    except HealthWatchException as e:
        logger.error(f"Domain error: {e.message}", extra={"extra_data": e.details})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
