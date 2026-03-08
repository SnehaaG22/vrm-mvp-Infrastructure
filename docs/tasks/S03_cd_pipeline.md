# S-03 Continuous Deployment Pipeline

## Overview

Staged deployments allow code to move from `main` to test and finally production with approval and rollback hooks.

## Running a staged deployment

A simple example uses `docker-compose` with an override file for each environment, e.g.:

```bash
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d
```

Rollback hooks could be implemented with tags or previous images, e.g.:

```bash
docker-compose pull && docker-compose up -d --rollback
```

## Deliverable

- Trigger a deployment from `main` by pushing a tagged commit and verify the staging service starts.
- Describe how to rollback (revert to previous tag, redeploy).
