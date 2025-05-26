from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from db.session import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, id: int, obj_in: dict) -> Optional[ModelType]:
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await db.commit()
        return await self.get(db, id)

    async def delete(self, db: AsyncSession, id: int) -> bool:
        query = delete(self.model).where(self.model.id == id)
        result = await db.execute(query)
        await db.commit()
        return result.rowcount > 0 