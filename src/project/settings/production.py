import os

from .base import *

# Security Settings
DEBUG = False  # Debug is False for testing production-like behavior locally
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Database Configuration (using SQLite for local development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Security Enhancements (Disable SSL-related settings for local development)
SECURE_SSL_REDIRECT = False  # Disable SSL redirect for local testing
SESSION_COOKIE_SECURE = False  # Allow cookies over HTTP
CSRF_COOKIE_SECURE = False  # Allow CSRF cookies over HTTP
SECURE_HSTS_SECONDS = 0  # Disable HSTS for local development
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Disable HSTS for subdomains
SECURE_HSTS_PRELOAD = False  # Disable HSTS preload

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
