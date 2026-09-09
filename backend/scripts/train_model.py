"""
Script to train ML models
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.ml.dataset import MLDataset
from app.ml.preprocessing import MLPreprocessor
from app.ml.trainer import MLTrainer
from app.database.session import SessionLocal


def main():
    db = SessionLocal()
    try:
        print("🔄 Loading dataset...")
        
        # Load dataset
        dataset = MLDataset(db)
        df = dataset.load_dataset()
        
        if df.empty:
            print("❌ No dataset found! Run create_dataset.py first.")
            return
        
        print(f"✅ Loaded dataset with {len(df)} samples")
        print(f"   Features: {len(df.columns) - 2}")  # Exclude project_id and target
        
        # Check if we have enough data
        if len(df) < 5:
            print("\n⚠️ WARNING: Only {len(df)} samples. Need at least 5 for meaningful ML.")
            print("   Create more projects and run create_dataset.py again.")
            print("   Training a baseline model anyway...")
        else:
            print("\n✅ Good! {len(df)} samples is enough for training.")
        
        # Preprocess
        print("\n🔄 Preprocessing data...")
        preprocessor = MLPreprocessor()
        result = preprocessor.prepare_features(df)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            return
        
        print(f"✅ Training set: {result['train_size']} samples")
        print(f"✅ Test set: {result['test_size']} samples")
        print(f"   Features: {len(result['feature_names'])}")
        
        # Train models
        print("\n🔄 Training models...")
        trainer = MLTrainer()
        results = trainer.train_models(
            result["X_train"],
            result["y_train"],
            result["X_test"],
            result["y_test"]
        )
        
        # Show results
        print("\n📊 Model Results:")
        print("-" * 50)
        for name, metrics in results.items():
            print(f"{name}:")
            print(f"   MAE: {metrics['mae']:.2f} hours")
            print(f"   RMSE: {metrics['rmse']:.2f} hours")
            print(f"   R²: {metrics['r2']:.4f}")
            print()
        
        # Save preprocessor and model
        print("🔄 Saving models...")
        preprocessor.save_preprocessor()
        trainer.save_model()
        
        print("\n✅ Training complete!")
        if trainer.best_model_name:
            print(f"🏆 Best model: {trainer.best_model_name}")
            print(f"   R²: {trainer.results[trainer.best_model_name].get('r2', 0):.4f}")
            print(f"   MAE: {trainer.results[trainer.best_model_name].get('mae', 0):.2f} hours")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()