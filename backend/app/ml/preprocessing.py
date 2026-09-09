"""
Phase 13: ML Preprocessing
Prepares data for ML training with scaling and encoding
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib


class MLPreprocessor:
    """
    Preprocesses ML data with scaling and encoding
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        self.is_fitted = False
    
    def prepare_features(self, df: pd.DataFrame, 
                         target_col: str = "target",
                         test_size: float = 0.2,
                         random_state: int = 42) -> Dict:
        """
        Prepare features and split data
        
        Args:
            df: Input DataFrame
            target_col: Target column name
            test_size: Test set size
            random_state: Random seed
            
        Returns:
            Dict with X_train, X_test, y_train, y_test
        """
        if df.empty:
            return {"error": "Dataset is empty"}
        
        # Drop non-feature columns
        exclude_cols = ["project_id", "project_type", target_col]
        feature_cols = [c for c in df.columns if c not in exclude_cols]
        self.feature_columns = feature_cols
        
        # Separate features and target
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # Handle missing values
        X = X.fillna(0)
        y = y.fillna(y.mean())
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Fit scaler on training data
        self.scaler.fit(X_train)
        self.is_fitted = True
        
        # Transform data
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return {
            "X_train": X_train_scaled,
            "X_test": X_test_scaled,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": feature_cols,
            "train_size": len(X_train),
            "test_size": len(X_test)
        }
    
    def scale_features(self, X: np.ndarray) -> np.ndarray:
        """Scale features using fitted scaler"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted yet")
        return self.scaler.transform(X)
    
    def save_preprocessor(self, filepath: str = "ml/models/preprocessor.pkl"):
        """Save preprocessor to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            "scaler": self.scaler,
            "feature_columns": self.feature_columns,
            "is_fitted": self.is_fitted
        }, filepath)
        print(f"✅ Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath: str = "ml/models/preprocessor.pkl"):
        """Load preprocessor from file"""
        data = joblib.load(filepath)
        self.scaler = data["scaler"]
        self.feature_columns = data["feature_columns"]
        self.is_fitted = data["is_fitted"]
        print(f"✅ Preprocessor loaded from {filepath}")
    
    def create_preprocessing_pipeline(self) -> Pipeline:
        """Create a complete preprocessing pipeline"""
        return Pipeline([
            ('scaler', StandardScaler())
        ])