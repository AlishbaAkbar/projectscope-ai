"""
Script to create ML dataset from existing projects
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal
from app.ml.dataset import MLDataset


def main():
    db = SessionLocal()
    try:
        print("🔄 Creating ML dataset...")
        
        dataset = MLDataset(db)
        df = dataset.create_dataset()
        
        if df.empty:
            print("❌ No data found! Create some projects first.")
            return
        
        print(f"✅ Created dataset with {len(df)} samples")
        print(f"   Features: {len(df.columns) - 2}")
        
        # Show sample
        print("\n📊 Sample data:")
        print(df.head())
        
        # Show statistics
        stats = dataset.get_dataset_stats(df)
        print(f"\n📈 Statistics:")
        print(f"   Total samples: {stats['total_samples']}")
        print(f"   Target mean: {stats['target_mean']:.2f} hours")
        print(f"   Target range: {stats['target_min']:.2f} - {stats['target_max']:.2f} hours")
        
        # Save dataset
        dataset.save_dataset(df)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()