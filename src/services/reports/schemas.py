from pydantic import BaseModel


class GenerateAutoReportRequest(BaseModel):
    text: str


class GenerateAutoReportResponse(BaseModel):
    report: str
