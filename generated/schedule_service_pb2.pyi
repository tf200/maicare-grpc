from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GenerateScheduleRequest(_message.Message):
    __slots__ = ("employees", "shifts", "week", "year")
    EMPLOYEES_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    employees: _containers.RepeatedCompositeFieldContainer[Employee]
    shifts: _containers.RepeatedCompositeFieldContainer[Shift]
    week: int
    year: int
    def __init__(
        self,
        employees: _Optional[_Iterable[_Union[Employee, _Mapping]]] = ...,
        shifts: _Optional[_Iterable[_Union[Shift, _Mapping]]] = ...,
        week: _Optional[int] = ...,
        year: _Optional[int] = ...,
    ) -> None: ...

class Employee(_message.Message):
    __slots__ = ("id", "first_name", "last_name", "target_hours")
    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_HOURS_FIELD_NUMBER: _ClassVar[int]
    id: str
    first_name: str
    last_name: str
    target_hours: float
    def __init__(
        self,
        id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        last_name: _Optional[str] = ...,
        target_hours: _Optional[float] = ...,
    ) -> None: ...

class Shift(_message.Message):
    __slots__ = ("id", "shift_name", "start_time", "end_time")
    ID_FIELD_NUMBER: _ClassVar[int]
    SHIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    shift_name: str
    start_time: str
    end_time: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        shift_name: _Optional[str] = ...,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
    ) -> None: ...

class GenerateScheduleResponse(_message.Message):
    __slots__ = ("status", "week", "year", "shifts", "grid_view", "summary")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    GRID_VIEW_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    status: str
    week: int
    year: int
    shifts: _containers.RepeatedCompositeFieldContainer[ScheduledShift]
    grid_view: GridView
    summary: _containers.RepeatedCompositeFieldContainer[EmployeeSummary]
    def __init__(
        self,
        status: _Optional[str] = ...,
        week: _Optional[int] = ...,
        year: _Optional[int] = ...,
        shifts: _Optional[_Iterable[_Union[ScheduledShift, _Mapping]]] = ...,
        grid_view: _Optional[_Union[GridView, _Mapping]] = ...,
        summary: _Optional[_Iterable[_Union[EmployeeSummary, _Mapping]]] = ...,
    ) -> None: ...

class ScheduledShift(_message.Message):
    __slots__ = (
        "date",
        "day_name",
        "shift_id",
        "shift_name",
        "start_time",
        "end_time",
        "hours",
        "employees",
    )
    DATE_FIELD_NUMBER: _ClassVar[int]
    DAY_NAME_FIELD_NUMBER: _ClassVar[int]
    SHIFT_ID_FIELD_NUMBER: _ClassVar[int]
    SHIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    EMPLOYEES_FIELD_NUMBER: _ClassVar[int]
    date: str
    day_name: str
    shift_id: int
    shift_name: str
    start_time: str
    end_time: str
    hours: float
    employees: _containers.RepeatedCompositeFieldContainer[AssignedEmployee]
    def __init__(
        self,
        date: _Optional[str] = ...,
        day_name: _Optional[str] = ...,
        shift_id: _Optional[int] = ...,
        shift_name: _Optional[str] = ...,
        start_time: _Optional[str] = ...,
        end_time: _Optional[str] = ...,
        hours: _Optional[float] = ...,
        employees: _Optional[_Iterable[_Union[AssignedEmployee, _Mapping]]] = ...,
    ) -> None: ...

class AssignedEmployee(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    def __init__(
        self, id: _Optional[str] = ..., name: _Optional[str] = ...
    ) -> None: ...

class GridView(_message.Message):
    __slots__ = ("days", "dates", "shifts_by_day")
    class ShiftsByDayEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GridDay
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[GridDay, _Mapping]] = ...,
        ) -> None: ...

    DAYS_FIELD_NUMBER: _ClassVar[int]
    DATES_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_BY_DAY_FIELD_NUMBER: _ClassVar[int]
    days: _containers.RepeatedScalarFieldContainer[str]
    dates: _containers.RepeatedScalarFieldContainer[str]
    shifts_by_day: _containers.MessageMap[str, GridDay]
    def __init__(
        self,
        days: _Optional[_Iterable[str]] = ...,
        dates: _Optional[_Iterable[str]] = ...,
        shifts_by_day: _Optional[_Mapping[str, GridDay]] = ...,
    ) -> None: ...

class GridDay(_message.Message):
    __slots__ = ("date", "shifts")
    class ShiftsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: GridShift
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[GridShift, _Mapping]] = ...,
        ) -> None: ...

    DATE_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    date: str
    shifts: _containers.MessageMap[str, GridShift]
    def __init__(
        self,
        date: _Optional[str] = ...,
        shifts: _Optional[_Mapping[str, GridShift]] = ...,
    ) -> None: ...

class GridShift(_message.Message):
    __slots__ = ("employees", "hours", "start", "end")
    EMPLOYEES_FIELD_NUMBER: _ClassVar[int]
    HOURS_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    employees: _containers.RepeatedScalarFieldContainer[str]
    hours: float
    start: str
    end: str
    def __init__(
        self,
        employees: _Optional[_Iterable[str]] = ...,
        hours: _Optional[float] = ...,
        start: _Optional[str] = ...,
        end: _Optional[str] = ...,
    ) -> None: ...

class EmployeeSummary(_message.Message):
    __slots__ = (
        "id",
        "first_name",
        "last_name",
        "target",
        "actual",
        "deviation",
        "status",
        "shifts",
    )
    class ShiftsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: int
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[int] = ...
        ) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_NAME_FIELD_NUMBER: _ClassVar[int]
    LAST_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_FIELD_NUMBER: _ClassVar[int]
    DEVIATION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SHIFTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    first_name: str
    last_name: str
    target: float
    actual: float
    deviation: float
    status: str
    shifts: _containers.ScalarMap[str, int]
    def __init__(
        self,
        id: _Optional[str] = ...,
        first_name: _Optional[str] = ...,
        last_name: _Optional[str] = ...,
        target: _Optional[float] = ...,
        actual: _Optional[float] = ...,
        deviation: _Optional[float] = ...,
        status: _Optional[str] = ...,
        shifts: _Optional[_Mapping[str, int]] = ...,
    ) -> None: ...
