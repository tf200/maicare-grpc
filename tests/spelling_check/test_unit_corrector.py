# tests/spelling_check/test_unit_corrector.py
import pytest
from unittest import mock

from spelling_check.corrector import correct_spelling_llm
from spelling_check.schema import LLMCorrectorResponse


def test_happy_path():
    fake_llm_output = """
    ```json
    {"corrected_text": "Hello world"}
    ```
    """
    with mock.patch("spelling_check.corrector.create_agent") as m_agent:
        m_agent.return_value.run_sync.return_value.output = fake_llm_output
        result = correct_spelling_llm("hellow wrold")
        assert result == LLMCorrectorResponse(corrected_text="Hello world")


def test_no_json_block_raises():
    bad_output = "No JSON here"
    with mock.patch("spelling_check.corrector.create_agent") as m_agent:
        m_agent.return_value.run_sync.return_value.output = bad_output
        with pytest.raises(ValueError, match="No valid JSON found"):
            correct_spelling_llm("foo")