import logging
import secrets

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class EmailVerificationService:
    """
    Service for handling email verification processes
    """

    @staticmethod
    def generate_verification_code(user_id, length=6):
        """
        Generate a secure verification code for a user

        Args:
            user_id (int): User's unique identifier
            length (int, optional): Length of verification code. Defaults to 6.

        Returns:
            str: Generated verification code
        """
        try:
            # Generate a secure hexadecimal token
            code = secrets.token_hex(length)[:length].upper()

            # Cache the code with a 10-minute expiration
            cache.set(f"2fa_code_{user_id}", code, timeout=600)

            logger.info(f"Verification code generated for user {user_id}")
            return code

        except Exception as e:
            logger.error(f"Error generating verification code: {e}")
            raise

    @classmethod
    def send_verification_email(cls, user, code):
        """
        Send a professional HTML verification email

        Args:
            user (User): User receiving the verification code
            code (str): Verification code to send
        """
        try:
            subject = "Verification Code for Your Account"

            # Prepare email context
            context = {
                "username": user.get_full_name() or user.username,
                "verification_code": code,
                "expiration_minutes": 10,
            }

            # Render HTML template
            html_content = render_to_string(
                "account/configer/verification_code_email.html", context
            )

            # Create and send email
            email = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )

            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)

            logger.info(f"Verification email sent to {user.email}")

        except Exception as e:
            logger.error(f"Error sending verification email: {e}")
            raise

    @staticmethod
    def validate_verification_code(user_id, user_input):
        """
        Validate user-provided verification code

        Args:
            user_id (int): User's unique identifier
            user_input (str): Code entered by user

        Returns:
            bool: Whether the verification code is valid
        """
        try:
            # Retrieve cached verification code
            cached_code = cache.get(f"2fa_code_{user_id}")

            # Validate input and remove cache if matched
            if cached_code and cached_code == user_input.upper():
                cache.delete(f"2fa_code_{user_id}")
                logger.info(f"Verification successful for user {user_id}")
                return True

            logger.warning(f"Invalid verification attempt for user {user_id}")
            return False

        except Exception as e:
            logger.error(f"Error validating verification code: {e}")
            return False
