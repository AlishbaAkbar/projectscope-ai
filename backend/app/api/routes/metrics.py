"""
Phase 26: Metrics & Health Endpoints
"""

from fastapi import APIRouter, Depends, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import os

from app.database.session import get_db, engine
from app.models.project import Project, Organization
from app.models.user import User
from app.core.config import settings

router = APIRouter()


# ============================================
# PROMETHEUS METRICS
# ============================================

@router.get("/metrics", response_class=PlainTextResponse)
async def prometheus_metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# ============================================
# HEALTH CHECKS
# ============================================

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check.
    Returns overall status + component statuses.
    """
    checks = {}
    overall_healthy = True
    
    # 1. Database
    try:
        start = time.time()
        db.execute(text("SELECT 1"))  # ✅ Fixed
        db_latency = int((time.time() - start) * 1000)
        checks["database"] = {
            "status": "healthy",
            "latency_ms": db_latency,
        }
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}
        overall_healthy = False
    
    # 2. System resources
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        checks["system"] = {
            "status": "healthy",
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_mb": memory.available // (1024 * 1024),
            "disk_percent": disk.percent,
        }
        
        # Warn if resources are high
        if cpu_percent > 90 or memory.percent > 90:
            checks["system"]["status"] = "warning"
    except Exception as e:
        checks["system"] = {"status": "unknown", "error": str(e)}
    
    # 3. Configuration
    checks["config"] = {
        "status": "healthy",
        "env": settings.APP_ENV,
        "ai_provider": settings.AI_PROVIDER,
        "ai_model": settings.AI_MODEL,
        "debug": settings.DEBUG,
    }
    
    return {
        "status": "healthy" if overall_healthy else "unhealthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION,
        "checks": checks,
    }


@router.get("/health/live")
async def liveness_probe():
    """Kubernetes liveness probe — is the process running?"""
    return {"status": "alive"}


@router.get("/health/ready")
async def readiness_probe(db: Session = Depends(get_db)):
    """Kubernetes readiness probe — can we serve traffic?"""
    try:
        
        db.execute(text("SELECT 1"))
        return {"status": "ready", "version": settings.APP_VERSION}
    except Exception as e:
        return Response(
            content=f'{{"status":"not_ready","error":"{e}"}}',
            status_code=503,
            media_type="application/json",
        )


@router.get("/health/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """Detailed health with business metrics"""
    try:
        # Count entities
        org_count = db.query(Organization).count()
        user_count = db.query(User).count()
        project_count = db.query(Project).count()
        
        # Latest LLM request
        from app.models.llm_request import LLMRequest
        latest_llm = db.query(LLMRequest).order_by(LLMRequest.id.desc()).first()
        
        return {
            "status": "healthy",
            "counts": {
                "organizations": org_count,
                "users": user_count,
                "projects": project_count,
            },
            "ai": {
                "provider": settings.AI_PROVIDER,
                "model": settings.AI_MODEL,
                "last_call": {
                    "status": latest_llm.status if latest_llm else None,
                    "latency_ms": latest_llm.latency_ms if latest_llm else None,
                    "fallback_used": latest_llm.fallback_used if latest_llm else None,
                } if latest_llm else None,
            },
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ============================================
# STATS
# ============================================

@router.get("/stats")
async def application_stats(db: Session = Depends(get_db)):
    """Application statistics (business metrics)"""
    try:
        from app.models.llm_request import LLMRequest
        from sqlalchemy import func
        
        org_count = db.query(Organization).count()
        user_count = db.query(User).count()
        project_count = db.query(Project).count()
        llm_count = db.query(LLMRequest).count()
        
        # Safe queries with getattr fallback
        try:
            llm_success = db.query(LLMRequest).filter(LLMRequest.status == "success").count()
            llm_fallback = db.query(LLMRequest).filter(LLMRequest.fallback_used == True).count()
            avg_latency = db.query(func.avg(LLMRequest.latency_ms)).scalar() or 0
        except Exception as e:
            print(f"⚠️ LLM stats error: {e}")
            llm_success = 0
            llm_fallback = 0
            avg_latency = 0
        
        return {
            "organizations": org_count,
            "users": user_count,
            "projects": project_count,
            "llm_requests": {
                "total": llm_count,
                "success": llm_success,
                "fallbacks": llm_fallback,
                "success_rate": round(llm_success / llm_count * 100, 2) if llm_count else 0,
                "avg_latency_ms": round(float(avg_latency), 2),
            },
        }
    except Exception as e:
        return {"error": str(e)}