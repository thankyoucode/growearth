import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
    User,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    # using first_name on place of username
    # first_name can not need to uniqe
    def create_user(self, email, first_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, first_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, help_text="User's first name")
    last_name = models.CharField(
        max_length=50, blank=True, help_text="User's last name (optional)"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True, verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        verbose_name="user permissions",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        return self.email


class UserOpinion(models.Model):
    """
    A unified model to capture user reviews and feedback.
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="opinions",
        help_text="The user who submitted the opinion.",
    )
    rating = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars.  Leave blank for general feedback.",
    )
    comment = models.TextField(blank=True, help_text="Detailed review or feedback.")
    is_review = models.BooleanField(
        default=False, help_text="Is this a review (with a rating)?"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Opinion"
        verbose_name_plural = "User Opinions"
        ordering = ["-created_at"]  # Most recent first

    def __str__(self):
        if self.is_review:
            return f"Review by {self.user.email} - {self.rating} stars"  # Change username to email
        else:
            return f"Feedback from {self.user.email}"  # Change username to email

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure that if a rating is provided,
        the 'is_review' flag is set to True.
        """
        if self.rating is not None:
            self.is_review = True
        super().save(*args, **kwargs)
