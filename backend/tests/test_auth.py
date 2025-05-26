import pytest
from fastapi import HTTPException
from services.auth import AuthService
from schemas.auth import UserCreate
from models.user import User
from db.repositories.base import BaseRepository
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from db.repositories.user import UserRepository
from core.exceptions import AuthenticationError
from core.config import get_settings

settings = get_settings()

@pytest.fixture
def mock_user_repo():
    return Mock(spec=UserRepository)

@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(mock_user_repo)

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

def test_create_user_success(auth_service, mock_user_repo):
    # Arrange
    email = "test@example.com"
    password = "password123"
    username = "testuser"
    user_id = 1
    mock_user_repo.create.return_value = Mock(
        id=user_id,
        email=email,
        username=username,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Act
    user = auth_service.create_user(email, password, username)

    # Assert
    assert user.id == user_id
    assert user.email == email
    assert user.username == username
    mock_user_repo.create.assert_called_once()

def test_create_user_duplicate_email(auth_service, mock_user_repo):
    # Arrange
    email = "test@example.com"
    password = "password123"
    username = "testuser"
    mock_user_repo.create.side_effect = Exception("Duplicate email")

    # Act & Assert
    with pytest.raises(AuthenticationError):
        auth_service.create_user(email, password, username)

def test_authenticate_user_success(auth_service, mock_user_repo):
    # Arrange
    email = "test@example.com"
    password = "password123"
    user = Mock(
        id=1,
        email=email,
        username="testuser",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_user_repo.get_by_email.return_value = user
    mock_user_repo.verify_password.return_value = True

    # Act
    result = auth_service.authenticate_user(email, password)

    # Assert
    assert result["access_token"] is not None
    assert result["token_type"] == "bearer"
    assert result["user"].email == email
    mock_user_repo.get_by_email.assert_called_once_with(email)
    mock_user_repo.verify_password.assert_called_once_with(user, password)

def test_authenticate_user_invalid_credentials(auth_service, mock_user_repo):
    # Arrange
    email = "test@example.com"
    password = "wrongpassword"
    user = Mock(
        id=1,
        email=email,
        username="testuser",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_user_repo.get_by_email.return_value = user
    mock_user_repo.verify_password.return_value = False

    # Act & Assert
    with pytest.raises(AuthenticationError):
        auth_service.authenticate_user(email, password)

def test_authenticate_user_not_found(auth_service, mock_user_repo):
    # Arrange
    email = "nonexistent@example.com"
    password = "password123"
    mock_user_repo.get_by_email.return_value = None

    # Act & Assert
    with pytest.raises(AuthenticationError):
        auth_service.authenticate_user(email, password)

def test_create_access_token(auth_service):
    # Arrange
    user = Mock(
        id=1,
        email="test@example.com",
        username="testuser",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    # Act
    token = auth_service.create_access_token(user)

    # Assert
    assert token is not None
    assert isinstance(token, str)

def test_verify_token_success(auth_service, mock_user_repo):
    # Arrange
    user = Mock(
        id=1,
        email="test@example.com",
        username="testuser",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_user_repo.get.return_value = user
    token = auth_service.create_access_token(user)

    # Act
    result = auth_service.verify_token(token)

    # Assert
    assert result.id == user.id
    assert result.email == user.email
    mock_user_repo.get.assert_called_once_with(user.id)

def test_verify_token_invalid(auth_service):
    # Arrange
    invalid_token = "invalid.token.here"

    # Act & Assert
    with pytest.raises(AuthenticationError):
        auth_service.verify_token(invalid_token)

def test_verify_token_expired(auth_service, mock_user_repo):
    # Arrange
    user = Mock(
        id=1,
        email="test@example.com",
        username="testuser",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    mock_user_repo.get.return_value = user

    # Create token with short expiration
    with patch('services.auth.settings.ACCESS_TOKEN_EXPIRE_MINUTES', 0):
        token = auth_service.create_access_token(user)

    # Act & Assert
    with pytest.raises(AuthenticationError):
        auth_service.verify_token(token) 