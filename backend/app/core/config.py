"""
Phase 23: Central Configuration
All security-relevant settings in one place
"""

import os
from functools import lru_cache
from typing import List


class Settings:
    """Application settings"""
    
    # ============================================
    # APPLICATION
    # ============================================
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_VERSION: str = "0.3.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # ============================================
    # SECURITY
    # ============================================
    JWT_SECRET: str = os.getenv("JWT_SECRET", "CHANGE_ME_IN_PRODUCTION")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ============================================
    # RATE LIMITING
    # ============================================
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_AUTH_PER_MINUTE: int = 5  # Stricter for auth
    RATE_LIMIT_AI_PER_MINUTE: int = 10   # AI endpoints
    
    # ============================================
    # CORS
    # ============================================
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # ============================================
    # REQUEST LIMITS
    # ============================================
    MAX_REQUEST_SIZE_MB: int = 5
    MAX_PROMPT_LENGTH: int = 10000
    MAX_FILE_SIZE_MB: int = 10
    
    # ============================================
    # AI SAFETY
    # ============================================
    AI_MAX_RETRIES: int = 2
    AI_TIMEOUT_SECONDS: float = 30.0
    AI_MAX_TOKENS: int = 4000
    
    # ============================================
    # DATABASE
    # ============================================
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./projectscope.db")
    
    # ============================================
    # FEATURE FLAGS
    # ============================================
    ENABLE_AUDIT_LOG: bool = True
    ENABLE_SECURITY_HEADERS: bool = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()