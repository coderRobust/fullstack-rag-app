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

# Log format
log_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with console and file handlers.
    
    Args:
        name: The name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = RotatingFileHandler(
        log_dir / f"{name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    return logger

# Create loggers for different components
auth_logger = setup_logger("auth")
document_logger = setup_logger("document")
rag_logger = setup_logger("rag")
api_logger = setup_logger("api")

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