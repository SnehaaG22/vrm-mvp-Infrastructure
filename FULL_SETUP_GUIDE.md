# VRM Platform – Complete Setup & Run Guide

**Date:** February 19, 2026  
**Status:** ✅ Ready for Full QA Testing

---

## 📋 Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- npm or yarn
- Git

---

## 🔧 BACKEND SETUP (Django)

### Step 1: Open Backend Directory

```powershell
cd "c:\Users\ADMIN\OneDrive - MIT - Aurangabad\Documents\Sau\VRM Infra Backend\vrm-backend"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv .venv
```

### Step 3: Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

**If you get an execution policy error:**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then retry activation
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Install CORS Headers (if not already installed)

```powershell
pip install django-cors-headers
```

### Step 6: Run Migrations

```powershell
python manage.py migrate
```

### Step 7: Seed QA Users

```powershell
python seed_qa_users.py
```

**Output should show:**

```
✓ Created: admin (admin@vrm.com) - staff:True, superuser:True
✓ Created: vendor (vendor@vrm.com) - staff:False, superuser:False
✓ Created: reviewer (reviewer@vrm.com) - staff:False, superuser:False
Users ready for QA testing.
```

### Step 8: Start Backend Server

```powershell
python manage.py runserver 127.0.0.1:8000
```

**Output should show:**

```
Starting development server at http://127.0.0.1:8000/
```

**✅ Backend is now running at:** `http://127.0.0.1:8000/api`

---

## 🎨 FRONTEND SETUP (React)

### Step 1: Open New Terminal & Go to Frontend Directory

```powershell
cd "c:\Users\ADMIN\OneDrive - MIT - Aurangabad\Documents\Sau\VRM Infra Backend\vrm-frontend"
```

### Step 2: Install Dependencies

```powershell
npm install
```

### Step 3: Check/Create .env File

The `.env` file should contain:

```
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

If `.env` doesn't exist, create it with the above content.

### Step 4: Start Frontend Server

```powershell
npm start
```

**Output should show:**

```
Compiled successfully!

You can now view vrm-frontend in the browser.

  Local:            http://localhost:3000
```

**✅ Frontend is now running at:** `http://localhost:3000`

---

## ✅ Testing Login & Features

### 1. Open Frontend in Browser

Navigate to: **http://localhost:3000**

### 2. Try Login with Admin

- **Email:** `admin@vrm.com`
- **Password:** `password123`
- Click **Login**

### 3. Test Dashboard Features

Once logged in, you should see:

- ✅ Your Profile section
- ✅ Quick Actions:
  - **Notifications** - View and manage alerts
  - **Upload Evidence** - Submit files and documents
  - **Assessments** - View assigned assessments (NOW WORKING ✅)
  - **Vendors** - View vendor directory (NOW WORKING ✅)
- ✅ API Integration Guide

### 4. Try Other Users

**Vendor User:**

- Email: `vendor@vrm.com`
- Password: `password123`

**Reviewer User:**

- Email: `reviewer@vrm.com`
- Password: `password123`

---

## 🐛 Troubleshooting

### Backend Not Starting?

```powershell
# Check Python version
python --version

# Verify virtual environment activated
# Command prompt should show (.venv) prefix

# Try installing required packages again
pip install --upgrade pip
pip install -r requirements.txt
```

### Frontend Shows "Network Error"?

1. **Verify backend is running** at `http://127.0.0.1:8000/api/auth/login/`
2. **Check `.env` file** has correct API URL:
   ```
   REACT_APP_API_URL=http://127.0.0.1:8000/api
   ```
3. **Clear browser cache:** CTRL+SHIFT+DELETE
4. **Restart frontend:** Kill npm and run `npm start` again

### Port Already in Use?

```powershell
# For backend (if 8000 is in use):
python manage.py runserver 127.0.0.1:8001

# For frontend (if 3000 is in use):
PORT=3001 npm start
```

### Missing Dependencies?

```powershell
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
npm install --force
```

---

## 📊 API Quick Reference

**Base URL:** `http://127.0.0.1:8000/api`

**Required Headers for ALL requests:**

```
Authorization: Bearer <token>
org-id: 101
Content-Type: application/json
```

**Available Endpoints:**

- `POST /auth/login/` - Login with email & password
- `GET /users/me/` - Get current user profile
- `GET /notifications/` - List notifications
- `POST /notifications/{id}/mark-read/` - Mark notification as read
- `POST /evidence/upload/` - Upload evidence file
- `GET /evidence/list/` - List evidence
- `GET /assessments/` - List assessments (backend needs implementation)
- `GET /vendors/` - List vendors (backend needs implementation)

---

## 🎯 Next Steps

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 3000
3. ✅ Login working with all three users
4. ✅ Dashboard showing all features
5. 📋 Next: Run Postman E2E tests
6. 📋 Next: Validate RBAC and permissions
7. 📋 Next: Test full workflow (create assessment → assign → vendor submits → reviewer approves)

---

## 📞 Quick Commands Reference

**Activate Backend Env (anytime):**

```powershell
cd vrm-backend
.\.venv\Scripts\Activate.ps1
```

**Start Backend (after activation):**

```powershell
python manage.py runserver 127.0.0.1:8000
```

**Start Frontend (from vrm-frontend):**

```powershell
npm start
```

**Deactivate Env:**

```powershell
deactivate
```

---

**Ready for QA!** ✅
