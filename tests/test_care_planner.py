# test_care_planner_service.py - Main test file
import pytest
from unittest.mock import patch, Mock
import grpc
from grpc import StatusCode

import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc
from care_planner.planner import CarePlannerService


class TestCarePlannerService:
    """Test suite for CarePlannerService"""

    @patch('care_planner.planner.generate_care_plan')
    def test_generate_care_plan_success(self, mock_generate, care_planner_service, 
                                      sample_request, mock_llm_response):
        """Test successful care plan generation"""
        # Arrange
        mock_generate.return_value = mock_llm_response
        context = Mock()
        
        # Act
        response = care_planner_service.GenerateCarePlan(sample_request, context)
        
        # Assert
        assert isinstance(response, pb2.PersonalizedCarePlanResponse)
        assert response.client_profile.age == 65
        assert response.client_profile.living_situation == "Independent"
        assert response.assessment_summary == "Client shows moderate mobility limitations requiring structured support."
        
        # Verify goals structure
        assert len(response.care_plan_objectives.short_term_goals) == 1
        assert len(response.care_plan_objectives.medium_term_goals) == 1
        assert len(response.care_plan_objectives.long_term_goals) == 1
        
        # Verify short term goal details
        short_goal = response.care_plan_objectives.short_term_goals[0]
        assert short_goal.goal_title == "Improve balance"
        assert short_goal.timeframe == "1-2 weeks"
        assert len(short_goal.specific_actions) == 2
        
        # Verify interventions
        assert len(response.interventions.daily_activities) == 2
        assert "Morning exercises" in response.interventions.daily_activities
        
        # Verify success metrics
        assert len(response.success_metrics) == 1
        metric = response.success_metrics[0]
        assert metric.metric == "Balance improvement"
        assert metric.target == "Reduce falls by 50%"
        
        # Verify risk factors
        assert len(response.risk_factors) == 1
        risk = response.risk_factors[0]
        assert risk.risk == "Fall risk"
        
        # Verify support network
        assert len(response.support_network) == 1
        support = response.support_network[0]
        assert support.role == "Family caregiver"
        
        # Verify review schedule
        assert response.review_schedule.daily == "Exercise completion check"
        assert response.review_schedule.weekly == "Progress assessment"
        assert response.review_schedule.monthly == "Comprehensive plan review"

    @patch('care_planner.planner.generate_care_plan')
    def test_generate_care_plan_input_transformation(self, mock_generate, 
                                                   care_planner_service, sample_request):
        """Test that input is correctly transformed for LLM call"""
        # Arrange
        mock_generate.return_value = Mock()  # We don't care about return value here
        context = Mock()
        
        # Act
        care_planner_service.GenerateCarePlan(sample_request, context)
        
        # Assert
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0][0]
        
        # Verify client_data transformation
        client_data = call_args["client_data"]
        assert client_data["age"] == 65
        assert client_data["living_situation"] == "Independent"
        assert client_data["education_level"] == "High School"
        assert client_data["assessment_domain"] == "Mobility"
        assert client_data["current_level"] == 2
        
        # Verify domain_definitions transformation
        domain_defs = call_args["domain_definitions"]
        assert "Mobility" in domain_defs
        mobility_levels = domain_defs["Mobility"]["levels"]
        assert isinstance(mobility_levels, dict)
        assert 1 in mobility_levels  # Keys should be converted to int
        assert mobility_levels[1] == "Independent mobility"

    @patch('care_planner.planner.generate_care_plan')
    @patch('care_planner.planner.logger')
    def test_generate_care_plan_exception_handling(self, mock_logger, mock_generate, 
                                                  care_planner_service, sample_request):
        """Test exception handling in GenerateCarePlan"""
        # Arrange
        mock_generate.side_effect = Exception("LLM service unavailable")
        context = Mock()
        
        # Act & Assert
        with pytest.raises(Exception, match="LLM service unavailable"):
            care_planner_service.GenerateCarePlan(sample_request, context)
        
        # Verify logging
        mock_logger.error.assert_called_once()
        assert "Error generating care plan:" in mock_logger.error.call_args[0][0]

    def test_empty_goals_handling(self, care_planner_service, sample_request, 
                                mock_llm_response):
        """Test handling of empty goal lists"""
        # Arrange
        mock_llm_response.care_plan_objectives.short_term_goals = []
        mock_llm_response.care_plan_objectives.medium_term_goals = []
        mock_llm_response.care_plan_objectives.long_term_goals = []
        
        with patch('care_planner.service.genearte_care_plan', return_value=mock_llm_response):
            context = Mock()
            
            # Act
            response = care_planner_service.GenerateCarePlan(sample_request, context)
            
            # Assert
            assert len(response.care_plan_objectives.short_term_goals) == 0
            assert len(response.care_plan_objectives.medium_term_goals) == 0
            assert len(response.care_plan_objectives.long_term_goals) == 0

    def test_complex_domain_definitions(self, care_planner_service, mock_llm_response):
        """Test handling of complex domain definitions with multiple domains"""
        # Arrange
        complex_request = pb2.PersonalizedCarePlanRequest(
            client_data=pb2.ClientData(
                age=75,
                living_situation="Assisted Living",
                education_level="College",
                domain_name="Cognitive",
                current_level=3,
                level_description="Moderate cognitive impairment"
            ),
            domain_definitions={
                "Cognitive": pb2.DomainLevels(
                    levels={
                        1: "No impairment",
                        2: "Mild impairment", 
                        3: "Moderate impairment",
                        4: "Severe impairment"
                    }
                ),
                "Social": pb2.DomainLevels(
                    levels={
                        1: "Highly social",
                        2: "Moderately social",
                        3: "Limited social interaction"
                    }
                )
            }
        )

        with patch('care_planner.planner.generate_care_plan', return_value=mock_llm_response) as mock_generate:
            context = Mock()
            
            # Act
            response = care_planner_service.GenerateCarePlan(complex_request, context)
            
            # Assert
            call_args = mock_generate.call_args[0][0]
            domain_defs = call_args["domain_definitions"]
            
            # Verify both domains are present
            assert "Cognitive" in domain_defs
            assert "Social" in domain_defs
            
            # Verify level conversion
            cognitive_levels = domain_defs["Cognitive"]["levels"]
            assert len(cognitive_levels) == 4
            assert all(isinstance(k, int) for k in cognitive_levels.keys())
            
            social_levels = domain_defs["Social"]["levels"]
            assert len(social_levels) == 3
            assert all(isinstance(k, int) for k in social_levels.keys())
            