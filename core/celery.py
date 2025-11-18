import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True

from core import settings  # noqa: E402
if settings.CELERY_WORKER_RUNNING is not True:  # simple guard if you want
    app.loader.import_default_modules()

__all__ = ('app',)