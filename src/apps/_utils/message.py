from enum import Enum

from django.contrib import messages


class MessageType(Enum):
    SUCCESS = "alert-success"
    ERROR = "alert-danger"
    WARNING = "alert-warning"
    INFO = "alert-info"


class MessageService:
    @staticmethod
    def add_message(request, message_type: MessageType, text: str):
        """
        Standardized message display method

        Args:
            request: Django request object
            message_type: MessageType enum
            text: Message text
        """
        messages.add_message(
            request,
            getattr(messages, message_type.name),
            text,
            extra_tags=message_type.value,
        )

    @classmethod
    def success(cls, request, text: str):
        """Convenience method for success messages"""
        cls.add_message(request, MessageType.SUCCESS, text)

    @classmethod
    def error(cls, request, text: str):
        """Convenience method for error messages"""
        cls.add_message(request, MessageType.ERROR, text)

    @classmethod
    def warning(cls, request, text: str):
        """Convenience method for warning messages"""
        cls.add_message(request, MessageType.WARNING, text)

    @classmethod
    def info(cls, request, text: str):
        """Convenience method for info messages"""
        cls.add_message(request, MessageType.INFO, text)
