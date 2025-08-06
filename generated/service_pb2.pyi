from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PersonalizedCarePlanRequest(_message.Message):
    __slots__ = ("client_data", "domain_definitions")
    class DomainDefinitionsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: DomainLevels
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[DomainLevels, _Mapping]] = ...) -> None: ...
    CLIENT_DATA_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_DEFINITIONS_FIELD_NUMBER: _ClassVar[int]
    client_data: ClientData
    domain_definitions: _containers.MessageMap[str, DomainLevels]
    def __init__(self, client_data: _Optional[_Union[ClientData, _Mapping]] = ..., domain_definitions: _Optional[_Mapping[str, DomainLevels]] = ...) -> None: ...

class ClientData(_message.Message):
    __slots__ = ("age", "living_situation", "education_level", "domain_name", "current_level", "level_description")
    AGE_FIELD_NUMBER: _ClassVar[int]
    LIVING_SITUATION_FIELD_NUMBER: _ClassVar[int]
    EDUCATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    age: int
    living_situation: str
    education_level: str
    domain_name: str
    current_level: int
    level_description: str
    def __init__(self, age: _Optional[int] = ..., living_situation: _Optional[str] = ..., education_level: _Optional[str] = ..., domain_name: _Optional[str] = ..., current_level: _Optional[int] = ..., level_description: _Optional[str] = ...) -> None: ...

class DomainLevels(_message.Message):
    __slots__ = ("levels",)
    class LevelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    levels: _containers.ScalarMap[int, str]
    def __init__(self, levels: _Optional[_Mapping[int, str]] = ...) -> None: ...

class PersonalizedCarePlanResponse(_message.Message):
    __slots__ = ("client_profile", "assessment_summary", "care_plan_objectives", "interventions", "resources_required", "success_metrics", "risk_factors", "support_network", "review_schedule", "emergency_protocols", "transition_criteria")
    CLIENT_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ASSESSMENT_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    CARE_PLAN_OBJECTIVES_FIELD_NUMBER: _ClassVar[int]
    INTERVENTIONS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_METRICS_FIELD_NUMBER: _ClassVar[int]
    RISK_FACTORS_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_NETWORK_FIELD_NUMBER: _ClassVar[int]
    REVIEW_SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
    TRANSITION_CRITERIA_FIELD_NUMBER: _ClassVar[int]
    client_profile: ClientProfile
    assessment_summary: str
    care_plan_objectives: CarePlanObjectives
    interventions: Interventions
    resources_required: _containers.RepeatedScalarFieldContainer[str]
    success_metrics: _containers.RepeatedCompositeFieldContainer[SuccessMetric]
    risk_factors: _containers.RepeatedCompositeFieldContainer[RiskFactor]
    support_network: _containers.RepeatedCompositeFieldContainer[SupportRole]
    review_schedule: ReviewSchedule
    emergency_protocols: _containers.RepeatedScalarFieldContainer[str]
    transition_criteria: TransitionCriteria
    def __init__(self, client_profile: _Optional[_Union[ClientProfile, _Mapping]] = ..., assessment_summary: _Optional[str] = ..., care_plan_objectives: _Optional[_Union[CarePlanObjectives, _Mapping]] = ..., interventions: _Optional[_Union[Interventions, _Mapping]] = ..., resources_required: _Optional[_Iterable[str]] = ..., success_metrics: _Optional[_Iterable[_Union[SuccessMetric, _Mapping]]] = ..., risk_factors: _Optional[_Iterable[_Union[RiskFactor, _Mapping]]] = ..., support_network: _Optional[_Iterable[_Union[SupportRole, _Mapping]]] = ..., review_schedule: _Optional[_Union[ReviewSchedule, _Mapping]] = ..., emergency_protocols: _Optional[_Iterable[str]] = ..., transition_criteria: _Optional[_Union[TransitionCriteria, _Mapping]] = ...) -> None: ...

class ClientProfile(_message.Message):
    __slots__ = ("age", "living_situation", "education_level", "assessment_domain", "current_level", "level_description")
    AGE_FIELD_NUMBER: _ClassVar[int]
    LIVING_SITUATION_FIELD_NUMBER: _ClassVar[int]
    EDUCATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    ASSESSMENT_DOMAIN_FIELD_NUMBER: _ClassVar[int]
    CURRENT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    LEVEL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    age: int
    living_situation: str
    education_level: str
    assessment_domain: str
    current_level: int
    level_description: str
    def __init__(self, age: _Optional[int] = ..., living_situation: _Optional[str] = ..., education_level: _Optional[str] = ..., assessment_domain: _Optional[str] = ..., current_level: _Optional[int] = ..., level_description: _Optional[str] = ...) -> None: ...

class CarePlanObjectives(_message.Message):
    __slots__ = ("short_term_goals", "medium_term_goals", "long_term_goals")
    SHORT_TERM_GOALS_FIELD_NUMBER: _ClassVar[int]
    MEDIUM_TERM_GOALS_FIELD_NUMBER: _ClassVar[int]
    LONG_TERM_GOALS_FIELD_NUMBER: _ClassVar[int]
    short_term_goals: _containers.RepeatedCompositeFieldContainer[Goal]
    medium_term_goals: _containers.RepeatedCompositeFieldContainer[Goal]
    long_term_goals: _containers.RepeatedCompositeFieldContainer[Goal]
    def __init__(self, short_term_goals: _Optional[_Iterable[_Union[Goal, _Mapping]]] = ..., medium_term_goals: _Optional[_Iterable[_Union[Goal, _Mapping]]] = ..., long_term_goals: _Optional[_Iterable[_Union[Goal, _Mapping]]] = ...) -> None: ...

class Goal(_message.Message):
    __slots__ = ("timeframe", "goal_title", "description", "specific_actions")
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    GOAL_TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SPECIFIC_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    timeframe: str
    goal_title: str
    description: str
    specific_actions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, timeframe: _Optional[str] = ..., goal_title: _Optional[str] = ..., description: _Optional[str] = ..., specific_actions: _Optional[_Iterable[str]] = ...) -> None: ...

class Interventions(_message.Message):
    __slots__ = ("daily_activities", "weekly_activities", "monthly_activities")
    DAILY_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    WEEKLY_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    daily_activities: _containers.RepeatedScalarFieldContainer[str]
    weekly_activities: _containers.RepeatedScalarFieldContainer[str]
    monthly_activities: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, daily_activities: _Optional[_Iterable[str]] = ..., weekly_activities: _Optional[_Iterable[str]] = ..., monthly_activities: _Optional[_Iterable[str]] = ...) -> None: ...

class SuccessMetric(_message.Message):
    __slots__ = ("metric", "target", "measurement_method")
    METRIC_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_METHOD_FIELD_NUMBER: _ClassVar[int]
    metric: str
    target: str
    measurement_method: str
    def __init__(self, metric: _Optional[str] = ..., target: _Optional[str] = ..., measurement_method: _Optional[str] = ...) -> None: ...

class RiskFactor(_message.Message):
    __slots__ = ("risk", "mitigation")
    RISK_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_FIELD_NUMBER: _ClassVar[int]
    risk: str
    mitigation: str
    def __init__(self, risk: _Optional[str] = ..., mitigation: _Optional[str] = ...) -> None: ...

class SupportRole(_message.Message):
    __slots__ = ("role", "responsibility")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    RESPONSIBILITY_FIELD_NUMBER: _ClassVar[int]
    role: str
    responsibility: str
    def __init__(self, role: _Optional[str] = ..., responsibility: _Optional[str] = ...) -> None: ...

class ReviewSchedule(_message.Message):
    __slots__ = ("daily", "weekly", "monthly", "quarterly")
    DAILY_FIELD_NUMBER: _ClassVar[int]
    WEEKLY_FIELD_NUMBER: _ClassVar[int]
    MONTHLY_FIELD_NUMBER: _ClassVar[int]
    QUARTERLY_FIELD_NUMBER: _ClassVar[int]
    daily: str
    weekly: str
    monthly: str
    quarterly: str
    def __init__(self, daily: _Optional[str] = ..., weekly: _Optional[str] = ..., monthly: _Optional[str] = ..., quarterly: _Optional[str] = ...) -> None: ...

class TransitionCriteria(_message.Message):
    __slots__ = ("next_level", "requirements")
    NEXT_LEVEL_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    next_level: int
    requirements: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, next_level: _Optional[int] = ..., requirements: _Optional[_Iterable[str]] = ...) -> None: ...
