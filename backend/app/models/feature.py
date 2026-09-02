from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Feature(Base):
    __tablename__ = "features"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    canonical_name = Column(String(100), nullable=False)
    description = Column(String(500))
    priority = Column(String(20), default="MEDIUM")
    complexity = Column(Integer, default=3)
    confidence = Column(Float, default=0.8)
    dependencies = Column(JSON, default=[])
    source_requirement_ids = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())