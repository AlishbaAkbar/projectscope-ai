"""
List all available Gemini models for your API key.
Run: python list_models.py
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configure
api_key = os.getenv("AI_PROVIDER_API_KEY")
if not api_key:
    print("❌ AI_PROVIDER_API_KEY not set in .env")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 70)
print("🔍 AVAILABLE GEMINI MODELS FOR YOUR API KEY")
print("=" * 70)
print()

try:
    models = list(genai.list_models())
    working_models = []
    
    for m in models:
        # Check if model supports generateContent
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name.replace("models/", "")
            print(f"✅ {model_name}")
            print(f"   Display: {m.display_name}")
            print(f"   Description: {m.description[:80]}")
            print()
            working_models.append(model_name)
    
    print("=" * 70)
    print(f"📊 Total: {len(working_models)} models support generateContent")
    print("=" * 70)
    print()
    print("🔧 RECOMMENDED MODEL FOR YOUR .env:")
    print()
    
    # Pick the best recommendation
    if "gemini-3.8-flash" in working_models:
        print("   AI_MODEL=gemini-3.8-flash")
    elif "gemini-2.5-flash-lite" in working_models:
        print("   AI_MODEL=gemini-2.5-flash-lite")
    elif "gemini-flash-latest" in working_models:
        print("   AI_MODEL=gemini-flash-latest")
    elif working_models:
        print(f"   AI_MODEL={working_models[0]}")
    else:
        print("   ❌ No working models found!")
    
    print()
    
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print()
    print("Common causes:")
    print("  - API key invalid or expired")
    print("  - Gemini API not enabled for this key")
    print("  - Network/firewall issue")