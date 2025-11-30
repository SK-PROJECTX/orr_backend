web: gunicorn core.wsgi:application --preload
worker: celery -A core worker --loglevel=info
