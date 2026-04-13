#!/bin/sh

# Restore PostgreSQL database from postgres_backup.sql
set -e

docker compose exec postgres psql -U vrm -d vrm_db < postgres_backup.sql

echo "Postgres restore completed from postgres_backup.sql"
