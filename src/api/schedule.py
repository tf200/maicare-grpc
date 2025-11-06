"""
Schedule gRPC Service
Thin gRPC layer for employee shift scheduling
"""

from logging import Logger
from datetime import datetime
import uuid
import grpc
from injector import inject
import generated.schedule_service_pb2 as pb2
import generated.schedule_service_pb2_grpc as pb2_grpc

from src.services.schedule.service import ScheduleService
from src.services.schedule.schema import (
    EmployeeSchema,
    ShiftSchema,
    ScheduleResponseSchema,
)


class ScheduleServicer(pb2_grpc.ScheduleServiceServicer):
    """
    gRPC servicer for Schedule Generation.
    Thin layer that maps protobuf <-> domain models and delegates to service layer.
    """

    @inject
    def __init__(self, schedule_service: ScheduleService, logger: Logger):
        """Initialize with business service and dependencies"""
        self.business_service = schedule_service
        self.logger = logger
        self.logger.info("ScheduleServicer initialized")

    def GenerateSchedule(self, request: pb2.GenerateScheduleRequest, context):
        """
        Handle gRPC GenerateSchedule request.

        Args:
            request: GenerateScheduleRequest protobuf message
            context: gRPC context

        Returns:
            GenerateScheduleResponse protobuf message
        """
        self.logger.info(
            f"Received GenerateSchedule request for week {request.week}, year {request.year}"
        )

        try:
            # Map protobuf request to domain models
            employees = self._map_employees_to_domain(request.employees)
            shifts = self._map_shifts_to_domain(request.shifts)

            # Delegate to business service
            schedule_result = self.business_service.generate_schedule(
                employees=employees, shifts=shifts, week=request.week, year=request.year
            )

            if schedule_result is None:
                self.logger.warning("No feasible schedule found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(
                    "No feasible schedule could be generated with the given constraints"
                )
                raise grpc.RpcError("No feasible schedule found")

            # Map domain model to protobuf response
            response = self._map_domain_to_response(schedule_result)

            self.logger.info(
                f"Schedule generated successfully with status: {schedule_result.status}"
            )
            return response

        except grpc.RpcError:
            # Re-raise gRPC errors as-is
            raise
        except Exception as e:
            self.logger.error(f"Error in GenerateSchedule: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to generate schedule: {str(e)}")
            raise

    def _map_employees_to_domain(self, pb_employees) -> list[EmployeeSchema]:
        """
        Map protobuf Employee messages to domain EmployeeSchema.

        Args:
            pb_employees: List of protobuf Employee messages

        Returns:
            List of EmployeeSchema objects
        """
        employees = []
        for emp in pb_employees:
            employees.append(
                EmployeeSchema(
                    id=uuid.UUID(emp.id),
                    first_name=emp.first_name,
                    last_name=emp.last_name,
                    target_hours=emp.target_hours,
                )
            )
        return employees

    def _map_shifts_to_domain(self, pb_shifts) -> list[ShiftSchema]:
        """
        Map protobuf Shift messages to domain ShiftSchema.

        Args:
            pb_shifts: List of protobuf Shift messages

        Returns:
            List of ShiftSchema objects
        """
        shifts = []
        for shift in pb_shifts:
            # Parse time strings in HH:MM format
            start_time = datetime.strptime(shift.start_time, "%H:%M").time()
            end_time = datetime.strptime(shift.end_time, "%H:%M").time()

            shifts.append(
                ShiftSchema(
                    id=shift.id,
                    shift_name=shift.shift_name,
                    start_time=start_time,
                    end_time=end_time,
                )
            )
        return shifts

    def _map_domain_to_response(
        self, schedule_result: ScheduleResponseSchema
    ) -> pb2.GenerateScheduleResponse:
        """
        Map domain ScheduleResponseSchema to protobuf response.

        Args:
            schedule_result: Domain model with schedule and summary

        Returns:
            GenerateScheduleResponse protobuf message
        """
        # Build flat shifts list
        pb_shifts = []
        for shift in schedule_result.shifts:
            pb_employees = [
                pb2.AssignedEmployee(id=str(emp.id), name=emp.name)
                for emp in shift.employees
            ]

            pb_shifts.append(
                pb2.ScheduledShift(
                    date=shift.date,
                    day_name=shift.day_name,
                    shift_id=shift.shift_id,
                    shift_name=shift.shift_name,
                    start_time=shift.start_time.isoformat(),
                    end_time=shift.end_time.isoformat(),
                    hours=shift.hours,
                    employees=pb_employees,
                )
            )

        # Build grid view
        grid_shifts_by_day = {}
        for day_name, grid_day in schedule_result.grid_view.shifts_by_day.items():
            grid_shifts_map = {}
            for shift_name, grid_shift in grid_day.shifts.items():
                grid_shifts_map[shift_name] = pb2.GridShift(
                    employees=grid_shift.employees,
                    hours=grid_shift.hours,
                    start=grid_shift.start,
                    end=grid_shift.end,
                )
            grid_shifts_by_day[day_name] = pb2.GridDay(
                date=grid_day.date,
                shifts=grid_shifts_map,
            )

        pb_grid_view = pb2.GridView(
            days=schedule_result.grid_view.days,
            dates=schedule_result.grid_view.dates,
            shifts_by_day=grid_shifts_by_day,
        )

        # Build summary list
        summary_list = []
        for emp_summary in schedule_result.summary:
            summary_list.append(
                pb2.EmployeeSummary(
                    id=str(emp_summary.id),
                    first_name=emp_summary.first_name,
                    last_name=emp_summary.last_name,
                    target=emp_summary.target,
                    actual=emp_summary.actual,
                    deviation=emp_summary.deviation,
                    status=emp_summary.status,
                    shifts=emp_summary.shifts,
                )
            )

        return pb2.GenerateScheduleResponse(
            status=schedule_result.status,
            week=schedule_result.week,
            year=schedule_result.year,
            shifts=pb_shifts,
            grid_view=pb_grid_view,
            summary=summary_list,
        )
