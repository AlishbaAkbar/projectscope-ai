"""
AI Provider Factory.
Instantiates the correct LLM provider based on settings or explicit override.
"""

from typing import Optional
from app.ai.providers.base import LLMProvider
from app.ai.providers.mock_provider import MockLLMProvider
from app.ai.providers.gemini_provider import GeminiProvider
from app.ai.providers.openai_provider import OpenAIProvider
from app.utils.config import get_settings


class LLMProviderFactory:
    """Factory to instantiate the appropriate LLM provider based on settings or override"""

    @staticmethod
    def get_provider(
        provider_name: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> LLMProvider:
        settings = get_settings()
        name = (provider_name or settings.AI_PROVIDER or "mock").lower().strip()
        key = api_key if api_key is not None else settings.AI_PROVIDER_API_KEY
        chosen_model = model or settings.AI_MODEL

        if name == "gemini":
            return GeminiProvider(
                api_key=key or "",
                model=chosen_model or "gemini-3.8-flash",
                timeout=settings.AI_TIMEOUT_SECONDS,
            )
        elif name in ["openai", "chatgpt"]:
            return OpenAIProvider(
                api_key=key or "",
                model=chosen_model or "gpt-4o-mini",
                timeout=settings.AI_TIMEOUT_SECONDS,
            )
        elif name in ["mock", "test", "local"]:
            return MockLLMProvider()
        else:
            # Fallback to mock if unknown provider
            return MockLLMProvider()


# ============================================
# STANDALONE FUNCTION WRAPPER
# ============================================

def get_provider(
    provider_name: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> LLMProvider:
    """
    Standalone convenience function — wraps LLMProviderFactory.get_provider().
    """
    return LLMProviderFactory.get_provider(
        provider_name=provider_name,
        api_key=api_key,
        model=model,
    )


# Aliases for convenience
create_provider = get_provider
get_llm_provider = get_provider


# ============================================
# EXPORTS
# ============================================

__all__ = [
    "LLMProviderFactory",
    "get_provider",
    "create_provider",
    "get_llm_provider",
]