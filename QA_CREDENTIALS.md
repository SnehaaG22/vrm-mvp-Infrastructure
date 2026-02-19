QA-ready credentials + role matrix

Overview

- These are example QA credentials and recommended role mappings for P0 runs. If seeded users are present in your DB, replace the values below with the actual seeded emails and role IDs.

Credentials (example)

- Admin: admin@example.com / Password: Passw0rd!
  - Role: Admin
  - Permissions: create/update/delete assessments, manage vendors, view/modify users, trigger scoring, set RBAC
- Reviewer: reviewer@example.com / Password: Passw0rd!
  - Role: Reviewer
  - Permissions: view assessments, review and approve/return, add review notes
- Vendor: vendor@example.com / Password: Passw0rd!
  - Role: Vendor
  - Permissions: submit templates, upload evidence, view own assessments

Role Matrix (QA shorthand)

- Admin: Full access. Can impersonate (if available), seed/test data, approve -> triggers scoring.
- Reviewer: Review flows only; cannot change vendor data or RBAC.
- Vendor: Can create templates, submit evidence and finalise submissions.

How to create local QA users quickly
Run in the backend repo root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
# (optionally) create additional users via shell
python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_user('reviewer', 'reviewer@example.com', 'Passw0rd!')
User.objects.create_user('vendor', 'vendor@example.com', 'Passw0rd!')
exit()
```

Notes

- Replace example passwords with stronger values for shared/staged environments.
- If your project seeds users via `seeds.py`, inspect `apps/*/seeds.py` to align emails and roles.

Quick verification steps for QA run

- Ensure `REACT_APP_API_URL` in the frontend `.env` is set to `http://127.0.0.1:8000/api`
- Start backend: `python manage.py runserver 0.0.0.0:8000`
- Login via POST `/api/auth/login/` and save token.
- Verify GET `/api/users/me/` returns user info.
- Run Postman environment with saved token for E2E run.
