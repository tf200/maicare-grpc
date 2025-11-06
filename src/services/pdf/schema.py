from typing import List, Optional
from pydantic import BaseModel, Field


class AppointmentCardData(BaseModel):
    id: Optional[int] = None
    client_name: Optional[str] = None
    date: Optional[str] = None
    mentor: Optional[str] = None
    general_information: List[str] = Field(default_factory=list)
    important_contacts: List[str] = Field(default_factory=list)
    household_info: List[str] = Field(default_factory=list)
    organization_agreements: List[str] = Field(default_factory=list)
    youth_officer_agreements: List[str] = Field(default_factory=list)
    treatment_agreements: List[str] = Field(default_factory=list)
    smoking_rules: List[str] = Field(default_factory=list)
    work: List[str] = Field(default_factory=list)
    school_internship: List[str] = Field(default_factory=list)
    travel: List[str] = Field(default_factory=list)
    leave: List[str] = Field(default_factory=list)
