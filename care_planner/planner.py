from care_planner.schema import LLMPersonalizedCarePlanResponse
import generated.service_pb2 as pb2
import generated.service_pb2_grpc as pb2_grpc
from .llm_config import generate_llm_care_plan
from config.logging_config import get_logger

# Get logger for this module
logger = get_logger(__name__)


class CarePlannerService(pb2_grpc.CarePlannerServicer):
    def GenerateCarePlan(self, request: pb2.PersonalizedCarePlanRequest, context):
        input: dict = {
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
        try:
            care_plan: LLMPersonalizedCarePlanResponse = generate_llm_care_plan(input)
            response = pb2.PersonalizedCarePlanResponse(
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
                    pb2.RiskFactor(risk=risk.risk, mitigation=risk.mitigation, risk_level=risk.risk_level)
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
                ),
            )
            return response
        except Exception as e:
            # Handle exceptions
            logger.error(f"Error generating care plan: {e}")
            raise
