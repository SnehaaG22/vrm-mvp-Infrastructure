# S-07 Security Scans in CI/CD

Security checks should run as part of the CI/CD pipeline.

## Common tools

- `bandit` for Python static analysis
- `safety` or `pip-audit` for dependency checks
- container scanners like `trivy` or `clair`

## Example CI step

```yaml
- name: Security scan
  run: |
    bandit -r .
    pip-audit --fail-on high
```

## Deliverable

- Execute the scans locally and capture the reports (put them in `docs/reports/`).
- Show that a PR fails when a critical issue is introduced (e.g., insecure function usage).
