# S-08 Backup and Disaster Recovery Drills

## Backup procedure

The application uses a SQLite database `db.sqlite3` in development. A backup can be taken via:

```bash
cp db.sqlite3 db.sqlite3.bak
```

For production, use database dumps (e.g. `pg_dump`).

## Restore procedure

```bash
mv db.sqlite3.bak db.sqlite3
```

test by deleting the file and restoring from backup. Document the commands in this runbook.

## Deliverable

- Create this file as a runbook with step-by-step instructions
- Execute the drill and note the time taken and any issues.
