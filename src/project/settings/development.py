# this is not best prectice to direct import all `base.py` settings
# here me some another way to do this same process
# here is some problem with if using ruff for code formating , this is fine to use
import os

from .base import *

# Development-specific configurations
DEBUG = True
ALLOWED_HOSTS = "localhost,127.0.0.1".split(",")

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Debugging and Development Tools
INSTALLED_APPS += [
    "debug_toolbar",
    "django_extensions",
    "tailwind",
    "django_browser_reload",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

# Email Configuration (Use console backend for development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

TAILWIND_APP_NAME = "tailwind"
TAILWIND_MODE = "watch"
# NPM_BIN_PATH = "/usr/local/bin/npm"

# STATICFILES_FINDERS = [
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#     "compressor.finders.CompressorFinder",
# ]
