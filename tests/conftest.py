# tests/conftest.py
"""Pytest configuration and shared fixtures for all tests."""

from concurrent import futures

import grpc
import pytest
from injector import Injector

from src.api.spelling_check import SpellingCheckServicer
from src.api.care_planner import CarePlannerServicer
from src.di.app_module import AppModule, ServiceModule
import generated.spelling_service_pb2_grpc as spelling_check_pb2_grpc
import generated.service_pb2_grpc as care_planner_pb2_grpc


@pytest.fixture(scope="session")
def injector():
    """Create a dependency injection container for tests."""
    return Injector([AppModule(), ServiceModule()])


@pytest.fixture(scope="session")
def grpc_server(injector):
    """
    Spin up a *real* grpc server on a free port and yield a connected channel.
    Fixtures that depend on it get a channel that is already connected.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))

    # Get servicers from injector
    spelling_servicer = injector.get(SpellingCheckServicer)
    care_planner_servicer = injector.get(CarePlannerServicer)

    spelling_check_pb2_grpc.add_SpellingCorrectionServicer_to_server(
        spelling_servicer, server
    )
    care_planner_pb2_grpc.add_CarePlannerServicer_to_server(
        care_planner_servicer, server
    )

    # pick free port
    port = server.add_insecure_port("localhost:0")
    server.start()

    channel = grpc.insecure_channel(f"localhost:{port}")
    yield channel

    server.stop(grace=None)
    channel.close()


@pytest.fixture
def spelling_stub(grpc_server):
    """Ready-to-use spelling_check gRPC stub."""
    return spelling_check_pb2_grpc.SpellingCorrectionStub(grpc_server)


@pytest.fixture
def care_planner_stub(grpc_server):
    """Ready-to-use care_planner gRPC stub."""
    return care_planner_pb2_grpc.CarePlannerStub(grpc_server)
