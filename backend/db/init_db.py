"""
Database initialization: creates tables using SQLAlchemy.
"""

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from db.models import Base
from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


async def init_db():
    """
    Create database tables.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
