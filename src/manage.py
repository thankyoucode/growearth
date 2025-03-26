#!/usr/bin/env python
import logging
import os
import sys
from pathlib import Path

# Basic Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [%(levelname)s]: %(message)s"
)


def select_settings():
    """Dynamically select settings module with robust environment handling"""
    # Priority:
    # 1. DJANGO_SETTINGS_MODULE environment variable
    # 2. DJANGO_ENV environment variable
    # 3. Default to development

    # Check if DJANGO_SETTINGS_MODULE is explicitly set
    if os.environ.get("DJANGO_SETTINGS_MODULE"):
        return os.environ["DJANGO_SETTINGS_MODULE"]

    # runat = "development"
    runat = "production"

    env = os.getenv("DJANGO_ENV", runat).lower()

    SETTINGS_MODULES = {
        "development": "project.settings.development",
        "production": "project.settings.production",
        "testing": "project.settings.testing",
        "staging": "project.settings.staging",
    }

    selected_settings = SETTINGS_MODULES.get(env, f"project.settings.{runat}")

    # Optional: Add logging
    print(f"🔧 Loading {env.upper()} settings: {selected_settings}")

    return selected_settings


def main():
    """Django management entry point"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", select_settings())

    try:
        from django.core.management import execute_from_command_line
    except ImportError as e:
        logging.error(f"Django import error: {e}")
        sys.exit(1)

    # try:
    #     execute_from_command_line(sys.argv)
    # except Exception as e:
    #     logging.error(f"Command execution error: {e}")
    #     sys.exit(1)

    # only for development
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
