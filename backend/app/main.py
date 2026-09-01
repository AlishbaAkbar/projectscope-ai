import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import get_settings
from app.utils.error_handlers import register_exception_handlers
from app.database.session import init_db
from app.api.routes.projects import router as projects_router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("projectscope")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    init_db()
    logger.info("Database initialized successfully.")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered software requirement analysis and project scoping engine.",
    version="0.1.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# Register Exception Handlers
register_exception_handlers(app)

# Register CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(projects_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "status": "online",
        "docs_url": "/docs",
        "api_v1": f"{settings.API_V1_PREFIX}/projects"
    }


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "ai_provider": settings.AI_PROVIDER,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
