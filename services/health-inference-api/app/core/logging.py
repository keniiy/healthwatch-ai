"""
Structured logging configuration.
Outputs JSON logs that can be parsed by Prometheus/Grafana.
"""

import logging
import sys
from typing import Any
import json
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs as JSON.

    Why JSON logs?
    - Easier to parse in Prometheus/Grafana
    - Structured data (not just strings)
    - Searchable in log aggregation systems
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields (custom context)
        extra_data = getattr(record, "extra_data", {})
        if extra_data:
            log_data.update(extra_data)

        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure application logging.

    In K8s, these logs go to stdout/stderr,
    which K8s captures and forwards to your logging system.
    """
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler with JSON formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(console_handler)

    # Suppress noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(name)
