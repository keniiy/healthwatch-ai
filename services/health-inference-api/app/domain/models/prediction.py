"""
Domain entities - Core business objects.
These are NOT Pydantic models (those are DTOs).
These are your business logic models.
"""

from dataclasses import dataclass
from enum import Enum


class RiskLevel(str, Enum):
    """Risk categories for health assessment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class HealthMetrics:
    """
    Patient health metrics (domain entity).

    This is your business model - immutable, validated.
    """

    age: int
    bmi: float
    blood_pressure_systolic: int

    def __post_init__(self):
        """Validate domain rules."""
        if self.age < 0 or self.age > 120:
            raise ValueError(f"Invalid age: {self.age}")
        if self.bmi < 10 or self.bmi > 60:
            raise ValueError(f"Invalid BMI: {self.bmi}")
        if self.blood_pressure_systolic < 60 or self.blood_pressure_systolic > 250:
            raise ValueError(f"Invalid blood pressure: {self.blood_pressure_systolic}")


@dataclass
class RiskAssessment:
    """
    Risk assessment result (domain entity).
    """

    risk_score: float  # 0.0 to 1.0
    risk_level: RiskLevel
    confidence: float  # Model confidence
    contributing_factors: list[str]

    def __post_init__(self):
        """Validate domain rules."""
        if not 0 <= self.risk_score <= 1:
            raise ValueError(f"Risk score must be 0-1, got {self.risk_score}")
        if not 0 <= self.confidence <= 1:
            raise ValueError(f"Confidence must be 0-1, got {self.confidence}")
