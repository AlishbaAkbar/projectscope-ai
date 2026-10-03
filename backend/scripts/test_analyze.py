"""
Test the analyzer end-to-end.
Run: python scripts/test_analyze.py
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ai.analyzer import RequirementAnalyzer
from app.database.session import SessionLocal


async def test_analyze():
    print("=" * 60)
    print("🧪 Testing Requirement Analyzer")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        analyzer = RequirementAnalyzer(db=db, project_id=None)
        
        result = await analyzer.analyze(
            project_name="Test Clinic",
            description=(
                "A comprehensive clinic management system with patient "
                "portal, appointment scheduling, electronic health records, "
                "video consultation, prescription management, billing with "
                "Stripe payments, and HIPAA-compliant admin dashboard."
            ),
            platform="Web",
        )
        
        print(f"\n✅ Analysis successful!")
        print(f"   Project type: {result.project_type}")
        print(f"   Users: {result.users}")
        print(f"   Requirements: {len(result.requirements)}")
        print(f"   Features: {len(result.features)}")
        print()
        print("Features detected:")
        for f in result.features[:10]:
            print(f"   - {f.name} ({f.priority})")
        
        return True
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    success = asyncio.run(test_analyze())
    sys.exit(0 if success else 1)