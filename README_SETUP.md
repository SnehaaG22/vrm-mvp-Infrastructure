# VRM Backend - Complete Setup & Run Guide

## Overview

VRM (Vendor Risk Management) Backend is a Django REST API that manages vendor assessments, evidence, renewals, and notifications. This guide provides step-by-step instructions for local development setup and testing.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation & Setup](#installation--setup)
3. [Running the Backend](#running-the-backend)
4. [QA Testing Credentials](#qa-testing-credentials)
5. [API Endpoints Reference](#api-endpoints-reference)
6. [Troubleshooting](#troubleshooting)
7. [Project Structure](#project-structure)

---

## System Requirements

**Required:**

- Python 3.10 or higher
- Django 5.2.10
- pip (Python package manager)
- Git

**Optional (for full stack):**

- Redis (for Celery tasks)
- Docker & Docker Compose (for containerized setup)

---

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/SnehaaG22/vrm-mvp-Infrastructure.git
cd vrm-mvp-Infrastructure
git checkout infra-changes
```

### Step 2: Create Virtual Environment

#### On Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**

- Django 5.2.10 - Web framework
- djangorestframework - REST API toolkit
- django-cors-headers - Cross-origin request support
- celery - Async task queue
- sqlite3 - Built-in database (dev only)

### Step 4: Initialize Database

```bash
python manage.py migrate
```

This creates the SQLite database and applies all migrations.

### Step 5: Seed QA Users (One-time)

```bash
python manage.py shell < apps/common/seeds.py
```

This populates the database with 3 test users:

- **Admin User**: admin@vrm.com / password123
- **Vendor User**: vendor@vrm.com / password123
- **Reviewer User**: reviewer@vrm.com / password123

To verify users were created:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all().values('id', 'email', 'username')
```

---

## Running the Backend

### Start Development Server

```bash
python manage.py runserver 127.0.0.1:8000
```

**Expected output:**

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Verify Server is Running

```bash
curl http://127.0.0.1:8000/api/auth/login/ -X POST -H "Content-Type: application/json" -d '{"email":"admin@vrm.com","password":"password123"}'
```

**Expected response:**

```json
{
  "token": "dev-token-5",
  "user": {
    "id": 5,
    "email": "admin@vrm.com",
    "first_name": "",
    "last_name": "",
    "org_id": null,
    "is_staff": false
  }
}
```

### Run System Check

```bash
python manage.py check
```

Should return: `System check identified no issues (0 silenced).`

---

## QA Testing Credentials

### Test User Matrix

| Role     | Email            | Password    | Token (after login) | Max Assessments |
| -------- | ---------------- | ----------- | ------------------- | --------------- |
| Admin    | admin@vrm.com    | password123 | dev-token-5         | Unlimited       |
| Vendor   | vendor@vrm.com   | password123 | dev-token-6         | Unlimited       |
| Reviewer | reviewer@vrm.com | password123 | dev-token-7         | Unlimited       |

### How to Get Token

1. Login via `/api/auth/login/` endpoint with email & password
2. Response includes `"token": "dev-token-X"`
3. Use token in subsequent requests: `Authorization: Bearer dev-token-X`

### Example cURL Test

```bash
# Step 1: Get token
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vrm.com","password":"password123"}'

# Step 2: Copy token from response, then list assessments
curl -X GET http://127.0.0.1:8000/api/assessments/ \
  -H "Authorization: Bearer dev-token-5"
```

---

## API Endpoints Reference

### Authentication Endpoints

| Method | Endpoint           | Auth Required | Purpose                  |
| ------ | ------------------ | ------------- | ------------------------ |
| POST   | `/api/auth/login/` | ❌ No         | Get dev-token            |
| GET    | `/api/users/me/`   | ✅ Yes        | Get current user profile |

### Assessment Endpoints

| Method | Endpoint                 | Auth Required | Purpose                          |
| ------ | ------------------------ | ------------- | -------------------------------- |
| GET    | `/api/assessments/`      | ✅ Yes        | List all assessments (paginated) |
| POST   | `/api/assessments/`      | ✅ Yes        | Create new assessment            |
| GET    | `/api/assessments/{id}/` | ✅ Yes        | Get assessment details           |
| PUT    | `/api/assessments/{id}/` | ✅ Yes        | Update assessment                |
| DELETE | `/api/assessments/{id}/` | ✅ Yes        | Delete assessment                |

### Vendor Endpoints

| Method | Endpoint             | Auth Required | Purpose                      |
| ------ | -------------------- | ------------- | ---------------------------- |
| GET    | `/api/vendors/`      | ✅ Yes        | List all vendors (paginated) |
| POST   | `/api/vendors/`      | ✅ Yes        | Create new vendor            |
| GET    | `/api/vendors/{id}/` | ✅ Yes        | Get vendor details           |
| PUT    | `/api/vendors/{id}/` | ✅ Yes        | Update vendor                |
| DELETE | `/api/vendors/{id}/` | ✅ Yes        | Delete vendor                |

### Notifications Endpoints

| Method | Endpoint                             | Auth Required | Purpose                   |
| ------ | ------------------------------------ | ------------- | ------------------------- |
| GET    | `/api/notifications/`                | ✅ Yes        | List notifications        |
| POST   | `/api/notifications/{id}/mark_read/` | ✅ Yes        | Mark notification as read |

### Evidence Endpoints

| Method | Endpoint                | Auth Required | Purpose              |
| ------ | ----------------------- | ------------- | -------------------- |
| POST   | `/api/evidence/upload/` | ✅ Yes        | Upload evidence file |
| GET    | `/api/evidence/`        | ✅ Yes        | List evidence        |

---

## Sample API Request/Response

### Create Assessment

**Request:**

```bash
curl -X POST http://127.0.0.1:8000/api/assessments/ \
  -H "Authorization: Bearer dev-token-5" \
  -H "Content-Type: application/json" \
  -d '{
    "vendor_id": 1,
    "vendor_name": "TestVendor Inc",
    "status": "draft"
  }'
```

**Response (201 Created):**

```json
{
  "id": 1,
  "vendor_id": 1,
  "vendor_name": "TestVendor Inc",
  "status": "draft",
  "created_at": "2025-02-19T10:30:00Z"
}
```

---

## Environment Variables

Create a `.env` file in the backend root directory (optional):

```env
DEBUG=True
SECRET_KEY=dev-secret
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Database Models

### Assessment Model

```
- id: Primary Key
- vendor_id: Foreign Key (vendor identifier)
- vendor_name: String
- status: Choice field (draft, in_progress, completed)
- created_at: DateTime (auto-created)
```

### Vendor Model

```
- id: Primary Key
- name: String
- category: String
- status: Choice field (active, inactive)
- email: Email field
- phone: Phone field
- created_at: DateTime (auto-created)
```

---

## Running Migrations

If you make changes to models, create and apply migrations:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

---

## Admin Panel Access

Access Django admin interface for data management:

1. Create superuser (if needed):

   ```bash
   python manage.py createsuperuser
   ```

2. Navigate to: `http://127.0.0.1:8000/admin/`

3. Login with superuser credentials

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'django'"

**Solution:** Activate virtual environment and reinstall dependencies

```bash
pip install -r requirements.txt
```

### "port 8000 already in use"

**Solution:** Kill existing process or use different port

```bash
# Use port 8001 instead
python manage.py runserver 127.0.0.1:8001

# Or find and kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### "CORS error when calling from frontend"

**Solution:** Verify CORS_ALLOWED_ORIGINS in settings.py includes frontend URL

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Token not working (401 Unauthorized)

**Solution:** Ensure token is sent in Authorization header

```bash
# Correct format:
Authorization: Bearer dev-token-5

# Not correct:
Authorization: dev-token-5
Token: dev-token-5
```

### "Authentication credentials were not provided"

**Solution:** Make sure /api/auth/login/ request includes AllowAny permission

- The LoginView should have `permission_classes = [AllowAny]`
- Check apps/common/views.py line 8

---

## Project Structure

```
vrm-backend/
├── manage.py                 # Django CLI tool
├── db.sqlite3               # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── README_SETUP.md          # This file
├── core/                    # Django project settings
│   ├── settings.py          # Main config (CORS, REST_FRAMEWORK, DATABASES)
│   ├── urls.py              # URL routing (API endpoints)
│   ├── wsgi.py              # WSGI server config
│   └── asgi.py              # ASGI server config
├── apps/
│   ├── common/              # Shared models & auth
│   │   ├── models.py        # Assessment, Vendor models
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # LoginView, UserProfileView, ViewSets
│   │   ├── auth.py          # DevTokenAuthentication class
│   │   ├── seeds.py         # QA user seeding script
│   │   ├── migrations/      # Database migrations
│   │   └── urls.py
│   ├── evidence/            # Evidence upload & storage
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tasks.py         # Celery tasks
│   ├── notifications/       # Notification system
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   └── renewals/            # Renewal tracking
│       ├── models.py
│       ├── views.py
│       └── urls.py
```

---

## Next Steps

### For QA Testing:

1. Start backend: `python manage.py runserver 127.0.0.1:8000`
2. Start frontend: See [Frontend README](../vrm-frontend/README_SETUP.md)
3. Open browser: `http://localhost:3000/login`
4. Login with credentials above
5. Run Postman E2E tests against `/api/` endpoints

### For Development:

1. Make model changes in `apps/*/models.py`
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Test via curl or Postman
5. Commit changes: `git add .` → `git commit -m "..."` → `git push`

### For Production:

1. Replace dev-token auth with JWT (JsonWebTokenAuthentication)
2. Set DEBUG=False
3. Use environment variables for secrets
4. Set up Postgres database instead of SQLite
5. Configure Redis for Celery
6. Deploy with Gunicorn + Nginx

---

## Support & Documentation

- **Django Docs**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **API Documentation**: See [UI_API_DOCUMENTATION.md](../UI_API_DOCUMENTATION.md)

---

**Last Updated:** February 19, 2025  
**Status:** ✅ Ready for QA Testing  
**Commit:** 646afba (Fix: Add AllowAny permission to LoginView)
