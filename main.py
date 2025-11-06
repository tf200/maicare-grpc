# server.py
import logging
import os
import grpc
import signal
import sys
from concurrent import futures
from injector import Injector

import generated.service_pb2_grpc as care_planner_pb2_grpc
import generated.spelling_service_pb2_grpc as spelling_service_pb2_grpc
import generated.reports_service_pb2_grpc as reports_service_pb2_grpc
import generated.schedule_service_pb2_grpc as schedule_service_pb2_grpc

# Import from new API layer
from src.api.care_planner import CarePlannerServicer
from src.api.reports import AutoReportGeneratorServicer
from src.api.spelling_check import SpellingCheckServicer
from src.api.schedule import ScheduleServicer

# Import DI modules
from src.di.app_module import AppModule, ServiceModule

# Import logging config first
from src.core.logging import get_logger

injector = Injector([AppModule(), ServiceModule()])
# Set up logging before importing other modules

config = injector.get(AppModule).provide_config()
logger: logging.Logger = injector.get(logging.Logger)

# Now import other modules that might use logging


# Get logger for this module
logger = get_logger(__name__)


def serve(port=50051, max_workers=4):
    """Start the gRPC server"""
    logger.info(f"Starting server with {max_workers} workers on port {port}")

    # Set up dependency injection

    # Create servicers using DI container
    care_planner_servicer = injector.get(CarePlannerServicer)
    spelling_servicer = injector.get(SpellingCheckServicer)
    auto_report_servicer = injector.get(AutoReportGeneratorServicer)
    schedule_servicer = injector.get(ScheduleServicer)

    server: grpc.Server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[
            ("grpc.keepalive_time_ms", 30000),
            ("grpc.keepalive_timeout_ms", 5000),
            ("grpc.keepalive_permit_without_calls", True),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.http2.min_time_between_pings_ms", 10000),
            ("grpc.http2.min_ping_interval_without_data_ms", 300000),
        ],
    )

    care_planner_pb2_grpc.add_CarePlannerServicer_to_server(
        care_planner_servicer, server
    )
    spelling_service_pb2_grpc.add_SpellingCorrectionServicer_to_server(
        spelling_servicer, server
    )
    reports_service_pb2_grpc.add_ReportGeneratorServicer_to_server(
        auto_report_servicer, server
    )
    schedule_service_pb2_grpc.add_ScheduleServiceServicer_to_server(
        schedule_servicer, server
    )

    try:
        listen_address = f"[::]:{port}"
        server.add_insecure_port(listen_address)
        server.start()
        logger.info(f"✅ Server started successfully on {listen_address}")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}", exc_info=True)
        return

    def signal_handler(signum, frame):
        logger.info("🛑 Received shutdown signal, gracefully stopping...")
        server.stop(grace=30)  # 30 second grace period
        logger.info("🛑 Server stopped")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        logger.info("Server waiting for requests...")
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("🛑 Server interrupted by user, stopping...")
        server.stop(grace=30)
        logger.info("🛑 Server stopped")


if __name__ == "__main__":
    # You can also pass these as command line arguments
    port = int(os.getenv("PORT", 50051))
    max_workers = int(os.getenv("MAX_WORKERS", 10))

    logger.info(f"Environment: {config.environment}")
    logger.info(f"Log Level: {config.log_level}")

    serve(port=port, max_workers=max_workers)
