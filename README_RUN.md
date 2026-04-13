# VRM Backend Run Guide

This file contains the complete step-by-step instructions to run the project, verify services, and validate the task implementation.

## 1. Start the Docker stack

From the project root:

```powershell
docker compose up -d --build
```

This starts all services:
- backend (Django)
- worker (Celery)
- beat (Celery scheduler)
- redis
- minio
- postgres
- pgadmin
- prometheus
- alertmanager
- grafana
- cadvisor
- blackbox-exporter

## 2. Verify containers are running

Run:

```powershell
docker compose ps --all
```

Check that all services show `Up`.

## 3. Run migrations

```powershell
docker compose exec backend python manage.py migrate
```

## 4. Create a superuser

```powershell
docker compose exec backend python manage.py createsuperuser
```

Use an email like `admin123@gmail.com` and a strong password.

## 5. Seed sample evidence (optional)

```powershell
docker compose exec backend bash
python manage.py shell
```

Then inside the shell:

```python
from apps.evidence.seeds import run
run()
exit()
```

## 6. Access the web interfaces

- Django admin: `http://127.0.0.1:8000/admin/`
- MinIO console: `http://localhost:9001/`
- pgAdmin: `http://localhost:5050/`
- Prometheus: `http://127.0.0.1:9090/`
- Alertmanager: `http://127.0.0.1:9093/`
- Grafana: `http://127.0.0.1:3000/`
- cAdvisor: `http://127.0.0.1:8080/`

### Grafana login

Default Grafana credentials:
- Username: `admin`
- Password: `admin`

If you do not remember the login, use these default values.

## 7. Verify service endpoints

The following endpoints should be reachable in your browser:

- `http://127.0.0.1:8000/admin/` should show the Django admin login.
- `http://localhost:9001/` should show the MinIO login page.
- `http://localhost:5050/` should show the pgAdmin login page.
- `http://127.0.0.1:9090/` should show Prometheus.
- `http://127.0.0.1:3000/` should show Grafana.

If a page refuses connection:
1. Confirm `docker compose ps --all` shows the service is Up.
2. Check service logs:
   - `docker compose logs prometheus --tail 50`
   - `docker compose logs grafana --tail 50`
3. Confirm the port mapping is correct in `docker-compose.yml`.

## 8. Run background tasks

### Synchronous task run

```powershell
docker compose exec backend python manage.py shell -c "from apps.evidence.tasks import evidence_expiry_reminder; from apps.renewals.tasks import renewal_due_reminder; evidence_expiry_reminder.apply(); renewal_due_reminder.apply()"
```

### Asynchronous Celery task run

```powershell
docker compose exec backend python manage.py shell -c "from apps.evidence.tasks import evidence_expiry_reminder; from apps.renewals.tasks import renewal_due_reminder; evidence_expiry_reminder.delay(); renewal_due_reminder.delay()"
```

## 9. Verify notification API behavior

Use PowerShell example:

```powershell
iwr "http://localhost:8000/api/notifications/" -Headers @{ "org-id" = "1" } -UseBasicParsing
```

Mark one notification read:

```powershell
iwr "http://localhost:8000/api/notifications/10/read/" -Method Patch -Headers @{ "org-id" = "1" } -UseBasicParsing
```

Mark all notifications read:

```powershell
iwr "http://localhost:8000/api/notifications/read-all/" -Method Post -Headers @{ "org-id" = "1" } -UseBasicParsing
```

## 10. Run tests

```powershell
docker compose exec backend python manage.py test
```

If you want to run specific apps:

```powershell
docker compose exec backend python manage.py test apps.notifications
docker compose exec backend python manage.py test apps.evidence
```

## 11. Windows backup/restore commands

If `sh` is not available on Windows PowerShell, use these commands instead:

### Backup PostgreSQL

```powershell
docker compose exec postgres pg_dump -U vrm -d vrm_db > postgres_backup.sql
```

### Restore PostgreSQL

```powershell
docker compose exec postgres psql -U vrm -d vrm_db < postgres_backup.sql
```

## 12. Final checklist

- [ ] `docker compose up -d --build` runs successfully
- [ ] `docker compose ps --all` shows all services Up
- [ ] `http://127.0.0.1:8000/admin/` opens
- [ ] `http://localhost:9001/` opens
- [ ] `http://localhost:5050/` opens
- [ ] `http://127.0.0.1:9090/` opens
- [ ] `http://127.0.0.1:3000/` opens
- [ ] default Grafana login is `admin/admin`
- [ ] tasks `evidence_expiry_reminder` and `renewal_due_reminder` can be triggered
- [ ] tests run without errors
