"""
Care Plan Generator
LLM-powered care plan generation logic
Migrated from: care_planner/generator.py
"""

import json
from logging import Logger
import re
from injector import inject
from json_repair import repair_json

from src.core.config import Config
from src.core.llm_client import LLMClient
from src.services.care_planner.schemas import LLMPersonalizedCarePlanResponse


SYSTEM_PROMPT = """
You are an AI assistant specializing in creating personalized care plans for youth in care. You will be provided with client assessment data and must generate a 
comprehensive, evidence-based care plan.
**IMPORTANT: Your response must be valid JSON format only. Do not include any text before or after the JSON.**
"""


PROMPT = """
## Required JSON Structure:
```json
{{
  "client_profile": {{
    "age": "number",
    "living_situation": "string",
    "education_level": "string",
    "assessment_domain": "string",
    "current_level": "number",
    "level_description": "string"
  }},
  "assessment_summary": "string - Brief summary of current situation and challenges",
  "care_plan_objectives": {{
    "short_term_goals": [
      {{
        "timeframe": "1-3 months",
        "goal_title": "string",
        "description": "string",
        "specific_actions": ["string", "string", "string"]
      }}
    ],
    "medium_term_goals": [
      {{
        "timeframe": "3-6 months", 
        "goal_title": "string",
        "description": "string",
        "specific_actions": ["string", "string", "string"]
      }}
    ],
    "long_term_goals": [
      {{
        "timeframe": "6-12 months",
        "goal_title": "string", 
        "description": "string",
        "specific_actions": ["string", "string", "string"]
      }}
    ]
  }},
  "interventions": {{
    "daily_activities": ["string", "string", "string"],
    "weekly_activities": ["string", "string", "string"],
    "monthly_activities": ["string", "string", "string"]
  }},
  "resources_required": ["string", "string", "string"],
  "success_metrics": [
    {{
      "metric": "string",
      "target": "string",
      "measurement_method": "string"
    }}
  ],
  "risk_factors": [
    {{
      "risk": "string",
      "risk_level": "low|medium|high",
      "mitigation": "string"
    }}
  ],
  "support_network": [
    {{
      "role": "string",
      "responsibility": "string"
    }}
  ],
  "review_schedule": {{
    "daily": "string",
    "weekly": "string", 
    "monthly": "string",
    "quarterly": "string"
  }},
  "emergency_protocols": ["string", "string", "string"],
  "transition_criteria": {{
    "next_level": "number",
    "requirements": ["string", "string", "string"]
  }}
}}
```

## Guidelines:
1. **Age-appropriate:** All interventions must match the client's developmental stage
2. **Context-aware:** Consider living situation and education level in all recommendations
3. **Evidence-based:** Use proven intervention methods for youth in care
4. **Measurable:** Include specific, trackable success metrics
5. **Realistic:** Set achievable goals within stated timeframes
6. **Comprehensive:** Address all aspects of the assessment domain
7. **Progressive:** Plan should logically move client toward next level
8. **Cultural sensitivity:** Consider diverse backgrounds and needs
9. **Safety-focused:** Always prioritize client wellbeing and safety
10. **Collaborative:** Include appropriate support network roles
11. **Json Validation:** Make sure you are following the required json structure

Remember: This is a professional care planning tool. Be thorough, specific, and practical in all recommendations.

Here are the inputs:
{inputs}
"""


class CarePlanGenerator:
    """
    Care plan generator using LLM.
    Handles LLM interaction and response parsing.
    """

    @inject
    def __init__(self, logger: Logger, config: Config):
        """
        Initialize generator with LLM client.

        Args:
            llm_client: LLM client for care plan generation
        """
        self.llm_client = LLMClient(
            model_name="x-ai/grok-4-fast",  # or read from Config if configurable
            config=config,
            system_prompt=SYSTEM_PROMPT,
        )
        self.logger = logger
        self.logger.info("CarePlanGenerator initialized")

    def generate_care_plan(self, inputs: dict) -> LLMPersonalizedCarePlanResponse:
        """
        Generate a personalized care plan using LLM.

        Args:
            inputs: Dictionary containing client data and domain definitions

        Returns:
            LLMPersonalizedCarePlanResponse: Validated care plan response

        Raises:
            Exception: If LLM generation or validation fails
        """
        try:
            llm_output: str = self.llm_client.run_sync(
                PROMPT.format(inputs=inputs)
            ).output

            # Extract JSON from markdown if present
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", llm_output)
            json_str = match.group(1) if match else llm_output.strip()

            # Try to repair malformed JSON
            try:
                json_response = json.loads(json_str)
            except json.JSONDecodeError:
                self.logger.warning("Initial JSON parse failed, attempting repair...")
                repaired = repair_json(json_str)
                json_response = json.loads(repaired)

            # Validate against schema
            validated = LLMPersonalizedCarePlanResponse.model_validate(json_response)
            self.logger.info("Care plan generated and validated successfully")

            return validated

        except Exception as e:
            self.logger.error(f"Error generating care plan: {e}")
            raise
