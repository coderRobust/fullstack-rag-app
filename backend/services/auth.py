"""
Authentication service implementation.
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.config import get_settings
from core.exceptions import AuthenticationError
from db.repositories.user import UserRepository
from schemas.user import UserCreate, UserUpdate, UserInDB

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)

    def create_user(self, db: Session, user_in: UserCreate) -> UserInDB:
        """Create a new user."""
        # Check if user exists
        if self.user_repository.get_by_email(db, email=user_in.email):
            raise AuthenticationError("Email already registered")
        
        # Create user with hashed password
        user_data = user_in.model_dump()
        user_data["hashed_password"] = self.get_password_hash(user_in.password)
        del user_data["password"]
        
        user = self.user_repository.create(db, obj_in=UserInDB(**user_data))
        
        # Generate access token
        access_token = self.create_access_token(user.id)
        
        return UserInDB(
            **user.__dict__,
            access_token=access_token
        )

    def authenticate_user(self, db: Session, email: str, password: str) -> UserInDB:
        """Authenticate a user."""
        user = self.user_repository.get_by_email(db, email=email)
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        if not self.verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        
        # Generate access token
        access_token = self.create_access_token(user.id)
        
        return UserInDB(
            **user.__dict__,
            access_token=access_token
        )

    def create_access_token(self, user_id: int) -> str:
        """Create JWT access token."""
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )

    def verify_token(self, db: Session, token: str) -> UserInDB:
        """Verify JWT token and return user."""
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            user_id = int(payload.get("sub"))
            if not user_id:
                raise AuthenticationError("Invalid token")
        except JWTError:
            raise AuthenticationError("Invalid token")
        
        user = self.user_repository.get(db, id=user_id)
        if not user:
            raise AuthenticationError("User not found")
        
        return UserInDB(**user.__dict__)

    def update_user(
        self,
        db: Session,
        *,
        db_obj: UserInDB,
        obj_in: UserUpdate
    ) -> UserInDB:
        """Update user information."""
        update_data = obj_in.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = self.get_password_hash(update_data["password"])
            del update_data["password"]
        
        user = self.user_repository.update(db, db_obj=db_obj, obj_in=update_data)
        return UserInDB(**user.__dict__)
