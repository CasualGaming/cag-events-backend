import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

if __name__ == "__main__":
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Failed to import Django. Is it installed?",
        ) from exc
    execute_from_command_line(sys.argv)
