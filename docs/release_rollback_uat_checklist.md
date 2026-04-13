# Release, Rollback, and UAT Checklist

## Launch readiness and UAT checklist

- [ ] Verify Docker Compose services start successfully.
- [ ] Run database migrations successfully.
- [ ] Confirm Django admin page is accessible.
- [ ] Confirm MinIO UI is accessible.
- [ ] Confirm pgAdmin is accessible.
- [ ] Verify API endpoints respond correctly with authentication.
- [ ] Validate Celery worker and beat are running.
- [ ] Trigger reminder tasks and verify notification records are created.
- [ ] Confirm evidence upload and storage path behavior.

## Release rollback governance

### Rollback preparation

- Keep SQL backups for the current and previous database state.
- Keep MinIO backups of evidence objects.
- Tag Docker images with versioned tags before deployment.

### Rollback procedure

1. Stop the application stack: `docker compose down`.
2. Re-deploy the previous Docker image or restore the previous version of `docker-compose.yml`.
3. Restore the previous database backup if needed.
4. Restart the stack: `docker compose up -d`.
5. Validate the application after rollback.
