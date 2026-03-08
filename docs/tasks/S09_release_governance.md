# S-09 Release Governance Handbook

This handbook outlines the release process, roles, and checklist.

## Checklist

- [x] Code reviewed and merged into `main`
- [x] CI pipeline green
- [x] UAT sign-off obtained
- [x] Version bumped and tagged
- [x] Release notes drafted
- [x] Rollback plan documented

## Roles

- **Developer:** prepares PR and ensures tests pass
- **QA:** verifies UAT environment
- **Release manager:** approves and triggers deployment

## Deliverable

- Document the steps above and include a sample tag command:
  `git tag -a v1.2.3 -m "release v1.2.3"`.

## Completion Note

- Completed and verified on 09-03-2026.
