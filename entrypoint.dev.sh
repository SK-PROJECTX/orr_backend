#!/bin/bash

if [ "$SERVICE" = "web" ]; then
    ./wait-for-it.sh db:5432 -- echo "DB is ready"
    poetry run python manage.py makemigrations
    poetry run python manage.py migrate
    poetry run python manage.py collectstatic --noinput || true
    poetry run python manage.py setup_admin_portal || true
    
    echo "Starting Stripe CLI to listen for webhooks..."
    stripe listen --api-key $STRIPE_SECRET_KEY --forward-to http://localhost:8000/stripe-webhook/ &

    echo "Starting Django development server..."
    exec poetry run python manage.py runserver 0.0.0.0:8000
else
    exec "$@"
fi
