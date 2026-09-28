from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import logging
from contextlib import asynccontextmanager

from app.api.routes.projects import router as projects_router
from app.api.routes.auth import router as auth_router
from app.database.session import init_db
from app.core.config import settings
from app.core.rate_limit import limiter, rate_limit_handler
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.request_size import RequestSizeLimitMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("projectscope")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting ProjectScope AI v{settings.APP_VERSION}...")
    logger.info(f"Environment: {settings.APP_ENV}")
    init_db()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="ProjectScope AI",
    version=settings.APP_VERSION,
    description="AI-powered software requirement analysis and project scoping engine.",
    lifespan=lifespan,
    redirect_slashes=False,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# ============================================
# 1. RATE LIMITING
# ============================================
if settings.RATE_LIMIT_ENABLED:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)

# ============================================
# 2. SECURITY HEADERS
# ============================================
if settings.ENABLE_SECURITY_HEADERS:
    app.add_middleware(SecurityHeadersMiddleware)

# ============================================
# 3. REQUEST SIZE LIMIT
# ============================================
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_size_mb=settings.MAX_REQUEST_SIZE_MB,
)

# ============================================
# 4. CORS
# ============================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# ============================================
# 5. ROUTES
# ============================================
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(projects_router, prefix="/api/v1", tags=["Projects"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to ProjectScope AI",
        "version": settings.APP_VERSION,
        "env": settings.APP_ENV,
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ProjectScope AI",
        "version": settings.APP_VERSION,
    }