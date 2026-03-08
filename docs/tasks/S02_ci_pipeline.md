# S-02 Continuous Integration Pipeline

## Current state

No CI configuration is present in the repository. Typical implementations would use GitHub Actions, GitLab CI, or Jenkins.

## Example workflow file

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: pytest
      - name: Run lint
        run: flake8 .
      - name: Security scan
        run: bandit -r .
```

## Deliverable

- Create the pipeline file and validate by running the jobs locally with `act` or by pushing a branch and observing the run.
- Document the commands used to trigger unit and integration tests.
