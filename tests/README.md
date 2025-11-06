# Tests Directory Structure

This directory contains all tests for the py-microservice project, organized by test type.

## Directory Structure

```
tests/
├── conftest.py              # Shared pytest fixtures and configuration
├── fixtures/                # Test data factories and utilities
│   ├── __init__.py
│   └── factories.py         # Builders for test objects
├── unit/                    # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── test_spelling_corrector.py
│   └── test_care_planner_generator.py
├── integration/             # Integration tests (test multiple components)
│   ├── __init__.py
│   └── test_grpc_services.py
├── care_planner/            # [DEPRECATED] Old test location
└── spelling_check/          # [DEPRECATED] Old test location
```

## Test Types

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual functions/classes in isolation
- **Speed**: Very fast (milliseconds)
- **Dependencies**: Minimal, heavily mocked
- **Location**: `tests/unit/`
- **Naming**: `test_<module_name>.py`

**Example**: Testing spelling correction logic without gRPC or external services.

### Integration Tests (`tests/integration/`)
- **Purpose**: Test multiple components working together
- **Speed**: Slower (seconds)
- **Dependencies**: May include real gRPC server, database connections
- **Location**: `tests/integration/`
- **Naming**: `test_<feature_name>.py`

**Example**: Testing full gRPC request/response cycle through the API layer.

## Running Tests

### Run all tests
```bash
uv run pytest tests/
```

### Run only unit tests (fast feedback)
```bash
uv run pytest tests/unit/ -v
```

### Run only integration tests
```bash
uv run pytest tests/integration/ -v
```

### Run with coverage
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

### Run specific test file
```bash
uv run pytest tests/unit/test_spelling_corrector.py -v
```

### Run specific test function
```bash
uv run pytest tests/unit/test_spelling_corrector.py::test_happy_path -v
```

## Fixtures

### Shared Fixtures (conftest.py)

- **`grpc_server`**: Session-scoped fixture that starts a real gRPC server for integration tests
- **`spelling_stub`**: gRPC stub for SpellingCheck service
- **`care_planner_stub`**: gRPC stub for CarePlanner service

### Test Utilities (fixtures/factories.py)

- **`ClientProfileBuilder`**: Build test ClientProfile objects
- **`GoalBuilder`**: Build test Goal objects
- **`SpellingResponseBuilder`**: Build test LLMCorrectorResponse objects
- **`mock_llm_json_response()`**: Helper to create mock LLM responses with JSON formatting
- **`create_sample_care_plan_response()`**: Generate sample care plan data

## Writing New Tests

### Unit Test Template

```python
"""Unit tests for <module> functionality."""
import pytest
from unittest import mock

from src.services.<module> import function_to_test


def test_successful_case():
    """Test the happy path."""
    # Arrange
    test_input = "test data"
    
    # Act
    result = function_to_test(test_input)
    
    # Assert
    assert result == expected_output


def test_error_case():
    """Test error handling."""
    with pytest.raises(ValueError, match="error message"):
        function_to_test("bad input")
```

### Integration Test Template

```python
"""Integration tests for <feature>."""
import grpc
import pytest


class Test<Feature>Service:
    """Integration tests for <Feature> gRPC service."""
    
    def test_successful_request(self, <feature>_stub):
        """Test successful gRPC request."""
        # Arrange
        request = create_test_request()
        
        # Act
        response = <feature>_stub.Method(request)
        
        # Assert
        assert response.field == expected_value
```

## Best Practices

### 1. Test Organization
- One test class per service/feature
- Descriptive test names that explain what is being tested
- Group related tests using classes

### 2. Arrange-Act-Assert Pattern
```python
def test_something():
    # Arrange: Set up test data and mocks
    test_data = create_test_data()
    
    # Act: Execute the function being tested
    result = function_under_test(test_data)
    
    # Assert: Verify the results
    assert result == expected
```

### 3. Mocking
- Mock external dependencies (LLMs, databases, external APIs)
- Use `unittest.mock.patch` for function-level mocking
- Use `pytest-mock` for more complex scenarios
- Mock at the boundary (e.g., mock LLM calls, not internal logic)

### 4. Test Independence
- Each test should be independent and not rely on others
- Use fixtures to set up common test state
- Clean up resources in teardown (fixtures handle this automatically)

### 5. Descriptive Names
```python
# Good
def test_correct_spelling_returns_corrected_text_when_valid_input():
    pass

# Bad
def test_spelling():
    pass
```

## Coverage Goals

- **Unit Tests**: Aim for 80%+ coverage of business logic
- **Integration Tests**: Cover all gRPC endpoints and critical workflows
- **Edge Cases**: Test error handling, boundary conditions, invalid inputs

## Continuous Integration

Tests run automatically on:
- Every pull request
- Commits to main/dev branches
- Pre-commit hooks (if configured)

## Deprecated Test Locations

The following directories contain old test files and will be removed in Phase 6:
- `tests/care_planner/` - Migrated to `tests/unit/test_care_planner_generator.py`
- `tests/spelling_check/` - Migrated to:
  - `tests/unit/test_spelling_corrector.py` (unit tests)
  - `tests/integration/test_grpc_services.py` (integration tests)

**Do not add new tests to these deprecated locations.**

## Future Enhancements

- [ ] Add performance/load tests
- [ ] Add end-to-end tests with real LLM calls (using test API keys)
- [ ] Add contract tests for gRPC interfaces
- [ ] Add mutation testing for better coverage quality
- [ ] Add property-based testing with Hypothesis
- [ ] Set up automatic test result reporting

## Troubleshooting

### Tests fail with import errors
- Ensure you're in the project root directory
- Run tests with `uv run pytest` to use the correct Python environment
- Check that `PYTHONPATH` includes the project root (usually automatic with pytest)

### gRPC server fixture fails
- Check that no other process is using the test port
- Verify all gRPC servicers are properly implemented
- Look for errors in the server startup logs

### Mock patches not working
- Ensure you're patching at the correct location (where it's used, not where it's defined)
- Use the full module path: `src.api.spelling_check.function_name`
- Check that the function is imported correctly in the module you're testing

---

**Last Updated**: Phase 5 (Test Migration Complete)
