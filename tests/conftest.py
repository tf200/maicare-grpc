import pytest
from unittest.mock import Mock, MagicMock
import grpc
from grpc_testing import server_from_dictionary, strict_real_time

import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc
from care_planner.planner import CarePlannerService
from care_planner.schema import (
    LLMPersonalizedCarePlanResponse, 
    ClientProfile, 
    CarePlanObjectives,
    Goal,
    Interventions,
    SuccessMetric,
    RiskFactor,
    SupportRole,
    ReviewSchedule,
    TransitionCriteria
)


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return LLMPersonalizedCarePlanResponse(
        client_profile=ClientProfile(
            age=65,
            living_situation="Independent",
            education_level="High School",
            assessment_domain="Mobility",
            current_level=2,
            level_description="Requires assistance with some activities"
        ),
        assessment_summary="Client shows moderate mobility limitations requiring structured support.",
        care_plan_objectives=CarePlanObjectives(
            short_term_goals=[
                Goal(
                    timeframe="1-2 weeks",
                    goal_title="Improve balance",
                    description="Focus on basic balance exercises",
                    specific_actions=["Daily balance exercises", "Use of stability aids"]
                )
            ],
            medium_term_goals=[
                Goal(
                    timeframe="1-3 months",
                    goal_title="Increase mobility",
                    description="Build strength and endurance",
                    specific_actions=["Walking program", "Physical therapy sessions"]
                )
            ],
            long_term_goals=[
                Goal(
                    timeframe="6-12 months",
                    goal_title="Independent mobility",
                    description="Achieve independent movement",
                    specific_actions=["Advanced exercises", "Regular assessments"]
                )
            ]
        ),
        interventions=Interventions(
            daily_activities=["Morning exercises", "Medication management"],
            weekly_activities=["Physical therapy", "Progress review"],
            monthly_activities=["Comprehensive assessment", "Plan adjustment"]
        ),
        resources_required=["Physical therapist", "Exercise equipment", "Mobility aids"],
        success_metrics=[
            SuccessMetric(
                metric="Balance improvement",
                target="Reduce falls by 50%",
                measurement_method="Weekly balance assessments"
            )
        ],
        risk_factors=[
            RiskFactor(
                risk="Fall risk",
                mitigation="Use of mobility aids and supervised exercises"
            )
        ],
        support_network=[
            SupportRole(
                role="Family caregiver",
                responsibility="Daily exercise supervision"
            )
        ],
        review_schedule=ReviewSchedule(
            daily="Exercise completion check",
            weekly="Progress assessment",
            monthly="Comprehensive plan review",
            quarterly="Long-term goal evaluation"
        ),
        emergency_protocols=["Call emergency services", "Contact family members"],
        transition_criteria=TransitionCriteria(
            next_level=3,
            requirements=["Achieve independent mobility", "Complete all exercises without assistance"]
        )
    )


@pytest.fixture
def sample_request():
    """Sample gRPC request for testing"""
    return pb2.PersonalizedCarePlanRequest(
        client_data=pb2.ClientData(
            age=65,
            living_situation="Independent",
            education_level="High School",
            domain_name="Mobility",
            current_level=2,
            level_description="Requires assistance with some activities"
        ),
        domain_definitions={
            "Mobility": pb2.DomainLevels(
                levels={
                    1: "Independent mobility",
                    2: "Requires some assistance",
                    3: "Requires significant assistance"
                }
            )
        }
    )


@pytest.fixture
def care_planner_service():
    """CarePlannerService instance for testing"""
    return CarePlannerService()


@pytest.fixture
def grpc_server(care_planner_service):
    """gRPC testing server"""
    servicers = {
        pb2.DESCRIPTOR.services_by_name['CarePlanner']: care_planner_service
    }
    return server_from_dictionary(servicers, strict_real_time())