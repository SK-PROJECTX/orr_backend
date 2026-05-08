import os
from .base import *
from urllib.parse import urlparse, parse_qs, unquote
from decouple import config

DEBUG = True

DATABASE_URL = config("DATABASE_URL")
DB_PASSWORD = config("DB_PASSWORD", default=None)

if DATABASE_URL:
    url = urlparse(DATABASE_URL)
    query_params = parse_qs(url.query)
    
    db_host = query_params.get('host', [url.hostname])[0]
    
    if db_host and db_host.startswith('/'):
        db_host = unquote(db_host)

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": DB_PASSWORD or (unquote(url.password) if url.password else None),
            "HOST": db_host,            
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
    "https://orr-solutions.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://localhost:3001",
    "http://localhost:5173",
    "https://www.orr.solutions",
    "https://orr.solutions",
]

CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://orr-backend-105825824472.asia-southeast2.run.app",
    "https://orr-backend.orr.solutions",
    "https://orr.solutions",
    "https://www.orr.solutions",
    "https://orr-solutions.vercel.app",
    "https://orr-admin-frontend.vercel.app",
    "https://orr-solutions-admin.vercel.app",
    "https://admin.orr.solutions",
]

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



