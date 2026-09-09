"""
Phase 13-16: ML Training
Trains and evaluates ML models
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
from datetime import datetime


class MLTrainer:
    """
    Trains and evaluates ML models
    """
    
    def __init__(self):
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
    
    def train_models(self, X_train: np.ndarray, y_train: np.ndarray,
                     X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Train multiple models and compare
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            
        Returns:
            Dict with model results
        """
        # Check if we have enough data
        if len(X_train) < 2:
            print("⚠️ Not enough training data. Using simple baseline model.")
            return self._train_baseline(X_train, y_train, X_test, y_test)
        
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(
                n_estimators=100, max_depth=10, random_state=42
            ),
            "Gradient Boosting": GradientBoostingRegressor(
                n_estimators=100, max_depth=5, random_state=42
            ),
            "XGBoost": XGBRegressor(
                n_estimators=100, max_depth=5, random_state=42
            )
        }
        
        results = {}
        
        for name, model in models.items():
            try:
                # Train
                model.fit(X_train, y_train)
                
                # Predict
                y_pred = model.predict(X_test)
                
                # Evaluate
                mae = mean_absolute_error(y_test, y_pred)
                rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                r2 = r2_score(y_test, y_pred)
                
                results[name] = {
                    "model": model,
                    "mae": round(mae, 2),
                    "rmse": round(rmse, 2),
                    "r2": round(r2, 4) if not np.isnan(r2) else 0.0,
                    "predictions": y_pred.tolist(),
                    "actual": y_test.tolist()
                }
                
                self.models[name] = model
            except Exception as e:
                print(f"⚠️ {name} failed: {e}")
        
        self.results = results
        self._select_best_model()
        
        return results
    
    def _train_baseline(self, X_train: np.ndarray, y_train: np.ndarray,
                        X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """Train a simple baseline model when data is limited"""
        
        # Use mean of training data as prediction
        mean_pred = np.mean(y_train) if len(y_train) > 0 else 0
        
        # Create predictions
        y_pred = np.full(len(y_test), mean_pred)
        
        # Calculate metrics
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Simple model (just for saving)
        from sklearn.dummy import DummyRegressor
        model = DummyRegressor(strategy="mean")
        model.fit(X_train, y_train)
        
        results = {
            "Baseline (Mean)": {
                "model": model,
                "mae": round(mae, 2),
                "rmse": round(rmse, 2),
                "r2": 0.0,
                "predictions": y_pred.tolist(),
                "actual": y_test.tolist()
            }
        }
        
        self.models = results
        self.results = results
        self.best_model = model
        self.best_model_name = "Baseline (Mean)"
        
        print(f"✅ Baseline model trained (MAE: {mae:.2f} hours)")
        
        return results
    
    def _select_best_model(self):
        """Select best model based on R² and MAE"""
        if not self.results:
            return
        
        best = None
        best_score = -float('inf')
        best_name = None
        
        for name, result in self.results.items():
            # Combine R² and MAE for scoring
            r2 = result.get("r2", 0)
            mae = result.get("mae", 999)
            score = r2 - (mae / 1000)
            if score > best_score:
                best_score = score
                best = result["model"]
                best_name = name
        
        self.best_model = best
        self.best_model_name = best_name
        
        if best_name:
            print(f"🏆 Best model: {best_name}")
            print(f"   R²: {self.results[best_name].get('r2', 0)}")
            print(f"   MAE: {self.results[best_name].get('mae', 0)} hours")
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using best model"""
        if self.best_model is None:
            raise ValueError("No model trained yet")
        return self.best_model.predict(X)
    
    def save_model(self, filepath: str = "ml/models/best_model.pkl"):
        """Save best model to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if self.best_model is None:
            # Save a dummy model if no best model
            from sklearn.dummy import DummyRegressor
            self.best_model = DummyRegressor(strategy="mean")
            self.best_model_name = "Baseline (Dummy)"
            self.results = {
                "Baseline (Dummy)": {
                    "mae": 0,
                    "rmse": 0,
                    "r2": 0
                }
            }
        
        joblib.dump({
            "model": self.best_model,
            "model_name": self.best_model_name,
            "results": self.results,
            "training_date": datetime.now().isoformat()
        }, filepath)
        print(f"✅ Best model saved to {filepath}")
    
    def load_model(self, filepath: str = "ml/models/best_model.pkl"):
        """Load best model from file"""
        data = joblib.load(filepath)
        self.best_model = data["model"]
        self.best_model_name = data["model_name"]
        self.results = data.get("results", {})
        print(f"✅ Best model loaded from {filepath}")
        print(f"   Model: {self.best_model_name}")
    
    def get_model_summary(self) -> Dict:
        """Get summary of all models"""
        if not self.results:
            return {"error": "No models trained"}
        
        summary = {}
        for name, result in self.results.items():
            summary[name] = {
                "mae": result.get("mae", 0),
                "rmse": result.get("rmse", 0),
                "r2": result.get("r2", 0)
            }
        
        return {
            "models": summary,
            "best_model": self.best_model_name,
            "best_metrics": self.results.get(self.best_model_name, {})
        }