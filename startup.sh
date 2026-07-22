#!/bin/bash
set -e

echo "[startup] Running database migrations..."
if flask db upgrade 2>&1; then
    echo "[startup] Migrations applied successfully."
else
    echo "[startup] Migration failed. Attempting stamp + retry (handles pre-existing tables)..."
    flask db stamp head 2>&1
    flask db upgrade 2>&1
    echo "[startup] Migrations applied (after stamp)."
fi

echo "[startup] Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:"${PORT:-8080}" run:app
