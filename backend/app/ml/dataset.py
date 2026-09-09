"""
Phase 13: ML Dataset
Collects and manages project data for ML training
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import json
import pandas as pd
import numpy as np

from app.models.project import Project, Requirement
from app.models.feature import Feature  # ✅ FIXED: Import from feature.py
from app.models.task import Task        # ✅ FIXED: Import from task.py
from app.models.role import Role
from app.services.role_service import RoleService


class MLDataset:
    """
    Manages ML dataset creation from project data
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.role_service = RoleService(db)
    
    def create_dataset(self, project_ids: List[int] = None) -> pd.DataFrame:
        """
        Create ML dataset from projects
        
        Args:
            project_ids: List of project IDs to include (None = all)
            
        Returns:
            DataFrame with features and target
        """
        # Get projects
        query = self.db.query(Project)
        if project_ids:
            query = query.filter(Project.id.in_(project_ids))
        projects = query.all()
        
        if not projects:
            return pd.DataFrame()
        
        data = []
        for project in projects:
            row = self._extract_project_features(project)
            if row:
                data.append(row)
        
        return pd.DataFrame(data)
    
    def _extract_project_features(self, project: Project) -> Optional[Dict]:
        """Extract features from a single project"""
        try:
            # Get related data
            features = self.db.query(Feature).filter(Feature.project_id == project.id).all()
            tasks = self.db.query(Task).filter(Task.project_id == project.id).all()
            
            if not tasks:
                return None
            
            # Basic features
            row = {
                "project_id": project.id,
                "project_type": project.type or "unknown",
                "num_features": len(features),
                "num_tasks": len(tasks),
                "total_estimated_hours": sum(t.estimated_hours for t in tasks),
                "actual_hours": self._get_actual_hours(project.id),
                "complexity_sum": sum(f.complexity for f in features),
                "avg_complexity": sum(f.complexity for f in features) / len(features) if features else 0,
                "max_complexity": max([f.complexity for f in features]) if features else 0,
                "num_payment": sum(1 for f in features if f.canonical_name == "PAYMENT"),
                "num_auth": sum(1 for f in features if f.canonical_name == "AUTHENTICATION"),
                "num_admin": sum(1 for f in features if f.canonical_name == "ADMIN_PANEL"),
                "num_mobile": sum(1 for f in features if f.canonical_name == "MOBILE_APP"),
                "num_roles": len(set(t.role_id for t in tasks)),
                "has_payment": 1 if any(f.canonical_name == "PAYMENT" for f in features) else 0,
                "has_auth": 1 if any(f.canonical_name == "AUTHENTICATION" for f in features) else 0,
                "has_admin": 1 if any(f.canonical_name == "ADMIN_PANEL" for f in features) else 0,
                "has_mobile": 1 if any(f.canonical_name == "MOBILE_APP" for f in features) else 0,
            }
            
            # Role-specific features
            role_hours = {}
            for task in tasks:
                role_name = self.role_service.format_role_for_task(task.role_id)["name"]
                role_hours[role_name] = role_hours.get(role_name, 0) + task.estimated_hours
            
            # Add role hours as features
            for role_name, hours in role_hours.items():
                col_name = f"hours_{role_name.lower().replace(' ', '_')}"
                row[col_name] = hours
            
            # Add target (actual hours if available, else estimated)
            if row["actual_hours"] and row["actual_hours"] > 0:
                row["target"] = row["actual_hours"]
            else:
                row["target"] = row["total_estimated_hours"]
            
            return row
            
        except Exception as e:
            print(f"Error extracting features for project {project.id}: {e}")
            return None
    
    def _get_actual_hours(self, project_id: int) -> Optional[float]:
        """Get actual hours from feedback or tasks"""
        # Try to get from feedback table
        # For now, use estimated hours as fallback
        return None
    
    def get_feature_columns(self) -> List[str]:
        """Get list of feature column names"""
        return [
            "num_features",
            "num_tasks",
            "complexity_sum",
            "avg_complexity",
            "max_complexity",
            "num_roles",
            "has_payment",
            "has_auth",
            "has_admin",
            "has_mobile",
            "num_payment",
            "num_auth",
            "num_admin",
            "num_mobile",
        ]
    
    def save_dataset(self, df: pd.DataFrame, filepath: str = "ml/data/dataset.csv"):
        """Save dataset to CSV"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        print(f"✅ Dataset saved to {filepath}")
        return filepath
    
    def load_dataset(self, filepath: str = "ml/data/dataset.csv") -> pd.DataFrame:
        """Load dataset from CSV"""
        return pd.read_csv(filepath)
    
    def get_dataset_stats(self, df: pd.DataFrame) -> Dict:
        """Get statistics about the dataset"""
        if df.empty:
            return {"error": "Dataset is empty"}
        
        return {
            "total_samples": len(df),
            "features": len(df.columns) - 2,  # Exclude project_id and target
            "target_mean": df["target"].mean() if "target" in df.columns else 0,
            "target_std": df["target"].std() if "target" in df.columns else 0,
            "target_min": df["target"].min() if "target" in df.columns else 0,
            "target_max": df["target"].max() if "target" in df.columns else 0,
            "feature_columns": [c for c in df.columns if c not in ["project_id", "target"]]
        }