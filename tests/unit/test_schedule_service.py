"""Unit tests for schedule generation service."""

import pytest
import uuid
from datetime import datetime, time
from unittest.mock import Mock
from logging import Logger

from src.services.schedule.service import ScheduleService, ShiftScheduler
from src.services.schedule.schema import (
    EmployeeSchema,
    ShiftSchema,
    ScheduleResponseSchema,
    ScheduledShiftSchema,
    EmployeeSummarySchema,
)


# ==================== Fixtures ====================


@pytest.fixture
def mock_logger():
    """Create a mock logger for testing."""
    return Mock(spec=Logger)


@pytest.fixture
def sample_employees():
    """Create sample employees for testing."""
    return [
        EmployeeSchema(
            id=uuid.uuid4(), first_name="John", last_name="Doe", target_hours=40.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="Jane", last_name="Smith", target_hours=35.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="Bob", last_name="Johnson", target_hours=30.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="Alice", last_name="Williams", target_hours=40.0
        ),
    ]


@pytest.fixture
def sample_shifts():
    """Create sample shifts for testing."""
    return [
        ShiftSchema(
            id=1, shift_name="Morning", start_time=time(8, 0), end_time=time(16, 0)
        ),
        ShiftSchema(
            id=2, shift_name="Evening", start_time=time(16, 0), end_time=time(22, 0)
        ),
        ShiftSchema(
            id=3, shift_name="Night", start_time=time(22, 0), end_time=time(6, 0)
        ),
    ]


@pytest.fixture
def schedule_service(mock_logger):
    """Create a ScheduleService instance for testing."""
    return ScheduleService(logger=mock_logger)


# ==================== ScheduleService Tests ====================


def test_schedule_service_initialization(mock_logger):
    """Test that ScheduleService initializes correctly."""
    service = ScheduleService(logger=mock_logger)

    assert service.logger == mock_logger
    assert service.model is not None
    assert service.assignments == {}
    assert service.DAYS == [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]


def test_generate_schedule_success(
    schedule_service, sample_employees, sample_shifts, mock_logger
):
    """Test successful schedule generation."""
    # Act
    result = schedule_service.generate_schedule(
        employees=sample_employees, shifts=sample_shifts, week=1, year=2024
    )

    # Assert
    assert result is not None
    assert isinstance(result, ScheduleResponseSchema)
    assert result.status in ["optimal", "feasible"]
    assert result.week == 1
    assert result.year == 2024
    assert len(result.shifts) > 0  # Flat shifts list
    assert len(result.grid_view.days) == 7  # 7 days
    assert len(result.summary) == len(sample_employees)

    # Verify logging
    mock_logger.info.assert_any_call("Generating schedule for week 1, 2024")
    mock_logger.info.assert_any_call("Schedule generated successfully.")


def test_generate_schedule_with_minimal_employees(
    schedule_service, sample_shifts, mock_logger
):
    """Test schedule generation with minimal number of employees."""
    # Create only 2 employees (minimum viable)
    minimal_employees = [
        EmployeeSchema(
            id=uuid.uuid4(), first_name="John", last_name="Doe", target_hours=40.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="Jane", last_name="Smith", target_hours=40.0
        ),
    ]

    # Act
    result = schedule_service.generate_schedule(
        employees=minimal_employees, shifts=sample_shifts, week=1, year=2024
    )

    # Assert - might be feasible or None depending on constraints
    if result:
        assert isinstance(result, ScheduleResponseSchema)
        assert len(result.summary) == 2


def test_generate_schedule_with_single_shift(
    schedule_service, sample_employees, mock_logger
):
    """Test schedule generation with a single shift type."""
    single_shift = [
        ShiftSchema(
            id=1, shift_name="Morning", start_time=time(9, 0), end_time=time(17, 0)
        )
    ]

    # Act
    result = schedule_service.generate_schedule(
        employees=sample_employees, shifts=single_shift, week=1, year=2024
    )

    # Assert
    assert result is not None
    assert isinstance(result, ScheduleResponseSchema)
    # Check that all shifts in the flat list are the "Morning" shift
    for shift in result.shifts:
        assert shift.shift_name == "Morning"


# ==================== ShiftScheduler Tests ====================


def test_shift_scheduler_initialization(sample_employees, sample_shifts):
    """Test ShiftScheduler initialization."""
    days = ["Monday", "Tuesday", "Wednesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=30
    )

    assert scheduler.employees == sample_employees
    assert scheduler.shifts == sample_shifts
    assert scheduler.days == days
    assert scheduler.max_solve_time == 30
    assert len(scheduler.shift_hours) == len(sample_shifts)


def test_calculate_shift_hours(sample_employees, sample_shifts):
    """Test shift hours calculation."""
    scheduler = ShiftScheduler(
        sample_employees,
        sample_shifts,
        ["Monday"],
        week=1,
        year=2024,
        max_solve_time=30,
    )

    # Morning shift: 8am-4pm = 8 hours
    assert scheduler.shift_hours[0] == 8.0

    # Evening shift: 4pm-10pm = 6 hours
    assert scheduler.shift_hours[1] == 6.0

    # Night shift: 10pm-6am = 8 hours (crosses midnight, handled correctly)
    assert scheduler.shift_hours[2] == 8.0


def test_calculate_shift_hours_with_partial_hours(sample_employees):
    """Test shift hours calculation with partial hours."""
    shifts = [
        ShiftSchema(
            id=1, shift_name="Short", start_time=time(9, 30), end_time=time(14, 45)
        )
    ]

    scheduler = ShiftScheduler(
        sample_employees, shifts, ["Monday"], week=1, year=2024, max_solve_time=30
    )

    # 9:30 to 14:45 = 5 hours 15 minutes = 5.25 hours
    assert abs(scheduler.shift_hours[0] - 5.25) < 0.01


def test_shifts_overlap_detection(sample_employees, sample_shifts):
    """Test overlap detection between shifts."""
    scheduler = ShiftScheduler(
        sample_employees,
        sample_shifts,
        ["Monday"],
        week=1,
        year=2024,
        max_solve_time=30,
    )

    # Evening shift ends at 22:00 (>= 20:00) and Morning starts at 8:00 (<= 10:00)
    # These are considered overlapping to prevent consecutive shifts
    assert scheduler._shifts_overlap(1, 0) == True  # Evening to Morning overlaps

    # Night shift ends at 6:00 (< 20:00), so it won't trigger the overlap check
    # even though it ends close to when Morning starts
    assert (
        scheduler._shifts_overlap(2, 0) == False
    )  # Night to Morning - end time too early


def test_shifts_overlap_edge_cases(sample_employees):
    """Test edge cases for shift overlap detection."""
    shifts = [
        ShiftSchema(
            id=1, shift_name="Late", start_time=time(20, 0), end_time=time(23, 59)
        ),
        ShiftSchema(
            id=2, shift_name="Early", start_time=time(6, 0), end_time=time(10, 0)
        ),
        ShiftSchema(
            id=3, shift_name="Mid", start_time=time(11, 0), end_time=time(19, 0)
        ),
    ]

    scheduler = ShiftScheduler(
        sample_employees, shifts, ["Monday"], week=1, year=2024, max_solve_time=30
    )

    # Late (ends 23:59) to Early (starts 6:00) = overlaps
    assert scheduler._shifts_overlap(0, 1) == True

    # Late to Mid (starts 11:00) = no overlap
    assert scheduler._shifts_overlap(0, 2) == False

    # Mid to Early = no overlap
    assert scheduler._shifts_overlap(2, 1) == False


def test_create_variables(sample_employees, sample_shifts):
    """Test variable creation for constraint programming."""
    days = ["Monday", "Tuesday", "Wednesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=30
    )

    scheduler.create_variables()

    # Should create variables for each (employee, day, shift) combination
    expected_vars = len(sample_employees) * len(days) * len(sample_shifts)
    assert len(scheduler.assignments) == expected_vars

    # Check a specific variable exists
    first_emp = sample_employees[0]
    assert (first_emp.id, 0, 0) in scheduler.assignments


def test_solve_returns_valid_schedule(sample_employees, sample_shifts):
    """Test that solve returns a valid schedule."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    # Should find a solution with sufficient employees
    assert result is not None
    assert isinstance(result, ScheduleResponseSchema)
    assert result.status in ["optimal", "feasible"]
    assert result.week == 1
    assert result.year == 2024

    # Verify all days are in grid view
    assert len(result.grid_view.days) == len(days)
    for day in days:
        assert day in result.grid_view.days
        assert day in result.grid_view.shifts_by_day

    # Verify all shifts are in the flat list
    shift_names = {shift.shift_name for shift in sample_shifts}
    for day in days:
        day_shifts = result.grid_view.shifts_by_day[day].shifts
        for shift_name in shift_names:
            assert shift_name in day_shifts


def test_solve_respects_shift_coverage_constraint(sample_employees, sample_shifts):
    """Test that each shift has 1-2 employees assigned."""
    days = ["Monday", "Tuesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Check using grid view
        for day in days:
            day_data = result.grid_view.shifts_by_day[day]
            for shift_name, shift_info in day_data.shifts.items():
                # Each shift should have 1-2 employees
                num_employees = len(shift_info.employees)
                assert 1 <= num_employees <= 2, (
                    f"{day} {shift_name} has {num_employees} employees"
                )


def test_solve_respects_one_shift_per_day_constraint(sample_employees, sample_shifts):
    """Test that employees work at most one shift per day."""
    days = ["Monday", "Tuesday", "Wednesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        for day in days:
            employee_day_assignments = {}
            day_data = result.grid_view.shifts_by_day[day]
            for shift_name, shift_info in day_data.shifts.items():
                for emp_name in shift_info.employees:
                    if emp_name in employee_day_assignments:
                        pytest.fail(f"{emp_name} assigned to multiple shifts on {day}")
                    employee_day_assignments[emp_name] = shift_name


def test_solve_optimizes_target_hours(sample_employees, sample_shifts):
    """Test that solution attempts to match target hours."""
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        for emp_summary in result.summary:
            # With constraints, deviation might be larger, but should be reasonable
            # Each employee can work max 1 shift/day * 5 days = 5 shifts
            # Shifts are 6-8 hours, so max ~40 hours, some employees want 40, some 30-35
            # So deviations could be reasonable but not perfect
            assert abs(emp_summary.deviation) <= 40.0, (
                f"Employee {emp_summary.first_name} has deviation of {emp_summary.deviation}"
            )

            # Status should reflect the deviation
            if abs(emp_summary.deviation) < 0.01:
                assert emp_summary.status == "perfect"
            elif emp_summary.deviation > 0:
                assert emp_summary.status == "overtime"
            else:
                assert emp_summary.status == "undertime"


def test_build_response_structure(sample_employees, sample_shifts):
    """Test the structure of the built response."""
    days = ["Monday", "Tuesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Check top-level structure
        assert result.week == 1
        assert result.year == 2024
        
        # Check shifts (flat list) structure
        assert isinstance(result.shifts, list)
        assert len(result.shifts) > 0
        for shift in result.shifts:
            assert isinstance(shift, ScheduledShiftSchema)
            assert isinstance(shift.shift_id, int)
            assert shift.shift_id > 0
            assert isinstance(shift.employees, list)
            assert isinstance(shift.hours, float)
            assert shift.hours > 0
            assert isinstance(shift.date, str)
            assert isinstance(shift.day_name, str)

        # Check grid view structure
        assert isinstance(result.grid_view.days, list)
        assert isinstance(result.grid_view.dates, list)
        assert isinstance(result.grid_view.shifts_by_day, dict)

        # Check summary structure
        assert isinstance(result.summary, list)
        assert len(result.summary) == len(sample_employees)
        for emp_summary in result.summary:
            assert isinstance(emp_summary, EmployeeSummarySchema)
            assert emp_summary.target > 0
            assert emp_summary.actual >= 0
            assert emp_summary.status in ["perfect", "overtime", "undertime"]
            assert isinstance(emp_summary.shifts, dict)


def test_solve_with_insufficient_employees():
    """Test schedule generation with insufficient employees."""
    # Only 1 employee for multiple shifts per day
    single_employee = [
        EmployeeSchema(
            id=uuid.uuid4(),
            first_name="John",
            last_name="Doe",
            target_hours=168.0,  # Impossible to achieve
        )
    ]

    multiple_shifts = [
        ShiftSchema(
            id=1, shift_name="Morning", start_time=time(8, 0), end_time=time(16, 0)
        ),
        ShiftSchema(
            id=2, shift_name="Evening", start_time=time(16, 0), end_time=time(22, 0)
        ),
        ShiftSchema(
            id=3, shift_name="Night", start_time=time(22, 0), end_time=time(6, 0)
        ),
    ]

    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    scheduler = ShiftScheduler(
        single_employee, multiple_shifts, days, week=1, year=2024, max_solve_time=30
    )

    result = scheduler.solve()

    # Should return None or a suboptimal solution
    # (depends on constraints - each shift needs 1-2 employees but we only have 1)
    if result:
        # If it finds a solution, verify it's at least valid
        assert isinstance(result, ScheduleResponseSchema)


def test_solve_with_high_target_hours(sample_shifts):
    """Test with employees having very high target hours."""
    high_target_employees = [
        EmployeeSchema(
            id=uuid.uuid4(),
            first_name="Workaholic",
            last_name="One",
            target_hours=100.0,  # Unrealistically high
        ),
        EmployeeSchema(
            id=uuid.uuid4(),
            first_name="Workaholic",
            last_name="Two",
            target_hours=100.0,
        ),
    ]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    scheduler = ShiftScheduler(
        high_target_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        for emp_summary in result.summary:
            # Should show undertime since targets are unreachable
            assert emp_summary.status in ["undertime", "perfect", "overtime"]
            assert emp_summary.actual < emp_summary.target


def test_solve_with_varied_shift_lengths():
    """Test schedule with shifts of different lengths."""
    employees = [
        EmployeeSchema(
            id=uuid.uuid4(), first_name="A", last_name="B", target_hours=20.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="C", last_name="D", target_hours=20.0
        ),
        EmployeeSchema(
            id=uuid.uuid4(), first_name="E", last_name="F", target_hours=20.0
        ),
    ]

    varied_shifts = [
        ShiftSchema(
            id=1,
            shift_name="Short",
            start_time=time(9, 0),
            end_time=time(13, 0),  # 4 hours
        ),
        ShiftSchema(
            id=2,
            shift_name="Medium",
            start_time=time(13, 0),
            end_time=time(19, 0),  # 6 hours
        ),
        ShiftSchema(
            id=3,
            shift_name="Long",
            start_time=time(19, 0),
            end_time=time(3, 0),  # 8 hours (crosses midnight)
        ),
    ]

    days = ["Monday", "Tuesday", "Wednesday"]
    scheduler = ShiftScheduler(
        employees, varied_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Verify shift hours are calculated correctly using grid view
        for day_name, day_data in result.grid_view.shifts_by_day.items():
            for shift_name, shift_info in day_data.shifts.items():
                if shift_name == "Short":
                    assert shift_info.hours == 4.0
                elif shift_name == "Medium":
                    assert shift_info.hours == 6.0
                elif shift_name == "Long":
                    # Long shift crosses midnight: 19:00 to 03:00 = 8 hours
                    assert shift_info.hours == 8.0


def test_employee_summary_shift_counts(sample_employees, sample_shifts):
    """Test that employee summaries include correct shift counts."""
    days = ["Monday", "Tuesday", "Wednesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        for emp_summary in result.summary:
            # Shift counts should sum to total shifts worked
            total_shifts = sum(emp_summary.shifts.values())
            assert total_shifts >= 0

            # Each shift type should be in the summary
            for shift in sample_shifts:
                assert shift.shift_name in emp_summary.shifts


def test_solve_timeout_handling(sample_employees, sample_shifts):
    """Test behavior when solver times out."""
    # Use a very short timeout
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=1
    )

    result = scheduler.solve()

    # Should either return None or a feasible (not optimal) solution
    if result:
        assert result.status in ["feasible", "optimal"]


def test_consecutive_night_shift_constraint(sample_employees, sample_shifts):
    """Test that no employee works 3+ consecutive night shifts."""
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Check night shift constraint for each employee
        night_shift_name = "Night"

        for emp in sample_employees:
            emp_full_name = f"{emp.first_name} {emp.last_name}"
            consecutive_nights = 0

            for day in days:
                if day in result.grid_view.shifts_by_day:
                    day_data = result.grid_view.shifts_by_day[day]
                    if night_shift_name in day_data.shifts:
                        if emp_full_name in day_data.shifts[night_shift_name].employees:
                            consecutive_nights += 1
                            assert consecutive_nights < 3, (
                                f"{emp_full_name} has {consecutive_nights} consecutive night shifts"
                            )
                        else:
                            consecutive_nights = 0
                    else:
                        consecutive_nights = 0


# ==================== Edge Cases ====================


def test_empty_employees_list(sample_shifts):
    """Test behavior with empty employees list."""
    scheduler = ShiftScheduler(
        [], sample_shifts, ["Monday"], week=1, year=2024, max_solve_time=30
    )
    result = scheduler.solve()

    # Should return None since no employees available
    assert result is None


def test_empty_shifts_list(sample_employees):
    """Test behavior with empty shifts list."""
    scheduler = ShiftScheduler(
        sample_employees, [], ["Monday"], week=1, year=2024, max_solve_time=30
    )
    result = scheduler.solve()

    # Should return a schedule (though empty)
    assert result is not None


def test_single_day_schedule(sample_employees, sample_shifts):
    """Test schedule generation for a single day."""
    scheduler = ShiftScheduler(
        sample_employees,
        sample_shifts,
        ["Monday"],
        week=1,
        year=2024,
        max_solve_time=30,
    )
    result = scheduler.solve()

    if result:
        assert len(result.grid_view.days) == 1
        assert "Monday" in result.grid_view.days
        assert "Monday" in result.grid_view.shifts_by_day


def test_full_week_schedule(sample_employees, sample_shifts):
    """Test schedule generation for a full week."""
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=90
    )

    result = scheduler.solve()

    assert result is not None
    assert len(result.grid_view.days) == 7

    # Verify each day has all shifts in grid view
    for day in days:
        assert day in result.grid_view.days
        assert day in result.grid_view.shifts_by_day
        day_data = result.grid_view.shifts_by_day[day]
        for shift in sample_shifts:
            assert shift.shift_name in day_data.shifts


def test_shift_id_in_response(sample_employees, sample_shifts):
    """Test that shift_id from request is included in response."""
    days = ["Monday", "Tuesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=1, year=2024, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Create a mapping of shift_name to shift_id from the request
        shift_id_map = {shift.shift_name: shift.id for shift in sample_shifts}

        # Verify each shift in the flat list has the correct shift_id
        for shift in result.shifts:
            expected_shift_id = shift_id_map[shift.shift_name]
            assert shift.shift_id == expected_shift_id, (
                f"Shift {shift.shift_name} on {shift.day_name} has ID {shift.shift_id}, expected {expected_shift_id}"
            )


def test_datetime_from_iso_week(sample_employees, sample_shifts):
    """Test that datetimes are correctly calculated from ISO week number."""
    week = 45  # Week 45 of 2025
    year = 2025
    days = ["Monday", "Tuesday"]
    scheduler = ShiftScheduler(
        sample_employees, sample_shifts, days, week=week, year=year, max_solve_time=60
    )

    result = scheduler.solve()

    if result:
        # Week 45 of 2025 starts on Monday, November 3, 2025
        # Verify the dates are correct using flat shifts list
        monday_shifts = [s for s in result.shifts if s.day_name == "Monday"]
        tuesday_shifts = [s for s in result.shifts if s.day_name == "Tuesday"]

        for shift in monday_shifts:
            # Check that start_time and end_time are datetime objects
            assert isinstance(shift.start_time, datetime)
            assert isinstance(shift.end_time, datetime)

            # Verify year and month
            assert shift.start_time.year == 2025
            assert shift.start_time.month == 11
            assert shift.start_time.day == 3  # Monday Nov 3

        for shift in tuesday_shifts:
            assert isinstance(shift.start_time, datetime)
            assert isinstance(shift.end_time, datetime)
            assert shift.start_time.year == 2025
            assert shift.start_time.month == 11
            assert shift.start_time.day == 4  # Tuesday Nov 4
