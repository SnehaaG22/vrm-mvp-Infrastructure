## 🔐 QA-Ready Credentials & Role Matrix – Feb 19, 2026

**Status:** ✅ P0 Unblocked – All endpoints working (verified 200 OK)

### Test Users (for dev environment)

| Username | Email                | Password    | Role     | Permissions                          |
| -------- | -------------------- | ----------- | -------- | ------------------------------------ |
| admin    | admin@example.com    | testpass123 | Admin    | Full access, create/approve, scoring |
| reviewer | reviewer@example.com | testpass123 | Reviewer | View assessments, review, approve    |
| vendor   | vendor@example.com   | testpass123 | Vendor   | Submit templates, upload evidence    |

### Endpoints Verified (Feb 19, 2026 – 16:50 IST)

**POST /api/auth/login/**

- Request: {"email":"admin@example.com", "password":"testpass123"}
- Response: 200 OK – Returns token "dev-token-2"

**GET /api/users/me/**

- Headers: Authorization: Bearer dev-token-2
- Response: 200 OK – Returns user profile

**GET /api/notifications/**

- Headers: Authorization: Bearer dev-token-2, org-id: 101
- Response: 200 OK – Returns notification list

### Frontend Env Setup

In `vrm-frontend/.env`:

```
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

Then run frontend: `npm start` (port 3000)

### Known Issues & Notes

- Dev auth uses `dev-token-<user_id>` format (not production-grade JWT)
- CORS enabled for http://localhost:3000
- Ready for Postman E2E runs and QA validation
