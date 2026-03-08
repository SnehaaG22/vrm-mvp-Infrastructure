# S-05 Centralised Logging and Observability

## Logging configuration

Inspect `core/settings.py` for handlers exporting to stdout or third-party systems.

## Metrics and dashboards

`monitoring/prometheus.yml` is present for scraping metrics. A Grafana dashboard should be added to visualise API and job performance.

## Deliverable

- Provide a sample Grafana dashboard JSON and instructions to import it.
- Verify logs from Django are collected (e.g., `docker-compose logs web`).
