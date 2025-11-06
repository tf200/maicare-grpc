"""Integration tests for gRPC services."""

import grpc
import pytest
from unittest import mock

from src.services.spelling.schemas import LLMCorrectorResponse
import generated.spelling_service_pb2 as spelling_pb2


class TestSpellingCheckService:
    """Integration tests for Spelling Check gRPC service."""

    def test_correct_spelling_success(self, spelling_stub):
        """Test successful spelling correction through gRPC."""
        expected = spelling_pb2.CorrectSpellingResponse(corrected_text="Hello world")

        with mock.patch("src.api.spelling_check.correct_spelling_llm") as m_corr:
            # return the pydantic model, not a plain string
            m_corr.return_value = LLMCorrectorResponse(corrected_text="Hello world")

            resp = spelling_stub.CorrectSpelling(
                spelling_pb2.CorrectSpellingRequest(initial_text="hellow wrold")
            )
            assert resp == expected

    def test_correct_spelling_propagates_exception(self, spelling_stub):
        """Test that service exceptions are properly propagated as gRPC errors."""
        with mock.patch(
            "src.api.spelling_check.correct_spelling_llm",
            side_effect=ValueError("boom"),
        ):
            with pytest.raises(grpc.RpcError) as exc:
                spelling_stub.CorrectSpelling(
                    spelling_pb2.CorrectSpellingRequest(initial_text="foo")
                )
            assert exc.value.code() == grpc.StatusCode.INTERNAL


class TestCarePlannerService:
    """Integration tests for Care Planner gRPC service."""

    # TODO: Add comprehensive integration tests for care planner service
    # - Test successful care plan generation
    # - Test error handling for invalid requests
    # - Test request/response mapping
    pass
