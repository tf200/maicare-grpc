import json
from logging import Logger
import re
from injector import inject
from json_repair import repair_json
from src.core.config import Config
from src.core.llm_client import LLMClient
from src.services.reports.schemas import (
    GenerateAutoReportRequest,
    GenerateAutoReportResponse,
)


SYSTEM_PROMPT = """
You are an AI assistant specializing creating a detailled summary of the past reports given to you 
"""


REPORT_GENERATION_PROMPT = """
Given the following reports, generate a comprehensive summary report that highlights key findings, trends, and recommendations.
```json
{{
    "report": "string - A detailed summary report based on the provided reports."
}}
```

here are the reports to analyze:
{reports}
"""


class AutomatiqueReportService:
    @inject
    def __init__(self, logger: Logger, config: Config):
        self.llm_client = LLMClient(
            model_name="x-ai/grok-4-fast", config=config, system_prompt=SYSTEM_PROMPT
        )
        self.logger = logger

    def generate_report(
        self, req: GenerateAutoReportRequest
    ) -> GenerateAutoReportResponse:
        try:
            llm_output: str = self.llm_client.run_sync(
                REPORT_GENERATION_PROMPT.format(reports=req.text)
            ).output

            match = re.search(r"```json\s*([\s\S]*?)\s*```", llm_output)
            json_str = match.group(1) if match else llm_output.strip()

            try:
                json_response = json.loads(json_str)
            except json.JSONDecodeError:
                repaired = repair_json(json_str)
                json_response = json.loads(repaired)
            validated = GenerateAutoReportResponse.model_validate(json_response)
            return validated
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            raise e
