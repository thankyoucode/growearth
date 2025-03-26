import os

from .base import *

# Security Settings
DEBUG = False  # Debug is False for testing production-like behavior locally
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".verce.app,.now.sh").split(",")

# Database Configuration (using SQLite for local development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "production.log",
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "ERROR",
    },
}
