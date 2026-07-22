#!/bin/bash
set -e

INITIAL_REV="0f225bf89d71"

echo "[startup] Running database migrations..."
if flask db upgrade 2>&1; then
    echo "[startup] Migrations applied successfully."
else
    echo "[startup] Tables may already exist. Stamping initial revision + retrying..."
    flask db stamp "$INITIAL_REV" 2>&1
    flask db upgrade 2>&1
    echo "[startup] Migrations applied (after stamp)."
fi

echo "[startup] Starting gunicorn..."
exec gunicorn --bind 0.0.0.0:"${PORT:-8080}" run:app
