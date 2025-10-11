#!/bin/sh
set -e

# Ensure the SQLite database directory exists when using SQLite
DB_URI="${DATABASE_URL:-sqlite:///insurance.db}"
case "$DB_URI" in
  sqlite:///*)
    DB_PATH="${DB_URI#sqlite:///}"
    DB_DIR=$(dirname "$DB_PATH")
    if [ "$DB_DIR" != "." ]; then
      mkdir -p "$DB_DIR"
    fi
    ;;
esac

# Run pending migrations when available, otherwise create the database
if flask db upgrade >/tmp/db-upgrade.log 2>&1; then
    echo "Database migrated successfully."
else
    echo "flask db upgrade failed, falling back to flask create-db"
    cat /tmp/db-upgrade.log
    flask create-db
fi

echo "Starting InsureMate on ${FLASK_RUN_HOST:-0.0.0.0}:${FLASK_RUN_PORT:-5000}"
exec "$@"
