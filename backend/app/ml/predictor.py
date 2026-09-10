"""
Phase 17: ML Predictor
Uses trained model for predictions
"""

from typing import Dict, List, Optional
import numpy as np
import pandas as pd
import joblib


class MLPredictor:
    """
    ML prediction service
    """
    
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.is_loaded = False
    
    def load(self, model_path: str = "ml/models/best_model.pkl",
             preprocessor_path: str = "ml/models/preprocessor.pkl"):
        """Load model and preprocessor"""
        # Load model
        data = joblib.load(model_path)
        self.model = data["model"]
        self.model_name = data.get("model_name", "Unknown")
        
        # Load preprocessor
        preprocessor_data = joblib.load(preprocessor_path)
        self.preprocessor = preprocessor_data
        self.feature_columns = preprocessor_data.get("feature_columns", [])
        
        self.is_loaded = True
        print(f"[OK] ML Predictor loaded")
        print(f"   Model: {self.model_name}")
        print(f"   Features: {len(self.feature_columns)}")
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict project effort
        
        Args:
            features: Dictionary of feature values
            
        Returns:
            Dict with prediction and confidence
        """
        if not self.is_loaded:
            raise ValueError("Predictor not loaded")
        
        # Convert features to array
        X = self._prepare_features(features)
        
        # Predict
        prediction = self.model.predict(X)[0]
        
        # Calculate confidence
        confidence = self._calculate_confidence(prediction)
        
        return {
            "predicted_hours": round(float(prediction), 2),
            "confidence": confidence,
            "model_used": self.model_name,
            "features_used": self.feature_columns
        }
    
    def _prepare_features(self, features: Dict) -> np.ndarray:
        """Prepare features for prediction"""
        # Create feature array with correct order
        X = []
        for col in self.feature_columns:
            X.append(features.get(col, 0))
        
        # Scale features
        X_scaled = self.preprocessor["scaler"].transform([X])
        return X_scaled
    
    def _calculate_confidence(self, prediction: float) -> float:
        """Calculate confidence score for prediction"""
        # Basic confidence based on model quality
        # Can be enhanced with prediction intervals
        
        # For now, return moderate confidence
        return 0.75
    
    def predict_from_project(self, project_data: Dict) -> Dict:
        """
        Predict from project data dictionary
        
        Args:
            project_data: Dictionary with project features
            
        Returns:
            Dict with prediction
        """
        # Extract features
        features = {
            "num_features": project_data.get("num_features", 0),
            "num_tasks": project_data.get("num_tasks", 0),
            "complexity_sum": project_data.get("complexity_sum", 0),
            "avg_complexity": project_data.get("avg_complexity", 0),
            "max_complexity": project_data.get("max_complexity", 0),
            "num_roles": project_data.get("num_roles", 0),
            "has_payment": project_data.get("has_payment", 0),
            "has_auth": project_data.get("has_auth", 0),
            "has_admin": project_data.get("has_admin", 0),
            "has_mobile": project_data.get("has_mobile", 0),
            "num_payment": project_data.get("num_payment", 0),
            "num_auth": project_data.get("num_auth", 0),
            "num_admin": project_data.get("num_admin", 0),
            "num_mobile": project_data.get("num_mobile", 0),
        }
        
        return self.predict(features)