from pydantic import BaseModel
from typing import List


class ClientProfile(BaseModel):
    age: int
    living_situation: str
    education_level: str
    assessment_domain: str
    current_level: int
    level_description: str


class Goal(BaseModel):
    timeframe: str
    goal_title: str
    description: str
    specific_actions: List[str]


class CarePlanObjectives(BaseModel):
    short_term_goals: List[Goal]
    medium_term_goals: List[Goal]
    long_term_goals: List[Goal]


class Interventions(BaseModel):
    daily_activities: List[str]
    weekly_activities: List[str]
    monthly_activities: List[str]


class SuccessMetric(BaseModel):
    metric: str
    target: str
    measurement_method: str


class RiskFactor(BaseModel):
    risk: str
    mitigation: str
    risk_level: str 

class SupportRole(BaseModel):
    role: str
    responsibility: str


class ReviewSchedule(BaseModel):
    daily: str
    weekly: str
    monthly: str
    quarterly: str


class TransitionCriteria(BaseModel):
    next_level: float
    requirements: List[str]


class LLMPersonalizedCarePlanResponse(BaseModel):
    client_profile: ClientProfile
    assessment_summary: str
    care_plan_objectives: CarePlanObjectives
    interventions: Interventions
    resources_required: List[str]
    success_metrics: List[SuccessMetric]
    risk_factors: List[RiskFactor]
    support_network: List[SupportRole]
    review_schedule: ReviewSchedule
    emergency_protocols: List[str]
    transition_criteria: TransitionCriteria
