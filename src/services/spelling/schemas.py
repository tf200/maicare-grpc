"""
Spelling Service Schemas
Pydantic models for spelling correction service
Migrated from: spelling_check/schema.py
"""

from pydantic import BaseModel


class LLMCorrectorResponse(BaseModel):
    """Response from LLM spelling corrector"""

    corrected_text: str
