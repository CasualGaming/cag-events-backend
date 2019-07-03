from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    name = "authentication"
    verbose_name = "Authentication and Authorization"

    def ready(self):
        # Register listeners
        from . import group_sync  # noqa: F401
