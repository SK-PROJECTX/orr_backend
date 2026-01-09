#!/bin/bash
set -e

export PATH="$HOME/.local/bin:$PATH"

echo "Running migrations..."
poetry run python manage.py migrate

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
poetry run python manage.py setup_admin_portal || true

echo "Starting Gunicorn..."
exec poetry run gunicorn core.wsgi:application --bind 0.0.0.0:8000 --preload
