"""Unit tests for spelling correction service logic."""

import pytest
from unittest.mock import Mock
from logging import Logger

from src.core.llm_client import LLMClient
from src.services.spelling.corrector import SpellingCorrectorService
from src.services.spelling.schemas import LLMCorrectorResponse


def test_correct_spelling_success():
    """Test successful spelling correction with valid JSON response."""
    # Arrange: Create mock LLM client and logger
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_response = Mock()
    mock_response.output = '```json\n{"corrected_text": "Hello world"}\n```'
    mock_llm.run_sync.return_value = mock_response

    # Create service with injected mocks
    service = SpellingCorrectorService(mock_llm, mock_logger)

    # Act: Call the service
    result = service.correct_spelling("hellow wrold")

    # Assert: Verify behavior
    assert result == LLMCorrectorResponse(corrected_text="Hello world")
    mock_llm.run_sync.assert_called_once_with("hellow wrold")


def test_correct_spelling_without_markdown():
    """Test spelling correction with plain JSON (no markdown block)."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_response = Mock()
    mock_response.output = '```json\n{"corrected_text": "Plain text"}\n```'
    mock_llm.run_sync.return_value = mock_response

    service = SpellingCorrectorService(mock_llm, mock_logger)

    # Act
    result = service.correct_spelling("test")

    # Assert
    assert result.corrected_text == "Plain text"


def test_correct_spelling_invalid_json_raises():
    """Test that invalid JSON output raises ValueError."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_response = Mock()
    mock_response.output = "No JSON here at all"
    mock_llm.run_sync.return_value = mock_response

    service = SpellingCorrectorService(mock_llm, mock_logger)

    # Act & Assert
    with pytest.raises(ValueError, match="No valid JSON found"):
        service.correct_spelling("foo")


def test_correct_spelling_llm_error_propagates():
    """Test that LLM errors are propagated."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_llm.run_sync.side_effect = Exception("LLM API error")

    service = SpellingCorrectorService(mock_llm, mock_logger)

    # Act & Assert
    with pytest.raises(Exception, match="LLM API error"):
        service.correct_spelling("test")


def test_correct_spelling_multilingual():
    """Test multilingual spelling correction."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_response = Mock()
    mock_response.output = '```json\n{"corrected_text": "Hola, ¿cómo estás?"}\n```'
    mock_llm.run_sync.return_value = mock_response

    service = SpellingCorrectorService(mock_llm, mock_logger)

    # Act
    result = service.correct_spelling("Ola, como estas?")

    # Assert
    assert result.corrected_text == "Hola, ¿cómo estás?"
    mock_llm.run_sync.assert_called_once()
