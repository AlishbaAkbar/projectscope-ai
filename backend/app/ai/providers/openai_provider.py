import logging
from typing import Optional
import httpx
from app.ai.providers.base import LLMProvider
from app.utils.error_handlers import LLMProviderException

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI API Provider implementation via REST API"""

    def __init__(self, api_key: str, model: Optional[str] = None, timeout: float = 30.0):
        if not api_key:
            raise LLMProviderException("OpenAI API key is required but was not provided.", provider="openai")
        self.api_key = api_key
        self.model = model or "gpt-4o-mini"
        self.timeout = timeout
        self.base_url = "https://api.openai.com/v1/chat/completions"

    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        return await self.generate(prompt, system_prompt)

    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)

                if response.status_code != 200:
                    error_msg = f"OpenAI API returned status {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise LLMProviderException(error_msg, provider="openai")

                data = response.json()
                choices = data.get("choices", [])
                if not choices:
                    raise LLMProviderException("No choices returned from OpenAI API.", provider="openai")

                message_content = choices[0].get("message", {}).get("content", "")
                if not message_content:
                    raise LLMProviderException("Empty response content from OpenAI API.", provider="openai")

                return message_content

        except httpx.TimeoutException:
            raise LLMProviderException(f"Request timed out after {self.timeout}s.", provider="openai")
        except httpx.RequestError as e:
            raise LLMProviderException(f"Network error connecting to OpenAI API: {str(e)}", provider="openai")
        except LLMProviderException:
            raise
        except Exception as e:
            raise LLMProviderException(f"Unexpected error in OpenAI provider: {str(e)}", provider="openai")
