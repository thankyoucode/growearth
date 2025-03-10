from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.store"  # Correct this to match your app's location

    def ready(self):
        from . import signals  # Import signals using the correct path
