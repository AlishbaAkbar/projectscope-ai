from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract interface for LLM providers"""

    @abstractmethod
    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a prompt to the LLM and return the raw response string (expected to be JSON).
        """
        pass

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generic generation method.
        """
        pass
