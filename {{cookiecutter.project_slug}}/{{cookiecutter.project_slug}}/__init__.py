import logging
import os
from logging import config as logging_config

from dynaconf import settings

LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
LOGFILE = os.path.join(settings.PROJECT_ROOT + "/logs/{{ cookiecutter.project_slug }}.log")
ERROR_LOGFILE = os.path.join(settings.PROJECT_ROOT + "/logs/{{ cookiecutter.project_slug }}-errors.log")


class RequireDebugFalse(logging.Filter):
    """Custom logging filter that logs when DEBUG mode is disabled."""

    def filter(self, record):
        return not settings.DEBUG


class RequireDebugTrue(logging.Filter):
    """Custom logging filter that logs when DEBUG mode is enabled."""

    def filter(self, record):
        return settings.DEBUG


logging_config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "require_debug_false": {"()": RequireDebugFalse},
            "require_debug_true": {"()": RequireDebugTrue},
        },
        "formatters": {
            "verbose": {"format": LOG_FORMAT, "datefmt": "%d/%b/%Y %H:%M:%S"}
        },
        "handlers": {
            # Logs to console when DEBUG mode is enabled.
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            # Handler for {{ cookiecutter.project_slug }} application modules that logs at DEBUG level.
            "{{ cookiecutter.project_slug }}_logs_handler": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOGFILE,
                "maxBytes": settings.LOG_FILE_SIZE,
                "backupCount": settings.LOG_FILE_BACKUP_COUNT,
                "formatter": "verbose",
            },
            "{{ cookiecutter.project_slug }}_error_logs_handler": {
                "level": "ERROR",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": ERROR_LOGFILE,
                "maxBytes": settings.LOG_FILE_SIZE,
                "backupCount": settings.LOG_FILE_BACKUP_COUNT,
                "formatter": "verbose",
            },
        },
        "loggers": {
            # Root logger which will capture all logs that are not captured or
            # intentionally propagated by other loggers. This will capture logs
            # written by third party packages. Only INFO and above level logs
            # will be captured.
            "": {
                "handlers": [
                    "console",
                    "{{ cookiecutter.project_slug }}_logs_handler",
                    "{{ cookiecutter.project_slug }}_error_logs_handler",
                ],
                "level": "WARNING",
            },
            # Logger to capture {{ cookiecutter.project_name }} application logs at DEBUG level.
            # Logs are not propagated to prevent duplicate logs as both this and
            # root logger writes to same log file.
            "{{ cookiecutter.project_slug }}": {
                "handlers": [
                    "console",
                    "{{ cookiecutter.project_slug }}_logs_handler",
                    "{{ cookiecutter.project_slug }}_error_logs_handler",
                ],
                "level": settings.LOG_LEVEL,
                "propagate": False,
            },
        },
    }
)
