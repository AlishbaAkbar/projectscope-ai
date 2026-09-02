from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.api.routes.projects import router as projects_router
from app.database.session import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("projectscope")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("Starting ProjectScope AI in development mode...")
    init_db()
    yield
    logger.info("Shutting down ProjectScope AI...")


app = FastAPI(
    title="ProjectScope AI",
    version="0.1.0",
    description="AI-powered software requirement analysis and project scoping engine.",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects_router, prefix="/api/v1", tags=["Projects"])


@app.get("/")
async def root():
    return {"message": "Welcome to ProjectScope AI", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ProjectScope AI"}