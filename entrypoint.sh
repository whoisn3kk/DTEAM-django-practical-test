#!/bin/sh

echo "Applying database migrations..."
poetry run python manage.py migrate

echo "Starting server..."
exec "$@"