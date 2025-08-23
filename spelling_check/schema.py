from pydantic import BaseModel





class LLMCorrectorResponse(BaseModel):
    corrected_text: str