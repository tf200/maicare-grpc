"""
Care Planner Schemas
Pydantic models for care planner service
Migrated from: care_planner/schema.py
"""

from pydantic import BaseModel
from typing import List


class ClientProfile(BaseModel):
    """Client profile information"""

    age: int
    living_situation: str
    education_level: str
    assessment_domain: str
    current_level: int
    level_description: str


class Goal(BaseModel):
    """Individual goal with timeframe and actions"""

    timeframe: str
    goal_title: str
    description: str
    specific_actions: List[str]


class CarePlanObjectives(BaseModel):
    """Collection of short, medium, and long-term goals"""

    short_term_goals: List[Goal]
    medium_term_goals: List[Goal]
    long_term_goals: List[Goal]


class Interventions(BaseModel):
    """Daily, weekly, and monthly intervention activities"""

    daily_activities: List[str]
    weekly_activities: List[str]
    monthly_activities: List[str]


class SuccessMetric(BaseModel):
    """Metric for measuring success"""

    metric: str
    target: str
    measurement_method: str


class RiskFactor(BaseModel):
    """Identified risk with mitigation strategy"""

    risk: str
    mitigation: str
    risk_level: str


class SupportRole(BaseModel):
    """Support network role and responsibility"""

    role: str
    responsibility: str


class ReviewSchedule(BaseModel):
    """Schedule for reviewing progress"""

    daily: str
    weekly: str
    monthly: str
    quarterly: str


class TransitionCriteria(BaseModel):
    """Criteria for transitioning to next level"""

    next_level: float
    requirements: List[str]


class LLMPersonalizedCarePlanResponse(BaseModel):
    """Complete personalized care plan response from LLM"""

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
