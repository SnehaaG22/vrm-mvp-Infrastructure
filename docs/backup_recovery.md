# Backup and Recovery Guide

This document describes how to perform backup and recovery for the current Docker-based stack.

## PostgreSQL backup

### Backup

Run from the repo root:

```bash
docker compose exec postgres pg_dump -U vrm -d vrm_db > postgres_backup.sql
```

### Restore

```bash
docker compose exec postgres psql -U vrm -d vrm_db < postgres_backup.sql
```

## MinIO backup

MinIO stores data in the Docker volume `minio_data`.

### Backup MinIO data

```bash
docker run --rm -v vrm-backend_minio_data:/data -v "$PWD":/backup busybox sh -c "cd /data && tar czf /backup/minio_backup.tgz ."
```

### Restore MinIO data

```bash
docker run --rm -v vrm-backend_minio_data:/data -v "$PWD":/backup busybox sh -c "cd /data && tar xzf /backup/minio_backup.tgz ."
```

## Disaster recovery drill

1. Stop the application stack: `docker compose down`
2. Restore the latest PostgreSQL dump.
3. Restore MinIO backup if needed.
4. Start the stack again: `docker compose up -d`
