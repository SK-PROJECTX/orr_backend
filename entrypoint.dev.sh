#!/bin/bash

if [ "$SERVICE" = "web" ]; then
    ./wait-for-it.sh db:5432 -- echo "DB is ready"

    poetry run python manage.py migrate
    poetry run python manage.py collectstatic --noinput || true
    poetry run python manage.py setup_admin_portal || true

    echo "Starting Django development server..."
    exec poetry run python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi
