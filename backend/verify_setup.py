"""
Full verification of ProjectScope AI setup.
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


async def verify_all():
    verification_ok = True
    print("=" * 70)
    print("🔍 PROJECTSCOPE AI SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    # 1. Environment
    print("1️⃣ Environment Variables:")
    print(f"   AI_PROVIDER:     {os.getenv('AI_PROVIDER')}")
    print(f"   AI_MODEL:        {os.getenv('AI_MODEL')}")
    print(f"   API_KEY:         {'configured' if os.getenv('AI_PROVIDER_API_KEY') else 'not configured'}")
    print(f"   DATABASE_URL:    {os.getenv('DATABASE_URL', 'sqlite:///./projectscope.db')}")
    print()
    
    # 2. Provider
    print("2️⃣ AI Provider:")
    try:
        from app.ai.providers.factory import get_provider
        provider = get_provider()
        print(f"   ✅ {type(provider).__name__}")
    except Exception as e:
        print(f"   ❌ {e}")
        return False
    print()
    
    # 3. Gemini call
    print("3️⃣ Gemini API Test:")
    try:
        result = await provider.generate("Reply with exactly: OK")
        print(f"   ✅ Response: {result.strip()[:50]}")
    except Exception as e:
        print(f"   ❌ {e}")
        verification_ok = False
    print()
    
    # 4. Database
    print("4️⃣ Database:")
    try:
        from app.database.session import SessionLocal
        from app.models.project import Project, Organization
        from app.models.user import User
        
        db = SessionLocal()
        print(f"   ✅ Connected")
        print(f"   Organizations: {db.query(Organization).count()}")
        print(f"   Users:         {db.query(User).count()}")
        print(f"   Projects:      {db.query(Project).count()}")
        db.close()
    except Exception as e:
        print(f"   ❌ {e}")
    print()
    
    # 5. ML Model
    print("5️⃣ ML Model:")
    try:
        from app.ml.predictor import MLPredictor
        p = MLPredictor()
        p.load()
        print(f"   ✅ Model loaded: {p.model_name}")
    except Exception as e:
        print(f"   ⚠️  {e}")
    print()
    
    # 6. RAG
    print("6️⃣ RAG System:")
    try:
        from app.rag.retriever import Retriever
        r = Retriever()
        stats = r.get_knowledge_base_stats()
        print(f"   ✅ {stats.get('total_documents', 0)} documents loaded")
    except Exception as e:
        print(f"   ⚠️  {e}")
    print()
    
    print("=" * 70)
    print("✅ VERIFICATION COMPLETE" if verification_ok else "❌ VERIFICATION COMPLETED WITH FAILURES")
    print("=" * 70)
    return verification_ok


if __name__ == "__main__":
    if not asyncio.run(verify_all()):
        raise SystemExit(1)
    