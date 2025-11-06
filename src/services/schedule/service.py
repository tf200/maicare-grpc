from logging import Logger
from typing import Optional
from injector import inject
from ortools.sat.python import cp_model

from src.services.schedule.schema import (
    EmployeeSchema,
    ShiftSchema,
    ScheduleResponseSchema,
    ScheduledShiftSchema,
    GridViewSchema,
    GridDaySchema,
    GridShiftSchema,
    EmployeeSummarySchema,
    AssignedEmployeeSchema,
)


class ScheduleService:
    DAYS = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    @inject
    def __init__(self, logger: Logger):
        self.logger = logger
        self.model = cp_model.CpModel()
        self.assignments = {}

    def generate_schedule(
        self,
        employees: list[EmployeeSchema],
        shifts: list[ShiftSchema],
        week: int,
        year: int,
    ):
        self.logger.info(f"Generating schedule for week {week}, {year}")

        scheduler = ShiftScheduler(
            employees, shifts, self.DAYS, week, year, max_solve_time=90
        )
        result = scheduler.solve()

        if result:
            self.logger.info("Schedule generated successfully.")
        else:
            self.logger.warning("No feasible schedule found.")

        return result


class ShiftScheduler:
    def __init__(
        self,
        employees: list[EmployeeSchema],
        shifts: list[ShiftSchema],
        days: list[str],
        week: int,
        year: int,
        max_solve_time: int = 30,
    ):
        self.employees = employees
        self.shifts = shifts
        self.days = days
        self.week = week
        self.year = year
        self.model = cp_model.CpModel()
        self.assignments = {}
        self.max_solve_time = max_solve_time

        self.shift_hours = [self._calculate_shift_hours(s) for s in shifts]

    def _calculate_shift_hours(self, shift: ShiftSchema) -> float:
        """Calculate shift duration in hours using time objects"""
        start = shift.start_time
        end = shift.end_time

        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute

        # Handle shifts that cross midnight
        if end_minutes < start_minutes:
            # Shift crosses midnight - add 24 hours (1440 minutes) to end time
            return (end_minutes + 1440 - start_minutes) / 60.0

        return (end_minutes - start_minutes) / 60.0

    def _get_date_from_iso_week(self, year: int, week: int, day_idx: int):
        """
        Get the actual date from ISO week number and day index.

        Args:
            year: ISO year
            week: ISO week number (1-53)
            day_idx: Day index (0=Monday, 6=Sunday)

        Returns:
            datetime.date object for that day
        """
        import datetime

        # Get the first day of the ISO week
        jan4 = datetime.date(year, 1, 4)  # January 4th is always in week 1
        week_start = jan4 - datetime.timedelta(days=jan4.isoweekday() - 1)
        target_week_start = week_start + datetime.timedelta(weeks=week - 1)
        return target_week_start + datetime.timedelta(days=day_idx)

    def _combine_date_time(self, date, time):
        """
        Combine a date and time into a datetime object.

        Args:
            date: datetime.date object
            time: datetime.time object

        Returns:
            datetime.datetime object
        """
        import datetime

        return datetime.datetime.combine(date, time)

    def create_variables(self) -> None:
        for emp in self.employees:
            for day_idx in range(len(self.days)):
                for shift_idx in range(len(self.shifts)):
                    var_name = f"{emp.id}_{self.days[day_idx]}_{self.shifts[shift_idx].shift_name}"
                    self.assignments[(emp.id, day_idx, shift_idx)] = (
                        self.model.NewBoolVar(var_name)
                    )

    def add_constraints(self) -> None:
        """Add all scheduling constraints"""

        # CONSTRAINT 1: Each shift must have 1-2 employees
        for day_idx in range(len(self.days)):
            for shift_idx in range(len(self.shifts)):
                shift_assignments = [
                    self.assignments[(emp.id, day_idx, shift_idx)]
                    for emp in self.employees
                ]
                self.model.Add(sum(shift_assignments) >= 1)  # At least 1
                self.model.Add(sum(shift_assignments) <= 2)  # At most 2

        # CONSTRAINT 2: Maximum one shift per day per employee
        for emp in self.employees:
            for day_idx in range(len(self.days)):
                day_shifts = [
                    self.assignments[(emp.id, day_idx, shift_idx)]
                    for shift_idx in range(len(self.shifts))
                ]
                self.model.Add(sum(day_shifts) <= 1)

        # CONSTRAINT 3: No consecutive shifts (check for overlapping times)
        for emp in self.employees:
            for day_idx in range(len(self.days) - 1):
                for shift_idx in range(len(self.shifts)):
                    for next_shift_idx in range(len(self.shifts)):
                        # Check if shift ends after midnight and next shift starts early
                        if self._shifts_overlap(shift_idx, next_shift_idx):
                            curr_shift = self.assignments[(emp.id, day_idx, shift_idx)]
                            next_shift = self.assignments[
                                (emp.id, day_idx + 1, next_shift_idx)
                            ]
                            self.model.Add(curr_shift + next_shift <= 1)

        # CONSTRAINT 4: No 3 consecutive shifts of the same type (if there's a "Night" shift)
        night_shifts = [i for i, s in enumerate(self.shifts) if s.start_time.hour >= 21]
        if night_shifts:
            night_idx = night_shifts[0]
            for emp in self.employees:
                for day_idx in range(len(self.days) - 2):
                    night_shift_vars = [
                        self.assignments[(emp.id, day_idx + i, night_idx)]
                        for i in range(3)
                    ]
                    self.model.Add(sum(night_shift_vars) <= 2)

    def _shifts_overlap(self, shift1_idx: int, shift2_idx: int) -> bool:
        """Check if shift1 ending late and shift2 starting early would be too close"""
        shift1 = self.shifts[shift1_idx]
        shift2 = self.shifts[shift2_idx]

        end1 = shift1.end_time  # time object
        start2 = shift2.start_time  # time object

        # If shift1 ends after 20:00 and shift2 starts before 10:00, consider them overlapping
        if end1.hour >= 20 and start2.hour <= 10:
            return True

        return False

    def add_objectives(self) -> None:
        """Add soft constraints as objectives to minimize"""
        deviation_vars = []

        for emp in self.employees:
            # Calculate total hours worked (each shift has different hours)
            total_hours = sum(
                self.assignments[(emp.id, day_idx, shift_idx)]
                * self.shift_hours[shift_idx]
                for day_idx in range(len(self.days))
                for shift_idx in range(len(self.shifts))
            )
            target = emp.target_hours

            # Create variable for deviation from target
            deviation = self.model.NewIntVar(0, 1000, f"deviation_{emp.id}")

            # deviation = |total_hours - target| (scaled by 10 for integer precision)
            scaled_hours = sum(
                self.assignments[(emp.id, day_idx, shift_idx)]
                * int(self.shift_hours[shift_idx] * 10)
                for day_idx in range(len(self.days))
                for shift_idx in range(len(self.shifts))
            )
            self.model.AddAbsEquality(deviation, scaled_hours - int(target * 10))
            deviation_vars.append(deviation)

        # Minimize total deviation
        self.model.Minimize(sum(deviation_vars))

    def solve(self) -> Optional[ScheduleResponseSchema]:
        """Solve the constraint programming model"""
        self.create_variables()
        self.add_constraints()
        self.add_objectives()

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.max_solve_time

        status = solver.Solve(self.model)

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return self._build_response(solver, status)  # type: ignore
        else:
            return None

    def _build_response(
        self, solver: cp_model.CpSolver, status: int
    ) -> ScheduleResponseSchema:
        """Build hybrid response with flat shifts list and grid view"""

        # Build flat shifts list for database
        shifts_list = []

        # Build grid view for frontend
        grid_days = []
        grid_dates = []
        grid_shifts_by_day = {}

        for day_idx, day in enumerate(self.days):
            # Calculate the actual date for this day using ISO week
            date_for_day = self._get_date_from_iso_week(self.year, self.week, day_idx)
            date_str = date_for_day.isoformat()  # "2025-02-03"

            grid_days.append(day)
            grid_dates.append(date_str)

            # Initialize grid day
            grid_day_shifts = {}

            for shift_idx, shift in enumerate(self.shifts):
                assigned = []
                for emp in self.employees:
                    if (
                        solver.Value(self.assignments[(emp.id, day_idx, shift_idx)])
                        == 1
                    ):
                        assigned.append(
                            AssignedEmployeeSchema(
                                id=emp.id, name=f"{emp.first_name} {emp.last_name}"
                            )
                        )

                # Combine date with time to create datetime objects
                start_datetime = self._combine_date_time(date_for_day, shift.start_time)
                end_datetime = self._combine_date_time(date_for_day, shift.end_time)

                # If end time is before start time, shift crosses midnight
                if shift.end_time < shift.start_time:
                    end_datetime = end_datetime.replace(day=end_datetime.day + 1)

                # Add to flat shifts list
                shifts_list.append(
                    ScheduledShiftSchema(
                        date=date_str,
                        day_name=day,
                        shift_id=shift.id,
                        shift_name=shift.shift_name,
                        start_time=start_datetime,
                        end_time=end_datetime,
                        hours=self.shift_hours[shift_idx],
                        employees=assigned,
                    )
                )

                # Add to grid view (compact format)
                employee_names = [emp.name for emp in assigned]
                grid_day_shifts[shift.shift_name] = GridShiftSchema(
                    employees=employee_names,
                    hours=self.shift_hours[shift_idx],
                    start=shift.start_time.strftime("%H:%M"),
                    end=shift.end_time.strftime("%H:%M"),
                )

            # Add day to grid
            grid_shifts_by_day[day] = GridDaySchema(
                date=date_str,
                shifts=grid_day_shifts,
            )

        # Build grid view
        grid_view = GridViewSchema(
            days=grid_days,
            dates=grid_dates,
            shifts_by_day=grid_shifts_by_day,
        )

        # Build summary
        summary = []
        for emp in self.employees:
            actual_hours = sum(
                solver.Value(self.assignments[(emp.id, day_idx, shift_idx)])
                * self.shift_hours[shift_idx]
                for day_idx in range(len(self.days))
                for shift_idx in range(len(self.shifts))
            )
            target = emp.target_hours
            deviation = actual_hours - target

            # Count shift types
            shift_counts = {}
            for shift_idx, shift in enumerate(self.shifts):
                count = sum(
                    solver.Value(self.assignments[(emp.id, day_idx, shift_idx)])
                    for day_idx in range(len(self.days))
                )
                shift_counts[shift.shift_name] = count

            status_str = (
                "perfect"
                if abs(deviation) < 0.01
                else "overtime"
                if deviation > 0
                else "undertime"
            )

            summary.append(
                EmployeeSummarySchema(
                    id=emp.id,
                    first_name=emp.first_name,
                    last_name=emp.last_name,
                    target=target,
                    actual=round(actual_hours, 2),
                    deviation=round(deviation, 2),
                    status=status_str,
                    shifts=shift_counts,
                )
            )

        return ScheduleResponseSchema(
            status="optimal" if status == cp_model.OPTIMAL else "feasible",
            week=self.week,
            year=self.year,
            shifts=shifts_list,
            grid_view=grid_view,
            summary=summary,
        )
