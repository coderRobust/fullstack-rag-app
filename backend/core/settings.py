"""
App configuration using Pydantic BaseSettings.
Loads sensitive keys from .env file.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    # App-specific
    APP_NAME: str = "Fullstack RAG App"
    ENV: str = "development"

    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # OpenAI or LLM config
    OPENAI_API_KEY: str

    # Database config
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
