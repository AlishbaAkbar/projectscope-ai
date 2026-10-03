"""
Debug: Check why features show None
"""

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.schemas import RawAnalysisResponse


async def debug():
    print("=" * 60)
    print("🔍 Debug Feature Names")
    print("=" * 60)
    
    provider = MockLLMProvider()
    result = await provider.generate(
        "Clinic management system with patient portal, appointments, "
        "video consultation, prescriptions, billing, and HIPAA compliance."
    )
    
    print("\n📝 Raw LLM Output (first 1000 chars):")
    print(result[:1000])
    print()
    
    # Parse JSON
    parsed = json.loads(result)
    print("📊 Parsed Features (raw):")
    for i, f in enumerate(parsed.get("features", [])[:5], 1):
        print(f"   {i}. name={f.get('name')!r} | keys={list(f.keys())}")
    print()
    
    # Validate with Pydantic
    validated = RawAnalysisResponse.model_validate(parsed)
    print("✅ Validated Features:")
    for i, f in enumerate(validated.features[:5], 1):
        print(f"   {i}. name={f.name!r} | priority={f.priority}")
    print()


if __name__ == "__main__":
    asyncio.run(debug())