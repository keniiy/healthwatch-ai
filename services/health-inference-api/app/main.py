"""
FastAPI application entry point.
This is what uvicorn runs.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import health, predictions

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Code before yield runs on startup.
    Code after yield runs on shutdown.
    """
    # Startup
    setup_logging(settings.LOG_LEVEL)
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Model path: {settings.MODEL_PATH}")

    yield

    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade ML inference API for healthcare risk prediction",
    lifespan=lifespan,
)

# CORS middleware (for web frontends)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: Restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(predictions.router, prefix=settings.API_PREFIX, tags=["ML"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": f"{settings.API_PREFIX}/health",
        "predict": f"{settings.API_PREFIX}/predict",
    }
