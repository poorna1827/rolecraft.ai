"""
Thin factory that delegates entirely to the provider registry.

Kept as a separate class so call‐sites can remain unchanged
(``LLMFactory.get_provider(name)``).
"""

from resume_writer.llm.base import LLMProvider
from resume_writer.llm.registry import LLMProviderRegistry


class LLMFactory:
    @staticmethod
    def get_provider(provider_name: str, **kwargs) -> LLMProvider:
        """Resolve *provider_name* to a concrete ``LLMProvider`` instance."""
        return LLMProviderRegistry.get(provider_name, **kwargs)
