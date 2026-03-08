# S-01 Environment and Secrets Strategy

This document describes the configuration of environment files and how secrets are managed for the VRM Infra backend.

## Environment files

- `config/dev.env` and `config/staging.env` contain environment-specific variables.
- Add any sensitive values (API keys, database credentials) as secrets stored in the appropriate deployment platform (e.g. GitHub Actions secrets or Vault).

## Secret management

- Use a secrets manager (HashiCorp Vault, AWS Secrets Manager) in production.
- Never commit plaintext secrets to the repository; use `.env` files only for local development with placeholders.

## Deliverable

- Provide an environment matrix in the README (see below) showing which variables are required in each environment.

```text
ENV_VAR      dev   staging   production
DATABASE_URL  yes   yes       yes (from vault)
SECRET_KEY    local placeholder   vault lookup
...
```
