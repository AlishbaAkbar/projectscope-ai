from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.session import Base


class Organization(Base):
    __tablename__ = "organizations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    plan = Column(String(50), default="free")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # ✅ Relationship to projects
    projects = relationship("Project", back_populates="organization", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True, default=1)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    type = Column(String(50))
    status = Column(String(50), default="draft")
    # ✅ NEW columns for frontend
    platform = Column(String(50), default="Web")
    industry = Column(String(100), nullable=True)
    budget = Column(Float, nullable=True)
    timeline = Column(String(50), nullable=True)
    target_users = Column(JSON, default=[])
    constraints = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # ✅ Relationship back to organization
    organization = relationship("Organization", back_populates="projects")
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")


class Requirement(Base):
    __tablename__ = "requirements"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    category = Column(String(50), default="general")
    text = Column(Text, nullable=False)
    source = Column(String(50), default="user_input")
    confidence = Column(Float, default=0.8)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    project = relationship("Project", back_populates="requirements")


class MissingInformation(Base):
    __tablename__ = "missing_information"
    __table_args__ = {'extend_existing': True}
    
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
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    text = Column(Text, nullable=False)
    category = Column(String(50))
    validated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())