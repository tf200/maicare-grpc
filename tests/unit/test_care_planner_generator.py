"""Unit tests for care planner generator."""

import pytest
from unittest.mock import Mock
from logging import Logger

from src.core.llm_client import LLMClient
from src.services.care_planner.generator import CarePlanGenerator
from src.services.care_planner.planner import CarePlannerService


def test_care_plan_generation_with_valid_input():
    """Test successful care plan generation with valid input."""
    # Arrange: Create mock LLM client and logger
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_response = Mock()
    # Minimal valid care plan JSON
    mock_response.output = """```json
    {
        "client_profile": {
            "age": 16,
            "living_situation": "Foster home",
            "education_level": "High school",
            "assessment_domain": "Independence",
            "current_level": 2,
            "level_description": "Developing skills"
        },
        "assessment_summary": "Client shows progress",
        "care_plan_objectives": {
            "short_term_goals": [{
                "timeframe": "1-3 months",
                "goal_title": "Improve daily routines",
                "description": "Build consistency",
                "specific_actions": ["Wake up at same time", "Make bed daily"]
            }],
            "medium_term_goals": [{
                "timeframe": "3-6 months",
                "goal_title": "Budget management",
                "description": "Learn to budget",
                "specific_actions": ["Track expenses", "Save money"]
            }],
            "long_term_goals": [{
                "timeframe": "6-12 months",
                "goal_title": "Independent living prep",
                "description": "Prepare for independence",
                "specific_actions": ["Find housing", "Job search"]
            }]
        },
        "interventions": {
            "daily_activities": ["Morning routine", "Homework time"],
            "weekly_activities": ["Life skills class", "Counseling"],
            "monthly_activities": ["Budget review", "Goal assessment"]
        },
        "resources_required": ["Life skills curriculum", "Budget worksheets"],
        "success_metrics": [{
            "metric": "Routine consistency",
            "target": "90% adherence",
            "measurement_method": "Daily checklist"
        }],
        "risk_factors": [{
            "risk": "Inconsistency",
            "risk_level": "medium",
            "mitigation": "Daily check-ins"
        }],
        "support_network": [{
            "role": "Foster parent",
            "responsibility": "Daily support"
        }],
        "review_schedule": {
            "daily": "Check-in with foster parent",
            "weekly": "Progress review",
            "monthly": "Goal assessment",
            "quarterly": "Comprehensive evaluation"
        },
        "emergency_protocols": ["Contact case manager", "Call crisis line"],
        "transition_criteria": {
            "next_level": 3,
            "requirements": ["Consistent routines", "Basic budgeting"]
        }
    }
    ```"""
    mock_llm.run_sync.return_value = mock_response

    # Create generator with mocks
    generator = CarePlanGenerator(mock_llm, mock_logger)

    # Act
    input_data = {
        "client_data": {
            "age": 16,
            "living_situation": "Foster home",
            "education_level": "High school",
            "assessment_domain": "Independence",
            "current_level": 2,
            "level_description": "Developing",
        }
    }
    result = generator.generate_care_plan(input_data)

    # Assert
    assert result.client_profile.age == 16
    assert result.client_profile.assessment_domain == "Independence"
    assert len(result.care_plan_objectives.short_term_goals) > 0
    mock_llm.run_sync.assert_called_once()


def test_care_planner_service_delegates_to_generator():
    """Test that CarePlannerService properly delegates to generator."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_generator_logger = Mock(spec=Logger)
    mock_response = Mock()
    mock_response.output = """```json
    {
        "client_profile": {"age": 15, "living_situation": "Group home", "education_level": "9th grade", "assessment_domain": "Social", "current_level": 1, "level_description": "Basic"},
        "assessment_summary": "Summary",
        "care_plan_objectives": {
            "short_term_goals": [{"timeframe": "1-3 months", "goal_title": "Goal", "description": "Desc", "specific_actions": ["Action"]}],
            "medium_term_goals": [{"timeframe": "3-6 months", "goal_title": "Goal", "description": "Desc", "specific_actions": ["Action"]}],
            "long_term_goals": [{"timeframe": "6-12 months", "goal_title": "Goal", "description": "Desc", "specific_actions": ["Action"]}]
        },
        "interventions": {"daily_activities": ["Activity"], "weekly_activities": ["Activity"], "monthly_activities": ["Activity"]},
        "resources_required": ["Resource"],
        "success_metrics": [{"metric": "Metric", "target": "Target", "measurement_method": "Method"}],
        "risk_factors": [{"risk": "Risk", "risk_level": "low", "mitigation": "Mitigation"}],
        "support_network": [{"role": "Role", "responsibility": "Responsibility"}],
        "review_schedule": {"daily": "Daily", "weekly": "Weekly", "monthly": "Monthly", "quarterly": "Quarterly"},
        "emergency_protocols": ["Protocol"],
        "transition_criteria": {"next_level": 2, "requirements": ["Requirement"]}
    }
    ```"""
    mock_llm.run_sync.return_value = mock_response

    # Create generator and service with proper dependencies
    generator = CarePlanGenerator(mock_llm, mock_generator_logger)
    service = CarePlannerService(generator, mock_logger)

    # Act
    input_data = {"client_data": {"age": 15, "assessment_domain": "Social"}}
    result = service.generate_care_plan(input_data)

    # Assert
    assert result is not None
    assert result.client_profile.age == 15


def test_care_plan_missing_client_data_raises_error():
    """Test that missing client_data raises ValueError."""
    # Arrange
    mock_llm = Mock(spec=LLMClient)
    mock_logger = Mock(spec=Logger)
    mock_generator_logger = Mock(spec=Logger)

    # Create generator and service with proper dependencies
    generator = CarePlanGenerator(mock_llm, mock_generator_logger)
    service = CarePlannerService(generator, mock_logger)

    # Act & Assert
    with pytest.raises(ValueError, match="Missing required field: client_data"):
        service.generate_care_plan({})
