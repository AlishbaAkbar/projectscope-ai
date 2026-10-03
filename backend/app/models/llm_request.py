from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.database.session import Base


class LLMRequest(Base):
    __tablename__ = "llm_requests"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True, nullable=True)

    provider = Column(String(50), nullable=False)
    model = Column(String(100), nullable=True, default="unknown")
    model_version = Column(String(50), nullable=True)

    prompt_tokens = Column(Integer, nullable=True)
    response_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)

    latency_ms = Column(Integer, default=0)
    retry_count = Column(Integer, default=0)

    status = Column(String(20), default="success")
    error_message = Column(Text, nullable=True)
    fallback_used = Column(Boolean, default=False)  # ✅ MUST HAVE THIS

    prompt_preview = Column(Text, nullable=True)
    response_preview = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
