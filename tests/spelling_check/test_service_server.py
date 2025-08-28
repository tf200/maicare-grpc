# tests/spelling_check/test_service_server.py
import grpc
import pytest
from unittest import mock
from spelling_check.schema import LLMCorrectorResponse

import generated.spelling_service_pb2 as spelling_pb2


def test_correct_spelling_success(spelling_stub):
    expected = spelling_pb2.CorrectSpellingResponse(corrected_text="Hello world")

    with mock.patch("spelling_check.service.correct_spelling_llm") as m_corr:
        # return the pydantic model, not a plain string
        m_corr.return_value = LLMCorrectorResponse(corrected_text="Hello world")

        resp = spelling_stub.CorrectSpelling(
            spelling_pb2.CorrectSpellingRequest(initial_text="hellow wrold")
        )
        assert resp == expected


def test_correct_spelling_propagates_exception(spelling_stub):
    with mock.patch(
        "spelling_check.service.correct_spelling_llm",
        side_effect=ValueError("boom"),
    ):
        with pytest.raises(grpc.RpcError) as exc:
            spelling_stub.CorrectSpelling(
                spelling_pb2.CorrectSpellingRequest(initial_text="foo")
            )
        assert exc.value.code() == grpc.StatusCode.UNKNOWN