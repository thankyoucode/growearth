# app/src/logging_config.py
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional, Union

from django.conf import settings
from django.utils import timezone


class LoggerConfig:
    """
    Centralized logging configuration utility
    """

    @staticmethod
    def create_logs_directory() -> str:
        """
        Create logs directory if it doesn't exist

        Returns:
            str: Path to the logs directory
        """
        log_dir = os.path.join(settings.BASE_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    @staticmethod
    def get_formatter() -> logging.Formatter:
        """
        Create a standard log formatter

        Returns:
            logging.Formatter: Configured log formatter
        """
        return logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    @classmethod
    def setup_logger(
        cls,
        name: str,
        log_level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,
        backup_count: int = 5,
    ) -> logging.Logger:
        """
        Configure a logger with rotating file and console handlers

        Args:
            name (str): Name of the logger
            log_level (int, optional): Logging level. Defaults to logging.INFO.
            max_bytes (int, optional): Max log file size. Defaults to 10MB.
            backup_count (int, optional): Number of backup log files. Defaults to 5.

        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory
        log_dir = cls.create_logs_directory()

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(log_level)

        # Clear existing handlers to prevent duplicate logs
        logger.handlers.clear()

        # Formatter
        formatter = cls.get_formatter()

        # File Handler
        log_file = os.path.join(log_dir, f"{name}.log")
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger


class SecurityLogger:
    """
    Specialized security event logging
    """

    @staticmethod
    def log_event(
        event_type: str, details: Union[dict, str], level: int = logging.INFO
    ) -> None:
        """
        Log security-related events with structured information

        Args:
            event_type (str): Type of security event
            details (Union[dict, str]): Event details
            level (int, optional): Log level. Defaults to logging.INFO.
        """
        logger = LoggerConfig.setup_logger("security_events")
        log_entry = {
            "timestamp": timezone.now().isoformat(),
            "event_type": event_type,
            "details": details,
        }
        logger.log(level, str(log_entry))
