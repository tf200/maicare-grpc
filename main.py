# server.py
import os
import grpc
import signal
import sys
from concurrent import futures
import generated.service_pb2_grpc as care_planner_pb2_grpc
import generated.spelling_service_pb2_grpc as spelling_service_pb2_grpc
from care_planner.planner import CarePlannerService
from spelling_check.service import SpellingCheckService

# Import logging config first
from config.logging_config import setup_logging, get_logger
from config.env_config import get_config

# Set up logging before importing other modules
config = get_config()
setup_logging(env=config.environment, log_level=config.log_level)

# Now import other modules that might use logging


# Get logger for this module
logger = get_logger(__name__)


def serve(port=50051, max_workers=4):
    """Start the gRPC server"""
    logger.info(f"Starting server with {max_workers} workers on port {port}")

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

    care_planner_pb2_grpc.add_CarePlannerServicer_to_server(CarePlannerService(), server)
    spelling_service_pb2_grpc.add_SpellingCorrectionServicer_to_server(SpellingCheckService(), server)



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
