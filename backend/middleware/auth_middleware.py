"""
Custom FastAPI middleware to extract JWT user from Authorization header.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from utils.security import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Always initialize user to None
        request.state.user = None

        # Extract Bearer token
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            jwt_token = token.split(" ")[1]
            payload = decode_access_token(jwt_token)

            if payload:
                request.state.user = payload

        return await call_next(request)
