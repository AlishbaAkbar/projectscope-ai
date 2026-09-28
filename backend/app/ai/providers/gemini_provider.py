import asyncio
import logging
from typing import Optional
import httpx
from app.ai.providers.base import LLMProvider
from app.utils.error_handlers import LLMProviderException

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    """Google Gemini AI Provider implementation via REST API"""

    def __init__(self, api_key: str, model: Optional[str] = None, timeout: float = 30.0):
        if not api_key:
            raise LLMProviderException("Gemini API key is required but was not provided.", provider="gemini")
        self.api_key = api_key
        self.model = model or "gemini-2.5-flash"
        self.timeout = timeout
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.generate(prompt, system_prompt)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        for attempt in range(3):
            try:
                return await self._call_gemini(prompt, system_prompt)
            except LLMProviderException as exc:
                if "503" not in str(exc) or attempt == 2:
                    raise
                delay = 2 ** attempt
                logger.warning("Gemini returned 503; retrying in %s seconds (attempt %s/3).", delay, attempt + 2)
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
            raise LLMProviderException(f"Request timed out after {self.timeout}s.", provider="gemini")
        except httpx.RequestError as e:
            raise LLMProviderException(f"Network error connecting to Gemini API: {str(e)}", provider="gemini")
        except LLMProviderException:
            raise
        except Exception as e:
            raise LLMProviderException(f"Unexpected error in Gemini provider: {str(e)}", provider="gemini")
