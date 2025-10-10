"""
Business logic for calculating health risk scores.
This is framework-agnostic - pure Python business rules.
"""

from app.domain.models.prediction import HealthMetrics, RiskAssessment, RiskLevel
from app.core.logging import get_logger

logger = get_logger(__name__)


class RiskScoringService:
    """
    Domain service for risk assessment.

    Why a separate service class?
    - Business logic is testable without FastAPI/K8s
    - Can swap algorithms without changing API layer
    - Single responsibility (SOLID principles)
    """

    def calculate_risk(self, metrics: HealthMetrics) -> RiskAssessment:
        """
        Calculate health risk based on patient metrics.

        This is a simplified algorithm for Week 1.
        Week 5: Replace with actual ML model predictions.
        """
        logger.info(
            "Calculating risk",
            extra={
                "extra_data": {
                    "age": metrics.age,
                    "bmi": metrics.bmi,
                    "bp": metrics.blood_pressure_systolic,
                }
            },
        )

        # Weighted risk calculation
        age_risk = self._calculate_age_risk(metrics.age)
        bmi_risk = self._calculate_bmi_risk(metrics.bmi)
        bp_risk = self._calculate_bp_risk(metrics.blood_pressure_systolic)

        # Combined score (weighted average)
        risk_score = (age_risk * 0.3) + (bmi_risk * 0.4) + (bp_risk * 0.3)

        # Determine risk level
        risk_level = self._categorize_risk(risk_score)

        # Identify contributing factors
        factors = self._identify_factors(metrics, age_risk, bmi_risk, bp_risk)

        logger.info(
            "Risk calculated",
            extra={
                "extra_data": {"risk_score": risk_score, "risk_level": risk_level.value}
            },
        )

        return RiskAssessment(
            risk_score=round(risk_score, 3),
            risk_level=risk_level,
            confidence=0.85,  # Placeholder
            contributing_factors=factors,
        )

    def _calculate_age_risk(self, age: int) -> float:
        """Age-based risk component."""
        if age < 30:
            return 0.1
        elif age < 50:
            return 0.3
        elif age < 65:
            return 0.6
        else:
            return 0.9

    def _calculate_bmi_risk(self, bmi: float) -> float:
        """BMI-based risk component."""
        if bmi < 18.5:
            return 0.4  # Underweight
        elif bmi < 25:
            return 0.1  # Normal
        elif bmi < 30:
            return 0.5  # Overweight
        else:
            return 0.8  # Obese

    def _calculate_bp_risk(self, bp: int) -> float:
        """Blood pressure-based risk component."""
        if bp < 120:
            return 0.1  # Normal
        elif bp < 130:
            return 0.3  # Elevated
        elif bp < 140:
            return 0.6  # Stage 1 hypertension
        else:
            return 0.9  # Stage 2 hypertension

    def _categorize_risk(self, score: float) -> RiskLevel:
        """Convert numeric score to risk category."""
        if score < 0.25:
            return RiskLevel.LOW
        elif score < 0.5:
            return RiskLevel.MEDIUM
        elif score < 0.75:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL

    def _identify_factors(
        self, metrics: HealthMetrics, age_risk: float, bmi_risk: float, bp_risk: float
    ) -> list[str]:
        """Identify which factors contribute most to risk."""
        factors = []

        if age_risk > 0.5:
            factors.append(f"Age ({metrics.age} years) is a significant risk factor")

        if bmi_risk > 0.5:
            bmi_category = "overweight" if metrics.bmi < 30 else "obese"
            factors.append(f"BMI ({metrics.bmi:.1f}) indicates {bmi_category}")

        if bp_risk > 0.5:
            factors.append(
                f"Blood pressure ({metrics.blood_pressure_systolic} mmHg) is elevated"
            )

        if not factors:
            factors.append("All metrics within healthy ranges")

        return factors
