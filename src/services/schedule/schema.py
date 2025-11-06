import datetime
import uuid
from typing import Dict, List, Optional
from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    target_hours: float


class ShiftSchema(BaseModel):
    id: int
    shift_name: str
    start_time: datetime.time  # Changed to time only
    end_time: datetime.time  # Changed to time only


class AssignedEmployeeSchema(BaseModel):
    id: uuid.UUID
    name: str


# Flat structure - for database insertion
class ScheduledShiftSchema(BaseModel):
    """Single shift entry for flat list structure (database-friendly)"""

    date: str  # ISO format date: "2025-02-03"
    day_name: str  # "Monday", "Tuesday", etc.
    shift_id: int
    shift_name: str
    start_time: datetime.datetime  # Full datetime with date
    end_time: datetime.datetime  # Full datetime with date
    hours: float
    employees: List[AssignedEmployeeSchema]


# Grid structure - for frontend visualization
class GridShiftSchema(BaseModel):
    """Shift info for grid view"""

    employees: List[str]  # Just employee names for compact display
    hours: float
    start: str  # Time only: "08:00"
    end: str  # Time only: "16:00"


class GridDaySchema(BaseModel):
    """Day info for grid view"""

    date: str  # ISO format date: "2025-02-03"
    shifts: Dict[str, GridShiftSchema]  # key: shift_name


class GridViewSchema(BaseModel):
    """Grid view for weekly calendar display"""

    days: List[str]  # ["Monday", "Tuesday", ...]
    dates: List[str]  # ["2025-02-03", "2025-02-04", ...]
    shifts_by_day: Dict[str, GridDaySchema]  # key: day_name


class EmployeeSummarySchema(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    target: float
    actual: float
    deviation: float
    status: str
    shifts: Dict[str, int]


class ScheduleResponseSchema(BaseModel):
    """Hybrid response structure with both flat and grid views"""

    status: str  # "optimal" or "feasible"
    week: int
    year: int
    shifts: List[ScheduledShiftSchema]  # Flat list for database
    grid_view: GridViewSchema  # Grid for frontend visualization
    summary: List[EmployeeSummarySchema]
