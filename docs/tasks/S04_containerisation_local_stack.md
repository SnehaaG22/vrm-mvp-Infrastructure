# S-04 Containerisation and Local Stack

The repository includes a `Dockerfile` and `docker-compose.yml` to build the application and run the full stack locally.

## Bringing up the stack

```bash
docker-compose up --build
```

All backend services should be accessible; the web server is typically on port 8000.

## Deliverable

- Successfully run the stack with one command and document the process.
- Ensure the Compose file includes all required services (database, cache, etc.).
