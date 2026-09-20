from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("features.id"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(500))
    estimated_hours = Column(Float, nullable=False)
    min_hours = Column(Float, default=0)
    max_hours = Column(Float, default=0)
    base_hours = Column(Float, default=0)
    complexity_factor = Column(Float, default=1.0)
    priority = Column(String(20), default="MEDIUM")
    dependencies = Column(JSON, default=[])
    confidence = Column(Float, default=0.8)
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ These must match Feature and Role back_populates
    feature = relationship("Feature", back_populates="tasks")
    role = relationship("Role", back_populates="tasks")