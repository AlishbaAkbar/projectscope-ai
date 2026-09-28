"""
Phase 23: Central Configuration
All security-relevant settings in one place
"""

import os
import secrets
from functools import lru_cache
from typing import List
from dotenv import load_dotenv

load_dotenv()

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
    JWT_SECRET: str = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)
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
    MAX_REQUEST_SIZE_MB: int = int(os.getenv("MAX_REQUEST_SIZE_MB", "5"))
    MAX_PROMPT_LENGTH: int = int(os.getenv("MAX_PROMPT_LENGTH", "10000"))
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    
    # ============================================
    # AI SAFETY
    # ============================================
    AI_MAX_RETRIES: int = int(os.getenv("AI_MAX_RETRIES", "2"))
    AI_TIMEOUT_SECONDS: float = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "4000"))
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
    AI_PROVIDER_API_KEY: str = os.getenv("AI_PROVIDER_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "gemini-2.5-flash")
    
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
    configured = Settings()
    if configured.APP_ENV.lower() == "production" and not os.getenv("JWT_SECRET"):
        raise RuntimeError("JWT_SECRET must be configured in production.")
    return configured


settings = get_settings()