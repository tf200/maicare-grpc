"""Unit tests for core exceptions."""

from src.core.exceptions import (
    ServiceError,
    LLMError,
    ValidationError,
    ConfigurationError,
    GRPCServiceError,
    JSONParsingError,
)


class TestServiceError:
    """Tests for ServiceError base class."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = ServiceError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.message == "Something went wrong"
        assert error.details == {}

    def test_error_with_details(self):
        """Test error with additional details."""
        error = ServiceError(
            "Operation failed", details={"operation": "save", "retry_count": 3}
        )
        assert "Operation failed" in str(error)
        assert "operation" in str(error)
        assert error.details["operation"] == "save"


class TestLLMError:
    """Tests for LLMError."""

    def test_llm_error_with_model(self):
        """Test LLM error with model name."""
        error = LLMError("Model timeout", model_name="gpt-4")
        assert error.model_name == "gpt-4"
        assert "Model timeout" in str(error)
        assert error.details["model_name"] == "gpt-4"

    def test_llm_error_without_model(self):
        """Test LLM error without model name."""
        error = LLMError("Generic LLM error")
        assert error.model_name is None
        assert "Generic LLM error" in str(error)


class TestValidationError:
    """Tests for ValidationError."""

    def test_validation_error_with_field(self):
        """Test validation error with field information."""
        error = ValidationError(
            "Invalid email format", field="email", invalid_value="not-an-email"
        )
        assert error.field == "email"
        assert error.invalid_value == "not-an-email"
        assert "Invalid email format" in str(error)
        assert error.details["field"] == "email"

    def test_validation_error_basic(self):
        """Test basic validation error."""
        error = ValidationError("Validation failed")
        assert error.field is None
        assert error.invalid_value is None


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_configuration_error_with_key(self):
        """Test configuration error with config key."""
        error = ConfigurationError("Missing API key", config_key="OPENROUTER_API_KEY")
        assert error.config_key == "OPENROUTER_API_KEY"
        assert "Missing API key" in str(error)
        assert error.details["config_key"] == "OPENROUTER_API_KEY"


class TestGRPCServiceError:
    """Tests for GRPCServiceError."""

    def test_grpc_error_with_status(self):
        """Test gRPC error with status code."""
        error = GRPCServiceError("Service unavailable", status_code="UNAVAILABLE")
        assert error.status_code == "UNAVAILABLE"
        assert "Service unavailable" in str(error)


class TestJSONParsingError:
    """Tests for JSONParsingError."""

    def test_json_error_with_content(self):
        """Test JSON parsing error with raw content."""
        raw_json = '{"invalid": json}'
        error = JSONParsingError("Failed to parse JSON", raw_content=raw_json)
        assert error.raw_content == raw_json
        assert "Failed to parse JSON" in str(error)

    def test_json_error_truncates_long_content(self):
        """Test that long content is truncated in error details."""
        long_content = "x" * 300
        error = JSONParsingError("Failed to parse JSON", raw_content=long_content)
        # Content should be truncated to 200 chars + "..."
        assert len(error.details["raw_content"]) == 203
        assert error.details["raw_content"].endswith("...")
