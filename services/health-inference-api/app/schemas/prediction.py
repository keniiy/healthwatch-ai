"""
Pydantic schemas (DTOs) for API request/response.
These are the "contracts" between your API and clients.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class HealthMetricsRequest(BaseModel):
    """
    Request schema for health prediction endpoint.

    This is what clients send in POST /predict.
    """

    age: int = Field(
        ..., ge=0, le=120, description="Patient age in years", examples=[45]
    )
    bmi: float = Field(
        ..., ge=10.0, le=60.0, description="Body Mass Index", examples=[26.5]
    )
    blood_pressure: int = Field(
        ...,
        ge=60,
        le=250,
        description="Systolic blood pressure in mmHg",
        examples=[130],
    )

    @field_validator("bmi")
    @classmethod
    def validate_bmi(cls, v: float) -> float:
        """Custom validation for BMI."""
        if v < 10 or v > 60:
            raise ValueError("BMI must be between 10 and 60")
        return round(v, 1)  # Round to 1 decimal place


class RiskAssessmentResponse(BaseModel):
    """
    Response schema for health prediction.

    This is what your API returns.
    """

    risk_score: float = Field(..., description="Risk score between 0 and 1")
    risk_level: str = Field(
        ..., description="Risk category: low, medium, high, critical"
    )
    confidence: float = Field(..., description="Model confidence score")
    contributing_factors: List[str] = Field(
        ..., description="Factors contributing to risk"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "risk_score": 0.483,
                "risk_level": "medium",
                "confidence": 0.85,
                "contributing_factors": [
                    "Age (45 years) is a moderate risk factor",
                    "BMI (26.5) indicates overweight",
                ],
            }
        }
