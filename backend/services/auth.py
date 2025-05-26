"""
Service for user authentication and registration.
"""

from sqlalchemy.future import select
from db.models import User
from db.init_db import AsyncSessionLocal
from utils.security import hash_password, verify_password, create_access_token
from schemas.user import UserCreate, UserLogin
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import get_settings
from core.exceptions import AuthenticationError, ValidationError
from db.repositories.base import BaseRepository
from models.user import User
from schemas.auth import TokenData, UserCreate, UserInDB

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: BaseRepository[User]):
        self.user_repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    async def authenticate_user(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        try:
            user = await self.user_repository.get_by_email(db, email)
            if not user:
                return None
            if not self.verify_password(password, user.hashed_password):
                return None
            return user
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        try:
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            return encoded_jwt
        except Exception as e:
            raise AuthenticationError(f"Error creating access token: {str(e)}")

    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> User:
        try:
            # Check if user already exists
            existing_user = await self.user_repository.get_by_email(db, user_in.email)
            if existing_user:
                raise ValidationError("Email already registered")
            
            user_data = user_in.dict()
            user_data["hashed_password"] = self.get_password_hash(user_data.pop("password"))
            return await self.user_repository.create(db, user_data)
        except ValidationError:
            raise
        except Exception as e:
            raise AuthenticationError(f"Error creating user: {str(e)}")

    async def get_current_user(self, db: AsyncSession, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise AuthenticationError("Invalid token payload")
            token_data = TokenData(email=email)
        except JWTError:
            raise AuthenticationError("Invalid token")
        
        user = await self.user_repository.get_by_email(db, email=token_data.email)
        if user is None:
            raise AuthenticationError("User not found")
        return user

async def register_user(user: UserCreate) -> str:
    """
    Register a user and return a JWT token.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == user.username))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            return None
        new_user = User(username=user.username,
                        password_hash=hash_password(user.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return create_access_token({"sub": new_user.username, "id": new_user.id})


async def authenticate_user(user: UserLogin) -> str:
    """
    Authenticate user and return a JWT token if valid.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == user.username))
        db_user = result.scalar_one_or_none()
        if db_user and verify_password(user.password, db_user.password_hash):
            return create_access_token({"sub": db_user.username, "id": db_user.id})
        return None
