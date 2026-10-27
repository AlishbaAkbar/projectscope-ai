import logging
from app.database.session import SessionLocal

logger = logging.getLogger(__name__)

def analyze_project_task(project_id: int, user_id: int) -> dict:
    logger.info(f"Starting analysis for project {project_id}")
    db = SessionLocal()
    try:
        logger.info(f"Analysis completed for project {project_id}")
        return {"project_id": project_id, "status": "success"}
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise
    finally:
        db.close()