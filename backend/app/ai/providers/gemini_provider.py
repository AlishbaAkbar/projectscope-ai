import asyncio
import logging
from typing import Optional
import httpx
from app.ai.providers.base import LLMProvider
from app.core.config import settings
from app.utils.error_handlers import LLMProviderException

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini AI Provider implementation via REST API"""

    def __init__(self, api_key: str, model: Optional[str] = None, timeout: Optional[float] = None):
        if not api_key:
            raise LLMProviderException("Gemini API key is required but was not provided.", provider="gemini")
        self.api_key = api_key
        self.model = model or settings.AI_MODEL
        self.timeout = min(timeout, settings.AI_TIMEOUT_SECONDS) if timeout else settings.AI_TIMEOUT_SECONDS
        self.max_retries = max(0, settings.AI_MAX_RETRIES)
        self.max_prompt_length = settings.MAX_PROMPT_LENGTH
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.generate(prompt, system_prompt)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        bounded_prompt = prompt[:self.max_prompt_length]
        for attempt in range(self.max_retries + 1):
            try:
                return await self._call_gemini(bounded_prompt, system_prompt)
            except (LLMProviderException, httpx.TimeoutException) as exc:
                message = str(exc).lower()
                transient = (
                    isinstance(exc, httpx.TimeoutException)
                    or any(code in message for code in ("429", "503", "unavailable", "timed out", "timeout"))
                )
                if not transient or attempt >= self.max_retries:
                    raise
                delay = min(2 ** attempt, 8)
                logger.warning(
                    "Transient Gemini failure; retrying in %s seconds (attempt %s/%s): %s",
                    delay,
                    attempt + 2,
                    self.max_retries + 1,
                    exc,
                )
                await asyncio.sleep(delay)

        raise LLMProviderException("Gemini request failed after retries.", provider="gemini")

    async def _call_gemini(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        url = f"{self.base_url}?key={self.api_key}"

        contents = [{"parts": [{"text": prompt}]}]
        payload = {
            "contents": contents,
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2,
            }
        }

        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)

                if response.status_code != 200:
                    error_msg = f"Gemini API returned status {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise LLMProviderException(error_msg, provider="gemini")

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    raise LLMProviderException("No candidates returned from Gemini API.", provider="gemini")

                content_parts = candidates[0].get("content", {}).get("parts", [])
                if not content_parts:
                    raise LLMProviderException("Empty content parts in Gemini response.", provider="gemini")

                return content_parts[0].get("text", "")

        except httpx.TimeoutException:
            raise LLMProviderException(f"Gemini request timed out after {self.timeout}s.", provider="gemini")
        except httpx.RequestError as e:
            raise LLMProviderException(f"Network error connecting to Gemini API: {str(e)}", provider="gemini")
        except LLMProviderException:
            raise
        except Exception as e:
            raise LLMProviderException(f"Unexpected error in Gemini provider: {str(e)}", provider="gemini")
