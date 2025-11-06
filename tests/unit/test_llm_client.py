"""Unit tests for LLM client wrapper."""

import pytest
from unittest import mock

from src.core.llm_client import LLMClient, create_llm_client
from src.core.exceptions import LLMError, ConfigurationError


class TestLLMClient:
    """Tests for LLMClient class."""

    def test_initialization_success(self):
        """Test successful LLM client initialization."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent"),
        ):
            client = LLMClient(
                model_name="test-model",
                system_prompt="You are a helpful assistant",
                api_key="test-key",
            )

            assert client.model_name == "test-model"
            assert client.system_prompt == "You are a helpful assistant"

    def test_initialization_without_api_key(self):
        """Test that initialization fails without API key."""
        with pytest.raises(ConfigurationError) as exc:
            LLMClient(model_name="test-model", system_prompt="Test prompt", api_key="")

        assert "API key is required" in str(exc.value)
        assert exc.value.config_key == "api_key"

    def test_initialization_without_model_name(self):
        """Test that initialization fails without model name."""
        with pytest.raises(ConfigurationError) as exc:
            LLMClient(model_name="", system_prompt="Test prompt", api_key="test-key")

        assert "Model name is required" in str(exc.value)
        assert exc.value.config_key == "model_name"

    def test_run_sync_success(self):
        """Test successful synchronous LLM request."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent") as mock_agent_class,
        ):
            # Setup mock
            mock_agent = mock.MagicMock()
            mock_response = mock.MagicMock()
            mock_response.output = "Test response"
            mock_agent.run_sync.return_value = mock_response
            mock_agent_class.return_value = mock_agent

            client = LLMClient(
                model_name="test-model", system_prompt="Test prompt", api_key="test-key"
            )

            result = client.run_sync("Test prompt")

            assert result.output == "Test response"
            mock_agent.run_sync.assert_called_once_with("Test prompt")

    def test_run_sync_failure(self):
        """Test that run_sync raises LLMError on failure."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent") as mock_agent_class,
        ):
            # Setup mock to raise exception
            mock_agent = mock.MagicMock()
            mock_agent.run_sync.side_effect = Exception("API error")
            mock_agent_class.return_value = mock_agent

            client = LLMClient(
                model_name="test-model", system_prompt="Test prompt", api_key="test-key"
            )

            with pytest.raises(LLMError) as exc:
                client.run_sync("Test prompt")

            assert "LLM request failed" in str(exc.value)
            assert exc.value.model_name == "test-model"
            assert "prompt_length" in exc.value.details

    @pytest.mark.asyncio
    async def test_run_async_success(self):
        """Test successful asynchronous LLM request."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent") as mock_agent_class,
        ):
            # Setup mock
            mock_agent = mock.MagicMock()
            mock_response = mock.MagicMock()
            mock_response.output = "Async response"

            # Mock async method
            async def mock_run(*args, **kwargs):
                return mock_response

            mock_agent.run = mock_run
            mock_agent_class.return_value = mock_agent

            client = LLMClient(
                model_name="test-model", system_prompt="Test prompt", api_key="test-key"
            )

            result = await client.run("Test prompt")

            assert result.output == "Async response"

    def test_repr(self):
        """Test string representation of LLMClient."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent"),
        ):
            client = LLMClient(
                model_name="test-model", system_prompt="Test prompt", api_key="test-key"
            )

            assert repr(client) == "LLMClient(model=test-model)"


class TestCreateLLMClient:
    """Tests for create_llm_client factory function."""

    def test_factory_function(self):
        """Test that factory function creates LLMClient correctly."""
        with (
            mock.patch("src.core.llm_client.OpenAIModel"),
            mock.patch("src.core.llm_client.OpenRouterProvider"),
            mock.patch("src.core.llm_client.Agent"),
        ):
            client = create_llm_client(
                model_name="test-model",
                system_prompt="Test prompt",
                api_key="test-key",
                provider_kwargs={"timeout": 30},
            )

            assert isinstance(client, LLMClient)
            assert client.model_name == "test-model"
