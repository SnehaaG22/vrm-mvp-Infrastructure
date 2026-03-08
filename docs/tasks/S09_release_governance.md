# S-09 Release Governance Handbook

This handbook outlines the release process, roles, and checklist.

## Checklist

- [ ] Code reviewed and merged into `main`
- [ ] CI pipeline green
- [ ] UAT sign-off obtained
- [ ] Version bumped and tagged
- [ ] Release notes drafted
- [ ] Rollback plan documented

## Roles

- **Developer:** prepares PR and ensures tests pass
- **QA:** verifies UAT environment
- **Release manager:** approves and triggers deployment

## Deliverable

- Document the steps above and include a sample tag command:
  `git tag -a v1.2.3 -m "release v1.2.3"`.
