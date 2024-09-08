#!/bin/sh

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for the PostgreSQL database..."
  sleep 1
done

# Run database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the application using gunicorn
# exec gunicorn config.wsgi:application --bind 0.0.0.0:8000
python3 manage.py runserver 0.0.0.0:8000
