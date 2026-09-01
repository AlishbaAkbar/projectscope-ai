import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.database.session import Base


def utcnow():
    return datetime.now(timezone.utc)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_type = Column(String(100), nullable=True)
    platform = Column(String(50), nullable=False, default="Web")
    target_users_json = Column(Text, nullable=True, default="[]")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    # Relationships
    requirements = relationship("Requirement", back_populates="project", cascade="all, delete-orphan")
    features = relationship("Feature", back_populates="project", cascade="all, delete-orphan")
    missing_information = relationship("MissingInformation", back_populates="project", cascade="all, delete-orphan")
    assumptions = relationship("Assumption", back_populates="project", cascade="all, delete-orphan")

    @property
    def target_users(self) -> List[str]:
        if not self.target_users_json:
            return []
        try:
            return json.loads(self.target_users_json)
        except Exception:
            return []

    @target_users.setter
    def target_users(self, value: List[str]):
        self.target_users_json = json.dumps(value if value is not None else [])


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(50), nullable=False, default="functional")  # functional, non_functional, technical, business
    text = Column(Text, nullable=False)
    source = Column(String(50), nullable=False, default="llm_analysis")
    confidence = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    project = relationship("Project", back_populates="requirements")


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    normalized_key = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    priority = Column(String(50), nullable=False, default="medium")  # low, medium, high, critical
    complexity = Column(String(50), nullable=False, default="medium")  # low, medium, high
    confidence = Column(Float, nullable=False, default=1.0)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    project = relationship("Project", back_populates="features")
    tasks = relationship("Task", back_populates="feature", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feature_id = Column(Integer, ForeignKey("features.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, default="Backend")  # Frontend, Backend, Database, QA, Integration
    estimated_hours = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    feature = relationship("Feature", back_populates="tasks")


class MissingInformation(Base):
    __tablename__ = "missing_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    question_or_detail = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    project = relationship("Project", back_populates="missing_information")


class Assumption(Base):
    __tablename__ = "assumptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    assumption_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    project = relationship("Project", back_populates="assumptions")
