"""
Reset the llm_requests table to apply new schema.
Run: python scripts/reset_llm_table.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.session import engine
from app.models import Base
from sqlalchemy import text, inspect


def reset_llm_table():
    print("=" * 60)
    print("🔧 Resetting llm_requests table")
    print("=" * 60)
    
    # Step 1: Drop llm_requests table
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS llm_requests"))
            conn.commit()
        print("✅ Dropped old llm_requests table")
    except Exception as e:
        print(f"⚠️  Drop error (may not exist): {e}")
    
    # Step 2: Recreate all tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Recreated all tables")
    except Exception as e:
        print(f"❌ Recreate error: {e}")
        return False
    
    # Step 3: Verify model column is nullable
    try:
        insp = inspect(engine)
        cols = insp.get_columns("llm_requests")
        
        model_col = next((c for c in cols if c["name"] == "model"), None)
        
        if model_col:
            nullable = model_col["nullable"]
            print(f"✅ model column nullable: {nullable}")
            if not nullable:
                print("❌ model column is NOT NULL — fix llm_request.py!")
                return False
        else:
            print("❌ model column not found!")
            return False
    except Exception as e:
        print(f"❌ Verify error: {e}")
        return False
    
    print("=" * 60)
    print("✅ llm_requests table reset complete!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = reset_llm_table()
    sys.exit(0 if success else 1)