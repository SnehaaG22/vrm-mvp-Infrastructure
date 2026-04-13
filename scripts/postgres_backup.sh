#!/bin/sh

# Backup PostgreSQL database from the running postgres container
set -e

docker compose exec postgres pg_dump -U vrm -d vrm_db > postgres_backup.sql

echo "Postgres backup created at postgres_backup.sql"
