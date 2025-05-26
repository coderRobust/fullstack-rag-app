from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseError(Exception):
    """Base error class for all custom exceptions"""
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationError(BaseError):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, details)

class AuthorizationError(BaseError):
    """Raised when user is not authorized to perform an action"""
    def __init__(self, message: str = "Not authorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, details)

class ValidationError(BaseError):
    """Raised when input validation fails"""
    def __init__(self, message: str = "Validation error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)

class NotFoundError(BaseError):
    """Raised when a requested resource is not found"""
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, details)

class DatabaseError(BaseError):
    """Raised when a database operation fails"""
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)

class DocumentProcessingError(BaseError):
    """Raised when document processing fails"""
    def __init__(self, message: str = "Document processing error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)

class QuestionAnsweringError(BaseError):
    """Raised when question answering fails"""
    def __init__(self, message: str = "Question answering error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)

class VectorStoreError(BaseError):
    """Raised when vector store operations fail"""
    def __init__(self, message: str = "Vector store error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR, details)

def handle_exception(error: Exception) -> HTTPException:
    """Convert custom exceptions to FastAPI HTTPException"""
    if isinstance(error, BaseError):
        return HTTPException(
            status_code=error.status_code,
            detail={
                "message": error.message,
                "details": error.details
            }
        )
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "message": "Internal server error",
            "details": {"error": str(error)}
        }
    ) 