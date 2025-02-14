import os
from pathlib import Path

from dotenv import load_dotenv

# Core Project Configuration
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv()

# Security and Core Settings
SECRET_KEY = os.getenv("SECRET_KEY", "default-very-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
# Application Definition
INSTALLED_APPS = [
    # Django Core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project Apps (Full Python Path)
    "apps.core.apps.CoreConfig",
    "apps.store.apps.StoreConfig",
    "apps.tags.apps.TagsConfig",
    "apps.account.apps.AccountConfig",
    # Third-Party
    "django_tailwind_cli",
    "fontawesomefree",
    # Optional: Simple Email-Based Authentication
    # "django_otp",
    # "django_otp.plugins.otp_totp",
    # "two_factor",
    # "phonenumbers",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_otp.middleware.OTPMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # "two_factor.backends.auth.TokenBackend",
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
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

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

# Disable Phone-Related Configurations
# TWO_FACTOR_CALL_GATEWAY = None
# TWO_FACTOR_SMS_GATEWAY = None

# LOGIN_URL = "two_factor:login"
# LOGIN_REDIRECT_URL = "two_factor:profile"

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER")

# Authentication Model that use in templates and login, register
AUTH_USER_MODEL = "account.CustomUser"
