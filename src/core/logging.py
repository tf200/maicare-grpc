"""
Logging Configuration
Migrated from: config/logging_config.py
"""

import logging
import logging.config
from pathlib import Path
from typing import Optional


def setup_logging(env: str = "development", log_level: str = "INFO"):
    """
    Set up logging configuration for the application

    Args:
        env: Environment (development, production, testing)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """

    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Base configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s - %(name)s - %(message)s"},
            "json": {
                "format": '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "file": "%(filename)s", "line": %(lineno)d, "message": "%(message)s"}',
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level,
                "formatter": "detailed" if env == "development" else "simple",
                "stream": "ext://sys.stdout",
            }
        },
        "root": {"level": log_level, "handlers": ["console"]},
        "loggers": {
            "grpc": {"level": "WARNING", "propagate": True},
            "urllib3": {"level": "WARNING", "propagate": True},
        },
    }

    # Add file handlers for production
    if env == "production":
        config["handlers"].update(
            {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "detailed",
                    "filename": log_dir / "app.log",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "encoding": "utf8",
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "ERROR",
                    "formatter": "detailed",
                    "filename": log_dir / "error.log",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "encoding": "utf8",
                },
                "json_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "INFO",
                    "formatter": "json",
                    "filename": log_dir / "app.json",
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "encoding": "utf8",
                },
            }
        )

        # Update root handler to include file handlers
        config["root"]["handlers"] = ["console", "file", "error_file", "json_file"]

        # Console should be less verbose in production
        config["handlers"]["console"]["level"] = "WARNING"

    # Apply the configuration
    logging.config.dictConfig(config)

    # Log the configuration
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured for {env} environment with level {log_level}")


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance

    Args:
        name: Logger name (usually __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
