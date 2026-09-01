from functools import lru_cache
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "ProjectScope AI"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./projectscope.db"

    # AI Configuration
    # Supported providers: "mock", "gemini", "openai"
    AI_PROVIDER: str = "mock"
    AI_PROVIDER_API_KEY: Optional[str] = None
    AI_MODEL: Optional[str] = None
    AI_MAX_RETRIES: int = 2
    AI_TIMEOUT_SECONDS: float = 30.0

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
