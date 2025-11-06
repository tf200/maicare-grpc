"""Test data factories and builders for creating test objects."""

from typing import Dict, Any
from src.services.care_planner.schemas import (
    ClientProfile,
    Goal,
)
from src.services.spelling.schemas import LLMCorrectorResponse


class ClientProfileBuilder:
    """Builder for creating test ClientProfile objects."""

    @staticmethod
    def build(
        name: str = "Test Client",
        age: int = 65,
        primary_diagnosis: str = "Diabetes Type 2",
        **kwargs,
    ) -> ClientProfile:
        """Build a ClientProfile with default or custom values."""
        defaults = {
            "name": name,
            "age": age,
            "primary_diagnosis": primary_diagnosis,
            "secondary_diagnoses": ["Hypertension"],
            "current_medications": ["Metformin"],
            "living_situation": "Lives alone",
            "support_network": "Has family nearby",
            "mobility_status": "Independent with walker",
            "cognitive_status": "Alert and oriented",
            "additional_notes": "Test notes",
        }
        defaults.update(kwargs)
        return ClientProfile(**defaults)


class GoalBuilder:
    """Builder for creating test Goal objects."""

    @staticmethod
    def build(goal_description: str = "Improve mobility", **kwargs) -> Goal:
        """Build a Goal with default or custom values."""
        defaults = {
            "goal_description": goal_description,
            "current_level": 3,
            "target_level": 7,
            "timeline": "3 months",
        }
        defaults.update(kwargs)
        return Goal(**defaults)


class SpellingResponseBuilder:
    """Builder for creating test LLMCorrectorResponse objects."""

    @staticmethod
    def build(corrected_text: str = "Hello world") -> LLMCorrectorResponse:
        """Build a LLMCorrectorResponse with default or custom values."""
        return LLMCorrectorResponse(corrected_text=corrected_text)


def mock_llm_json_response(data: Dict[str, Any]) -> str:
    """
    Create a mock LLM response with JSON block formatting.

    Args:
        data: Dictionary to be converted to JSON

    Returns:
        String formatted as LLM would return with JSON markers
    """
    import json

    return f"""```json
{json.dumps(data, indent=2)}
```"""


def create_sample_care_plan_response() -> Dict[str, Any]:
    """Create a sample care plan response structure for testing."""
    return {
        "goals": [
            {
                "goal_description": "Improve mobility",
                "current_level": 3,
                "target_level": 7,
                "timeline": "3 months",
            }
        ],
        "objectives": {
            "primary_objectives": ["Increase independence"],
            "secondary_objectives": ["Reduce fall risk"],
        },
        "strategic_priorities": {
            "immediate_actions": ["Assessment"],
            "short_term_focus": ["Exercise program"],
            "long_term_vision": ["Full independence"],
        },
        "next_steps": {
            "next_level": 4,
            "recommended_interventions": ["Physical therapy"],
            "monitoring_plan": "Weekly check-ins",
        },
    }
