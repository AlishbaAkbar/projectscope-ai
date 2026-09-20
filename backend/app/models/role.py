from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    hourly_rate = Column(Float, nullable=False, default=50.0)
    skill_metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ Must have this — matches Task.role back_populates
    tasks = relationship("Task", back_populates="role")