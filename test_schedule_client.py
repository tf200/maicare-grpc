#!/usr/bin/env python3
"""
Test client for Schedule Service to verify the response structure
"""

import grpc
import json
from google.protobuf.json_format import MessageToDict
import generated.schedule_service_pb2 as pb2
import generated.schedule_service_pb2_grpc as pb2_grpc


def test_schedule_service():
    # Create a channel to the server
    channel = grpc.insecure_channel("localhost:50051")
    stub = pb2_grpc.ScheduleServiceStub(channel)

    # Create test request
    request = pb2.GenerateScheduleRequest(
        employees=[
            pb2.Employee(
                id="123e4567-e89b-12d3-a456-426614174000",
                first_name="John",
                last_name="Doe",
                target_hours=40.0,
            ),
            pb2.Employee(
                id="223e4567-e89b-12d3-a456-426614174001",
                first_name="Jane",
                last_name="Smith",
                target_hours=35.0,
            ),
            pb2.Employee(
                id="323e4567-e89b-12d3-a456-426614174002",
                first_name="Bob",
                last_name="Johnson",
                target_hours=30.0,
            ),
        ],
        shifts=[
            pb2.Shift(id=1, shift_name="Morning", start_time="08:00", end_time="16:00"),
            pb2.Shift(id=2, shift_name="Evening", start_time="16:00", end_time="00:00"),
            pb2.Shift(id=3, shift_name="Night", start_time="00:00", end_time="08:00"),
        ],
        week=45,
        year=2025,
    )

    print("Sending request to GenerateSchedule...")
    try:
        response = stub.GenerateSchedule(request)

        # Convert to dictionary for better viewing
        response_dict = MessageToDict(response, preserving_proto_field_name=True)

        print("\n" + "=" * 80)
        print("RESPONSE (as JSON):")
        print("=" * 80)
        print(json.dumps(response_dict, indent=2))

        # Show employee structure specifically
        print("\n" + "=" * 80)
        print("EMPLOYEE STRUCTURE IN SHIFTS:")
        print("=" * 80)
        for day_name, day_schedule in response_dict.get("schedule", {}).items():
            print(f"\n{day_name}:")
            for shift_name, shift_assignment in day_schedule.get("shifts", {}).items():
                print(f"  {shift_name}:")
                print(f"    shift_id: {shift_assignment.get('shift_id')}")
                print(f"    employees:")
                for emp in shift_assignment.get("employees", []):
                    print(f"      - id: {emp.get('id')}")
                    print(f"        name: {emp.get('name')}")
                print(f"    hours: {shift_assignment.get('hours')}")

    except grpc.RpcError as e:
        print(f"Error: {e.code()}: {e.details()}")
        return

    channel.close()


if __name__ == "__main__":
    test_schedule_service()
