#!/bin/bash
set -e

# Run migrations automatically on startup
# We use || true so that if the DB isn't ready, the container still starts
echo "Applying database migrations..."
python manage.py migrate --noinput || echo "Migrations failed, continuing to start server..."

echo "Starting Gunicorn on port ${PORT:-8080}..."
echo "Current environment configuration active."
exec gunicorn core.wsgi:application \
  --bind 0.0.0.0:${PORT:-8080} \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --log-level info

