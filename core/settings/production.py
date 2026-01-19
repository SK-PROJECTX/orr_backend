import os
from decouple import config
from .base import *
from urllib.parse import urlparse

# Production-specific settings
DEBUG = False

ALLOWED_HOSTS = [
    "orr-backend-web-latest.onrender.com",
    "localhost",
    "127.0.0.1",
    ".onrender.com",
    ".vercel.app",
]

DATABASE_URL = config("DATABASE_URL")

if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port or "5432",
        }
    }
else:
    raise ValueError("DATABASE_URL is not set")

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://admin.orr.solutions",
    "https://orr-admin-frontend.vercel.app",
    "https://orr-solutions-admin.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173",
]

CORS_ALLOW_CREDENTIALS = True

# Static files for production
STATIC_ROOT = "/app/staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name} — {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {"handlers": ["console"], "level": "INFO", "propagate": True},
    },
}



