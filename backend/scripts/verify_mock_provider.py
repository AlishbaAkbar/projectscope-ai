"""
Verify MockLLMProvider has model attribute.
Run: python scripts/verify_mock_provider.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ai.providers.mock_provider import MockLLMProvider


def verify():
    print("=" * 60)
    print("🔍 Verifying MockLLMProvider")
    print("=" * 60)
    
    provider = MockLLMProvider()
    
    # Check model attribute
    model = getattr(provider, "model", None)
    if model:
        print(f"✅ model attribute: {model}")
    else:
        print(f"❌ model attribute missing or None!")
        print("   → Add 'self.model = \"mock\"' in MockLLMProvider.__init__")
        return False
    
    # Check provider attribute
    provider_name = getattr(provider, "provider", None)
    if provider_name:
        print(f"✅ provider attribute: {provider_name}")
    else:
        print(f"⚠️  provider attribute missing (not critical)")
    
    print("=" * 60)
    print("✅ MockLLMProvider verified!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)