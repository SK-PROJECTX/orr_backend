#!/bin/bash
set -e

echo "Starting Gunicorn..."
exec poetry run gunicorn core.wsgi:application \
  --bind 0.0.0.0:${PORT:-8080} \
  --workers 2 \
  --threads 4 \
  --timeout 120

