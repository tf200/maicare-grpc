# tests/conftest.py
import os
import tempfile
from concurrent import futures
from unittest import mock

import grpc
import pytest
from grpc_health.v1 import health_pb2_grpc

from spelling_check.service import SpellingCheckService
from care_planner.planner import CarePlannerService
import generated.spelling_service_pb2_grpc as spelling_check_pb2_grpc
import generated.service_pb2_grpc as care_planner_pb2_grpc


@pytest.fixture(scope="session")
def grpc_server():
    """
    Spin up a *real* grpc server on a free port and yield a connected channel.
    Fixtures that depend on it get a channel that is already connected.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    spelling_check_pb2_grpc.add_SpellingCorrectionServicer_to_server(
        SpellingCheckService(), server
    )
    care_planner_pb2_grpc.add_CarePlannerServicer_to_server(
        CarePlannerService(), server
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