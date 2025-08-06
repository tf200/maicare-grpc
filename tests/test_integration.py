# test_integration.py - Integration tests using gRPC testing framework
import pytest
import grpc
from grpc_testing import server_from_dictionary, strict_real_time
from unittest.mock import patch

import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc


class TestCarePlannerServiceIntegration:
    """Integration tests for the gRPC service"""

    @patch('care_planner.planner.generate_care_plan')
    def test_grpc_end_to_end(self, mock_generate, grpc_server, sample_request, mock_llm_response):
        """Test complete gRPC call flow"""
        # Arrange
        mock_generate.return_value = mock_llm_response
        
        # Act
        method = grpc_server.invoke_unary_unary(
            method_descriptor=(pb2.DESCRIPTOR
                             .services_by_name['CarePlanner']
                             .methods_by_name['GenerateCarePlan']),
            invocation_metadata={},
            request=sample_request,
            timeout=30
        )
        
        response, metadata, code, details = method.termination()
        
        # Assert
        assert code == grpc.StatusCode.OK
        assert response.client_profile.age == 65
        assert len(response.care_plan_objectives.short_term_goals) == 1

    def test_grpc_error_handling(self, grpc_server, sample_request):
        """Test gRPC error handling"""
        # Arrange
        with patch('care_planner.planner.generate_care_plan', side_effect=Exception("Service error")):

            # Act
            method = grpc_server.invoke_unary_unary(
                method_descriptor=(pb2.DESCRIPTOR
                                 .services_by_name['CarePlanner']
                                 .methods_by_name['GenerateCarePlan']),
                invocation_metadata={},
                request=sample_request,
                timeout=30
            )
            
            response, metadata, code, details = method.termination()
            
            # Assert
            assert code != grpc.StatusCode.OK