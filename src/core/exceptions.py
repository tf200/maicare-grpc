"""
Custom Exceptions
Application-specific exception classes for the microservice.
"""

from typing import Optional, Any


class ServiceError(Exception):
    """
    Base exception for all service-level errors.

    This is the root exception class that all other custom exceptions inherit from.
    """

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        """
        Initialize ServiceError.

        Args:
            message: Human-readable error message
            details: Optional dictionary with additional error context
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class LLMError(ServiceError):
    """
    Exception raised when LLM operations fail.

    Examples:
        - LLM API timeout
        - Invalid LLM response format
        - LLM rate limiting
        - Model unavailable
    """

    def __init__(
        self,
        message: str,
        model_name: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize LLMError.

        Args:
            message: Error message
            model_name: Name of the LLM model that caused the error
            details: Additional error context
        """
        error_details = details or {}
        if model_name:
            error_details["model_name"] = model_name
        super().__init__(message, error_details)
        self.model_name = model_name


class ValidationError(ServiceError):
    """
    Exception raised when data validation fails.

    Examples:
        - Invalid input format
        - Missing required fields
        - Schema validation failure
        - Type conversion errors
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        invalid_value: Optional[Any] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize ValidationError.

        Args:
            message: Error message
            field: Name of the field that failed validation
            invalid_value: The value that failed validation
            details: Additional error context
        """
        error_details = details or {}
        if field:
            error_details["field"] = field
        if invalid_value is not None:
            error_details["invalid_value"] = str(invalid_value)
        super().__init__(message, error_details)
        self.field = field
        self.invalid_value = invalid_value


class ConfigurationError(ServiceError):
    """
    Exception raised when configuration is invalid or missing.

    Examples:
        - Missing required environment variables
        - Invalid configuration values
        - Configuration file not found
        - Incompatible configuration settings
    """

    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize ConfigurationError.

        Args:
            message: Error message
            config_key: The configuration key that caused the error
            details: Additional error context
        """
        error_details = details or {}
        if config_key:
            error_details["config_key"] = config_key
        super().__init__(message, error_details)
        self.config_key = config_key


class GRPCServiceError(ServiceError):
    """
    Exception raised when gRPC service operations fail.

    Examples:
        - gRPC connection failure
        - Service unavailable
        - Request timeout
        - Invalid gRPC request/response
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize GRPCServiceError.

        Args:
            message: Error message
            status_code: gRPC status code
            details: Additional error context
        """
        error_details = details or {}
        if status_code:
            error_details["status_code"] = status_code
        super().__init__(message, error_details)
        self.status_code = status_code


class JSONParsingError(ServiceError):
    """
    Exception raised when JSON parsing fails.

    Examples:
        - Invalid JSON format in LLM response
        - Missing JSON markers
        - Malformed JSON structure
    """

    def __init__(
        self,
        message: str,
        raw_content: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize JSONParsingError.

        Args:
            message: Error message
            raw_content: The raw content that failed to parse
            details: Additional error context
        """
        error_details = details or {}
        if raw_content:
            # Truncate long content for readability
            error_details["raw_content"] = (
                raw_content[:200] + "..." if len(raw_content) > 200 else raw_content
            )
        super().__init__(message, error_details)
        self.raw_content = raw_content


class ObjectStorageError(ServiceError):
    """
    Exception raised when object storage operations fail.

    Examples:
        - Upload/download failures
        - Bucket access errors
        - Object not found
        - Connection timeouts
    """

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        bucket: Optional[str] = None,
        key: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize ObjectStorageError.

        Args:
            message: Error message
            operation: The storage operation that failed (upload, download, delete, etc.)
            bucket: Bucket name
            key: Object key
            details: Additional error context
        """
        error_details = details or {}
        if operation:
            error_details["operation"] = operation
        if bucket:
            error_details["bucket"] = bucket
        if key:
            error_details["key"] = key
        super().__init__(message, error_details)
        self.operation = operation
        self.bucket = bucket
        self.key = key
