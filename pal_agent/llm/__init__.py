"""Model layer: provider-agnostic LLM access with JSON-Schema structured output (N4)."""

from .provider import (ClaudeCLIProvider, LLMProvider, StubProvider, SchemaError,
                       get_provider)

__all__ = ["LLMProvider", "StubProvider", "ClaudeCLIProvider", "SchemaError",
           "get_provider"]
