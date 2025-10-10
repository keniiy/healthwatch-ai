"""
Health check endpoints for Kubernetes probes.
"""

from fastapi import APIRouter, status
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Health check",
    response_description="Service is healthy",
)
async def health_check():
    """
    Kubernetes liveness probe endpoint.

    Returns 200 OK if service is running.
    K8s restarts pod if this returns non-200.
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Readiness check",
    response_description="Service is ready to accept traffic",
)
async def readiness_check():
    """
    Kubernetes readiness probe endpoint.

    Returns 200 OK if service can handle requests.
    K8s removes pod from load balancer if this returns non-200.

    In production, check:
    - Database connection
    - Model loaded
    - External dependencies available
    """
    # Week 1: Simple check
    # Week 5: Add model.is_loaded() check
    return {"status": "ready", "service": settings.APP_NAME}
