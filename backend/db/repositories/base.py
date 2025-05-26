from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from pydantic import BaseModel
from core.exceptions import NotFoundError, DatabaseError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID"""
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except Exception as e:
            raise DatabaseError(f"Error retrieving {self.model.__name__}", details={"error": str(e)})

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Get multiple records with optional filtering"""
        try:
            query = db.query(self.model)
            if filters:
                for key, value in filters.items():
                    query = query.filter(getattr(self.model, key) == value)
            return query.offset(skip).limit(limit).all()
        except Exception as e:
            raise DatabaseError(f"Error retrieving {self.model.__name__}s", details={"error": str(e)})

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        try:
            db_obj = self.model(**obj_in.model_dump())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseError(f"Error creating {self.model.__name__}", details={"error": str(e)})

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update a record"""
        try:
            update_data = obj_in.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(db_obj, field, update_data[field])
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            raise DatabaseError(f"Error updating {self.model.__name__}", details={"error": str(e)})

    def delete(self, db: Session, *, id: Any) -> ModelType:
        """Delete a record"""
        try:
            obj = db.query(self.model).get(id)
            if not obj:
                raise NotFoundError(f"{self.model.__name__} not found", details={"id": id})
            db.delete(obj)
            db.commit()
            return obj
        except Exception as e:
            db.rollback()
            if isinstance(e, NotFoundError):
                raise e
            raise DatabaseError(f"Error deleting {self.model.__name__}", details={"error": str(e)})

    def exists(self, db: Session, id: Any) -> bool:
        """Check if a record exists"""
        try:
            return db.query(self.model).filter(self.model.id == id).first() is not None
        except Exception as e:
            raise DatabaseError(f"Error checking {self.model.__name__} existence", details={"error": str(e)}) 