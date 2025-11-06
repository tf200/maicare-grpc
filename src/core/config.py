"""
Core Configuration Module
Consolidates environment, LLM, and application configuration.
Migrated from: config/env_config.py and config/llm_config.py
"""

from typing import Any, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider


class Config(BaseSettings):
    """
    Application configuration using Pydantic BaseSettings.
    Automatically loads from environment variables and .env file.
    """

    # Environment settings
    environment: str = Field(
        default="development", description="Application environment"
    )

    # Logging configuration
    log_level: str = Field(default="INFO", description="Logging level")

    # API Keys
    openrouter_api_key: str = Field(default="", description="OpenRouter API key")

    # Object Storage
    object_storage_endpoint: str = Field(
        default="", description="Object storage endpoint URL"
    )
    object_storage_key: str = Field(default="", description="Object storage access key")
    object_storage_key_id: str = Field(
        default="", description="Object storage access key ID"
    )
    object_storage_bucket: str = Field(
        default="", description="Object storage bucket name"
    )

    # Server Configuration
    grpc_port: int = Field(default=50051, description="gRPC server port")
    grpc_max_workers: int = Field(default=4, description="Maximum worker threads")

    @field_validator("environment")
    def validate_environment(cls, v):
        """Ensure environment is lowercase"""
        return v.lower()

    @field_validator("log_level")
    def validate_log_level(cls, v):
        """Ensure log level is uppercase"""
        return v.upper()

    @field_validator("openrouter_api_key")
    def validate_api_key(cls, v):
        """Validate API key format"""
        if not v or v.isspace():
            raise ValueError("OPENROUTER_API_KEY cannot be empty or whitespace")
        if len(v) < 10:  # Assuming minimum length
            raise ValueError("OPENROUTER_API_KEY appears to be too short")
        return v.strip()

    @field_validator("object_storage_endpoint")
    def validate_object_storage_endpoint(cls, v):
        """Validate object storage endpoint URL"""
        if v and not (v.startswith("http://") or v.startswith("https://")):
            raise ValueError(
                "OBJECT_STORAGE_ENDPOINT must start with http:// or https://"
            )
        return v.strip()

    @field_validator(
        "object_storage_key_id", "object_storage_key", "object_storage_bucket"
    )
    def validate_object_storage_fields(cls, v, info):
        """Validate object storage related fields"""
        field_name = info.field_name.upper()
        if not v or v.isspace():
            raise ValueError(f"{field_name} cannot be empty or whitespace")
        return v.strip()

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment == "development"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


def create_agent(
    model_name: str,
    system_prompt: str,
    api_key: str,
    provider_kwargs: Optional[dict[str, Any]] = None,
) -> Agent:
    """
    Create a Pydantic AI agent with OpenRouter provider.

    Args:
        model_name: Name of the LLM model to use
        system_prompt: System prompt for the agent
        api_key: OpenRouter API key
        provider_kwargs: Additional provider configuration

    Returns:
        Configured Agent instance
    """
    provider_params = {"api_key": api_key}
    if provider_kwargs:
        provider_params.update(provider_kwargs)

    model = OpenAIModel(model_name, provider=OpenRouterProvider(**provider_params))

    return Agent(
        model=model,
        system_prompt=system_prompt,
    )
