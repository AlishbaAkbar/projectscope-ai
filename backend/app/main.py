from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORS

from app.api.routes.auth import router as auth_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.projects import router as projects_router
from app.core.config import settings
from app.core.logging_config import configure_logging, logger
from app.core.rate_limit import limiter, rate_limit_handler
from app.database.session import init_db
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.request_size import RequestSizeLimitMiddleware
from app.middleware.request_tracing import RequestTracingMiddleware
from app.middleware.security_headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info(
        "app_starting",
        version=settings.APP_VERSION,
        env=settings.APP_ENV,
        ai_provider=settings.AI_PROVIDER,
        ai_model=settings.AI_MODEL,
    )
    init_db()
    logger.info("app_started")
    yield
    logger.info("app_shutting_down")


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
# MIDDLEWARE (order matters!)
# ============================================

# 1. Request tracing (outermost — logs everything)
app.add_middleware(RequestTracingMiddleware)

# 2. Rate limiting
if settings.RATE_LIMIT_ENABLED:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
    app.add_middleware(SlowAPIMiddleware)

# 3. Security headers
if settings.ENABLE_SECURITY_HEADERS:
    app.add_middleware(SecurityHeadersMiddleware)

# 4. Request size limit
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_size_mb=settings.MAX_REQUEST_SIZE_MB,
)

# 5. CORS
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
# ROUTES
# ============================================

app.include_router(metrics_router, tags=["Observability"])
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
async def simple_health():
    return {"status": "healthy", "service": "ProjectScope AI","version": settings.APP_VERSION,}
