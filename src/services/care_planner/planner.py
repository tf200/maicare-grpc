"""
Care Planner Business Logic
Core business logic for care plan generation (framework-agnostic)
"""

from logging import Logger
from typing import Dict, Any

from injector import inject

from src.services.care_planner.generator import CarePlanGenerator
from src.services.care_planner.schemas import LLMPersonalizedCarePlanResponse


class CarePlannerService:
    """
    Business logic for care plan generation.
    This is framework-agnostic and can be used by any API layer (gRPC, REST, etc.)
    """

    @inject
    def __init__(self, care_plan_generator: CarePlanGenerator, logger: Logger):
        """
        Initialize care planner with LLM client.

        Args:
            llm_client: LLM client for care plan generation
        """
        self.generator = care_plan_generator
        self.logger = logger
        self.logger.info("CarePlannerService initialized")

    def generate_care_plan(
        self, input_data: Dict[str, Any]
    ) -> LLMPersonalizedCarePlanResponse:
        """
        Generate a personalized care plan based on client data.

        Args:
            input_data: Dictionary containing:
                - client_data: Client profile and assessment information
                - domain_definitions: Domain-specific level definitions

        Returns:
            LLMPersonalizedCarePlanResponse: Generated care plan

        Raises:
            Exception: If care plan generation fails
        """
        self.logger.info(
            f"Generating care plan for domain: {input_data.get('client_data', {}).get('assessment_domain', 'unknown')}"
        )

        try:
            # Validate input has required fields
            if "client_data" not in input_data:
                raise ValueError("Missing required field: client_data")

            # Generate care plan using LLM
            care_plan = self.generator.generate_care_plan(input_data)

            self.logger.info("Care plan generated successfully")
            return care_plan

        except Exception as e:
            self.logger.error(f"Failed to generate care plan: {e}")
            raise
