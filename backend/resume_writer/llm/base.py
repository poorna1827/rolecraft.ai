from abc import ABC, abstractmethod
from resume_writer.models.resume import ResumeData


class LLMProvider(ABC):
    """
    Abstract base class for all LLM providers.

    To add a new provider, subclass this and register it via
    ``LLMProviderRegistry.register``.
    """

    @abstractmethod
    def generate_resume(self, system_prompt: str, user_prompt: str) -> ResumeData:
        """Generate a structured resume JSON based on prompts."""
        ...
