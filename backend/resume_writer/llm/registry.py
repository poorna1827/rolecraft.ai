"""
Provider registry – Open/Closed implementation.

New providers register themselves here; the factory simply delegates to
this registry.  No ``if/elif`` chains to maintain.
"""

from __future__ import annotations

from typing import Callable, Dict, Type

from resume_writer.llm.base import LLMProvider


class LLMProviderRegistry:
    """Thread-safe, singleton-style registry for LLM provider classes."""

    _providers: Dict[str, Type[LLMProvider]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        """
        Class decorator that registers a provider under *name*.

        Usage::

            @LLMProviderRegistry.register("my_provider")
            class MyProvider(LLMProvider):
                ...
        """

        def decorator(provider_cls: Type[LLMProvider]) -> Type[LLMProvider]:
            if not issubclass(provider_cls, LLMProvider):
                raise TypeError(
                    f"{provider_cls.__name__} must subclass LLMProvider"
                )
            cls._providers[name.lower().strip()] = provider_cls
            return provider_cls

        return decorator

    @classmethod
    def get(cls, name: str, **kwargs) -> LLMProvider:
        """Return a *new instance* of the provider registered under *name*."""
        key = name.lower().strip()
        provider_cls = cls._providers.get(key)
        if provider_cls is None:
            available = ", ".join(sorted(cls._providers)) or "(none)"
            raise ValueError(
                f"Unknown LLM provider '{name}'. "
                f"Available providers: {available}"
            )
        return provider_cls(**kwargs)

    @classmethod
    def available(cls) -> list[str]:
        """Return sorted list of registered provider names."""
        return sorted(cls._providers)
