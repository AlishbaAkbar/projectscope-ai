import httpx
import pytest

import app.ai.providers.gemini_provider as gemini_module
from app.ai.providers.gemini_provider import GeminiProvider
from app.core.config import settings
from app.utils.error_handlers import LLMProviderException


@pytest.mark.asyncio
async def test_gemini_retries_transient_statuses_with_bounded_backoff(monkeypatch):
    monkeypatch.setattr(settings, "AI_MAX_RETRIES", 3)
    provider = GeminiProvider(api_key="test-key")
    attempts = 0
    delays = []

    async def call_gemini(prompt, system_prompt=None):
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            code = 429 if attempts == 1 else 503
            raise LLMProviderException(f"API returned status {code}", provider="gemini")
        return "ok"

    async def sleep(delay):
        delays.append(delay)

    monkeypatch.setattr(provider, "_call_gemini", call_gemini)
    monkeypatch.setattr(gemini_module.asyncio, "sleep", sleep)

    assert await provider.generate("test") == "ok"
    assert delays == [1, 2]


@pytest.mark.asyncio
async def test_gemini_retries_timeout_and_truncates_prompt(monkeypatch):
    monkeypatch.setattr(settings, "AI_MAX_RETRIES", 2)
    monkeypatch.setattr(settings, "MAX_PROMPT_LENGTH", 8)
    provider = GeminiProvider(api_key="test-key")
    captured_prompts = []

    async def call_gemini(prompt, system_prompt=None):
        captured_prompts.append(prompt)
        if len(captured_prompts) == 1:
            raise httpx.TimeoutException("request timed out")
        return "ok"

    async def no_wait(_):
        return None

    monkeypatch.setattr(provider, "_call_gemini", call_gemini)
    monkeypatch.setattr(gemini_module.asyncio, "sleep", no_wait)

    assert await provider.generate("long prompt beyond maximum") == "ok"
    assert captured_prompts == ["long pro", "long pro"]


@pytest.mark.asyncio
async def test_gemini_propagates_non_transient_errors(monkeypatch):
    provider = GeminiProvider(api_key="test-key")

    async def unauthorized(prompt, system_prompt=None):
        raise LLMProviderException("API returned status 401", provider="gemini")

    monkeypatch.setattr(provider, "_call_gemini", unauthorized)
    with pytest.raises(LLMProviderException, match="401"):
        await provider.generate("test")
