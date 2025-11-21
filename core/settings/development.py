import os

from decouple import config

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "PASSWORD": config("DATABASE_PASSWORD"),
        "HOST": config("DATABASE_HOST", default="localhost"),
        "PORT": config("DATABASE_PORT", default="5432"),
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # ==== FORMATTERS ====
    "formatters": {
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime} [{levelname}] {name} — {message}",
            "style": "{",
        },
        "celery": {
            "format": "{asctime} [CELERY:{levelname}] {name} — {message}",
            "style": "{",
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(levelname)s]%(reset)s %(message)s",
        },
    },
    # ==== HANDLERS ====
    "handlers": {
        # Console (dev only)
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
        # General app logs (INFO and above)
        "app_info_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/app_info.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5MB per file
            "backupCount": 5,
            "formatter": "verbose",
            "level": "INFO",
        },
        # Errors only (WARNING, ERROR, CRITICAL)
        "app_error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/app_error.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
            "formatter": "verbose",
            "level": "WARNING",
        },
        # Celery logs
        "celery_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/celery.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 3,
            "formatter": "celery",
            "level": "INFO",
        },
        # Django internal logs
        "django_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django.log"),
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 3,
            "formatter": "verbose",
            "level": "INFO",
        },
        # Debug everything (optional)
        "debug_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/debug.log"),
            "maxBytes": 1024 * 1024 * 10,
            "backupCount": 3,
            "formatter": "verbose",
            "level": "DEBUG",
        },
    },
    # ==== LOGGERS ====
    "loggers": {
        # Catch everything for debugging
        "": {
            "handlers": ["console", "debug_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        # Django internal logs
        "django": {
            "handlers": ["django_file"],
            "level": "INFO",
            "propagate": False,
        },
        # Celery logs
        "celery": {
            "handlers": ["celery_file"],
            "level": "INFO",
            "propagate": False,
        },
        # Your app modules
        "core": {  # rename to your project/app name
            "handlers": ["app_info_file", "app_error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
