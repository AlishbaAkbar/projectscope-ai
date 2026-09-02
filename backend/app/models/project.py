from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    plan = Column(String(50), default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(50))
    status = Column(String(50), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Requirement(Base):
    __tablename__ = "requirements"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(String(50), default="general")
    text = Column(Text, nullable=False)
    source = Column(String(50), default="user_input")
    confidence = Column(Float, default=0.8)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MissingInformation(Base):
    __tablename__ = "missing_information"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    question = Column(Text, nullable=False)
    context = Column(Text)
    priority = Column(String(20), default="HIGH")
    answered = Column(Boolean, default=False)
    answer = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Assumption(Base):
    __tablename__ = "assumptions"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    text = Column(Text, nullable=False)
    category = Column(String(50))
    validated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())