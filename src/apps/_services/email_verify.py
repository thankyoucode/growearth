import logging
import secrets
from typing import Optional, TypeVar, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .logging_config import LoggerConfig

# Type Variable for User Model
UserModelType = TypeVar("UserModelType", bound=AbstractBaseUser)

# Get the current user model dynamically
User = get_user_model()

# Setup Logger
logger = LoggerConfig.setup_logger("email_verification")


class EmailVerificationService:
    """
    Comprehensive email verification service for Grow Earth platform
    """

    @staticmethod
    def generate_verification_code(
        user_id: int, length: int = 6, expiration: int = 600
    ) -> str:
        """
        Generate a secure verification code for a specific user

        Args:
            user_id (int): Unique identifier for the user
            length (int, optional): Length of verification code. Defaults to 6.
            expiration (int, optional): Code expiration time in seconds. Defaults to 10 minutes.

        Returns:
            str: Generated verification code
        """
        try:
            # Generate cryptographically secure code
            code = "".join(
                secrets.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                for _ in range(length)
            )

            # Cache the code with specified expiration
            cache_key = f"verification_code_{user_id}"
            cache.set(cache_key, code, timeout=expiration)

            logger.info(f"Verification code generated for user {user_id}")
            return code

        except Exception as e:
            logger.error(f"Code generation error: {e}")
            raise

    @classmethod
    def send_verification_email(
        cls,
        user: Union[AbstractBaseUser, AbstractUser],
        code: str,
        email_template: str = "accounts/configer/verification_code_email.html",
    ) -> bool:
        """
        Send verification email with HTML template

        Args:
            user (Union[AbstractBaseUser, AbstractUser]): User receiving the verification code
            code (str): Verification code to send
            email_template (str, optional): Path to email template

        Returns:
            bool: Email sending status
        """
        try:
            subject = "Verification Code for Grow Earth Account"

            # Prepare email context
            context = {
                "username": getattr(user, "get_full_name", lambda: user.username)()
                or user.username,
                "verification_code": code,
                "expiration_minutes": 10,
                "site_name": "Grow Earth",
            }

            # Render HTML template
            html_content = render_to_string(email_template, context)

            # Create and send email
            email = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
                body=f"Your verification code is: {code}",
            )

            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            logger.info(f"Verification email sent to {user.email}")
            return True

        except Exception as e:
            logger.error(f"Email sending error: {e}")
            return False

    @staticmethod
    def validate_verification_code(
        user_id: int, user_input: str, invalidate: bool = True
    ) -> bool:
        """
        Validate user-provided verification code

        Args:
            user_id (int): User's unique identifier
            user_input (str): Code entered by user
            invalidate (bool, optional): Remove code after successful validation. Defaults to True.

        Returns:
            bool: Verification status
        """
        try:
            cache_key = f"verification_code_{user_id}"
            cached_code = cache.get(cache_key)

            # Validate input
            if cached_code and cached_code == user_input.upper():
                if invalidate:
                    cache.delete(cache_key)

                logger.info(f"Verification successful for user {user_id}")
                return True

            logger.warning(f"Invalid verification attempt for user {user_id}")
            return False

        except Exception as e:
            logger.error(f"Verification validation error: {e}")
            return False

    @classmethod
    def resend_verification_code(
        cls,
        user: Union[AbstractBaseUser, AbstractUser],
        previous_code: Optional[str] = None,
    ) -> str:
        """
        Resend verification code for a user

        Args:
            user (Union[AbstractBaseUser, AbstractUser]): User requesting code resend
            previous_code (str, optional): Previous verification code to invalidate

        Returns:
            str: New verification code
        """
        try:
            # Invalidate previous code if provided
            if previous_code:
                cache.delete(f"verification_code_{user.id}")

            # Generate and send new code
            new_code = cls.generate_verification_code(user.id)
            cls.send_verification_email(user, new_code)

            logger.info(f"Verification code resent for user {user.id}")
            return new_code

        except Exception as e:
            logger.error(f"Code resend error: {e}")
            raise
