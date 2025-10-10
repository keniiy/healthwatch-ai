"""
ML model loading and management.
This is an infrastructure concern - interacts with file system.
"""
from pathlib import Path
from typing import Optional
import joblib

from app.core.config import get_settings
from app.core.exceptions import ModelLoadError
from app.core.logging import get_logger

logger = get_logger(__name__)
settings = get_settings()


class ModelLoader:
    """
    Loads and manages ML models from persistent storage.
    
    In production, this loads from K8s volume (/models).
    In Week 1, we don't have a real model yet (comes in Week 5).
    """
    
    def __init__(self):
        self.model_path = Path(settings.MODEL_PATH)
        self._model: Optional[object] = None
    
    def load_model(self) -> object:
        """
        Load ML model from disk.
        
        Returns:
            Loaded model object (sklearn, pytorch, etc.)
        
        Raises:
            ModelLoadError: If model file doesn't exist or loading fails
        """
        model_file = self.model_path / settings.MODEL_NAME
        
        # For Week 1: Model file doesn't exist yet
        if not model_file.exists():
            logger.warning(
                f"Model file not found at {model_file}. Using dummy model for Week 1."
            )
            return None  # We'll handle this gracefully
        
        try:
            logger.info(f"Loading model from {model_file}")
            self._model = joblib.load(model_file)
            logger.info("Model loaded successfully")
            return self._model
        
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise ModelLoadError(
                message="Failed to load ML model",
                details={"model_path": str(model_file), "error": str(e)}
            )
    
    def get_model(self) -> Optional[object]:
        """Get the loaded model instance."""
        return self._model
    
    def is_model_loaded(self) -> bool:
        """Check if model is successfully loaded."""
        return self._model is not None
