"""
LLM provider setup for PydanticAI agents.
"""

from pydantic_ai import Model
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel

from .settings import settings


def get_llm_model() -> Model:
    """
    Get configured LLM model based on settings.

    Returns:
        Model: Configured PydanticAI model instance

    Raises:
        ValueError: If provider is unsupported
    """
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return OpenAIModel(
            settings.llm_model,
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url
        )
    elif provider == "anthropic":
        return AnthropicModel(
            settings.llm_model,
            api_key=settings.llm_api_key
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")