"""
Phase 23: Audit Log Model
Tracks sensitive operations for compliance & forensics
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, JSON
)
from sqlalchemy.sql import func
from app.database.session import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Who
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True, index=True)
    
    # What
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=True)  # "project", "user", "auth"
    resource_id = Column(Integer, nullable=True)
    
    # Details
    details = Column(JSON, default={})
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Result
    status = Column(String(20), default="success")  # success, failure, denied
    error_message = Column(Text, nullable=True)
    
    # When
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)