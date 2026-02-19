# QA Testing Credentials & Role Matrix

**Document Status:** ✅ Ready for QA - February 19, 2025

---

## Quick Summary

| User Type | Email | Password | token (auto-issued) | Full Access |
|-----------|-------|----------|-------------------|------------|
| **Admin** | admin@vrm.com | password123 | dev-token-5 | ✅ All pages & all operations |
| **Vendor** | vendor@vrm.com | password123 | dev-token-6 | ✅ All pages & all operations |
| **Reviewer** | reviewer@vrm.com | password123 | dev-token-7 | ✅ All pages & all operations |

---

## How to Get a Token

### Step 1: Login via API
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vrm.com","password":"password123"}'
```

### Step 2: Copy the Token from Response
```json
{
  "token": "dev-token-5",
  "user": {
    "id": 5,
    "email": "admin@vrm.com",
    ...
  }
}
```

### Step 3: Use in Subsequent Requests
```bash
curl -X GET http://127.0.0.1:8000/api/assessments/ \
  -H "Authorization: Bearer dev-token-5"
```

---

## Frontend Login Instructions

1. Open: http://localhost:3000/login
2. Enter Email: `admin@vrm.com`
3. Enter Password: `password123`
4. Click "Login"
5. You'll be redirected to Dashboard
6. Token is auto-stored in browser localStorage

---

## Detailed Credentials Table

### Admin User
| Property | Value |
|----------|-------|
| **Email** | admin@vrm.com |
| **Password** | password123 |
| **User ID** | 5 |
| **Token Format** | dev-token-5 |
| **Role** | Administrator |
| **Permissions** | Can access all resources and all operations |

### Vendor User
| Property | Value |
|----------|-------|
| **Email** | vendor@vrm.com |
| **Password** | password123 |
| **User ID** | 6 |
| **Token Format** | dev-token-6 |
| **Role** | Vendor |
| **Permissions** | Can access all resources and all operations |

### Reviewer User
| Property | Value |
|----------|-------|
| **Email** | reviewer@vrm.com |
| **Password** | password123 |
| **User ID** | 7 |
| **Token Format** | dev-token-7 |
| **Role** | Reviewer |
| **Permissions** | Can access all resources and all operations |

---

## Role-Based Access Control Matrix

### Accessible Pages by Role

| Page/Feature | Admin | Vendor | Reviewer |
|--------------|-------|--------|----------|
| Dashboard | ✅ | ✅ | ✅ |
| Notifications | ✅ | ✅ | ✅ |
| Assessments List | ✅ | ✅ | ✅ |
| Vendors List | ✅ | ✅ | ✅ |
| Evidence Upload | ✅ | ✅ | ✅ |

### API Endpoints Access

| Endpoint | Admin | Vendor | Reviewer | Auth Required |
|----------|-------|--------|----------|---------------|
| POST /api/auth/login/ | ✅ | ✅ | ✅ | ❌ |
| GET /api/users/me/ | ✅ | ✅ | ✅ | ✅ |
| GET /api/assessments/ | ✅ | ✅ | ✅ | ✅ |
| POST /api/assessments/ | ✅ | ✅ | ✅ | ✅ |
| GET /api/vendors/ | ✅ | ✅ | ✅ | ✅ |
| POST /api/vendors/ | ✅ | ✅ | ✅ | ✅ |
| GET /api/notifications/ | ✅ | ✅ | ✅ | ✅ |
| POST /api/evidence/upload/ | ✅ | ✅ | ✅ | ✅ |

---

## Postman E2E Test Flow

### 1. Setup Postman Environment

Create environment with variables:
```json
{
  "base_url": "http://127.0.0.1:8000/api",
  "token": "dev-token-5",
  "email": "admin@vrm.com",
  "password": "password123"
}
```

### 2. Test Sequence (Happy Path)

#### Test 1: Login (No Auth Required)
```
POST {{base_url}}/auth/login/
Body: {
  "email": "admin@vrm.com",
  "password": "password123"
}
Expected: 200 OK + token
```

#### Test 2: Get User Profile (With Auth)
```
GET {{base_url}}/users/me/
Headers: Authorization: Bearer {{token}}
Expected: 200 OK + user data
```

#### Test 3: List Assessments (With Auth)
```
GET {{base_url}}/assessments/
Headers: Authorization: Bearer {{token}}
Expected: 200 OK + assessment list
```

#### Test 4: Create Assessment (With Auth)
```
POST {{base_url}}/assessments/
Headers: Authorization: Bearer {{token}}
Body: {
  "vendor_id": 1,
  "vendor_name": "Test Vendor",
  "status": "draft"
}
Expected: 201 Created + assessment object
```

#### Test 5: List Vendors (With Auth)
```
GET {{base_url}}/vendors/
Headers: Authorization: Bearer {{token}}
Expected: 200 OK + vendor list
```

#### Test 6: Create Vendor (With Auth)
```
POST {{base_url}}/vendors/
Headers: Authorization: Bearer {{token}}
Body: {
  "name": "New Test Vendor",
  "category": "IT",
  "status": "active",
  "email": "vendor@test.com",
  "phone": "+91-9999999999"
}
Expected: 201 Created + vendor object
```

#### Test 7: Get Notifications (With Auth)
```
GET {{base_url}}/notifications/
Headers: Authorization: Bearer {{token}}
Expected: 200 OK + notification list
```

### 3. Negative Test Cases

#### Test: Missing Auth Token (Should Fail - 401)
```
GET {{base_url}}/assessments/
(No Authorization header)
Expected: 401 Unauthorized
```

#### Test: Invalid Token (Should Fail - 401)
```
GET {{base_url}}/assessments/
Headers: Authorization: Bearer invalid-token
Expected: 401 Unauthorized
```

#### Test: Invalid Login Credentials (Should Fail - 401)
```
POST {{base_url}}/auth/login/
Body: {
  "email": "invalid@email.com",
  "password": "wrongpassword"
}
Expected: 401 Unauthorized
```

#### Test: Missing Required Fields (Should Fail - 400)
```
POST {{base_url}}/auth/login/
Body: { "email": "admin@vrm.com" }
(missing password)
Expected: 400 Bad Request
```

---

## Testing Checklist

### Backend Tests
- [ ] Start backend: `python manage.py runserver 127.0.0.1:8000`
- [ ] System check passes: `python manage.py check` → "0 silenced"
- [ ] Database migrations applied: `python manage.py showmigrations --list | grep common`
- [ ] Can login as admin@vrm.com (get dev-token-5)
- [ ] Can login as vendor@vrm.com (get dev-token-6)
- [ ] Can login as reviewer@vrm.com (get dev-token-7)
- [ ] Can list assessments with valid token
- [ ] Can create assessment with valid token
- [ ] Can list vendors with valid token
- [ ] Can create vendor with valid token
- [ ] Get 401 Unauthorized without token
- [ ] Get 401 Unauthorized with invalid token

### Frontend Tests
- [ ] Start frontend: `npm start` (from vrm-frontend)
- [ ] Page loads at http://localhost:3000
- [ ] Can login with admin@vrm.com / password123
- [ ] Dashboard displays user info after login
- [ ] Can navigate to Assessments page
- [ ] Assessments page shows list or proper loading state
- [ ] Can navigate to Vendors page
- [ ] Vendors page shows list or proper loading state
- [ ] Can navigate to Notifications page
- [ ] Notifications page shows list or proper loading state
- [ ] Can access Evidence Upload page
- [ ] Logout functionality works
- [ ] Refreshing page maintains login session

### API Tests (Postman)
- [ ] Login endpoint returns token (200)
- [ ] User me endpoint returns user data (200)
- [ ] Assessments GET returns list (200)
- [ ] Assessments POST creates record (201)
- [ ] Vendors GET returns list (200)
- [ ] Vendors POST creates record (201)
- [ ] Notifications GET returns list (200)
- [ ] Missing auth header returns 401
- [ ] Invalid token returns 401
- [ ] Invalid credentials return 401

---

## Common Issues & Solutions

### "Authentication credentials were not provided" on Login
**Issue:** LoginView doesn't allow unauthenticated access  
**Fix:** Ensure `permission_classes = [AllowAny]` is added to LoginView in `apps/common/views.py`  
**Status:** ✅ FIXED in commit 646afba

### "Network Error" on Frontend Pages
**Issue:** Frontend can't reach backend  
**Fix:** 
1. Verify backend is running: `python manage.py runserver`
2. Verify `.env` has correct API URL: `REACT_APP_API_URL=http://127.0.0.1:8000/api`
3. Verify CORS is configured in backend settings

### Tokens Not Persisting Across Page Refresh
**Status:** ✅ WORKING - Tokens stored in browser localStorage automatically

### "Port already in use" Errors
**Solution:** Kill existing processes or use different port
```bash
# Frontend on 3001 instead of 3000
PORT=3001 npm start

# Backend on 8001 instead of 8000
python manage.py runserver 127.0.0.1:8001
```

---

## Documentation Links

- [Backend Full Setup Guide](./vrm-backend/README_SETUP.md)
- [Frontend Full Setup Guide](./vrm-frontend/README_SETUP.md)
- [API Documentation](./UI_API_DOCUMENTATION.md)
- [UI Quick Reference](./UI_QUICK_REFERENCE.md)

---

## Support Contact

**For Issues:**
1. Check documentation links above
2. Review browser console (F12) for errors
3. Check backend server logs for API errors
4. Verify database has test users (see migrations)

**Git Branches:**
- Backend: https://github.com/SnehaaG22/vrm-mvp-Infrastructure (branch: infra-changes)
- Frontend: https://github.com/SnehaaG22/vrm-frontend

---

## Version Info

| Component | Version | Status |
|-----------|---------|--------|
| Backend | Django 5.2.10 | ✅ Running |
| Frontend | React 18.2.0 | ✅ Running |
| Database | SQLite 3 | ✅ Initialized |
| Authentication | dev-token-N | ✅ Working |
| API | REST | ✅ Functional |

---

**Last Updated:** February 19, 2025  
**Commit:** 646afba (Fix: Add AllowAny permission to LoginView)  
**Status:** ✅ QA Ready - All systems operational
