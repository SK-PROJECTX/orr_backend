#!/bin/bash
set -e

echo "Running migrations..."
poetry run python manage.py migrate

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
poetry run python manage.py setup_admin_portal || true

python create_cms_seed_data.py
python create_service_pillar_content.py
python create_service_pillar_data.py

echo "Starting Gunicorn..."
exec poetry run gunicorn core.wsgi:application --bind 0.0.0.0:8000 --preload
