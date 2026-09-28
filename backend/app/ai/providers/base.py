"""
Base classes for AI providers.
"""

from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    async def analyze(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Analyze a prompt and return structured response."""
        pass
    
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate text from prompt."""
        pass


# Alias for backward compatibility
BaseProvider = LLMProvider