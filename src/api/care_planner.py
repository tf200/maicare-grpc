"""
Care Planner gRPC Service
Thin gRPC layer for care plan generation
Migrated from: care_planner/planner.py
"""

from logging import Logger
import grpc
from injector import inject
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc

from src.services.care_planner.planner import CarePlannerService
from src.services.care_planner.schemas import LLMPersonalizedCarePlanResponse


class CarePlannerServicer(pb2_grpc.CarePlannerServicer):
    """
    gRPC servicer for Care Planner.
    Thin layer that maps protobuf <-> domain models and delegates to service layer.
    """

    @inject
    def __init__(self, care_planner_service: CarePlannerService, logger: Logger):
        """Initialize with business service and dependencies"""
        # Get configuration
        # Inject LLM client into service
        self.business_service = care_planner_service
        self.logger = logger
        self.logger.info("CarePlannerServicer initialized")

    def GenerateCarePlan(self, request: pb2.PersonalizedCarePlanRequest, context):
        """
        Handle gRPC GenerateCarePlan request.

        Args:
            request: PersonalizedCarePlanRequest protobuf message
            context: gRPC context

        Returns:
            PersonalizedCarePlanResponse protobuf message
        """
        self.logger.info("Received GenerateCarePlan request")

        try:
            # Map protobuf request to domain model
            input_data = self._map_request_to_domain(request)

            # Delegate to business service
            care_plan = self.business_service.generate_care_plan(input_data)

            # Map domain model to protobuf response
            response = self._map_domain_to_response(care_plan)

            self.logger.info("Care plan generated successfully")
            return response

        except Exception as e:
            self.logger.error(f"Error in GenerateCarePlan: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to generate care plan: {str(e)}")
            raise

    def _map_request_to_domain(self, request: pb2.PersonalizedCarePlanRequest) -> dict:
        """
        Map protobuf request to domain model.

        Args:
            request: Protobuf request

        Returns:
            Dictionary with client_data and domain_definitions
        """
        return {
            "client_data": {
                "age": request.client_data.age,
                "living_situation": request.client_data.living_situation,
                "education_level": request.client_data.education_level,
                "assessment_domain": request.client_data.domain_name,
                "current_level": request.client_data.current_level,
                "level_description": request.client_data.level_description,
            },
            "domain_definitions": {
                key: {"levels": {int(k): v for k, v in v.levels.items()}}
                for key, v in request.domain_definitions.items()
            },
        }

    def _map_domain_to_response(
        self, care_plan: LLMPersonalizedCarePlanResponse
    ) -> pb2.PersonalizedCarePlanResponse:
        """
        Map domain model to protobuf response.

        Args:
            care_plan: Domain model care plan

        Returns:
            Protobuf response message
        """
        return pb2.PersonalizedCarePlanResponse(
            client_profile=pb2.ClientProfile(
                age=care_plan.client_profile.age,
                living_situation=care_plan.client_profile.living_situation,
                education_level=care_plan.client_profile.education_level,
                assessment_domain=care_plan.client_profile.assessment_domain,
                current_level=care_plan.client_profile.current_level,
                level_description=care_plan.client_profile.level_description,
            ),
            assessment_summary=care_plan.assessment_summary,
            care_plan_objectives=pb2.CarePlanObjectives(
                short_term_goals=[
                    pb2.Goal(
                        timeframe=goal.timeframe,
                        goal_title=goal.goal_title,
                        description=goal.description,
                        specific_actions=goal.specific_actions,
                    )
                    for goal in care_plan.care_plan_objectives.short_term_goals
                ],
                medium_term_goals=[
                    pb2.Goal(
                        timeframe=goal.timeframe,
                        goal_title=goal.goal_title,
                        description=goal.description,
                        specific_actions=goal.specific_actions,
                    )
                    for goal in care_plan.care_plan_objectives.medium_term_goals
                ],
                long_term_goals=[
                    pb2.Goal(
                        timeframe=goal.timeframe,
                        goal_title=goal.goal_title,
                        description=goal.description,
                        specific_actions=goal.specific_actions,
                    )
                    for goal in care_plan.care_plan_objectives.long_term_goals
                ],
            ),
            interventions=pb2.Interventions(
                daily_activities=care_plan.interventions.daily_activities,
                weekly_activities=care_plan.interventions.weekly_activities,
                monthly_activities=care_plan.interventions.monthly_activities,
            ),
            resources_required=care_plan.resources_required,
            success_metrics=[
                pb2.SuccessMetric(
                    metric=metric.metric,
                    target=metric.target,
                    measurement_method=metric.measurement_method,
                )
                for metric in care_plan.success_metrics
            ],
            risk_factors=[
                pb2.RiskFactor(
                    risk=risk.risk,
                    mitigation=risk.mitigation,
                    risk_level=risk.risk_level,
                )
                for risk in care_plan.risk_factors
            ],
            support_network=[
                pb2.SupportRole(role=role.role, responsibility=role.responsibility)
                for role in care_plan.support_network
            ],
            review_schedule=pb2.ReviewSchedule(
                daily=care_plan.review_schedule.daily,
                weekly=care_plan.review_schedule.weekly,
                monthly=care_plan.review_schedule.monthly,
                quarterly=care_plan.review_schedule.quarterly,
            ),
            emergency_protocols=care_plan.emergency_protocols,
            transition_criteria=pb2.TransitionCriteria(
                next_level=int(care_plan.transition_criteria.next_level),
                requirements=care_plan.transition_criteria.requirements,
            ),
        )
