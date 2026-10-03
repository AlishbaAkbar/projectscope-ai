"""
LLM Request Logger
Persists metadata for every LLM call to the database.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.llm_request import LLMRequest


class LLMLogger:
    """Logs LLM requests for audit and reproducibility"""
    
    @staticmethod
    def log(
        db: Session,
        provider: str,
        model: str,
        project_id: Optional[int] = None,
        model_version: Optional[str] = None,
        prompt_tokens: Optional[int] = None,
        response_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        latency_ms: int = 0,
        retry_count: int = 0,
        status: str = "success",
        error_message: Optional[str] = None,
        fallback_used: bool = False,
        prompt_preview: Optional[str] = None,
        response_preview: Optional[str] = None,
    ):
        """Create an LLM request log entry"""
        
        # ✅ Safe defaults to prevent NOT NULL errors
        provider = provider or "unknown"
        model = model or "unknown"
        
        try:
            log_entry = LLMRequest(
                project_id=project_id,
                provider=provider,
                model=model,
                model_version=model_version,
                prompt_tokens=prompt_tokens,
                response_tokens=response_tokens,
                total_tokens=total_tokens,
                latency_ms=latency_ms,
                retry_count=retry_count,
                status=status,
                error_message=error_message,
                fallback_used=fallback_used,
                prompt_preview=(prompt_preview or "")[:500] if prompt_preview else None,
                response_preview=(response_preview or "")[:500] if response_preview else None,
            )
            db.add(log_entry)
            db.commit()
        except Exception as e:
            # Never crash the request due to logging failure
            print(f"⚠️ LLM log failed: {e}")
            try:
                db.rollback()
            except Exception:
                pass