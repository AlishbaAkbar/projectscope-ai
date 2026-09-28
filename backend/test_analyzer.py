"""
Test the full analyzer with Gemini provider.
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from app.ai.providers.factory import get_provider


async def test():
    print("=" * 70)
    print("TESTING ANALYZER WITH GEMINI")
    print("=" * 70)
    print()
    
    # Get provider
    provider = get_provider()
    print(f"✅ Provider: {type(provider).__name__}")
    print()
    
    # Test description
    description = """
    A comprehensive clinic management system with:
    - Patient portal with secure login
    - Doctor appointment scheduling
    - Electronic health records
    - Video consultation
    - Prescription management with pharmacy integration
    - Billing with Stripe payments
    - Lab reports
    - SMS/email reminders
    - HIPAA-compliant admin dashboard
    """
    
    print("📝 Sending description to Gemini...")
    print()
    
    prompt = f"""Analyze this project and return ONLY valid JSON (no markdown, no explanation):

Project: {description}

Return JSON with these exact keys:
{{
    "project_type": "healthcare",
    "users": ["patient", "doctor", "admin"],
    "requirements": [
        {{"text": "requirement text", "category": "functional", "confidence": 0.95}}
    ],
    "features": [
        {{"name": "feature_name", "description": "desc", "priority": "high", "complexity": "medium", "confidence": 0.9}}
    ],
    "missing_information": [],
    "assumptions": []
}}

Include 6-8 requirements and 5-7 features."""
    
    result = await provider.generate(prompt)
    
    print("✅ Gemini Response:")
    print()
    print(result[:2000])
    print()
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test())