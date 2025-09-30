import json
import re
from venv import create
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from care_planner.schema import LLMPersonalizedCarePlanResponse

from config.llm_config import create_agent
from config.logging_config import get_logger
from config.env_config import get_config

SYSTEM_PROMPT = """
You are an AI assistant specializing in creating personalized care plans for youth in care. You will be provided with client assessment data and must generate a 
comprehensive, evidence-based care plan.
**IMPORTANT: Your response must be valid JSON format only. Do not include any text before or after the JSON.**
"""


PROMPT = """
...
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
11. **Json Validation:** Make sure you are following the reauired jsin structure

Remember: This is a professional care planning tool. Be thorough, specific, and practical in all recommendations.

here are the inputs:
{inputs}
"""


logger = get_logger(__name__)
config = get_config()


def generate_llm_care_plan(inputs: dict) -> LLMPersonalizedCarePlanResponse:
    """
    Generate a personalized care plan based on the provided inputs.
    """
    try:
        agent = create_agent(
            model_name="openai/gpt-5",
            system_prompt=SYSTEM_PROMPT,
            api_key=config.openrouter_api_key,
        )
        llm_output: str = agent.run_sync(
            user_prompt=PROMPT.format(inputs=inputs),
        ).output
        match = re.search(r"```json\s*([\s\S]*?)\s*```", llm_output)
        if match:
            json_response = json.loads(match.group(1))
            validated = LLMPersonalizedCarePlanResponse.model_validate(json_response)
            return validated
        else:
            logger.error("No valid JSON found in the response.")
            raise ValueError("No valid JSON found in the response.")
    except Exception as e:
        logger.error(f"Error generating care plan: {e}")
        raise e
