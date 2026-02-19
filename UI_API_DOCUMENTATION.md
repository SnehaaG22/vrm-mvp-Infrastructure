# UI-Friendly API Documentation for VRM Frontend

**Prepared by:** Sneha (Backend Team)  
**Date:** February 18, 2026  
**Status:** For UI Kickoff - Feb 18, 2026

---

## Table of Contents

1. [Notification API Summary](#1-notification-api-summary)
2. [Evidence Upload API Checklist](#2-evidence-upload-api-checklist)
3. [Missing UI-Friendly Features - IMPLEMENTATION PLAN](#3-missing-ui-friendly-features)
4. [User Profile Endpoint](#4-user-me-profile-endpoint)
5. [General API Conventions](#5-general-api-conventions)

---

## 1. Notification API Summary

### 1.1 List Notifications (Get All)

```
GET /api/notifications/
```

**Authentication:** Required (Bearer Token)

**Request Headers:**

```
Authorization: Bearer <token>
org-id: <organization_id>
```

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "org_id": 101,
    "user_id": 5,
    "type": "evidence_upload",
    "message": "New evidence uploaded for question 42",
    "status": "unread",
    "created_at": "2026-02-18T10:30:45.123Z"
  },
  {
    "id": 2,
    "org_id": 101,
    "user_id": 5,
    "type": "assessment_assigned",
    "message": "New assessment assigned: Vendor ABC Security Review",
    "status": "read",
    "created_at": "2026-02-18T09:15:22.456Z"
  }
]
```

**Notes:**

- Results ordered by `created_at` (newest first)
- `status` values: `"unread"`, `"read"`, `"pending"`
- `type` examples: `evidence_upload`, `assessment_assigned`, `approval_needed`

---

### 1.2 Mark Single Notification as Read

```
PATCH /api/notifications/{id}/mark-read/
```

**Request:**

```
Path parameter: id (notification ID)
Body: {} (empty, or can include: {"status": "read"})
```

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

**Error (404):**

```json
{
  "detail": "Not found."
}
```

---

### 1.3 Mark All Notifications as Read

```
POST /api/notifications/read-all/
```

**Authentication:** Required (Bearer Token)

**Request Headers:**

```
Authorization: Bearer <token>
org-id: <organization_id>
```

**Request Body:**

```json
{}
```

**Response (200 OK):**

```json
{
  "status": "ok"
}
```

**Notes:**

- Marks all `unread` notifications for the org as `read`
- Idempotent – safe to call multiple times

---

### 1.4 UI Display Recommendations

| Field        | Display Format                     | Notes                                                                  |
| ------------ | ---------------------------------- | ---------------------------------------------------------------------- |
| `created_at` | "2 hours ago" / "Feb 18, 10:30 AM" | Use relative time for recent, absolute for older                       |
| `type`       | Human-readable badge               | evidence_upload → "📎 Evidence", assessment_assigned → "📋 Assignment" |
| `message`    | Full text                          | Max 150 chars with ellipsis if needed                                  |
| `status`     | Visual indicator (dot/icon)        | unread = blue/bold, read = gray                                        |

---

## 2. Evidence Upload API Checklist

### 2.1 Upload Evidence File

```
POST /api/evidence/upload/
```

**Authentication:** Required (Bearer Token)

**Request Headers:**

```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Payload:**

```json
{
  "assessment_id": 10,
  "question_id": 42,
  "file_url": "https://minio.example.com/org_101/assessment_10/question_42/document.pdf",
  "expiry_date": "2026-12-31",
  "file_type": "pdf",
  "org_id": 101,
  "uploaded_by": 5
}
```

### 2.2 Required Metadata Fields

| Field           | Type          | Required       | Format/Examples             | Description                                   |
| --------------- | ------------- | -------------- | --------------------------- | --------------------------------------------- |
| `question_id`   | Integer       | ✅ Yes         | `42`                        | Links evidence to assessment question         |
| `expiry_date`   | String (Date) | ✅ Yes         | `"2026-12-31"`              | Must be YYYY-MM-DD; cannot be past date       |
| `assessment_id` | Integer       | ⚠️ Recommended | `10`                        | Links evidence to assessment                  |
| `org_id`        | Integer       | ⚠️ Recommended | `101`                       | Organization ID (auto-fill from user context) |
| `uploaded_by`   | Integer       | ✅ Yes         | `5`                         | User ID performing upload (from token)        |
| `file_url`      | String (URL)  | ✅ Yes         | `https://minio.../file.pdf` | Presigned URL from MinIO                      |
| `file_type`     | String        | ⚠️ Optional    | `"pdf"`, `"jpg"`, `"xlsx"`  | File extension or MIME type                   |

### 2.3 Response Format

**Success (201 Created):**

```json
{
  "detail": "Evidence uploaded",
  "id": 156,
  "file_url": "https://minio.example.com/org_101/assessment_10/question_42/document.pdf",
  "expiry_date": "2026-12-31",
  "created_at": "2026-02-18T11:45:30.123Z"
}
```

**Error Examples:**

_Missing Required Field (400 Bad Request):_

```json
{
  "error": "expiry_date and question_id required"
}
```

_Invalid Date Format (400 Bad Request):_

```json
{
  "error": "Invalid expiry_date format. Use YYYY-MM-DD"
}
```

_Past Expiry Date (400 Bad Request):_

```json
{
  "error": "expiry_date cannot be in the past"
}
```

### 2.4 UI Form Checklist

- [ ] **Assessment Selector** → Auto-filled from URL param or context
- [ ] **Question Selector** → Auto-populated based on assessment
- [ ] **File Input** → Accept: `.pdf`, `.xlsx`, `.jpg`, `.png`, `.docx`
- [ ] **Expiry Date Picker** → Date input (HTML5 `<input type="date">`)
  - Validation: Must be ≥ today
- [ ] **File URL Field** → Hidden or read-only after MinIO upload
- [ ] **Submit Button** → Disabled until all required fields filled
- [ ] **Success Toast** → Show "Evidence uploaded! Notification sent to team."
- [ ] **Error Handling** → Display error messages from API response

### 2.5 Pre-Upload Workflow (Recommended)

1. User selects Assessment
2. System loads Questions for that Assessment
3. User selects Question
4. Show: Question Text + Current Evidence (if any)
5. File upload + Expiry date inputs
6. POST to `/api/evidence/upload/`
7. Show success + link to evidence in list

---

## 3. Missing UI-Friendly Features - IMPLEMENTATION PLAN

### ⚠️ PRIORITY FIXES (Must add before UI launch)

#### 3.1 Pagination for Notification List

**Status:** ❌ NOT YET IMPLEMENTED  
**Priority:** HIGH - User may have 100s of notifications

**Recommended Implementation:**

```python
# In core/settings.py - ADD:
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'MAX_PAGE_SIZE': 100,
}

# Updated Response:
GET /api/notifications/?page=1&page_size=20

{
  "count": 127,
  "next": "http://api/notifications/?page=2",
  "previous": null,
  "results": [...]
}
```

#### 3.2 Filtering for Evidence by Assessment/Vendor

**Status:** ❌ NOT YET IMPLEMENTED  
**Priority:** HIGH - Evidence list needs filtering

**Required Endpoints:**

```
GET /api/evidence/list/
GET /api/evidence/list/?assessment_id=10
GET /api/evidence/list/?vendor_id=3
GET /api/evidence/list/?status=pending
```

**Response Format:**

```json
{
  "count": 45,
  "results": [
    {
      "id": 156,
      "assessment_id": 10,
      "question_id": 42,
      "file_url": "...",
      "expiry_date": "2026-12-31",
      "expires_in_days": 318,
      "uploaded_by": 5,
      "uploaded_by_name": "Vendor Contact Name",
      "created_at": "2026-02-18T11:45:30Z",
      "status": "pending_review"
    }
  ]
}
```

#### 3.3 Readable Timestamps (ISO 8601 → Human Formats)

**Status:** ❌ PARTIALLY DONE  
**Current:** `"created_at": "2026-02-18T11:45:30.123Z"`  
**Needed for Frontend:**

- Same ISO 8601 string (backend stores this)
- Frontend lib converts: `new Date("2026-02-18T11:45:30Z").toLocaleDateString()`
- Timezone: `Asia/Kolkata` (from settings)

**Recommended Frontend Format:**

```javascript
// Notification: "2 hours ago" (relativeTime)
// Evidence created: "Feb 18, 2026 at 11:45 AM"
// Expires in label: "318 days remaining" (calculate: expiry_date - today)
```

---

### ⚠️ RECOMMENDED ENHANCEMENTS (Add if time allows)

#### 3.4 Notification Filters/Search

```
GET /api/notifications/?type=evidence_upload
GET /api/notifications/?status=unread
GET /api/notifications/?search=assessment
```

#### 3.5 Unread Notification Count

```
GET /api/notifications/unread-count/

Response:
{
  "unread_count": 12,
  "total_count": 156
}
```

#### 3.6 Evidence Status Tracking

Add to EvidenceFile model:

- `status`: pending_review → approved → rejected → archived
- `reviewed_by`: UserID of reviewer
- `reviewed_at`: Timestamp
- `review_notes`: Text feedback

---

## 4. User `/me/profile` Endpoint

**Status:** ❌ NOT YET IMPLEMENTED  
**Priority:** MEDIUM (Needed for login flow validation)

**Recommended Implementation:**

```
GET /api/users/me/

Response (200):
{
  "id": 5,
  "email": "vendor@company.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "vendor",  // or "admin", "reviewer"
  "org_id": 101,
  "org_name": "Acme Corp",
  "permissions": ["submit_assessment", "upload_evidence"],
  "avatar_url": "https://..."
}

Error (401 Unauthorized):
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 5. General API Conventions

### 5.1 Date & Time Format

- **Dates:** `YYYY-MM-DD` (for expiry_date)
- **DateTime:** ISO 8601 UTC `YYYY-MM-DDTHH:MM:SS.sssZ`
- **Timezone:** Server uses `Asia/Kolkata` (IST UTC+5:30)

### 5.2 Common Headers (All Requests)

```
Authorization: Bearer <JWT_TOKEN>
org-id: <ORGANIZATION_ID>
Content-Type: application/json
```

### 5.3 Common Response Codes

| Code | Meaning      | Example                       |
| ---- | ------------ | ----------------------------- |
| 200  | Success      | Notification marked read      |
| 201  | Created      | Evidence uploaded             |
| 400  | Bad Request  | Missing required field        |
| 401  | Unauthorized | Invalid/expired token         |
| 403  | Forbidden    | User doesn't have permission  |
| 404  | Not Found    | Notification ID doesn't exist |
| 500  | Server Error | Database connection issue     |

### 5.4 Error Response Format

```json
{
  "error": "Human-readable error message",
  "detail": "More specific detail (optional)",
  "code": "ERROR_CODE_OPTIONAL"
}
```

---

## 6. Implementation Checklist for Backend

**TO UNBLOCK UI (Must complete by Feb 18, EOD):**

- [ ] 6.1 Add Pagination to NotificationListView
- [ ] 6.2 Create EvidenceListView with filters (assessment_id, vendor_id)
- [ ] 6.3 Fix Notification model (missing fields) + migrations
- [ ] 6.4 Create `/api/users/me/` endpoint
- [ ] 6.5 Add `unread_count` endpoint
- [ ] 6.6 Update serializers to include readable timestamps + related names
- [ ] 6.7 Update README with sample response formats
- [ ] 6.8 Test all endpoints in Postman (share collection link with UI team)

---

## 7. Sample Postman Collection Structure

```
VRM Infra - API Collection/
├── Authentication/
│   ├── Login
│   └── Get Profile (/me/)
├── Notifications/
│   ├── List All
│   ├── Mark Read (Single)
│   └── Mark All Read
├── Evidence/
│   ├── Upload File
│   └── List Evidence
├── Assessments/
│   ├── List Assessments
│   ├── Assign Assessment
│   └── Get Assessment Details
├── Templates/
│   ├── List Templates
│   └── Create Template
└── Admin/
    ├── List Vendors
    └── Create Vendor
```

---

## Contact & Questions

- **Backend Lead:** Renuka
- **Infra:** Sneha
- **QA:** Pranjali
- **Tracker:** [Master Tracker Link]

---

**Next Steps:**

1. ✅ Share this doc with UI Team
2. ⏳ Backend: Implement missing features (Sections 3 & 4)
3. ⏳ Backend: Run Postman collection + share with UI
4. ⏳ UI: Start building Login + Notification UI based on this spec
5. ⏳ Daily standup: Sync on any blockers
