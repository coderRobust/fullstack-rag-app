"""
Logging configuration for the application.
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from core.config import get_settings

settings = get_settings()

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging
def setup_logging():
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # Create handlers
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("langchain").setLevel(logging.INFO)

    return root_logger

# Create loggers for different components
auth_logger = setup_logging()
document_logger = setup_logging()
rag_logger = setup_logging()
api_logger = setup_logging()

def log_api_request(logger: logging.Logger, request_info: dict):
    """
    Log API request information.
    
    Args:
        logger: Logger instance
        request_info: Dictionary containing request information
    """
    logger.info(
        "API Request: %s %s - Status: %s - Duration: %s ms",
        request_info.get("method", "UNKNOWN"),
        request_info.get("path", "UNKNOWN"),
        request_info.get("status_code", "UNKNOWN"),
        request_info.get("duration", 0)
    )

def log_error(logger: logging.Logger, error: Exception, context: dict = None):
    """
    Log error information with context.
    
    Args:
        logger: Logger instance
        error: Exception instance
        context: Additional context information
    """
    error_info = {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context or {}
    }
    logger.error("Error occurred: %s", error_info, exc_info=True) 