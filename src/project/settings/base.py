import os
from pathlib import Path

from dotenv import load_dotenv

# Core Project Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()

# Security and Core Settings
SECRET_KEY = os.getenv("SECRET_KEY", "default-very-secret-key")
# DEBUG = os.getenv("DEBUG", "False") == "True"
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
# Application Definition
INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_tailwind_cli",
    "fontawesomefree",
    # Project Apps (Full Python Path)
    "apps.core.apps.CoreConfig",
    "apps.store.apps.StoreConfig",
    "apps.tags.apps.TagsConfig",
    "apps.accounts.apps.AccountsConfig",
    "django_countries",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.store.middleware.merge_cart.MergeCartMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Template Configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR
            / "templates/components",  # expariment to define sub folder of main templates folder
            BASE_DIR / "templates/core",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "project.context_processors.navigation_links",
                "project.context_processors.footer_context",
            ],
        },
    }
]

# Default Settings
ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static and Media Files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Source directories for static files
STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory for collected static files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # Directory for uploaded media files


# Database Configuration for SQLite3
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        # SQLite-specific optimizations
        "OPTIONS": {
            "timeout": 20,  # Increase connection timeout
            "isolation_level": None,  # Enable autocommit
        },
    }
}
# Additional SQLite Performance Configurations
DATABASES["default"].update(
    {
        "ATOMIC_REQUESTS": False,  # Disable atomic transactions for better performance
        "CONN_MAX_AGE": 0,  # Disable connection persistence
    }
)

# sys.path.append(os.path.abspath(os.path.join(BASE_DIR, 'src')))

# LOGIN_URL = "accounts/login/"
# LOGIN_REDIRECT_URL = "accounts/login/"

# Authentication Model that use in templates and login, register
AUTH_USER_MODEL = "accounts.CustomUser"

# TAILWIND_CLI_PATH = "src/static/tailwindcss"
