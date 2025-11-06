"""
LLM Client Wrapper
Abstraction layer for LLM communication using pydantic-ai.

This module provides a centralized interface for LLM operations,
making it easy to switch providers or models in the future.
"""

from typing import Optional, Any, Dict
from injector import inject
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from src.core.config import Config
from src.core.exceptions import LLMError, ConfigurationError


class LLMClient:
    """
    Wrapper for pydantic-ai Agent with additional functionality.

    Provides a clean interface for LLM operations with error handling,
    retry logic, and consistent configuration management.
    """

    @inject
    def __init__(
        self,
        model_name: str,
        system_prompt: str,
        config: Config,
        provider_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize LLM client.

        Args:
            model_name: Name of the LLM model (e.g., 'x-ai/grok-beta')
            system_prompt: System prompt for the agent
            api_key: OpenRouter API key
            provider_kwargs: Additional provider configuration

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not config.openrouter_api_key:
            raise ConfigurationError(
                "API key is required for LLM client", config_key="api_key"
            )

        if not model_name:
            raise ConfigurationError(
                "Model name is required for LLM client", config_key="model_name"
            )

        self.model_name = model_name
        self.system_prompt = system_prompt
        self._api_key = config.openrouter_api_key

        # Initialize provider
        try:
            provider_params = {"api_key": self._api_key}
            if provider_kwargs:
                provider_params.update(provider_kwargs)

            model = OpenAIModel(
                model_name, provider=OpenRouterProvider(**provider_params)
            )

            self._agent = Agent(
                model=model,
                system_prompt=system_prompt,
            )
        except Exception as e:
            raise LLMError(
                f"Failed to initialize LLM client: {str(e)}", model_name=model_name
            )

    @property
    def agent(self) -> Agent:
        """Get the underlying pydantic-ai Agent."""
        return self._agent

    def run_sync(self, prompt: str, **kwargs) -> Any:
        """
        Run LLM request synchronously.

        Args:
            prompt: User prompt/message
            **kwargs: Additional arguments passed to agent.run_sync()

        Returns:
            Agent response

        Raises:
            LLMError: If LLM request fails
        """
        try:
            return self._agent.run_sync(prompt, **kwargs)
        except Exception as e:
            raise LLMError(
                f"LLM request failed: {str(e)}",
                model_name=self.model_name,
                details={"prompt_length": len(prompt)},
            )

    async def run(self, prompt: str, **kwargs) -> Any:
        """
        Run LLM request asynchronously.

        Args:
            prompt: User prompt/message
            **kwargs: Additional arguments passed to agent.run()

        Returns:
            Agent response

        Raises:
            LLMError: If LLM request fails
        """
        try:
            return await self._agent.run(prompt, **kwargs)
        except Exception as e:
            raise LLMError(
                f"Async LLM request failed: {str(e)}",
                model_name=self.model_name,
                details={"prompt_length": len(prompt)},
            )

    def __repr__(self) -> str:
        """String representation of LLMClient."""
        return f"LLMClient(model={self.model_name})"
