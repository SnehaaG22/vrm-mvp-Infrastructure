# Observability and Dashboard Guidance

This repo now includes a basic observability stack in Docker Compose for service availability monitoring.

## Current observability status

- Docker container logs are available using `docker compose logs`.
- Celery worker and beat logs are available via `docker compose logs -f worker` and `docker compose logs -f beat`.
- Prometheus, Grafana, Alertmanager, cAdvisor, and Blackbox Exporter are now included in Docker Compose.
- Basic availability alerts are configured for the backend admin page, MinIO console, and pgAdmin.

## How to access observability services

- Prometheus: http://127.0.0.1:9090
- Grafana: http://127.0.0.1:3000
- Alertmanager: http://127.0.0.1:9093
- cAdvisor: http://127.0.0.1:8080

## Implementation details

- `monitoring/prometheus.yml` configures Prometheus scrape targets and alert rules.
- `monitoring/rules.yml` defines reliability alerts for service availability.
- `monitoring/alertmanager.yml` configures Alertmanager.

## Recommended next steps

1. Instrument Django with Prometheus metrics using `django-prometheus`.
2. Add a centralized logging stack such as Loki and Grafana.
3. Add tracing with Jaeger or OpenTelemetry for deeper performance visibility.
