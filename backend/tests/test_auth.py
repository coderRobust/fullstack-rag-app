import pytest
from fastapi import HTTPException
from services.auth import AuthService
from schemas.auth import UserCreate
from models.user import User
from db.repositories.base import BaseRepository

@pytest.fixture
def auth_service(test_db):
    user_repository = BaseRepository(User)
    return AuthService(user_repository)

@pytest.mark.asyncio
async def test_create_user(auth_service, test_db):
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    user = await auth_service.create_user(test_db, user_data)
    assert user.email == user_data.email
    assert user.hashed_password != user_data.password

@pytest.mark.asyncio
async def test_authenticate_user(auth_service, test_db):
    # Create user first
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    await auth_service.create_user(test_db, user_data)
    
    # Test authentication
    user = await auth_service.authenticate_user(
        test_db,
        email="test@example.com",
        password="testpassword123"
    )
    assert user is not None
    assert user.email == "test@example.com"

@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(auth_service, test_db):
    # Create user first
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    await auth_service.create_user(test_db, user_data)
    
    # Test authentication with wrong password
    user = await auth_service.authenticate_user(
        test_db,
        email="test@example.com",
        password="wrongpassword"
    )
    assert user is None

@pytest.mark.asyncio
async def test_create_access_token(auth_service):
    data = {"sub": "test@example.com"}
    token = auth_service.create_access_token(data)
    assert token is not None
    assert isinstance(token, str)

@pytest.mark.asyncio
async def test_get_current_user(auth_service, test_db):
    # Create user and token
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword123"
    )
    user = await auth_service.create_user(test_db, user_data)
    token = auth_service.create_access_token({"sub": user.email})
    
    # Test getting current user
    current_user = await auth_service.get_current_user(test_db, token)
    assert current_user is not None
    assert current_user.email == user.email 