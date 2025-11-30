set -e

echo "Running migrations..."
poetry run python manage.py migrate

echo "Collecting static files..."
poetry run python manage.py collectstatic --noinput

ech0 "Creating Django Admin"
poetry python manage.py create_superuser


