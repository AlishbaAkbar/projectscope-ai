"""
Train ML model directly from the GitHub dataset (100 projects).
Bypasses the DB → dataset flow.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from pathlib import Path

from app.ml.preprocessing import MLPreprocessor
from app.ml.trainer import MLTrainer


def main():
    print("=" * 70)
    print("🧠 Training ML model from CSV dataset")
    print("=" * 70)
    
    # 1. Load dataset
    dataset_path = Path("ml/data/dataset.csv")
    if not dataset_path.exists():
        print(f"❌ Dataset not found at {dataset_path}")
        return
    
    df = pd.read_csv(dataset_path)
    print(f"✅ Loaded dataset: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    
    # 2. Column mapping
    column_map = {
        "Project_ID": "project_id",
        "Project_Type": "project_type",
        "Platform": "platform",
        "Number_of_Features": "num_features",
        "Number_of_Tasks": "num_tasks",
        "Number_of_Team_Roles": "num_roles",
        "Total_Combined_Feature_Complexity": "complexity_sum",
        "Average_Feature_Complexity": "avg_complexity",
        "Maximum_Feature_Complexity": "max_complexity",
        "Payment_Integration": "has_payment",
        "Authentication": "has_auth",
        "Admin_Panel": "has_admin",
        "Mobile_Application": "has_mobile",
        "Real_Time_Features": "has_realtime",
        "AI_ML_Features": "has_ai_ml",
        "Number_of_External_Integrations": "num_integrations",
        "Number_of_Requirements": "num_requirements",
        "Security_Level_1_5": "security_level",
        "Database_Complexity_1_5": "database_complexity",
        "Actual_Team_Size": "team_size",
        "Team_Seniority_1_5": "team_seniority",
        "Actual_Hours_Spent": "target",
    }
    
    df = df.rename(columns=column_map)
    
    # 3. Convert Yes/No to 1/0
    binary_cols = ["has_payment", "has_auth", "has_admin", "has_mobile", "has_realtime", "has_ai_ml"]
    for col in binary_cols:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0}).fillna(0).astype(int)
    
    print(f"\n✅ Converted Yes/No to 1/0")
    
    # 4. Drop non-feature columns
    drop_cols = ["project_id", "project_type", "platform"]
    feature_cols = [c for c in df.columns if c not in drop_cols + ["target"]]
    
    print(f"\n📊 Features used ({len(feature_cols)}):")
    for col in feature_cols:
        print(f"   - {col}")
    
    # 5. Prepare X and y
    X = df[feature_cols].fillna(0)
    y = df["target"].dropna()
    
    # Align index
    X = X.loc[y.index]
    
    print(f"\n📈 Target stats:")
    print(f"   Mean:   {y.mean():.1f} hours")
    print(f"   Median: {y.median():.1f} hours")
    print(f"   Min:    {y.min():.1f} hours")
    print(f"   Max:    {y.max():.1f} hours")
    print(f"   Std:    {y.std():.1f} hours")
    
    # 6. Preprocess
    print("\n🔄 Preprocessing data...")
    preprocessor = MLPreprocessor()
    
    # Custom preprocessing (fit scaler on all data)
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save preprocessor
    import joblib
    os.makedirs("ml/models", exist_ok=True)
    joblib.dump({
        "scaler": scaler,
        "feature_columns": feature_cols,
        "is_fitted": True,
    }, "ml/models/preprocessor.pkl")
    print("✅ Preprocessor saved")
    
    print(f"\n✅ Training set: {X_train.shape[0]} samples")
    print(f"✅ Test set:     {X_test.shape[0]} samples")
    
    # 7. Train models
    print("\n🔄 Training models...")
    trainer = MLTrainer()
    results = trainer.train_models(X_train_scaled, y_train.values, X_test_scaled, y_test.values)
    
    # 8. Show results
    print("\n📊 Model Results:")
    print("-" * 60)
    for name, metrics in results.items():
        print(f"{name:25} MAE: {metrics['mae']:>7.2f}h  RMSE: {metrics['rmse']:>7.2f}h  R²: {metrics['r2']:>6.4f}")
    
    # 9. Save best model
    trainer.save_model()
    print(f"\n🏆 Best model: {trainer.best_model_name}")
    print(f"✅ Model saved to ml/models/best_model.pkl")
    
    print("\n" + "=" * 70)
    print("✅ Training complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()