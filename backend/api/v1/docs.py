"""
API Documentation for the RAG Document Management and Q&A System.
This module contains detailed descriptions and examples for all API endpoints.
"""

from typing import Dict, Any

# API Tags
TAGS_METADATA = [
    {
        "name": "Auth",
        "description": "Authentication operations including user registration and login.",
    },
    {
        "name": "Documents",
        "description": "Document management operations including upload, list, and delete.",
    },
    {
        "name": "Q&A",
        "description": "Question answering operations using RAG pipeline.",
    },
]

# API Examples
EXAMPLES = {
    "user_create": {
        "summary": "Create a new user",
        "value": {
            "email": "user@example.com",
            "password": "strongpassword123"
        }
    },
    "user_login": {
        "summary": "Login with user credentials",
        "value": {
            "email": "user@example.com",
            "password": "strongpassword123"
        }
    },
    "document_upload": {
        "summary": "Upload a new document",
        "value": {
            "file": "(binary)",
            "metadata": {
                "title": "Sample Document",
                "description": "A sample document for testing"
            }
        }
    },
    "question": {
        "summary": "Ask a question about a document",
        "value": {
            "document_id": 1,
            "question": "What is the main topic of this document?"
        }
    }
}

# API Responses
RESPONSES = {
    "auth": {
        "200": {
            "description": "Successful authentication",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "token_type": "bearer"
                    }
                }
            }
        },
        "401": {
            "description": "Authentication failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Could not validate credentials"
                    }
                }
            }
        }
    },
    "document": {
        "200": {
            "description": "Successful document operation",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "title": "Sample Document",
                        "created_at": "2024-03-20T10:00:00Z"
                    }
                }
            }
        },
        "404": {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Document with id 1 not found"
                    }
                }
            }
        }
    },
    "qa": {
        "200": {
            "description": "Successful question answering",
            "content": {
                "application/json": {
                    "example": {
                        "answer": "The main topic of this document is...",
                        "confidence": 0.95
                    }
                }
            }
        },
        "404": {
            "description": "Document not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Document with id 1 not found"
                    }
                }
            }
        }
    }
}

def get_api_docs() -> Dict[str, Any]:
    """Get API documentation configuration."""
    return {
        "title": "RAG Document Management and Q&A API",
        "description": """
        This API provides endpoints for:
        * User authentication and management
        * Document upload and management
        * Question answering using RAG (Retrieval-Augmented Generation)
        
        ## Authentication
        All endpoints except `/auth/register` and `/auth/login` require authentication.
        Include the JWT token in the Authorization header:
        ```
        Authorization: Bearer <token>
        ```
        
        ## Rate Limiting
        API calls are limited to 100 requests per minute per IP address.
        
        ## Error Handling
        The API uses standard HTTP status codes and returns detailed error messages.
        """,
        "version": "1.0.0",
        "openapi_tags": TAGS_METADATA,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "swagger_ui_parameters": {
            "persistAuthorization": True,
            "displayRequestDuration": True,
            "filter": True
        }
    } 