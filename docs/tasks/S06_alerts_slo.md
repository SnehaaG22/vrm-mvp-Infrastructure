# S-06 Alerts and SLO Baseline

Define service level objectives and associated alerting rules.

## Example SLOs

- **Availability**: 99.9% uptime for the API over 30 days
- **Latency**: 95th percentile request time < 500ms

## Alert rules

`monitoring/alert_rules.yml` already holds rules; verify they cover P0 incidents (e.g. `api_down`, `high_error_rate`).

```yaml
- alert: APIDown
  expr: up{job="web"} == 0
  for: 5m
  labels:
    severity: P0
  annotations:
    summary: "API is down"
```

## Deliverable

- Document the SLOs in this file
- Explain how alerts are configured in Prometheus
