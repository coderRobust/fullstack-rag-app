"""
Router for authentication endpoints: register and login.
"""

from fastapi import APIRouter, HTTPException, status
from schemas.user import UserCreate, UserLogin, TokenResponse
from services.auth import register_user, authenticate_user
from utils.security import create_access_token

router = APIRouter()


@router.post("/register", response_model=TokenResponse)
async def register(user: UserCreate):
    """
    Register a new user and return a JWT token.
    """
    token = await register_user(user)
    if not token:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"access_token": token}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """
    Authenticate user credentials and return a JWT token.
    """
    token = await authenticate_user(user)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token}


@router.get("/test-token", tags=["Auth"])
def generate_test_token():
    """
    Generate a test JWT token for Swagger UI.
    """
    user_data = {
        "id": 1,
        "username": "demo_user"
    }
    token = create_access_token(user_data)
    return {"access_token": token}
