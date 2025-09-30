"""
Configuration management using pydantic-settings.
MIRROR: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
"""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider (openai, anthropic)")
    llm_api_key: str = Field(..., description="API key for the LLM provider")
    llm_model: str = Field(default="gpt-4", description="Model name to use")
    llm_base_url: Optional[str] = Field(
        default="https://api.openai.com/v1",
        description="Base URL for the LLM API"
    )

    # Brave Search Configuration
    brave_api_key: str = Field(..., description="Brave Search API key")
    brave_search_url: str = Field(
        default="https://api.search.brave.com/res/v1/web/search",
        description="Brave Search API endpoint"
    )

    # Gmail API Configuration
    gmail_credentials_path: str = Field(
        default="credentials.json",
        description="Path to Gmail OAuth credentials JSON"
    )
    gmail_token_path: str = Field(
        default="token.json",
        description="Path to Gmail OAuth token JSON"
    )

    # Application Configuration
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="INFO", description="Logging level")
    debug: bool = Field(default=False, description="Debug mode")

    @field_validator("llm_api_key", "brave_api_key")
    @classmethod
    def validate_api_keys(cls, v: str) -> str:
        """Ensure API keys are not empty."""
        if not v or v.strip() == "":
            raise ValueError("API key cannot be empty")
        return v


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    # For testing, create settings with dummy values
    import os
    os.environ.setdefault("LLM_API_KEY", "test_key")
    os.environ.setdefault("BRAVE_API_KEY", "test_key")
    settings = Settings()