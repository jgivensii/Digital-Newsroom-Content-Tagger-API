#!/bin/sh
# entrypoint.flask.sh
# Run Alembic migrations then start the Flask server.
set -e

echo "==> Running database migrations..."
flask --app content_api.app:create_app db upgrade

echo "==> Starting Flask server..."
exec flask --app content_api.app:create_app run --host 0.0.0.0 --port 5000
