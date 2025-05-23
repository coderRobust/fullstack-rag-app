"""
Service for user authentication and registration.
"""

from sqlalchemy.future import select
from db.models import User
from db.init_db import AsyncSessionLocal
from utils.security import hash_password, verify_password, create_access_token
from schemas.user import UserCreate, UserLogin


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
